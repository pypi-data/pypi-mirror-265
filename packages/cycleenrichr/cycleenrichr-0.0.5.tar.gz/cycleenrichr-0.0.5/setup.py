import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="cycleenrichr",
    version="0.0.5",
    author="Alexander Lachmann",
    author_email="alexander.lachmann@mssm.edu",
    description="Cycleenrichr uses PrismEXP predictions to calculate enrichment of gene sets that do not have gene annotations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maayanlab/cycleenrichr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
            'h5py>=3.7.0',
            'numpy>=1.23.3',
            'pandas>=1.5.0',
            'scipy>=1.12.0',
            'setuptools>=67.8.0',
            'setuptools>=58.0.4',
            'statsmodels>=0.14.0',
            'tqdm>=4.64.1'
        ],
    python_requires='>=3.7',
    package_data={
        "cycleenrichr": ["data/*"]
    },
    include_package_data=True,
)