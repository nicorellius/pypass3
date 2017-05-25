from setuptools import setup, find_packages

setup(
    name='pypass',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'click',
        'rdoclient',
        'pytest',
    ],
    entry_points="""
        [console_scripts]
        generate=scripts.generate:cli
    """,

    # Metadata for upload to PyPI
    author='Nick Vincent-Maloney (nicorellius)',
    author_email='nick@cistech.io',
    description="""PyPass3: Password Generator application.
        Dice Roll Optional, Mostly-Random Word, Number, 
        and Mixed Character Password Generator""",
    license='MIT',
    keywords='password passphrase numbers words mixed eff dice roll',
    url='http://pypass.cistech.io/',
)
