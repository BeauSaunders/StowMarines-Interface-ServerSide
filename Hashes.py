


import JSONFunctions
from hashlib import sha256
import os
import re


# Get Location of Current File path, so can open smi_ss_cfg.txt
CurrentPythonLocator = os.path.dirname(os.path.realpath(__file__))
smi_ss_cfg_Locator = CurrentPythonLocator + "\\" + "smi_ss_cfg.txt"

print(smi_ss_cfg_Locator)
DirectoryLocations = []

with open(smi_ss_cfg_Locator,mode= "r") as Locators:
    for line in Locators:
        line = line.strip()
        DirectoryLocations.append(line)
        
    HashLOCATOR = DirectoryLocations[2]
    




def create_hash_dict(mod_location, Modname):
    '''Appends to a dictionary that holds the file name/location in mod, and the hash'''

    global hashes_dict

    hashes_dict = {
        
    }

    files_arr = []

    for root, dirs, files in os.walk(mod_location):
        for file in files:

            # Get the full file path
            full_file_LOCATOR = os.path.join(root, file)
            files_arr.append(full_file_LOCATOR)
           
    no_of_files = len(files_arr)
    progress_tracker = 0
    printProgressBar(0, no_of_files, prefix = 'Progress:', suffix = 'Complete', length = 50)




    for file in files_arr:
        # calls to the "openfilecontent" function, where its contents will be read
        progress_tracker += 1
        file_content = openfilecontent(file)
        
        # Example hash function (replace with your actual hash function)
        hash(file_content, file)
        printProgressBar(progress_tracker, no_of_files, prefix = 'Progress:', suffix = 'Complete', length = 50)
        # print(f"        {progress_tracker} / {no_of_files}", end="\r")


    CreateJSON(hashes_dict, Modname)

    return 0

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
    



def openfilecontent(file):
    '''Opens each file to read the content inside'''

    with open(file, mode="rb") as f:
        
        file_content = f.read()

        string_data = file_content.decode('utf-8', errors='ignore')  # Convert bytes to string (utf-8 encoding)


    return string_data





def hash(file_content, full_file_LOCATOR):
    '''Creates a hash for all content inside of each file'''

    global file_LOCATOR

    # Converts input (file content) into hash
    hash = sha256(file_content.encode('utf-8')).hexdigest()

    index = full_file_LOCATOR.index("@")
    file_LOCATOR = full_file_LOCATOR[index:]

    
    file_LOCATOR = re.sub(r'\\', "/", file_LOCATOR)




    hashes_dict.update({file_LOCATOR: hash})

    return hashes_dict





def CreateJSON(hashes_dict, Modname):
    '''Fromats hash Dict to JSON format and writes to the json file inside of hash directory location'''

    All_Hashes_JsonFormat = JSONFunctions.FormatJSON(hashes_dict)


    hashname = Modname + "_hashes"
    JSON_File_Location = HashLOCATOR + "\\" + hashname + ".json"
    

    with open(JSON_File_Location, mode ="w") as f:
        f.write(All_Hashes_JsonFormat)

    print(f"\n --- {Modname} Was Succesfully stored as a HASH --- \n")
        
    