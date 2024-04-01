from setuptools import setup, find_packages
from setuptools.command.install import install
import time


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='MonoCipher',
    version='0.1.4b0',
    description='A package for monoalphabetic ciphers (message encryption and decryption).',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/rakeshkanna-rk/MonoCipher',
    author='Rakesh Kanna',
    license='MIT',
    author_email='rakeshkanna0108@gmail.com',
    project_urls={
        'GitHub': 'https://github.com/rakeshkanna-rk/MonoCipher/',
        'PyPI' : 'https://pypi.org/project/MonoCipher/'
    },
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.20.0",
        "click>=8.1.7",
        "colorama>=0.4.6"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'monocipher = MonoCipher:mc_cli' 
        ]
    },
    keywords=['encryption', 'cryptography', 'security'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
