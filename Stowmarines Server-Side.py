


from pathlib import Path
import os
import JSONFunctions
import re
import shutil
import Chunk_Hashing

# Get Location of Current File path, so can open smi_ss_cfg.txt
CurrentPythonLocator = os.path.dirname(os.path.realpath(__file__))
smi_ss_cfg_Locator = CurrentPythonLocator + "\\" + "smi_ss_cfg.txt"

DirectoryLocations = []

with open(smi_ss_cfg_Locator,mode= "r") as Locators:
    for line in Locators:
        line = line.strip()
        DirectoryLocations.append(line)
    JSON_Location = DirectoryLocations[0]
    MODS_Directory = DirectoryLocations[1]


jsonData = JSONFunctions.LoadJSONFromFile(JSON_Location)

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'




def system():
    def start():
        global special

        '''Starting Menu/Console'''
        inp = input('''\nDo You Want To Update:
                    
    --- All (Case Sensitive) ---
    or
    --- Update Specific Mod ---
    or
    --- Del Specific Mod ---
                    \n''')
        
        # Decides which route to take based on Input
        if inp == "all":
            special = True
            alltocalculate()
            
        elif re.search("^del", inp):
            special = True
            deleteJSON(inp)
   
        else:
            special = False
            calculateModSize(inp)
        
        




    def calculateModSize(Modname):
        '''Calculate a Given Mod's Total Size'''
        # Cocatenates Locator-Prefix with the Mod Input
        print(f"Processing: {color.PURPLE}{color.BOLD}{Modname}{color.END}")
        mod_location = MODS_Directory + Modname

        ModsCheck = []
        # Checks if the Mod exists as a Directory
        for dirs in os.walk(MODS_Directory):
            if Modname != ".a3s":
                ModsCheck.append(Modname)
                
            break
        
        # Calculates Total Size Of Single Directory (All Contents Included)
        if Modname in ModsCheck:
            root_directory = Path(mod_location)
            size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    
        else:
            print("\n*** Error: Mod Was Not Found As a Directory ***\n")
            restart()

        singlemodsize = size

        UpdateJSON(mod_location,singlemodsize,Modname)

        return singlemodsize
    




    def alltocalculate():
        '''Collects/Sends every Mod To Be Calculated'''

        filtered_mod_condition = True

        global indexcounter
        global TotalDirectories

        if filtered_mod_condition:
            filtered_mod = ".a3s"
            indexaffector = -1
        else:
            indexaffector = 0
        

        # Calculates total number of directories found in mod folder location (The -1 is to exclude .a3s)
        TotalDirectories = len(next(os.walk(MODS_Directory))[0]) + indexaffector
        
        
        indexcounter = 0

        # Sends each mod found in mod folder to "calculateModSize" function
        for root, dirs, files in os.walk(MODS_Directory):
            for Modname in dirs:
                if Modname != filtered_mod:
                    if indexcounter < TotalDirectories:
                        indexcounter += 1
                    size = calculateModSize(Modname)
                    print(f"{indexcounter} / {TotalDirectories} \n")
                if indexcounter == TotalDirectories:
                    restart()
            break
        




    def UpdateJSON(mod_location, singlemodsize,Modname):
        '''Updates The JSON File With New Updated Directory Size'''
        isTrue = False

        allModsCheck = [] 

        # Checks if the Mod exists as a Directory
        for root, dirs, files in os.walk(MODS_Directory):
            for name in dirs:
                allModsCheck.append(name)
            break
        
        if Modname in allModsCheck:
                        Chunk_Hashing.create_hash_dict(mod_location,Modname)


        # Checks if the Mod is in the JSON file
        existsinJSON = JSONFunctions.DoesModExist(Modname, jsonData)


        # If Mod DOES exist in JSON file, updates it
        if existsinJSON:
            newData = JSONFunctions.SetVariableValue(Modname, jsonData, "ModSize",singlemodsize)


        elif Modname in allModsCheck:
        # If the mod DOES exist as a Directory, and the Mod DOESN'T exist in JSON file, adds it to the JSON file
            newData = JSONFunctions.AddMod(Modname, jsonData, singlemodsize)
            print("\n--- Mod Was Added In JSON file, After Not Being Found ---\n")
        else:
            print("\n*** Error: Mod Was Not Found As a Directory ***\n")
            restart()


        # Checks whether the mod name starts with "@{OPTIONAL}" and sets boolean state on JSON file
        if re.search(r'^@{OPTIONAL}', Modname):
            newData = JSONFunctions.SetVariableValue(Modname, jsonData, "Optional", True)
            isTrue = True
        if isTrue == False:
            newData = JSONFunctions.SetVariableValue(Modname, jsonData, "Optional", False)

        newData = JSONFunctions.FormatJSON(newData)


        # Writes to JSON file with updated content
        with open(JSON_Location, mode="w") as file:
            file.write(newData)
        print(f"\n --- {Modname} Was Succesfully Updated In The JSON File --- \n")
        print(f"{color.GREEN}UPDATED: {Modname}{color.END}  : {color.YELLOW}{singlemodsize}{color.END}\n")

        # Once all mods have updated, restarts the system
        if special == False:
            restart()
        




    def deleteJSON(inp):
        '''Deletes a Mod From JSON, After Checking If It Stil Exists'''

        # Removes the "del" and the space from initial input
        Modname = re.sub("del ","",inp)

        while True:
            print("\n --- ARE YOU SURE YOU WANT TO DELETE:", Modname, "(y/n) --- \n")
            Confirm = input().lower()
            if not re.match(r"^[yn]$", Confirm):
                print("\nError! Only letters y/n allowed!")
                continue 
            break
        if Confirm == "y":
            # Checks if the Mod is in the JSON file
            existsinJSON = JSONFunctions.DoesModExist(Modname, jsonData)

            # If the mod DOES exist in the JSON file, deletes it
            if existsinJSON:
                newData = JSONFunctions.DelMod(Modname, jsonData)

                newData = JSONFunctions.FormatJSON(newData)

                # Writes to JSON file with updated content
                with open(JSON_Location, mode="w") as file:
                    file.write(newData)

                print("\n --- '",Modname,"' Was Succesfully Removed From The JSON File --- \n")
            
            else:
                print("\n*** Error: Mod Was Not Found In JSON File ***\n")
                restart()

            deleteDIRECTORY(Modname)
        else:
            print("\n*** System Restarting, After Declining The DELETE Process *** ")
            restart()





    def deleteDIRECTORY(Modname):
        '''Deletes a Mod From DIRECTORIES, After Checking It Still Exists'''
        # Empty array to store mods found as a directory
        allmods = []

        # Checks if the Mod exists as a Directory
        for root, dirs, files in os.walk(MODS_Directory):
            for name in dirs:
                allmods.append(name)
            break

        # If the mod DOES exist as a Directory, deletes it
        if Modname in allmods:
            Modname = MODS_Directory + Modname
            shutil.rmtree(Modname)
            Modname = re.sub("{MODS_Directory}","",Modname)
            print("\n --- '",Modname,"' Was Succesfully Removed As A Dictionary --- \n")
            restart()

        # If the mod DOESN'T exist as a Directory, returns an Error
        else:
            print("\n*** Mod Was Not Found As a Directory ***\n")
            restart()





    def restart():
        print('''
''')
        system()




    start()
system()

