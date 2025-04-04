from textnode import *
import shutil 
import os

def recursive_copy(source="static", destination="public"):
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
        



def main():
    recursive_copy()

main()