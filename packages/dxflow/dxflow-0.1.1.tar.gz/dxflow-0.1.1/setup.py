from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dxflow',
    version='0.1.1',
    author='DiPhyx Team',
    author_email='info@diphyx.com',
    description='A Python SDK for the DiPhyx cloud computing platform, designed to streamline scientific discovery.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/diphyx/dxflow_sdk',
    py_modules=['dxflow'],  # Specify the module name here
    install_requires=[
        'requests',
        'tuspy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.6',
)

