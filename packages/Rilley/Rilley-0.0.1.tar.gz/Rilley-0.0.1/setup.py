from setuptools import setup

setup(
    author='CryptoGu1',
    author_email='Kriptoairdrop9@gmail.com',
    name='Rilley',
    version='0.0.1',
    description='A simple package for https://app.tea.xyz/. Example Second project https://github.com/CryptoGu1/Rilley1.git and third - https://github.com/CryptoGu1/Rilley2.git',
    url='https://github.com/CryptoGu1/Rilley.git',
    project_urls={
        'Homepage': 'https://github.com/CryptoGu1/Rilley.git',
        'Source': 'https://github.com/CryptoGu1/Rilley.git',
    },
    py_modules=['hi_tea'],
    entry_points={
        'console_scripts': [
            'hi-tea=hi_tea:hello_tea_xyz'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
    install_requires=[
        'Rilley1',
        'Rilley2',
        # add your projects
    ],
)
