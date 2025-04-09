import os
import shutil
from copy_files import copy
from page_generator import generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()