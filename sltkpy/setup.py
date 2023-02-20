from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Sinhala Language Tool Kit'
LONG_DESCRIPTION = 'Sinhala Language Tool Kit'

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
        packages=find_packages(),
        install_requires=[], # add any additional packages
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)