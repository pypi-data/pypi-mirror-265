from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='summator',
    version='0.0.1',
    author='Manar Yabrak',
    author_email='manar.mofid@gmail.com',
    description='A Python toolkit for sum two numbers.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['summator'],
    install_requires=[
        'numpy==1.21.4'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)