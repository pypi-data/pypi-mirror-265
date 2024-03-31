from setuptools import setup

setup(
    author='dcry2306',
    author_email='kilaz2306@gmail.com',
    name='dcrypr',
    version='0.0.1',
    description='A simple package for https://app.tea.xyz/. Example pr1 - https://github.com/dcry2306/pr2.git and pr2 - https://github.com/dcry2306/pr2.git',
    url='https://github.com/CryptoGu1/GuDory.git',
    project_urls={
        'Homepage': 'https://github.com/dcry2306/pr1.git',
        'Source': 'https://github.com/dcry2306/pr1.git',
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
        'pr2',
        'pr3',
        # add your projects
    ],
)
