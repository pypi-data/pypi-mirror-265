from setuptools import setup, find_packages

setup(
    name="llmreader",
    version="0.2.0",
    description="Intercept OpenAI inputs",
    author="Ethan Hou",
    author_email="ethanfhou10@gmail.com",
    packages=find_packages(),
    install_requires=[
        # Add your package dependencies here
        # e.g., 'requests >= 2.25.1',
    ],
    classifiers=[
        # Trove classifiers
        # Full list at https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
