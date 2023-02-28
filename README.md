# s3_object_validator
S3 Object Validtor

This tool is meant to scan through a directory or files to clean them up before you upload them directly to S3.
This tool is destructive by default so make sure to run with -s if you want to just scan what files would cause potential issues.
Run tool with 
python3 s3_object_validator.py path

## Import
If you need to import then import the file
from s3_object_validator import validator
