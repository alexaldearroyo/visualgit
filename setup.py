from setuptools import setup, find_packages

setup(
    name="vigit",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vigit = vigit.main:main',
        ],
    },
    # Agrega dependencias si las hay
    install_requires=[
        'simple_term_menu',
    ],
)
