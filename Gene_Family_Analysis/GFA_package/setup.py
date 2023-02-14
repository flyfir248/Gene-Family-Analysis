"""The setup script."""

from setuptools import setup, find_packages

requirements = [
    'Click',
    'matplotlib',
    'pandas',
    'requests',
    'scipy',
    'Pillow',
    'pathlib',
    'flask',
    'typing',
    'logging',
]

test_requirements = ['pytest>=3', ]

setup(
    author="group4",
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    description="Gene Family analysis Package",
    entry_points={
        'console_scripts': [
            'GFA=GFA.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='GFA',
    name='GFA',
    packages=find_packages(include=['GFA', 'GFA.*']),
    test_suite='Tests',
    tests_require=test_requirements,
    version='0.1.0',
    zip_safe=False,
)
