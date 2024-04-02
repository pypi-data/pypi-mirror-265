from setuptools import setup, find_packages

setup(
    name='nwpeval',
    version='1.4.0',
    description='A package for computing metrics for NWP model evaluation',
    author='Debasish Mahapatra',
    author_email='debasish.atmos@gmail.com | debasish.mahapatra@ugent.be',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pygrib',
        'xarray',
        'scipy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)