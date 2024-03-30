""" ... """

from setuptools import find_packages, setup

setup(
    name='asm-secrets-manager',
    version='1.0.1',
    description='Just another Secrets Manager',
    long_description="This library objective is to aim the variables and secrets management for our software applications on remote repositories on most safe way.",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/albertosanmartinmartinez/secrets-manager", # https://albertosanmartinmartinez.es
    author='Alberto Sanmartín Martínez',
    author_email='albertosanmartinmartinez@gmail.com',
    license="GPL v3",
    packages=find_packages(),
    install_requires=[
      "rsa==4.9"
    ],
    test_require=[
      
    ],
    classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Environment :: Console",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: GNU General Public License (GPL)",
      "Natural Language :: English",
      "Operating System :: Unix",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)