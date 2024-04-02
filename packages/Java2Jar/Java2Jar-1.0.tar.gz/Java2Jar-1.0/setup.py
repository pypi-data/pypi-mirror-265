from setuptools import setup, find_packages

# Read the contents of your README.md file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Java2Jar',
    version='1.0',
    packages=find_packages(),
    scripts=['Java2Jar.py'],
    description='A tool to convert Java files to JAR files',
    author='Soumalya Das',
    long_description=long_description,  # Use the contents of your README.md file
    long_description_content_type='text/markdown',  # Set the content type of the long description
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)