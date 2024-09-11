



from pathlib import Path
import os
import JSONFunctions
import re
import shutil

JSON_Location = "D:\\Github\\StowMarines-Interface-ServerSide\\Mods123.json"
MODS_Directory = "D:\\mods\\"

jsonData = JSONFunctions.LoadJSONFromFile(JSON_Location)


def system():
    def start():
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
            alltocalculate()
        elif re.search("^del", inp):
            deleteJSON(inp)
        else:
            calculateModSize(inp)
        




    def calculateModSize(Modname):
        '''Calculate a Given Mod's Total Size'''
        # Cocatenates Locator-Prefix with the Mod Input
        mod = MODS_Directory + Modname

        ModsCheck = []

        # Checks if the Mod exists as a Directory
        for root, dirs, files in os.walk(MODS_Directory):
            for name in dirs:
                ModsCheck.append(name)
            break

        # Calculates Total Size Of Single Directory (All Contents Included)
        if Modname in ModsCheck:
            root_directory = Path(mod)
            size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
        else:
            print("\n*** Error: Mod Was Not Found As a Directory ***\n")
            restart()
        singlemodsize = size

        UpdateJSON(singlemodsize,Modname)

        return singlemodsize
    




    def alltocalculate():
        filtered_mod = ".a3s"
        '''Collects/Sends every Mod To Be Calculated'''

        # Calculates total number of directories found in mod folder location
        TotalDirectories = len(next(os.walk(MODS_Directory))[1]) - 1
        indexcounter = 0

        # Sends each mod found in mod folder to "calculateModSize" function
        for root, dirs, files in os.walk(MODS_Directory):
            for Modname in dirs:
                if Modname != ".a3s":
                    indexcounter += 1
                    size = calculateModSize(Modname)
                    print("UPDATED:", Modname, ":", size)
                    print(indexcounter, "/", TotalDirectories)
            break
        




    def UpdateJSON(singlemodsize,Modname):
        '''Updates The JSON File With New Updated Directory Size'''
        isTrue = False

        allModsCheck = []

        # Checks if the Mod exists as a Directory
        for root, dirs, files in os.walk(MODS_Directory):
            for name in dirs:
                allModsCheck.append(name)
            break

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
        print("\n --- '",Modname,"' Was Succesfully Updated In The JSON File --- \n")





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

