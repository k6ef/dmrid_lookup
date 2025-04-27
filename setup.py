import re
from setuptools import setup

# Read the version dynamically from dmrid_lookup.py
with open("dmrid_lookup.py", "r") as f:
    version = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', f.read()).group(1)

setup(
    name="dmrid-lookup",
    version=version,
    py_modules=["dmrid_lookup"],
    install_requires=[
        "requests",
        "rich",
    ],
    entry_points={
        "console_scripts": [
            "dmrid_lookup=dmrid_lookup:main",
        ],
    },
    author="Mark Cohen",
    author_email="k6ef@k6ef.net",
    description="A CLI tool to lookup DMR ID from callsign or vice-versa using radioid.net",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/k6ef/dmrid-lookup",  # Update to your actual repo
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Ham Radio",
    ],
    python_requires=">=3.7",
)

