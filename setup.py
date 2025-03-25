from setuptools import setup, find_packages

VERSION = '0.1.0-beta-1' 
DESCRIPTION = 'Sinhala Language Tool Kit'
LONG_DESCRIPTION = open("README.md", 'r').read()

# Setting up

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*

setup(
        name="sltkpy", 
        version=VERSION,
        author="Buddhi Kavindra Ranasinghe",
        author_email="info@buddhilive.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(exclude=['tests']),
        install_requires=['regex'],
        package_data={"sltkpy": ["*.txt", "*.json"]},
        include_package_data=True,
        data_files=[('shared', ['sltkpy/models/vocab.json'])],
        keywords=['python', 'Sinhala Tokenizer'],
        license='MIT',
        url='https://github.com/buddhilive/sltkpy',
        classifiers= [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Education",
            "Intended Audience :: Developers",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Text Processing :: Linguistic",
        ]
)