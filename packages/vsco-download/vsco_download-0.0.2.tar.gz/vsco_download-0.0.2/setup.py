from setuptools import setup, find_packages
setup(
    name='vsco_download',
    version='0.0.2',
    author='Lockermanwxlf',
    author_email='sexyandhandsome12@gmail.com',
    description='A wrapper for VSCO download endpoints',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    install_requires=['requests']
)