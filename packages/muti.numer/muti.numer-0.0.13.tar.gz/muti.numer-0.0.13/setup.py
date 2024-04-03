import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  url          = "https://github.com/E-C-Ares/",
  name         = "muti.numer",
  version      = "0.0.13",
  author       = "E.C.Ares",
  author_email = "E.C.Ares@outlook.com",
  license      = 'MIT DIVIƷON',
  description  = "utils for math-numer",
  long_description=long_description,
  long_description_content_type="text/markdown",
  packages     = setuptools.find_packages(),
  classifiers  = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ])