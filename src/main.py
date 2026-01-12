import os
import shutil
import sys

from textnode import *
from htmlnode import *
from markdown_blocks import *

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

def main():
    recursive_copy()
    generate_pages_recursive()

def recursive_copy(source="static", desitination="docs"):
    if not os.path.exists(source):
        raise Exception("source path does not exist")
    
    if os.path.exists(desitination):
        shutil.rmtree(desitination)
    os.mkdir(desitination)

    source_items = os.listdir(source)
    for source_item in source_items:
        source_item_path = os.path.join(source, source_item)
        desitination_item_path = os.path.join(desitination, source_item)

        if os.path.isfile(source_item_path):
            print(f"Copying file: {source_item} to {desitination}")
            shutil.copy(source_item_path, desitination_item_path)
        else:
            print(f"Creating directory: {desitination_item_path}")
            os.mkdir(desitination_item_path)
            recursive_copy(source_item_path, desitination_item_path)

    return

def generate_page(from_path="content/index.md", template_path="template.html", dest_path="docs/index.html", basepath=basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        markdown_contents = f.read()

    with open(template_path) as t:
        template = t.read()

    html_content = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)

    page_contents = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    page_contents = page_contents.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as d:
        d.write(page_contents)

def generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path="docs", basepath=basepath):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
        return
    
    dir_paths = os.listdir(dir_path_content)
    for dir_path in dir_paths:
        if os.path.isfile(dir_path):
            generate_page(dir_path, template_path, dest_dir_path, basepath)

        new_dir_path = os.path.join(dir_path_content, dir_path)
        new_dest_path = os.path.join(dest_dir_path, dir_path).replace(".md", ".html")
        generate_pages_recursive(new_dir_path, template_path, new_dest_path, basepath)


if __name__ == "__main__":
    main()