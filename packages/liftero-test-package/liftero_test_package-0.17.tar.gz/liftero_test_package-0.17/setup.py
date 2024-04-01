from setuptools import setup, find_packages

setup(
    name='liftero_test_package',
    version='0.17',
    packages=find_packages(),
    install_requires=[
        # List your project
        # 's dependencies here.
        # For example: 'requests >= 2.22.0',
    ],
    # Additional metadata about your package.
    author="Tomasz Palacz",
    author_email="tomasz@liftero.com",
    description="Dedicated package for parsing, analysis and plotting test results data",
    license="MIT",
    keywords="rocket engine test analysis",
)
