from setuptools import setup, find_packages

setup(
    name='anytone',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', 'unidecode',
    ],
    entry_points='''
        [console_scripts]
        anytone=bmr.anytone:main
    ''',
)