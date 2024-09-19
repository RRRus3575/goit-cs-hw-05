import argparse
import os
import asyncio
import shutil

def create_arg_parser():
    parser = argparse.ArgumentParser(description='Sort files into folders based on their extensions.')
    parser.add_argument(
        '--source', 
        type=str, 
        default=r'C:\Users\Руслан\Documents\GitHub\goit-cs-hw-05\task_1\test_source', 
        help='Path to the source folder (default: C:\\Users\\Руслан\\Documents\\GitHub\\goit-cs-hw-05\\task_1\\test_source)'
    )
    parser.add_argument(
        '--output', 
        type=str, 
        help='Path to the output folder (if not specified, it will be created inside the source folder)'
    )
    return parser

async def initialize_folders(source, output):
    if output is None:
        output = os.path.join(os.path.dirname(source), 'test_output')
    
    print(f"Output folder will be created at: {output}")

    if not os.path.exists(output):
        print(f"Creating output folder at: {output}")
        os.makedirs(output, exist_ok=True)
    else:
        print(f"Output folder already exists at: {output}")
    
    return output  


async def copy_file(file_path, output):
    extension = os.path.splitext(file_path)[1][1:]  
    if extension:  
        target_folder = os.path.join(output, extension)
        os.makedirs(target_folder, exist_ok=True)  

        target_file_path = os.path.join(target_folder, os.path.basename(file_path))

        if not os.path.exists(target_file_path):
            try:
                await asyncio.to_thread(shutil.copy, file_path, target_file_path)  
                print(f"Copied {file_path} to {target_file_path}")
            except Exception as e:
                print(f"Error copying {file_path}: {e}") 
        else:
            print(f"File {target_file_path} already exists. Skipping.")

async def read_folder(source, output):
    tasks = []
    for root, _, files in os.walk(source):
        for file in files:
            file_path = os.path.join(root, file)
            tasks.append(copy_file(file_path, output))
    await asyncio.gather(*tasks)

async def main():
    parser = create_arg_parser()
    args = parser.parse_args()
    output_folder = await initialize_folders(args.source, args.output)
    await read_folder(args.source, output_folder)

if __name__ == '__main__':
    asyncio.run(main())
