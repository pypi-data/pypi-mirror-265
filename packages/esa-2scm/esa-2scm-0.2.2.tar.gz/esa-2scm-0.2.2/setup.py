"""
The esa-2scm package is an implementation of the ESA-2SCM algorithm (Sanghoon Lee, 2024)
For documentation and algorithm/methodology details, please refer to my original article: http://www.snbperi.org/article/230

Should you use this package, I kindly request you to cite my article:
Lee, Sanghoon (2024). ESA-2SCM for Causal Discovery: Causal Modeling with Elastic Segmentation-based Synthetic Instrumental Variable, SnB Political and Economic Research Institute, 1, 21. <snbperi.org/article/230>
"""


from setuptools import setup, find_packages

with open("README.md", "r", encoding='utf-8') as fh:
    README = fh.read()

setup(
    author="Sanghoon Lee (DSsoli)",
    author_email="solisoli3197@gmail.com",
    name="esa-2scm",
    version="0.2.2",
    description="ESA-2SCM Python Package for Causal Discovery",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=["numpy", "pandas", "scipy", "scikit-learn"],
    url="https://github.com/DSsoli/esa-2scm.git",
    packages=find_packages(include=['esa_2scm', 'esa_2scm.*']),
    package_data={"esa_2scm": ['LICENSE', 'examples/*']},
    include_package_data=True
)