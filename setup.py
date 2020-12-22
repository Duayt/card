import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

tests_require=['pytest',
                   'ipykernel',
                   'pytest-cov',
                   'pytest-xdist',
                   'autopep8'
                    ]
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
        "numpy==1.19.3",
        "pygame==2.0.0",
    ],
    extras_require={'tests':tests_require},

)
