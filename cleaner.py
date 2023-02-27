import argparse
from pathlib import Path
import s3ObjectValidator

parser = argparse.ArgumentParser()

parser.add_argument("Path", type=str ,help="Path to scan directories/files")
parser.add_argument("-d", "--directory", default=False, action="store_true" ,help="Makes scan only include directories")
parser.add_argument("-f", "--files", default=False, action="store_true" ,help="Makes scan only include files")
parser.add_argument("-v", "--verbose", default=False, action="store_true" ,help="Increase verbosity of program" )

args = parser.parse_args()

if not Path(args.Path).exists():
    print("File or directory path does not exist")
    exit()

if args.directory:
    cleaned = s3ObjectValidator.sanitizeStructure(args.Path,False,True)
elif args.files:
    cleaned = s3ObjectValidator.sanitizeStructure(args.Path,True,False)
else:
    cleaned = s3ObjectValidator.sanitizeStructure(args.Path,True,True)
print("Done sanitizing")