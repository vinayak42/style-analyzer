"""Generation of the typo correction candidates. Contains features extraction and serialization."""

from itertools import chain
from multiprocessing import Pool
import pickle
from typing import List, NamedTuple, Set, Union

from gensim.models import FastText
from modelforge import merge_strings, split_strings
import numpy
import pandas
from scipy.spatial.distance import cosine
from tqdm import tqdm

from lookout.style.typos.symspell import EditDistance, SymSpell
from lookout.style.typos.utils import (add_context_info, CANDIDATE_COLUMN, FEATURES_COLUMN,
                                       ID_COLUMN, read_frequencies, read_vocabulary, TYPO_COLUMN)


TypoInfo = NamedTuple("TypoInfo", (("index", int),
                                   ("typo", str),
                                   ("before", list),
                                   ("after", list)))

Features = NamedTuple("Features", (("index", int),
                                   ("typo", str),
                                   ("candidate", str),
                                   ("vec", numpy.ndarray)))


class CandidatesGenerator:
    """
    Looks for candidates for correction of typos and generates features \
    for them. Candidates are generated in three ways: \
    1. Closest by cosine distance of embeddings to the given token. \
    2. Closest by cosine distance to the compound vector of token context. \
    3. Closest by the edit distance and most frequent tokens from vocabulary.
    """

    DEFAULT_RADIUS = 3
    DEFAULT_MAX_DISTANCE = 2
    DEFAULT_NEIGHBORS_NUMBER = 0
    DEFAULT_EDIT_DISTANCE = 20

    def __init__(self):
        """Initialize a new instance of CandidatesGenerator."""
        self.checker = None
        self.fasttext = None
        self.neighbors_number = self.DEFAULT_NEIGHBORS_NUMBER
        self.edit_candidates_number = self.DEFAULT_EDIT_DISTANCE
        self.max_distance = self.DEFAULT_MAX_DISTANCE
        self.radius = self.DEFAULT_RADIUS
        self.tokens = []
        self.frequencies = {}

    def construct(self, vocabulary_file: str, frequencies_file: str, embeddings_file: str,
                  neighbors: int = DEFAULT_NEIGHBORS_NUMBER,
                  edit_candidates: int = DEFAULT_EDIT_DISTANCE,
                  max_distance: int = DEFAULT_MAX_DISTANCE, radius: int = DEFAULT_RADIUS,
                  max_corrected_length: int = 12) -> None:
        """
        Construct correction candidates generator.

        :param vocabulary_file: Text file used to generate vocabulary of correction candidates. \
                                First token in every line split is added to the vocabulary.
        :param frequencies_file: Path to the text file with frequencies. Each line must be two \
                                 values separated with a whitespace: "token count".
        :param embeddings_file: Path to the dump of FastText model.
        :param neighbors: Number of neighbors of context and typo embeddings \
                          to consider as candidates.
        :param edit_candidates: Number of the most frequent tokens among tokens on \
                                equal edit distance from the typo to consider as candidates.
        :param max_distance: Maximum edit distance for symspell lookup for candidates.
        :param radius: Maximum edit distance from typo allowed for candidates.
        :param max_corrected_length: Maximum length of prefix in which symspell lookup \
                                     for typos is conducted
        """
        self.checker = SymSpell(max_dictionary_edit_distance=max_distance,
                                prefix_length=max_corrected_length)
        self.checker.load_dictionary(vocabulary_file)
        self.fasttext = FastText.load_fasttext_format(embeddings_file)
        self.neighbors_number = neighbors
        self.edit_candidates_number = edit_candidates
        self.max_distance = max_distance
        self.radius = radius
        self.tokens = read_vocabulary(vocabulary_file)
        self.frequencies = read_frequencies(frequencies_file)

    def generate_candidates(self, data: pandas.DataFrame, threads_number: int,
                            save_candidates_file: str = None,
                            start_pool_size: int = 64) -> pandas.DataFrame:
        """
        Generate candidates for typos inside data.

        :param data: DataFrame, containing column TYPO_COLUMN.
        :param threads_number: Number of threads for multiprocessing.
        :param save_candidates_file: File to save candidates to.
        :param start_pool_size: Length of data, starting from which multiprocessing is desired.
        :return: DataFrame containing candidates for corrections
                 and features for their ranking for each typo.
        """
        data = add_context_info(data)

        typos = [TypoInfo(index, data.loc[index].typo, data.loc[index].before,
                          data.loc[index].after)
                 for i, index in enumerate(data.index)]

        if len(typos) > start_pool_size:
            with Pool(min(threads_number, len(typos))) as pool:
                candidates = list(tqdm(pool.imap(self._lookup_corrections_for_token, typos,
                                                 chunksize=min(256, 1 + len(typos) //
                                                               threads_number)),
                                       total=len(typos)))
        else:
            candidates = list(map(self._lookup_corrections_for_token, typos))

        candidates = pandas.DataFrame(list(chain.from_iterable(candidates)))
        candidates.columns = [ID_COLUMN, TYPO_COLUMN, CANDIDATE_COLUMN, FEATURES_COLUMN]
        candidates[ID_COLUMN] = candidates[ID_COLUMN].astype(data.index.dtype)

        if save_candidates_file is not None:
            candidates.to_pickle(save_candidates_file)

        return candidates

    def _lookup_corrections_for_token(self, typo_info: TypoInfo) -> List[Features]:
        candidates = []
        candidate_tokens = self._get_candidate_tokens(typo_info)
        typo_vec = self._vec(typo_info.typo)
        dist_calc = EditDistance(typo_info.typo, "damerau")
        for candidate in set(candidate_tokens):
            candidate_vec = self.fasttext.wv[candidate]
            dist = dist_calc.damerau_levenshtein_distance(candidate, self.radius)

            if dist < 0:
                continue
            candidates.append(self._generate_features(typo_info, dist, typo_vec,
                                                      candidate, candidate_vec))

        return candidates

    def _get_candidate_tokens(self, typo_info: TypoInfo) -> Set[str]:
        candidate_tokens = []
        last_dist = -1
        edit_candidates_count = 0
        if self.edit_candidates_number > 0:
            for suggestion in self.checker.lookup(typo_info.typo, 2, self.max_distance):
                if suggestion.distance != last_dist:
                    edit_candidates_count = 0
                    last_dist = suggestion.distance
                if edit_candidates_count >= self.edit_candidates_number:
                    continue
                candidate_tokens.append(suggestion.term)
                edit_candidates_count += 1
        if self.neighbors_number > 0:
            typo_neighbors = self._closest(self._vec(typo_info.typo), self.neighbors_number)
            candidate_tokens.extend(typo_neighbors)

            if len(typo_info.before + typo_info.after) > 0:
                context_neighbors = self._closest(self._compound_vec(typo_info.before +
                                                                     typo_info.after),
                                                  self.neighbors_number)
                candidate_tokens.extend(context_neighbors)

        candidate_tokens = {candidate for candidate in candidate_tokens
                            if candidate in self.tokens}
        if not len(candidate_tokens):
            candidate_tokens.add(typo_info.typo)
        return candidate_tokens

    def _generate_features(self, typo_info: TypoInfo, dist: int, typo_vec: numpy.ndarray,
                           candidate: str, candidate_vec: numpy.ndarray
                           ) -> Features:
        """
        Compile features for a single correction candidate.

        :param typo_info: instance of TypoInfo class.
        :param dist: edit distance from candidate to typo.
        :param typo_vec: embedding of the original token.
        :param candidate: candidate token.
        :param candidate_vec: embedding of the candidate token.
        :return: index, typo and candidate tokens, frequencies info, \
                 cosine distances between embeggings and contexts, \
                 edit distance between the tokens, \
                 embeddings of the tokens and contexts.
        """
        before_vec = self._compound_vec(typo_info.before)
        after_vec = self._compound_vec(typo_info.after)
        context_vec = self._compound_vec(typo_info.before + typo_info.after)
        return Features(typo_info.index, typo_info.typo, candidate, numpy.concatenate(((
            self._freq(typo_info.typo),
            self._freq(candidate),
            self._freq_relation(typo_info.typo, candidate),
            self._cos(typo_vec, before_vec),
            self._cos(typo_vec, after_vec),
            self._cos(typo_vec, context_vec),
            self._cos(candidate_vec, before_vec),
            self._cos(candidate_vec, after_vec),
            self._cos(candidate_vec, context_vec),
            self._cos(typo_vec, candidate_vec),
            dist),
            before_vec,
            after_vec,
            typo_vec,
            candidate_vec,
            context_vec)).astype(numpy.float32))

    def _vec(self, token: str) -> numpy.ndarray:
        return self.fasttext.wv[token]

    def _freq(self, token: str) -> float:
        return float(self.frequencies.get(token, 0))

    @staticmethod
    def _cos(first_vec: numpy.ndarray, second_vec: numpy.ndarray) -> float:
        if numpy.linalg.norm(first_vec) * numpy.linalg.norm(second_vec) != 0:
            return cosine(first_vec, second_vec)
        return 1.0

    def _closest(self, item: Union[numpy.ndarray, str], quantity: int) -> List[str]:
        return [token for token, _ in self.fasttext.wv.most_similar([item], topn=quantity)]

    def _freq_relation(self, first_token: str, second_token: str) -> float:
        return -numpy.log((1.0 * self._freq(first_token) + 1e-5) /
                          (1.0 * self._freq(second_token) + 1e-5))

    def _compound_vec(self, split: List[str]) -> numpy.ndarray:
        compound_vec = numpy.zeros(self.fasttext.wv["a"].shape)
        if len(split) == 0:
            return compound_vec
        else:
            for token in split:
                compound_vec += self.fasttext.wv[token]
        return compound_vec

    def _generate_tree(self) -> dict:
        tree = self.__dict__.copy()
        tree["checker"] = self.checker.__dict__.copy()
        tree["tokens"] = merge_strings(self.tokens)
        tree["fasttext"] = pickle.dumps(self.fasttext)
        return tree

    def _load_tree(self, tree: dict) -> None:
        self.__dict__.update(tree)

        self.tokens = split_strings(self.tokens)
        self.fasttext = pickle.loads(self.fasttext)
        self.checker = SymSpell(max_dictionary_edit_distance=self.max_distance)
        checker_tree = tree["checker"]
        checker_tree["_deletes"] = {int(h): deletes
                                    for h, deletes in checker_tree["_deletes"].items()}
        self.checker.__dict__.update(checker_tree)

    def __str__(self):
        """
        Represent the candidates generator.
        """
        return ("Vocabulary_size %d. \n"
                "Neighbors number %d. \n"
                "Maximum distance for search %d. \n"
                "Maximum distance allowed %d. \n"
                "Token for distance %d.") % (len(self.tokens), self.neighbors_number,
                                             self.max_distance, self.radius,
                                             self.edit_candidates_number)


def get_candidates_features(candidates: pandas.DataFrame) -> numpy.ndarray:
    """
    Take the feature vectors belonging to the typo correction candidates from the table.
    """
    return numpy.vstack(candidates[FEATURES_COLUMN].values)


def get_candidates_metadata(candidates: pandas.DataFrame) -> pandas.DataFrame:
    """
    Take the information about the typo correction candidates from the table.
    """
    return candidates[[ID_COLUMN, TYPO_COLUMN, CANDIDATE_COLUMN]]
