from setuptools import setup

requirements = []
f = open('requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    requirements.append(l.rstrip())
f.close()

sql_requirements = []
f = open('sql_requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    sql_requirements.append(l.rstrip())
f.close()

test_requirements = []
f = open('test_requirements.txt', 'r')
while True:
    l = f.readline()
    if l == '':
        break
    test_requirements.append(l.rstrip())
f.close()

f = open('README.md', 'r')
description = f.read()
f.close()

setup(
        name="funga-eth",
        version="0.8.0",
        description="Ethereum implementation of the funga keystore and signer",
        author="Louis Holbrook",
        author_email="dev@holbrook.no",
        packages=[
            'funga.eth.signer',
            'funga.eth',
            'funga.eth.cli',
            'funga.eth.keystore',
            'funga.eth.runnable',
            ],
        install_requires=requirements,
        extras_require={
            'sql': sql_requirements,
            },
        tests_require=test_requirements,
        entry_points = {
            'console_scripts': [
                'funga-ethd=funga.eth.runnable.signer:main',
                'eth-keyfile=funga.eth.runnable.keyfile:main',
                'eth-sign-msg=funga.eth.runnable.msg:main',
                ],
            },
        url='https://git.defalsify.org/funga-eth',
        include_package_data=True,
        long_description=description,
        long_description_content_type='text/markdown',
        )
