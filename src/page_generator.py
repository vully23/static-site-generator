import os
from pathlib import Path
from block_markdown import markdown_to_html_node, extract_title
from copy_files import copy

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        source_markdown_file = file.read()
    with open(template_path) as file:
        template = file.read()
    html_string = markdown_to_html_node(source_markdown_file).to_html()
    title = extract_title(source_markdown_file)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    os.makedirs(os.path.dirname(dest_path) , exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(source_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(source_path, template_path, dest_path)
        else:
            generate_pages_recursive(source_path, template_path, dest_path)