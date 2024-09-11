"""
Script Title: JSON Functions
Author: Beau Saunders
Date: 09-09-2024
Description: A collection of tools for the StowMarines Interface Server Side Module to utilise JSON
Usage: Place the script in the same directory as your working script, import it with: import JSONFunctions
"""

import json

errMsg_Prefix = "JSONFunctions Error: "

def FormatJSON(input):
    '''Formats a JSON string into pretty print (e.g. indentation etc)'''
    return json.dumps(input, indent=2)


def LoadJSONFromFile(path):
    '''Opens a file and reads it's contents to a string and returns the JSON string'''
    with open(path, 'r') as file:
        file_content = file.read()

    if file_content == None:
        __LogError__("LoadJSONFromFile", "Failed to load contents of file at " + path)
        return None
    else:
        # parse the data into json and return
        return json.loads(file_content)


def GetModSize(modName, jsonData):
    '''Fetches the mod data from the name and returns the mod size from the data'''
    modData = GetModData(modName, jsonData)

    if modData == None:
        __LogError__("GetModSize", "Failed to get mod data for: " + modName)
        return None
    else:
        return modData["ModSize"]


def GetModData(modName, jsonData):
    '''Fetches the mod data from the list of mod info's given the mod'''
    modName = (modName).lower()

    # iterate through the list of mods
    for mod in jsonData["ModInfo"]:
        # check if the current mod's name matches the input mod name
        if (mod["ModName"]).lower() == modName:
            # return the mod data
            return mod
        
    # return None if the mod name is not found
    __LogError__("GetModData", "No mod data was found for: " + modName)
    return None


def SetVariableValue(modName, jsonData, variableName, value):
    '''Updates the value for the given mod name and given variable and returns the complete updated json string. 
    Variable is created if it doesn't already exist'''
    modData = GetModData(modName, jsonData)

    modData[variableName] = value
    return jsonData


def DoesModExist(modName, jsonData):
    '''Attempts to find the mod in the data, returns whether it was found or not (boolean)'''
    modData = GetModData(modName, jsonData)

    if modData == None:
        return False
    else:
        return True
    

def AddMod(modName, jsonData, modSize):
    '''Creates a new data block for the mod, given it's size. Returns the new JsonData.'''

    # dreate new data block for new mod
    newModData = {"ModName":modName, "ModSize":modSize}

    # append it to the existing JSON array
    jsonData["ModInfo"].append(newModData)

    if modName.startswith("@{OPTIONAL}"):
        jsonData = SetOptional(modName, jsonData, True)

    return jsonData


def DelMod(modName, jsonData):
    '''Deletes the mod data in the JSON string given it's name. . Returns the new JsonData.'''
    modData = GetModData(modName, jsonData)

    jsonData["ModInfo"].remove(modData)

    newJsonData = jsonData

    return newJsonData


def SetOptional(modName, jsonData, optional):
    '''Delcares a mod as optional, or not optional'''

    modData = GetModData(modName, jsonData)
    modData["Optional"] = optional
    return jsonData


# region Internal Tools
def __LogError__(function, msg):
    print(errMsg_Prefix, '[',function, '] ', msg)

# endregion