# StowMarinesInterface_ServerSide

## Description
The server-side functionality for the StowMarines Interface.</br></br>
The system is responsible for calculating mod sizes, names and optional states in a json file that is used by the client to determine updates.

## Setup/Config
- [ ] Place folder in SMI Server Directory.

- [ ] Adjust smi_ss_cfg.txt:</br>
`PATH\TO\SERVER\MOD\MANIFEST\FILE.json`</br>
`PATH\TO\SMI\MODS\FOLDER\\`</br>
`PATH\TO\SMI\HASH\FOLDER`</br>
</br>

> [!IMPORTANT]
> Ensure the mods folder path ends with `\\`

## Commands
> [!NOTE]
> "ModName" refers to the actual name of the mod folder you are editing
</br>

* `"ModName"` - Updates or adds the given mod name
* `all` - Updates or adds all folders found in the server's mod directory
* `del "ModName"` - Deletes the given mod name's folder and removes it's from the json file

## Authors
Lead Developer - [@BeauSaunders](https://github.com/BeauSaunders)</br>
Developer - [@FennsFJS](https://github.com/FennsFJS)</br>

## License
All Rights Reserved. This software is for private use in the StowMarines Community on their server. Use is only granted for those with direct permission from the author (Beau Saunders).
