from setuptools import setup, find_packages

setup(
    name='nn_metrics',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'nn_metrics = nn_metrics.scripts.cli:main'
        ]
    },
    author='Ariffudin',
    author_email='sudo.ariffudin@email.com',
    description='A collection of neural network machine learning error metrics.',
    long_description=open('README.md').read(),
    long_description_content_type='text/plain',
    license='MIT',
    keywords='nn neural-network metrics nn-metrics',
    url='https://github.com/arif-x/nn-metrics',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    dependency_links=[
        'git+https://github.com/arif-x/nn-metrics'
    ],
    project_urls={
        'Source': 'https://github.com/arif-x/nn-metrics',
        'Source Code': 'https://github.com/arif-x/nn-metrics'
    }
)