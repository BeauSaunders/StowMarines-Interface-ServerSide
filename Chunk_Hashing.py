


import JSONFunctions
from hashlib import sha256
import hashlib
import os
import re
import mmap
import time
from concurrent.futures import ThreadPoolExecutor, as_completed





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
    
    hashes_dict = {}

    files_arr = []

    for root, _, files in os.walk(mod_location):
        for file in files:

            # Get the full file path
            full_file_LOCATOR = os.path.join(root, file)
            files_arr.append(full_file_LOCATOR)

           
    no_of_files = len(files_arr)
    progress_tracker = 0
    printProgressBar(0, no_of_files, prefix = 'Progress:', suffix = 'Complete', length = 50)


    total_start_time = time.time()


    with ThreadPoolExecutor(max_workers=4) as executor:
        # Correctly submit the hash_file with full file path
        future_to_file = {executor.submit(hash_file, file): file for file in files_arr}

        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                # Get the result directly from hash_file
                file_LOCATOR, hash_value = future.result()
                if hash_value is not None:  # Only update if hash_value is valid
                    # Update the global dictionary
                    hashes_dict.update({file_LOCATOR: hash_value})

                # Increment progress tracker
                progress_tracker += 1
                printProgressBar(progress_tracker, no_of_files, prefix='Progress:', suffix='Complete', length=50)

            except Exception as exc:
                print(f"{file} generated an exception: {exc}")

        
    total_end_time = time.time()
    total_duration = total_end_time - total_start_time
    print(f"\nTotal time taken for hashing all files {total_duration:.6f} seconds.")

    CreateJSON(hashes_dict, Modname)

    return 0





def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
    





def hash_file(full_file_LOCATOR):
    '''Creates a hash for all content inside of each file'''
    
    try:

        # Extract part of the file location (e.g., everything after "@")
        index = full_file_LOCATOR.index("@")
        file_LOCATOR = full_file_LOCATOR[index:]
        file_LOCATOR = re.sub(r'\\', "/", file_LOCATOR)


        # Open the file and create hash
        with open(full_file_LOCATOR, mode="rb") as f:
            # Memory-map the file
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

            hasher = hashlib.sha256()

            # Read the file in chunks
            chunk_size = 1024 * 1024 * 64  # 64 MB chunks
            while True:
                chunk = mm.read(chunk_size) # Read a chunk from the memory-mapped file
                if not chunk: # If the chunk is empty, we've reached the end of the file
                    break
                hasher.update(chunk)  # Update the hash with the chunk of data

            mm.close()

        hash_value = hasher.hexdigest()
        return file_LOCATOR, hash_value
    
    except FileNotFoundError:
        print(f"File: {full_file_LOCATOR} not found.")
        return None, None
    except Exception as e:
        print(f"Error processing file {full_file_LOCATOR}: {e}")
        return None, None





def CreateJSON(hashes_dict, Modname):
    '''Fromats hash Dict to JSON format and writes to the json file inside of hash directory location'''

    All_Hashes_JsonFormat = JSONFunctions.FormatJSON(hashes_dict)


    hashname = Modname + "_hashes"
    JSON_File_Location = HashLOCATOR + "\\" + hashname + ".json"
    

    with open(JSON_File_Location, mode ="w") as f:
        f.write(All_Hashes_JsonFormat)

    print(f"\n --- {Modname} Was Succesfully stored as a HASH --- \n")
        
    