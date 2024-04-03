import setuptools

with open("README.md", "r") as file:
  long_description = file.read()

setuptools.setup(
  name="pyDbs",
  version="0.0.8",
  author="Rasmus K. Skjødt Berg",
  author_email="rasmus.kehlet.berg@econ.ku.dk",
  description="Custom database class (relies on pandas, scipy)",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/ChampionApe/pyDbs",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
  ],
  python_requires='>=3.8',
  install_requires=["pandas", "scipy","openpyxl"],
)