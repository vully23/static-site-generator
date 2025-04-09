import sys
import os
import shutil
from copy_files import copy
from page_generator import generate_pages_recursive

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()