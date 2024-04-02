from setuptools import find_packages, setup

setup(
    name='Energy4TreeClassification',
    packages=find_packages(include=['Numpy','Graphviz']),
    version='0.1.2',
    description='Enerrgy4TreeClassification is a module that offers functions that made decision tree classification using Logistic regression and visualize it',
    author='Marhal Tom',
    install_requires=['Numpy','Graphviz']
)