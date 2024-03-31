from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='DataPrepKitt',
    version='0.0.2',
    author='Manar Yabrak',
    author_email='manar.mofid@gmail.com',
    description='This package aims to be a comprehensive toolkit for preprocessing datasets.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['DataPrepKitt'],
    install_requires=[
        'numpy==1.21.4',
        'pandas==1.3.4',
        'openpyxl==3.1.2'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)