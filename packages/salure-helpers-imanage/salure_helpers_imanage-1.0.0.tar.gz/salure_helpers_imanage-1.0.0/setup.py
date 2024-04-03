from setuptools import setup


setup(
    name='salure_helpers_imanage',
    version='1.0.0',
    description='Imanage cloud wrapper from Salure',
    long_description='Imanage cloud wrapper from Salure',
    author='D&A Salure',
    author_email='support@salureconnnect.com',
    packages=["salure_helpers.imanage"],
    license='Salure License',
    install_requires=[
        'salure-helpers-salureconnect>=1',
        'requests>=2,<=3'
    ],
    zip_safe=False,
)