from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install

with open('README.md', 'r') as f:
    readme = f.read()

class Install(install):
    def run(self):
        install.run(self)
        import nltk
        nltk.download("cmudict")

setup(
    name="count-syllable",
    version="0.1.0",
    py_modules=["count_syllable"],
    cmdclass={"install": Install},
    install_requires=["nltk"],
    setup_requires=["nltk"],

    # metadata to display on PyPI
    author="Shinya Akagi",
    description="Count syllables in English",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/ShinyaAkagiI/count_syllable", 
    license="PSF",
)
