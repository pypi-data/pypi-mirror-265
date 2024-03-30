from setuptools import setup

setup(
    author='CryptoGu1',
    author_email='Kriptoairdrop9@gmail.com',
    name='Dorytea1',
    version='1.0.6',
    description='A simple package for https://app.tea.xyz/. Example Dory1 - https://github.com/CryptoGu1/Dorytea1.git and tea-Dory2 - https://github.com/CryptoGu1/Dorytea2.git',
    url='https://github.com/CryptoGu1/Dorytea1.git',
    project_urls={
        'Homepage': 'https://github.com/CryptoGu1/Dorytea1.git',
        'Source': 'https://github.com/CryptoGu1/Dorytea1.git',
    },
    py_modules=['hello_tea'],
    entry_points={
        'console_scripts': [
            'hello-tea=hello_tea:hello_tea_func'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests>=2.20.0',
        'Dorytea2',
    ],
)
