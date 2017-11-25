from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = "needl",
    version = "0.0.1",
    author = "Paul Price",
    author_email = "paul.price@gmail.com",
    description = ("Random Internet traffic generator concealing your real traffic."),
    license = "MIT",
    keywords = "privacy tracking internet",
    url = "https://github.com/eth0izzle/Needl",
    packages = find_packages(),
    long_description=read('README.md'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'needl = needl.main:main'
            ]
        },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
)
