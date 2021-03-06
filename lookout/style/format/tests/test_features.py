from collections import ChainMap, defaultdict
import lzma
from pathlib import Path
import unittest

import bblfsh
import numpy

from lookout.core.api.service_data_pb2 import File
from lookout.style.format.analyzer import FormatAnalyzer
from lookout.style.format.feature_extractor import FeatureExtractor
from lookout.style.format.feature_utils import (
    CLASS_INDEX, CLASSES, CLS_NEWLINE, CLS_NOOP, CLS_SINGLE_QUOTE, CLS_SPACE, CLS_SPACE_DEC,
    CLS_SPACE_INC, VirtualNode)


class FeaturesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = Path(__file__).parent
        # str() is needed for Python 3.5
        with lzma.open(str(base / "benchmark.js.xz"), mode="rt") as fin:
            cls.contents = fin.read()
        with lzma.open(str(base / "benchmark.uast.xz")) as fin:
            cls.uast = bblfsh.Node.FromString(fin.read())
        config = FormatAnalyzer._load_train_config({})
        final_config = config["javascript"]
        cls.extractor = FeatureExtractor(language="javascript",
                                         **final_config["feature_extractor"])
        cls.extractor_noops = FeatureExtractor(language="javascript",
                                               **ChainMap({"insert_noops": True},
                                                          final_config["feature_extractor"]))

    def test_parse_file_exact_match(self):
        test_js_code_filepath = Path(__file__).parent / "for_parse_test.js.xz"
        with lzma.open(str(test_js_code_filepath), mode="rt") as f:
            code = f.read()
        uast = bblfsh.BblfshClient("0.0.0.0:9432").parse(
            filename="", language="javascript", contents=code.encode()).uast
        nodes, parents = self.extractor._parse_file(code, uast, test_js_code_filepath)
        self.assertEqual("".join(n.value for n in nodes), code)

    def test_parse_file_comment_after_regexp(self):
        code = "x = // comment\n/<regexp>/;"
        uast = bblfsh.BblfshClient("0.0.0.0:9432").parse(
            filename="", language="javascript", contents=code.encode()).uast
        nodes, parents = self.extractor._parse_file(code, uast, "")
        self.assertEqual("".join(n.value for n in nodes), code)

    def test_parse_file(self):
        nodes, parents = self.extractor._parse_file(self.contents, self.uast, "test_file")
        text = []
        offset = line = col = 0
        for n in nodes:
            if line == n.start.line - 1:
                line += 1
                col = 1
            self.assertEqual((offset, line, col), n.start, n.value)
            text.append(n.value)
            if n.node is not None:
                self.assertIsNotNone(parents.get(id(n.node)), n)
            offset, line, col = n.end
        self.assertEqual("".join(text), self.contents)

    def test_classify_vnodes(self):
        nodes, _ = self.extractor._parse_file(self.contents, self.uast, "test_file")
        nodes = list(self.extractor._classify_vnodes(nodes, "test_file"))
        text = "".join(n.value for n in nodes)
        self.assertEqual(text, self.contents)
        cls_counts = defaultdict(int)
        offset = line = col = 0
        for n in nodes:
            if line == n.start.line - 1:
                line += 1
                col = 1
            self.assertEqual((offset, line, col), n.start, n.value)
            if n.y is not None:
                cls_counts[CLASSES[n.y]] += 1
            offset, line, col = n.end
        self.assertEqual(cls_counts[CLS_SPACE_INC], cls_counts[CLS_SPACE_DEC])
        self.assertGreater(cls_counts[CLS_SPACE_INC], 0)
        self.assertGreater(cls_counts[CLS_SPACE], 0)
        self.assertGreater(cls_counts[CLS_NEWLINE], 0)
        self.assertGreater(cls_counts[CLS_SINGLE_QUOTE], 0)
        self.assertTrue(cls_counts[CLS_SINGLE_QUOTE] % 2 == 0)

    def test_extract_features(self):
        file = File(content=bytes(self.contents, "utf-8"),
                    uast=self.uast)
        files = [file, file]

        res = self.extractor.extract_features(files)
        self.assertIsNotNone(res, "Failed to parse files.")
        self.check_X_y(*res)

    def check_X_y(self, X, y, vnodes_y, vnodes):
        self.assertEqual(X.shape[0], y.shape[0])
        self.assertEqual(X.shape[0], len(vnodes_y))
        for vn in vnodes_y:
            self.assertIsInstance(vn, VirtualNode)
        self.assertEqual(X.shape[1], self.extractor.count_features())
        not_set = X == -1
        unset_rows = numpy.nonzero(numpy.all(not_set, axis=1))[0]
        unset_columns = numpy.nonzero(numpy.all(not_set, axis=0))[0]
        self.assertEqual(len(unset_rows), 0, "%d rows are unset" % len(unset_rows))
        self.assertEqual(len(unset_columns), 0,
                         "columns %s are unset" % ", ".join(map(str, unset_columns)))

    def test_extract_features_all_lines(self):
        file = File(content=bytes(self.contents, "utf-8"),
                    uast=self.uast)
        files = [file, file]

        self.check_X_y(*self.extractor.extract_features(
            files, [list(range(1, self.contents.count("\n") + 1))] * 2))

    def test_extract_features_some_lines(self):
        file = File(content=bytes(self.contents, "utf-8"),
                    uast=self.uast)
        files = [file]

        X1, y1, vn1_y, vn1 = self.extractor.extract_features(
            files, [list(range(1, self.contents.count("\n") // 2 + 1))] * 2)
        self.check_X_y(X1, y1, vn1_y, vn1)
        X2, y2, vn2_y, vn2 = self.extractor.extract_features(files)
        self.assertTrue((X1 == X2[:len(X1)]).all())
        self.assertTrue((y1 == y2[:len(y1)]).all())
        self.assertTrue(vn1_y == vn2_y[:len(vn1_y)])
        self.assertLess(len(y1), len(y2))

    def test_noop_vnodes(self):
        vnodes, parents = self.extractor_noops._parse_file(self.contents, self.uast, "test_file")
        vnodes = self.extractor_noops._classify_vnodes(vnodes, "test_file")
        vnodes = self.extractor_noops._add_noops(vnodes, "test_file")
        for i, vnode in enumerate(vnodes):
            if i % 2:
                self.assertNotEqual(vnode.y, CLASS_INDEX[CLS_NOOP])
            else:
                self.assertEqual(vnode.y, CLASS_INDEX[CLS_NOOP])
                self.assertEqual(vnode.start.offset, vnode.end.offset)
                self.assertEqual(vnode.start.col, vnode.end.col)
                self.assertEqual(vnode.start.line, vnode.end.line)


if __name__ == "__main__":
    unittest.main()
