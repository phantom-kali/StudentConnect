"""
Use this for quick overview of a category

"""


import os

def print_urls_content(root_folder):
    # Traverse the folder and its subfolders
    for dirpath, _, filenames in os.walk(root_folder):
        if 'models.py' in filenames:
            urls_file_path = os.path.join(dirpath, 'models.py')
            print(f'Contents of {urls_file_path}:')
            with open(urls_file_path, 'r') as file:
                print(file.read())
            print('-' * 80)  # Separator for readability

if __name__ == '__main__':
    root_folder = '.'
    print_urls_content(root_folder)
