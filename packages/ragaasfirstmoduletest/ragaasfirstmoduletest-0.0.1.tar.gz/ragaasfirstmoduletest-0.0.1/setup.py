from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'My first RAGAAS package and test'
LONG_DESCRIPTION = 'My first RAGAAS package with a slightly longer description and test'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="ragaasfirstmoduletest", 
        version=VERSION,
        author="Tung Nguyen",
        author_email="Xuan.Nguyen@carelon.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["deepeval", "ragas"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
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