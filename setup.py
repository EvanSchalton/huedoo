from setuptools import setup, find_packages

setup(
    name='huedoo',
    version='0.0.0a0',
    description='Huedoo - Philips Hue Light Management',
    author='Evan Schalton',
    author_email='Evan.Schalton@Gmail.com',
    url='https://github.com/EvanSchalton/huedoo',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'pydantic'
    ],
)
