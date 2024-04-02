from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="rnaseqdata",
    version='0.0.8',
    author="Tiezheng Yuan",
    author_email="tiezhengyuan@hotmail.com",
    description="New Data type known as SeqData for RNA-Seq data analysis",
    url = "https://github.com/Tiezhengyuan/ernav2_seqdata",
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_dir={'': 'src'},
    install_requires=['numpy', 'pandas'],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
