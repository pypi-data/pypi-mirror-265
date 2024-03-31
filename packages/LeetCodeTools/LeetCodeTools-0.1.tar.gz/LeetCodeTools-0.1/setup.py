from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="LeetCodeTools",
    version="0.1",
    packages=["LeetCodeTools"],
    install_requires=[],
    setup_requires=[],
    test_requires=[],
    description="A simple package that includes some tools for LeetCode problems.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hmralavi/LeetCodeTools",
    author="Hamid Alavi",
    author_email="hmralavi@gmail.com",
    python_requires=">=3.9",
    license="MIT",
)
