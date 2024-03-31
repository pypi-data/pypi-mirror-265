from setuptools import setup,find_packages

with open('readme.md','r') as f:
    description = f.read()
setup(
    name = 'wordcombinator',
    version = '0.2.1',
    packages = find_packages(),
    install_requires = [
        # Add third-party libraries
    ],
    author='saish',
    url = 'https://github.com/SaishSaw',
    long_description=description,
    long_description_content_type='text/markdown'
)