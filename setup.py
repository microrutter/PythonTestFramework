import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RATS", # Replace with your own username
    version="2",
    author="Wayne Rutter",
    author_email="microrutter2514@hotmail.com",
    description="A Test Automation Framework using selenium and BeautifulSoup",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microrutter/PythonTestFramework",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)