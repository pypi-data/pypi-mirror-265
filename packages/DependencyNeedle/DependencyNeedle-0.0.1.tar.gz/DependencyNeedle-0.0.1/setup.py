from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Dependency Injection Container'
LONG_DESCRIPTION = ('Dependancy injection container to '
                    'automate inversion of control.')

setup(
    name="DependencyNeedle",
    version=VERSION,
    author="Abdelrahman Torky",
    author_email="24torky@email.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'Dependency Injection',
              'Dependency Injection Container',
              'Inversion of Control', 'Clean Architecture'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ]
)
