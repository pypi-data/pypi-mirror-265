from setuptools import setup

setup(
    name='strings_repository',
    version='0.2.0',
    description='Simple commandline tool for pulling data from strings repository (https://github.com/HereTrix/strings_repository)',
    url='https://github.com/HereTrix/strings_repository_cli',
    download_url='https://github.com/HereTrix/strings_repository_cli/archive/refs/tags/0.1.0.tar.gz',
    author='HereTrix',
    license='MIT',
    packages=['strings_repository'],
    install_requires=[
        'typer',
        'pyyaml',
        'requests',
    ],
    scripts=['bin/strings_repository'],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3',
    ]
)
