from setuptools import setup, find_packages

setup(
    name="JustPeachy",
    version="0.0.1",
    author="JustPeachy.ai",
    author_email="dev@justpeachy.ai",
    description="A basic 'hello world' package for a multi-agent autonomous AI agent system framework",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/justpeachyai/JustPeachy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
