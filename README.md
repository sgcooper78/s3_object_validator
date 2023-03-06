
# s3_object_validator

S3 Object Validtor

  
This tool is meant to scan through a directory or files to clean them up before you upload them directly to S3.

This tool is destructive by default so make sure to run with -s if you want to just scan what files would cause potential issues.

The tool can be ran directory as a CLI or with the python -m interface.

    s3_object_validator path
or

    python3 s3_object_validator path

## Import

If you need to import then

    from s3_object_validator import validator

## options

 - Path required first argument, relative or full path of where to scan. 
 - -d or --directory makes sure to only scan directories.
 - -f or --files  makes sure to only scan files.
 - -s or --scan to only scan and not do anything destructive. 
 - -v or --verbose to add in more output