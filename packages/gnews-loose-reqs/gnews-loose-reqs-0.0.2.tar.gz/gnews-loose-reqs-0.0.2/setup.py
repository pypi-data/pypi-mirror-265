from setuptools import setup, find_packages

with open('requirements.txt') as f:
  requirements = f.read().splitlines()

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
    name='gnews-loose-reqs',
    version='0.0.2',
    # setup_requires=['setuptools_scm'],
    # use_scm_version={
    #     "local_scheme": "no-local-version"
    # },
    description=
    'It is just GNews 0.3.6 (https://github.com/ranahaani/GNews) with loose requeriments. I am in a hurry :)',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
