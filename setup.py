from setuptools import setup

setup(
    name="chatgpt_md_converter",
    version="0.3.8",
    author="Kostiantyn Kriuchkov",
    author_email="latand666@gmail.com",
    description="A package for converting markdown to HTML for chat Telegram bots",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/botfather-dev/formatter-chatgpt-telegram",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
