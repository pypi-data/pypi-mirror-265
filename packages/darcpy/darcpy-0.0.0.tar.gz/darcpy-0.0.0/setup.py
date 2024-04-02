from setuptools import setup, find_packages

setup(
    name='darcpy',
    version='0.0.0',
    packages=find_packages(),
    description='A very serious and righteous mapping library.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kevin K McGuigan',
    author_email='kmcguig@outlook.com',
    license='MIT',
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)