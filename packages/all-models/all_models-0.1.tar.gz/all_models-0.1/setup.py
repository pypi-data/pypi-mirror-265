from setuptools import setup, find_packages

setup(
    name='all_models',
    version='0.1',
    description='A package that contains all regression and classification models',
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'scikit-learn', 'xgboost']
)