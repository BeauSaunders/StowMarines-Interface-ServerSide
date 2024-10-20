


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

    # Calculates all subdirs infinitely in mod
    subdirs = [x[0] for x in os.walk(mod_location)]

    hashes_dict = {
        
    }


    for subdir in subdirs:
        for root, dirs, files in os.walk(subdir):
            for file in files:
                
                # Get location of current file in memory
                full_file_LOCATOR = os.path.join(root, file)

                # calls to the "openfilecontent" function, where it's contents will be read
                file_content = openfilecontent(full_file_LOCATOR)


                hash(file_content, full_file_LOCATOR)


            break

    CreateJSON(hashes_dict, Modname)

    return 0





def openfilecontent(file):
    '''Opens each file to read the content inside'''

    with open(file, mode="r") as f:
        file_content = f.read()
    return file_content





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
        
    