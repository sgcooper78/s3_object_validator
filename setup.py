from setuptools import setup, find_packages

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name="s3_object_validator",
    version="0.0.2",
    url='https://github.com/sgcooper78/s3_object_validator',
    author="Scott Cooper",
    author_email="sgcooper78@gmail.com",
    description="Validator for S3 object key names",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'aws', 's3'],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: GNU Affero General Public License v3",
    "Operating System :: OS Independent",
    ],
    entry_points={'console_scripts': ['s3_object_validator = s3_object_validator.validator:main']},
    include_package_data=True
)