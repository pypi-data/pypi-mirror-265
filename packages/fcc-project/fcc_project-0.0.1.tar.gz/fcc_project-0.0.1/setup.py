import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fcc_project",
    version="0.0.1",
    author="Tomas Vainoras",
    author_email="vainoras@gmail.com",
    description="freecodecamp test project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tomasvai/demo_repo",
    project_urls={
        "Bug Tracker": "package issues URL",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: Windows",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
