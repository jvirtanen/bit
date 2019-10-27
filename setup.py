from setuptools import setup, find_packages


setup(
    name='bit',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bit = bit.__main__:main'
        ]
    }
)
