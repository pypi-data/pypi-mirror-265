from setuptools import setup, find_packages

VERSION = '1.0' 
DESCRIPTION = 'Statistical Gaussian Fitting'
LONG_DESCRIPTION = 'This package outputs an array of data that corresponds to a user-inputted standard deviation. Currently only supports data that corresponds to a symmetric Gaussian distribution.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="statfit", 
        version=VERSION,
        author="Cliff Sun",
        author_email="cliffxuelisun@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy", "matplotlib"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'statistical fitting'],
        classifiers=[ 
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent", 
    ]
)