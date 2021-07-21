from setuptools import setup, find_packages


setup(
    name='commons',
    version='1.0.3',
    description='commons library',
    author='Wittgena Lee',
    author_email='wittgena@gmail.com',
    packages=find_packages(),
    install_requires=[
        "selenium",
        "boto3",
        "xmltodict",
        "google-api-python-client",
        "oauth2client",
        "openpyxl",
        "dropbox"
    ]
)
