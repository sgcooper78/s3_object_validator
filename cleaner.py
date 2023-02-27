import argparse
from pathlib import Path
import s3ObjectValidator

parser = argparse.ArgumentParser()

parser.add_argument("Path", type=str ,help="Path to scan directories/files")
parser.add_argument("-d", "--directory", default=False, action="store_true" ,help="Makes scan only include directories")
parser.add_argument("-s", "--scan", default=True, action="store_true" ,help="Makes scan non-destructive")
parser.add_argument("-f", "--files", default=False, action="store_true" ,help="Makes scan only include files")
parser.add_argument("-v", "--verbose", default=False, action="store_true" ,help="Increase verbosity of program" )

args = parser.parse_args()

if not Path(args.Path).exists():
    print("File or directory path does not exist")
    exit()

cleaned = s3ObjectValidator.sanitizeStructure(args.Path,args.files,args.directory,args.scan,args.verbose)
print("Done sanitizing")