from setuptools import setup, find_packages


setup(
    name="job-dispatcher",
    version="0.2.0",
    description="A simplified python interface for running embarassingly parallel calculations.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Mattia Felice Palermo",
    author_email="mattiafelice.palermo@gmail.com",
    packages=find_packages(),
    package_data={"jobdispatcher": ["packing/*",],},
    url="https://github.com/mattiafelice-palermo/job-dispatcher", 
    install_requires=[],
    classifiers=['Development Status :: 5 - Production/Stable',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3',
                 'Topic :: Software Development :: Libraries :: Python Modules',
                 'Topic :: Scientific/Engineering'],
)
