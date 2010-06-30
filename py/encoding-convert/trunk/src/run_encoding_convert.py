#!/usr/bin/python
import os,sys
from encoding_convert import convert as convert

def copy_file_to_pwd(filename):
    f1 = open(filename)
    new_filename = filename[1:]
    new_filename_folder = new_filename[:new_filename.rfind('/')]
    try:
        os.makedirs(new_filename_folder)
    except OSError, e:
        pass;
    f2 = open(new_filename,'w')
    f2.write(f1.read())
    f1.close()
    f2.close()
    
def run_convert(filename):
    if not convert(filename):
        copy_file_to_pwd(filename)

def explore(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(root, file)
            run_convert(path)

def main():
    for path in sys.argv[1:]:
        if os.path.isfile(path):
            run_convert(path)
        elif os.path.isdir(path):
            explore(path)

if __name__ == "__main__":
    main()