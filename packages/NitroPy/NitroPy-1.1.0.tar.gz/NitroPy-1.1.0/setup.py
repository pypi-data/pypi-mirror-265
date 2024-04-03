from setuptools import setup

setup(
    name='NitroPy',
    version='1.1.0',
    author='Malakai',
    author_email='Almightyslider2@gmail.com',
    description='A package for interacting with Nitrotype racers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    #    url='https://github.com/yourusername/nitrotype-package',
    packages=[
        "nitrotype"
    ],
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

    python_requires='>=3.6',
    install_requires=[
        'cloudscraper',
        'beautifulsoup4',
    ],
)
