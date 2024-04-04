from setuptools import setup, find_packages



setup(
    name="imagenai",
    version='0.1',
    packages=find_packages(),
    install_requires = [
        'numpy>=1.26.4',
        'matplotlib>=3.8.3',
        'requests>=2.31.0'
    ],
)