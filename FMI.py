import os
import hashlib
import time
import logging
from colorama import init, Fore, Back, Style

# Setting up logging environment
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Creating a file handler and set the logging level
fh = logging.FileHandler(r'C:\Users\ASUS\Desktop\Project\FMI-Python\Logs\Integrity_File_Monitoring_Log.log')
fh.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(fh)



def calculate_file_hash(filepath):
    with open(filepath, 'rb') as f:
        file_hash = hashlib.sha256()
        while chunk := f.read(4096):
            file_hash.update(chunk)
        return file_hash.hexdigest()

def erase_baseline_if_already_exist():
    baseline_file_path = r'C:\Users\ASUS\Desktop\Project\FMI-Python\baseline.txt'
    if os.path.exists(baseline_file_path):
        os.remove(baseline_file_path)

while True:
    print()
    print("\033[36mWhat would you like to do?\033[0m")
    print("\033[35mA) Collect new Baseline?\033[0m")
    print("\033[35mB) Begin Monitoring files with saved Baseline?\033[0m")
    print("\033[35mC) Exit?\033[0m")

    response = input("Please enter 'A' or 'B': ").upper()
    print()

    if response == 'A':
        # Delete baseline if exist
        erase_baseline_if_already_exist()

        # Calculate hash from the target files and store in baseline.txt
        # Collect all the files in the folder
        files_folder = r'C:\Users\ASUS\Desktop\Project\FMI-Python\Files'
        files = os.listdir(files_folder)

        # For each file calculate the hash, and write to baseline.txt
        baseline_file = r'C:\Users\ASUS\Desktop\Project\FMI-Python\baseline.txt'
        with open(baseline_file, 'w') as f:
            files_folder = r'C:\Users\ASUS\Desktop\Project\FMI-Python\Files'
            files = os.listdir(files_folder)
            for file_name in files:
                file_path = os.path.join(files_folder, file_name)
                file_hash = calculate_file_hash(file_path)
                f.write(f"{file_path}|{file_hash}\n")

    elif response == 'B':
        # Load file hash from baseline.txt and store them in a dictionary
        file_hash_dictionary = {}
        baseline_file = r'C:\Users\ASUS\Desktop\Project\FMI-Python\baseline.txt'
        with open(baseline_file, 'r') as f:
            for line in f:
                file_path, file_hash = line.strip().split('|')
                file_hash_dictionary[file_path] = file_hash

        # Begin monitoring files with saved baseline
        while True:
            time.sleep(1)

            # Collect all the files in the folder
            files_folder = r'C:\Users\ASUS\Desktop\Project\FMI-Python\Files'
            files = os.listdir(files_folder)
            #files = os.listdir(os.path.join(os.getcwd(), 'Desktop', 'Project', 'FMI-Python', 'Files'))

            # For each file calculate the hash, and compare with the saved hash
            for file_name in files:
                file_path = os.path.join(files_folder, file_name)
                file_hash = calculate_file_hash(file_path)

                # Notify if a new file has been created
                if file_path not in file_hash_dictionary:
                    #print(Fore.GREEN + f"{file_path} has been created!")
                    logger.info('File created: {}'.format(file_path))
                    file_hash_dictionary[file_path] = file_hash

                else:
                    if file_hash_dictionary[file_path] == file_hash:
                        # The file has not changed.
                        pass
                    else:
                        #print(Fore.YELLOW + f"{file_path} has been changed!!!")
                        logger.warning('File modified: {}'.format(file_path))
                        file_hash_dictionary[file_path] = file_hash

            # Check if any baseline file has been deleted
            for file_path in file_hash_dictionary:
                if not os.path.exists(file_path):
                    # One of the baseline file has been deleted!!
                    #print(Fore.RED + f"{file_path} has been deleted!!!")
                    logger.critical('File deleted: {}'.format(file_path))

    elif response == 'C':
        break
logging.shutdown()