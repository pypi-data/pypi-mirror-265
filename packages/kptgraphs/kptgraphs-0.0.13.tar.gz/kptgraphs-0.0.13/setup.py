from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.13"
DESCRIPTION = "My Version of Plotting Graphs for simple data analysis. "
LONG_DESCRIPTION = "A package that lets you plot graphs built on top of matplotlib and seaborn. The process is not that much more simple than using those libraries themselves, but these graphs match the style I use in my projects."

# Setting up
setup(
    name="kptgraphs",
    version=VERSION,
    author="Krishnaraj Thadesar",
    author_email="<kpt.krishnaraj@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "matplotlib >= 3.8.3",
        "seaborn >= 0.13.2",
        "pandas >= 2.2.0",
        "numpy >= 1.26.3",
    ],
    keywords=["python", "data", "graphs", "plotting", "matplotlib", "seaborn"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
