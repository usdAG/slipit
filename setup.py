import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='slipit',
    version='1.0.0',
    url='https://github.com/usdAG/slipit',
    author='Tobias Neitzel (@qtc_de)',
    description='slipit - Utility for creating archives with path traversal elements',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
                        'python-magic',
                     ],
    packages=[
                'slipit',
                'slipit.provider'
             ],
    scripts=[
                'bin/slipit'
            ],
    classifiers=[
                    'Programming Language :: Python :: 3',
                    'Operating System :: Unix',
                    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                ],
)
