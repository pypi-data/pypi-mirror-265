from setuptools import setup, find_packages

setup(
    name='neural_network_implementation',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'nn_error_metrics'
    ],
    author='Ariffudin',
    author_email='sudo.ariffudin@email.com',
    description='A neural network implementation.',
    long_description=open('README.md').read(),
    long_description_content_type='text/plain',
    license='MIT',
    keywords='nn neural-network',
    url='https://github.com/arif-x/neural-network-implementation',
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
        'git+https://github.com/arif-x/neural-network-implementation'
    ],
    project_urls={
        'Source': 'https://github.com/arif-x/neural-network-implementation',
        'Source Code': 'https://github.com/arif-x/neural-network-implementation'
    }
)