from setuptools import setup, find_packages


setup(
    name='enterble',
    version='1.1.6',
    description='BLE device scanner and data collector for Flowtime',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Natural Language :: Chinese (Simplified)',
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "Intended Audience :: Developers",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    url='https://github.com/Entertech/Enter-Biomodule-BLE-PC-SDK.git',
    author='Lockey',
    author_email='chenyitao@entertech.cn',
    license='Entertech',
    packages=find_packages(
        include=[
            'enterble',
            'enterble.*',
        ],
        exclude=[
            'tests',
            'docs',
            'examples',
            '__pycache__',
            '*.pyc',
            '*.pyo',
        ]
    ),
    include_package_data=False,
    install_requires=[
        'bleak==0.19.0',
    ],
    zip_safe=False
)
