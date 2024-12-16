from setuptools import setup, find_packages

setup(
    name="meeting_assistant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=0.28.1",
        "python-dotenv>=1.0.0",
        "pydub>=0.25.1",
        "moviepy>=1.0.3",
        "requests>=2.31.0",
        "tiktoken>=0.5.1",
        "tqdm>=4.66.1",
        "numpy>=1.24.3",
    ],
    python_requires=">=3.7",
) 