from setuptools import setup, find_packages

setup(
    name='workhub_client',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    # include additional metadata such as author, description, classifiers
    author="WorkHub Platform Inc.",
    author_email="ashaheen@workhub.ai",
    description="Python API to use WorkHub API for conversational AI.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
