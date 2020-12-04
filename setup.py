import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cardgames",  # Replace with your own username
    version="0.0.1",
    author="Tanawat C",
    author_email="poom_tanawat@hotmail.com",
    description="A card game repos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Duayt/card",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "numpy",
    ],

    # extras_require={'plotting': ['matplotlib>=2.2.0,, 'jupyter']},
    tests_require=['pytest',
                   'pylint'
                   'mypy',
                   'ipykernel',
                   'pytest',
                   'pytest-cov',
                   'pytest-xdist',
                   'autopep8'
                    ],
)
