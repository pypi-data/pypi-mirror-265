from setuptools import find_packages, setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

DESCRIPTION = 'OLS decrypt library'
setup(
    name='olscrypto',
    packages=find_packages(include=['olscrypto']),
    version='0.1.7',
    author='Highmaru, Inc.',
    author_email="dhshin@highmaru.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest==4.4.1'],
    # test_suite='tests'
    install_requires=['pycryptodome>=3.20.0'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)