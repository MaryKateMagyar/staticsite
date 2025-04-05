import shutil 
import os
import sys

from textnode import *
from htmlnode import *

basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

def recursive_copy(source="static", destination="docs"):
    if not os.path.exists(source):
        raise Exception("source path does not exist")
    
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    os.mkdir(destination)

    source_items = os.listdir(source)

    for item in source_items:
        source_item_path = os.path.join(source, item)
        destination_item_path = os.path.join(destination, item)

        if os.path.isfile(source_item_path):
            print(f"Copying file: {source_item_path} to {destination_item_path}")
            shutil.copy(source_item_path, destination_item_path)
        else:
            print(f"Creating directory: {destination_item_path}")
            os.mkdir(destination_item_path)
            recursive_copy(source_item_path, destination_item_path)
    
    return
        
def generate_page(from_path="content/index.md", template_path="template.html", dest_path="docs/index.html", basepath=basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    
    with open(from_path) as f:
        markdown_contents = f.read()

    with open(template_path) as t:
        template_contents = t.read()

    content = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)
    
    page_contents = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", content)
    page_contents = page_contents.replace('href="/', f'href="{basepath}').replace("href='/", f"href='{basepath}")
    page_contents = page_contents.replace('src="/', f'src="{basepath}').replace("src='/", f"src='{basepath}")


    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as page:
        page.write(page_contents)

def generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path="docs", basepath=basepath):
    if os.path.isfile(dir_path_content):
        generate_page(dir_path_content, template_path, dest_dir_path)
        return

    dir_paths = os.listdir(dir_path_content)
    for path in dir_paths:
        if os.path.isfile(path):
            generate_page(path, template_path, dest_dir_path)
        
        new_dir_path = os.path.join(dir_path_content, path)
        new_dest_path = os.path.join(dest_dir_path, path).replace(".md", ".html")
        generate_pages_recursive(new_dir_path, template_path, new_dest_path)

def main():
    recursive_copy()
    generate_pages_recursive()


main()