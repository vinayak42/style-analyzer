from importlib.machinery import SourceFileLoader
import os

from setuptools import find_packages, setup

lookout = SourceFileLoader("lookout", "./lookout/__init__.py").load_module()

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

tests_require = ["docker>=3.4.0,<4.0"]

setup(
    name="lookout-style",
    description="Machine learning-based assisted code review - code style analyzers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=".".join(map(str, lookout.__version__)),
    license="AGPL-3.0",
    author="source{d}",
    author_email="machine-learning@sourced.tech",
    url="https://github.com/src-d/style-analyzer",
    download_url="https://github.com/src-d/style-analyzer",
    packages=find_packages(exclude=("lookout.style.format.tests",)),
    namespace_packages=["lookout"],
    entry_points={
        "console_scripts": ["analyzer=lookout.__main__:main"],
    },
    keywords=["machine learning on source code", "babelfish"],
    install_requires=[
        "bblfsh!=2.12.2",
        "sourced-ml>=0.6.0,<0.7",
        "xxhash>=0.5.0,<2.0",
        "stringcase>=1.2.0,<2.0",
        "sqlalchemy>=1.0.0,<2.0",
        "sqlalchemy-utils>=0.33,<2.0",
        "pympler>=0.5,<2.0",
        "cachetools>=2.0,<3.0",
        "configargparse>=0.13,<2.0",
        "humanfriendly>=4.0,<5.0",
        "psycopg2-binary>=2.7,<3.0",
        "scikit-learn>=0.19,<0.20",
        "tqdm>=4.0,<5.0",
        "scikit-optimize>=0.5,<2.0",
        "pandas>=0.22,<2.0",
        "gensim>=3.5.0,<4.0",
        "google-compute-engine>=2.8.3,<3.0",  # for gensim
        "xgboost>=0.72,<2.0",
        "typing;python_version<'3.5'",
    ],
    extras_require={
        "tf": ["tensorflow>=1.0,<2.0"],
        "tf_gpu": ["tensorflow-gpu>=1.0,<2.0"],
        "plot": ["matplotlib>=2.0,<3.0"],
        "test": tests_require,
        "web": ["Flask>=1.0.0,<2.0", "Flask-Cors>=3.0.0,<4.0"],
    },
    tests_require=tests_require,
    package_data={"": ["LICENSE.md", "README.md"], },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Quality Assurance"
    ]
)
