from setuptools import setup, find_packages

setup(
    name="vectorview",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Vectorview",
    author_email="lukas@vectorview.ai",
    description="Automated red teaming of LLM chatbots",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Vectorview/vectorview_py",
)
