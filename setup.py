from setuptools import setup, find_packages

setup(
    name="vigit",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'vg = vigit.main:main',
        ],
    },
    # Add dependencies if any
    install_requires=[
        'simple_term_menu',
    ],
)
