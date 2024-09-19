import os
import random
import string

def create_random_folder_name(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_test_files(base_folder):
    os.makedirs(base_folder, exist_ok=True)

    extensions = ['txt', 'jpg', 'pdf', 'png', 'docx']
    num_files = 5  

    for _ in range(10):  
        random_folder_name = create_random_folder_name()
        random_folder_path = os.path.join(base_folder, random_folder_name)

        os.makedirs(random_folder_path, exist_ok=True)

        for ext in extensions:
            for i in range(num_files):
                file_path = os.path.join(random_folder_path, f'test_file_{i + 1}.{ext}')
                with open(file_path, 'w') as f:
                    f.write(f'This is a test file for the {ext} extension.\n')

if __name__ == '__main__':
    create_test_files('test_source')  
