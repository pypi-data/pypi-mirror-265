#!/usr/bin/env python

import re
from pathlib import Path

from setuptools import setup


def find_version(file_paths):
    version_file = Path(file_paths).read_text()
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name="robotframework-debug",
    version=find_version("RobotDebug/version.py"),
    description="RobotFramework debug shell",
    long_description=Path("README.rst").read_text(),
    long_description_content_type=("text/x-rst"),
    author="René Rohner",
    author_email="snooz@postoe.de",
    license="New BSD",
    packages=["RobotDebug"],
    entry_points={
        "console_scripts": [
            "irobot = RobotDebug.shell:shell",
            "robotdebug = RobotDebug.shell:shell",
        ],
    },
    zip_safe=False,
    url="https://github.com/imbus/robotframework-debug/",
    keywords="robotframework,debug,shell,repl",
    install_requires=[
        "prompt-toolkit >= 3.0.38",
        "robotframework >= 5.0, < 8.0",
        "pygments >= 2.14.0",
        "pyperclip >= 1.8.2",
    ],
    python_requires=">=3.8.0",
    tests_require=["pexpect", "coverage", "docutils"],
    test_suite="tests.test_debuglibrary.suite",
    platforms=["Linux", "Unix", "Windows", "MacOS X"],
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
    ],
)
