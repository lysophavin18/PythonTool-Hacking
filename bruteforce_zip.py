from zipfile import ZipFile
import argparse
import os

parser = argparse.ArgumentParser(
    description="\nUsage python3 bruteforce_zip.py -z <zipfile.zip> -p <passfile.txt>")
parser.add_argument("-z", dest="ziparchive", help="zip archive file", required=True)
parser.add_argument("-p", dest="passfile", help="Password File", required=True)
parsed_arg = parser.parse_args()

ziparchive_path = os.path.abspath(parsed_arg.ziparchive)
passfile_path = os.path.abspath(parsed_arg.passfile)

try:
    ziparchive = ZipFile(ziparchive_path)
except Exception as e:
    print(f"Error opening zip file: {e}")
    print(parser.description)
    exit(0)

foundpass = ""
try:
    with open(passfile_path, "r") as f:
        for line in f:
            password = line.strip("\n")
            password = password.encode("utf-8")

            try:
                ziparchive.extractall(pwd=password)
                print("\nFound password: ", password.decode())
                foundpass = password.decode()
                break
            except RuntimeError:
                pass
            except zipfile.BadZipFile:      
                pass
            except zipfile.LargeZipFile:
                pass

    if foundpass == "":
        print("\nPassword not found. Try a bigger password list.")
except FileNotFoundError as e:
    print(f"Error opening password file: {e}")
