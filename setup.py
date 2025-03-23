from setuptools import setup, find_packages

VERSION = '0.0.6' 
DESCRIPTION = 'Sinhala Language Tool Kit'
LONG_DESCRIPTION = open("README.md", 'r').read()

# Setting up

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*

setup(
       # the name must match the folder name 'sltk'
        name="sltkpy", 
        version=VERSION,
        author="Buddhi Kavindra Ranasinghe",
        author_email="info@buddhilive.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[], # add any additional packages
        package_data={"sltkpy": ["*.txt", "*.json"]},
        include_package_data=True,
        data_files=[('shared', ['sltkpy/models/vocab.json'])],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)