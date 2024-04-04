import os
from setuptools import setup, find_packages


def read_file(filepath):
    setuppy_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path_relative_to_setuppy = os.path.join(setuppy_dir, filepath)
    with open(absolute_path_relative_to_setuppy) as f:
        file_content = f.read()
    return file_content


__VERSION__ = "0.0.7"
README_TEXT = read_file("README.md")


# https://packaging.python.org/en/latest/key_projects/#setuptools
setup(
    name="guia_cli",
    version=__VERSION__,
    author="Anderson Bosa",
    description="Gu, a simple IA agent that specializes in software engineering, aiding in coding tasks and providing technical guidance.",
    long_description=README_TEXT,
    long_description_content_type="text/markdown",
    keywords="IA assistant gemini-pro",
    url="https://github.com/andersonbosa/guia-cli",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "crewai>=0.19.0",
        "langchain_google_genai",
        "python-dotenv>=1.0.1",
    ],
    entry_points={
        "console_scripts": [
            "gu = guia_cli.main:main",
            "guia = guia_cli.main:main",
            "gucli = guia_cli.main:main",
        ],
    },
)
