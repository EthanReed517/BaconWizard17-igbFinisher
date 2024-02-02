# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# To be able to set the title
import ctypes
# To be able to copy and move files
import os
# To be able to parse the ini file
import configparser
# To be able to copy files
import shutil
# To simplify operations
import resources


# ######### #
# FUNCTIONS #
# ######### #
# Define the function for getting the settings.
def parseConfig():
    # Check if the config file exists
    verifyConfigExistence()
    # Start a list to store the settings
    settings = []
    # Get the character numbers
    for game in ["XML1", "XML2", "MUA1", "MUA2"]:
        number = characterNumberGetter(game)
        settings.append(number)
    # Get the other settings
    for settingName in ["hexEditChoice","runAlchemyChoice","multiPose"]:
        setting = settingsGetter(settingName)
        settings.append(setting)
    # Return the collected data
    return settings

# Define the function to check if the config file exists
def verifyConfigExistence():
    # Eternal loop until broken
    while True:
        try:
            # Check if the file exists
            assert os.path.exists("settings.ini")
            # Break out of the loop if there are no errors
            break
        except AssertionError:
            # The assertion failed (the file does not exist)
            # Print the error message
            resources.printError("ERROR: settings.ini does not exist. Restore the file and try again.")
            # Wait for user confirmation
            resources.pressAnyKey("Press any key to try again...")
    # Print the success message
    #print("settings.ini found.")

# Define the function to check if XVI32 was installed
def verifyXVI32Existence():
    # Eternal loop until broken
    while True:
        try:
            # Check if the file exists
            assert os.path.exists("XVI32")
            # Break out of the loop if there are no errors
            break
        except AssertionError:
            # The assertion failed (the file does not exist)
            # Print the error message
            resources.printError("ERROR: folder \"XVI32\" does not exist. Install XVI32 and try again.")
            # Wait for user confirmation
            resources.pressAnyKey("Press any key to try again...")
    # Eternal loop until broken
    while True:
        try:
            # Check if the file exists
            assert os.path.exists("XVI32\\XVI32.exe")
            # Break out of the loop if there are no errors
            break
        except AssertionError:
            # The assertion failed (the file does not exist)
            # Print the error message
            resources.printError("ERROR: XVI32.exe does not exist in the \"XVI32\". Install XVI32 and try again.")
            # Wait for user confirmation
            resources.pressAnyKey("Press any key to try again...")
    # Print the success message
    #print("XVI32 installation found.")

# Define the function to get the character numbers
def characterNumberGetter(game):
    # Get the name of the setting to look for
    setting = game + "Num"
    # Prepare to parse the settings
    config = configparser.ConfigParser()
    # Read the settings
    config.read('settings.ini')
    # Get the number
    number = config['Settings'][setting]
    # Check if the number is acceptable
    # Eternal loop until broken
    while True:
        try:
            # Check the acceptance criteria
            assert 0 <= int(number) <= 255
            # break out of the loop if there are no errors
            break
        except ValueError:
            # The value is not a number
            # Check if the value is blank
            if number == "":
                # The value is blank, which is allowed.
                # Break out of the while statement
                break
            else:
                # The value is not blank
                # Get a new use input
                resources.printError("ERROR: Character number for " + str(game) + " is set to " + str(number) + ", which is not a number. Please enter a number.")
                number = input("Enter a new value: ")
        except AssertionError:
            # The number is not within the accepted range (assertion failed)
            resources.printError("ERROR: Character number for " + str(game) + " is set to " + str(number) + ", which is not within the acceptable range (0-255). Please enter a number.")
            number = input("Enter a new value: ")
    # Update the number in the settings
    config['Settings'][setting] = number
    # Write the new value to the settings
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
    # Return the collected value
    return number

# Define the function to get the other settings
def settingsGetter(settingName):
    # Prepare to parse the settings
    config = configparser.ConfigParser()
    # Read the settings
    config.read('settings.ini')
    # Get the general settings
    setting = config['Settings'][settingName]
    # Check if the value is acceptable
    # Eternal loop until broken
    while True:
        try:
            # Check the acceptance criteria
            assert (setting == "True") or (setting == "False")
            # break out of the loop if there are no errors
            break
        except (ValueError, AssertionError):
            # The value is not acceptable
            resources.printError("ERROR: The value for setting " + str(settingName) + " is set to " + str(setting) + ", which is not an acceptable value. It must be True or False. Please enter an acceptable value.")
            setting = input("Enter a new value: ")
    # Update the setting in the settings
    config['Settings'][settingName] = setting
    # Write the new value to the settings
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)
    # Return the collected value
    return setting

# Define the function for getting the asset type from the file name
def getAssetTypeFromName():
    # Create the list of possible file names
    fileNameList = ["igActor01_Animation01DB.igb", "123XX (Mannequin).igb", "123XX (3D Head).igb", "hud_head_123XX.igb", "123XX (Character Select Portrait).igb"]
    # Create the list of asset types
    assetTypeList = ["Skin", "Mannequin", "3D Head", "Conversation Portrait", "Character Select Portrait"]
    # Start a counter to keep track of valid files
    validCounter = 0
    # Initialize the return variable
    assetType = "Unknown"
    # Compare the file name and asset type lists
    for fileName, assetTypes in zip(fileNameList, assetTypeList):
        # Check if a file of that name exists
        if os.path.exists(fileName):
            # A file of that name exists
            # Update the variable
            assetType = assetTypes
            # Update the counter
            validCounter += 1
    # Check if more than 1 asset is present
    if validCounter > 1:
        # More than 1 asset is present
        # Warn the user
        resources.printWarning("WARNING: More than 1 igb file with a known file name was found. Only 1 igb file can be processed at a time. The file being processed is a " + assetType + ".\n")
    # Check if only 1 asset is present
    elif validCounter == 1:
        # Only 1 asset
        # State the asset type
        resources.printSuccess("The asset type was automatically identified as a " + assetType + ".\n")
    # return the asset type
    return assetType

# Define the validator for the file name of unknown assets
def fileNameValidatorStart(fileName):
    if len(fileName) == 0:
        return "Please enter a file name."
    elif ".igb" in fileName:
        return "Do not include the file extension."
    elif not(os.path.exists(fileName + ".igb")):
        return "The file does not exist."
    else:
        return True

# Define the function to get asset choice options
def getAssetChoices(XML1Num, XML2Num, MUA1Num, MUA2Num):
    assetChoices = ["Skin"]
    if (not(MUA1Num == "")) or (not(MUA2Num == "")):
        assetChoices.append("Mannequin")
    if (not(XML1Num == "")) or (not(XML2Num == "")):
        assetChoices.append("3D Head")
    assetChoices.append("Conversation Portrait")
    if (not(XML1Num == "")) or (not(XML2Num == "")):
        assetChoices.append("Character Select Portrait")
    assetChoices.append("Other")
    return assetChoices

# Define the function to get the file path
def getFilePath(Game1Num, Game2Num, Game1Name, Game2Name):
    # Determine which games are in use
    if (Game1Num == "") and (Game2Num == ""):
        # Neither game is in use
        filePath = None
    else:
        # At least one game is in use
        if not(Game1Num == ""):
            # Game 1 is in use
            if not(Game2Num == ""):
                # Game 1 and Game 2 are in use
                games = Game1Name + "/" + Game2Name
            else:
                # Only Game 1 is in use
                games = Game1Name
        else:
            # Only Game 2 is in use
            games = Game2Name
        # Create the message for the prompt
        message = "Enter the path to the folder for the " + games + " release:"
        # Ask the question
        filePath = resources.path(message, pathValidator)
    # Replace any incorrect slashes
    filePath = filePath.replace("\\", "/")
    # Return the path
    return filePath

# Define the validator for the file path
def pathValidator(path):
    if len(path) == 0:
        return "Please enter a file path."
    elif os.path.exists(path) == False:
        return "Path does not exist"
    else:
        return True

# Define the function to process skins
def skinProcessing(XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath):
    # Determine the texture size
    textureSize = resources.select("What is the original size of the main texture?", ["256x256 or less", "Over 256x256"])
    # Ask additional questions based on texture size
    if textureSize == "256x256 or less":
        # Standard Texture
        # Ask which type of skin is being used
        skinType = resources.select("Is this for a primary skin or secondary skin?", ["Primary skin", "Secondary skin"])
        # Filter based on skin type
        if skinType == "Primary skin":
            # Primary skin
            # Initialize list with main format
            textureFormatList = ["PC, PS2, Xbox, and MUA1 360"]
            # Determine if MUA1/MUA2-specific format is needed
            if (not(MUA1Num == "")) or (not(MUA2Num == "")):
                # MUA1 or MUA2 are in use
                # Add the texture option
                textureFormatList.append("Wii")
            # Add the remaining texture option
            textureFormatList.append("GameCube, PSP, and MUA2 PS2")
        else:
            # Secondary skin
            # Initialize list with main format
            textureFormatList = ["PC, Xbox, and MUA1 360"]
            # Determine if MUA1/MUA2-specific format is needed
            if (not(MUA1Num == "")) or (not(MUA2Num == "")):
                # MUA1 or MUA2 are in use
                # Add the texture option
                textureFormatList.append("Wii")
            # Add the remaining texture options
            textureFormatList.extend(["PS2","GameCube, PSP, and MUA2 PS2"])
    else:
        # Texture size is over 256x256
        # Initialize a list to store the options in
        textureFormatList = []
        # Check if MUA1-Specific format is needed
        if not(MUA1Num == ""):
            # MUA1 is in use
            # Append the texture option
            textureFormatList.append("MUA1 PC, Steam, 360, and PS3")
        # Add remaining texture options
        textureFormatList.extend(["XML2 PC, Xbox, and Wii","PS2","GameCube, PSP, and MUA2 PS2"])
    # Ask which texture format was used
    textureFormat = resources.select("What texture format was used for this asset?", textureFormatList)
    # Determine if cel shading needs to be asked about
    if (textureFormat == "Wii" or textureFormat == "MUA1 PC, Steam, 360, and PS3"):
        # Texture format that would not use cel shading
        celChoice = False
    else:
        # Texture format that could be with a cel shaded skin
        # Determine if the skin has cel shading or not
        celChoice = resources.confirm("Does the skin use cel shading?", False)
    # Filter based on cel shading choice
    if celChoice == True:
        # cel shading is used
        # Set up file names
        XML1Name = XML1Num + "XX (Skin).igb"
        XML2Name = XML2Num + "XX (Skin).igb"
        MUA1Name = None
        MUA2Name = None
    else:
        # cel shading is not used
        # set up file names
        XML1Name = XML1Num + "XX (Skin - No Cel).igb"
        XML2Name = XML2Num + "XX (Skin - No Cel).igb"
        MUA1Name = MUA1Num + "XX (Skin).igb"
        MUA2Name = MUA2Num + "XX (Skin).igb"
    # #################################################################### #
    # ADDITION NEEDED - Need to verify that the file exists before copying #
    # #################################################################### #
    # ################################################ #
    # ADDITION NEEDED - If numbers match, need to skip #
    # ################################################ #
    # Copy the files
    for num, name in zip([XML1Num, XML2Num, MUA1Num, MUA2Num], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
        # Determine if the number is used
        if (not(num == "") and not(name == None)):
            # Number isn't empty, need to copy
            # Perform the copying
            shutil.copy("igActor01_Animation01DB.igb", name)
    # Copy the hex editing batch file
    shutil.copy("Scripts/hexSkin.bat", "./")
    # Perform the hex editing
    for num, name in zip([XML1Num, XML2Num, MUA1Num, MUA2Num], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
        # Determine if the file should be considered
        if not(name == None):
        # Name is not none
        # Determine if the file exists
            if os.path.exists(name):
            # the file exists
            # Determine the length of the character number
                if len(num) == 2:
                    # 2-digit character number
                    # Establish hex editing values
                    hexNum = "3" + num[0] + " 3" + num[1] + " 30 31"
                    hexAppearance = hexNum + " 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
                    hexOutline = hexNum + " 5F 6F 75 74 6C 69 6E 65 00"
                    hexOther = hexNum + " 5F 5F"
                else:
                    # 3-digit character number
                    # Establish hex editing values
                    hexNum = "3" + num[0] + " 3" + num[1] + " 3" + num[2] + " 30 31"
                    hexAppearance = hexNum + " 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
                    hexOutline = hexNum + " 5F 6F 75 74 6C 69 6E 65"
                    hexOther = hexNum + " 5F"
            # Hex edit
            os.system('hexSkin.bat "' + name + '" "69 67 41 63 74 6F 72 30 31 41 70 70 65 61 72 61 6E 63 65" "' + hexAppearance + '" "31 32 33 30 31 5F 6F 75 74 6C 69 6E 65" "' + hexOutline + '" "31 32 33 30 31 5F" "' + hexOther + '" "31 32 33 30 31" "' + hexNum + '"')
    # Delete the hex editing file
    if os.path.isfile("hexSkin.bat"):
        os.remove("hexSkin.bat")
    # Filter remaining operations based on texture type
    if (textureFormat == "PC, PS2, Xbox, and MUA1 360") or (textureFormat == "PC, Xbox, and MUA1 360"):
        # 256x256 or less, main texture, primary or secondary skin
        # Check if primary or secondary skin
        if textureFormat == "PC, PS2, Xbox, and MUA1 360": 
            # Primary skin
            # Copy any files that don't need optimization.
            copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
            copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2 and Xbox)")
        else:
            # Secondary skin
            # Copy any files that don't need optimization.
            copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
            copyToDestination(XML2Name, XMLPath, "for XML2 (PC and Xbox)")
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Xbox)")
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/skin1-1.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" skin1-1.ini')
        # Copy the first optimized alchemy file
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/skin1-2.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" skin1-2.ini')
        # Copy the second optimized alchemy file
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "skin1-1.ini", "skin1-2.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    elif textureFormat == "Wii":
        # Wii
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    elif textureFormat == "PS2":
        # PS2 only (secondary skin with texture size 256x256 or less, or any skin with texture size over 256x256)
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (PS2)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PS2)")
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2)")
    elif textureFormat == "GameCube, PSP, and MUA2 PS2":
        # GameCube, PSP, and MUA2 PS2
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/skin3.ini", "./")
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Call the Alchemy batch file
            os.system('Alchemy.bat "' + MUA1Name + '" skin3.ini')
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PS2 and PSP)")
        else:
            # MUA1 and MUA2 are not the same
            # Call the Alchemy batch file
            os.system('Alchemy.bat "' + MUA1Name + '" skin3.ini')
            os.system('Alchemy.bat "' + MUA2Name + '" skin3.ini')
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (PS2 and PSP)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "skin3.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    elif textureFormat == "MUA1 PC, Steam, 360, and PS3":
        # MUA1 PC, Steam, 360, and PS3 (over 256x256)
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/skin1-1.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" skin1-1.ini')
        # Copy the files
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC, Steam, 360, and PS3)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "skin1-1.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    else:
        # XML2 PC, Xbox, and Wii
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PC and Xbox)")
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    # Delete the lingering files
    deleteLingering(["igActor01_Appearance.igb", XML1Name, XML2Name, MUA1Name, MUA2Name])

# Define the function to process mannequins
def mannequinProcessing(MUA1Num, MUA2Num, MUAPath, multiPose):
    # Determine the texture size
    textureSize = resources.select("What is the original size of the main texture?", ["256x256 or less", "Over 256x256"])
    # Ask additional questions based on texture size
    if textureSize == "256x256 or less":
        # Standard Texture
        # Initialize list with main format
        textureFormatList = ["PC, PS2, Xbox, and MUA1 360", "Wii", "GameCube, PSP, and MUA2 PS2"]
    else:
        # Texture size is over 256x256
        # Initialize a list to store the options in
        textureFormatList = ["MUA1 PC, Steam, 360, and PS3","XML2 PC, Xbox, and Wii","PS2","GameCube, PSP, and MUA2 PS2"]
    # Ask which texture format was used
    textureFormat = resources.select("What texture format was used for this asset?", textureFormatList)
    # Filter names based on whether or not the character uses multiple mannequin poses
    if multiPose == "True":
        # Character uses multiple poses
        # determine the pose name
        mannequinPose = resources.select("Which mannequin pose is being used?", ["MUA1 Pose", "MUA1 Last-Gen Pose", "MUA1 Next-Gen Pose", "MUA2 Pose", "OCP Pose", "Custom Pose"])
        # Set up file names
        MUA1Name = MUA1Num + "XX (Mannequin - " + mannequinPose + ").igb"
        MUA2Name = MUA2Num + "XX (Mannequin - " + mannequinPose + ").igb"
    else:
        # Character uses one pose
        # set up file names
        MUA1Name = MUA1Num + "XX (Mannequin).igb"
        MUA2Name = MUA2Num + "XX (Mannequin).igb"
    # #################################################################### #
    # ADDITION NEEDED - Need to verify that the file exists before copying #
    # #################################################################### #
    # ################################################ #
    # ADDITION NEEDED - If numbers match, need to skip #
    # ################################################ #
    # Copy the files
    for num, name in zip([MUA1Num, MUA2Num], [MUA1Name, MUA2Name]):
        # Determine if the number is used
        if not(num == ""):
            # Number isn't empty, need to copy
            # Perform the copying
            shutil.copy("123XX (Mannequin).igb", name)
    # Copy the hex editing batch file
    shutil.copy("Scripts/hexManOrHead.bat", "./")
    # Perform the hex editing
    for num, name in zip([MUA1Num, MUA2Num], [MUA1Name, MUA2Name]):
        # Determine if the file exists
        if os.path.exists(name):
        # the file exists
        # Determine the length of the character number
            if len(num) == 2:
                # 2-digit character number
                # Establish hex editing values
                hexNum = "3" + num[0] + " 3" + num[1] + " 30 31"
                hexOther = hexNum + " 5F 5F"
            else:
                # 3-digit character number
                # Establish hex editing values
                hexNum = "3" + num[0] + " 3" + num[1] + " 3" + num[2] + " 30 31"
                hexOther = hexNum + " 5F"
        # Hex edit
        os.system('hexManOrHead.bat "' + name + '" "31 32 33 30 31 5F" "' + hexOther + '" "31 32 33 30 31" "' + hexNum + '"')
    # Delete the hex editing file
    if os.path.isfile("hexManOrHead.bat"):
        os.remove("hexManOrHead.bat")
    # Filter remaining operations based on texture type
    if textureFormat == "PC, PS2, Xbox, and MUA1 360":
        # 256x256 or less, main texture
        # Copy any files that don't need optimization.
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2 and Xbox)")
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/mann1-1.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" mann1-1.ini')
        # Copy the first optimized alchemy file
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/mann1-2.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" mann1-2.ini')
        # Copy the second optimized alchemy file
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "mann1-1.ini", "mann1-2.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    elif textureFormat == "Wii":
        # Wii
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    elif textureFormat == "PS2":
        # PS2 only (any skin with texture size over 256x256)
        # Copy the files
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2)")
    elif textureFormat == "GameCube, PSP, and MUA2 PS2":
        # GameCube, PSP, and MUA2 PS2
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/mann3.ini", "./")
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Call the Alchemy batch file
            os.system('Alchemy.bat "' + MUA1Name + '" mann3.ini')
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PS2 and PSP)")
        else:
            # MUA1 and MUA2 are not the same
            # Call the Alchemy batch file
            os.system('Alchemy.bat "' + MUA1Name + '" mann3.ini')
            os.system('Alchemy.bat "' + MUA2Name + '" mann3.ini')
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (PS2 and PSP)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "mann3.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    elif textureFormat == "MUA1 PC, Steam, 360, and PS3":
        # MUA1 PC, Steam, 360, and PS3 (over 256x256)
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/mann1-1.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" mann1-1.ini')
        # Copy the files
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC, Steam, 360, and PS3)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "mann1-1.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    else:
        # XML2 PC, Xbox, and Wii
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    # Delete the lingering files
    deleteLingering(["123XX (Mannequin).igb", MUA1Name, MUA2Name])

# Define the function to process 3D Heads
def headProcessing(XML1Num, XML2Num, XMLPath):
    # Determine the texture size
    textureSize = resources.select("What is the original size of the main texture?", ["256x256 or less", "Over 256x256"])
    # Ask additional questions based on texture size
    if textureSize == "256x256 or less":
        # Standard Texture
        # Initialize list with main format
        textureFormatList = ["PC, PS2, Xbox, and MUA1 360", "GameCube, PSP, and MUA2 PS2"]
    else:
        # Texture size is over 256x256
        # Initialize a list to store the options in
        textureFormatList = ["XML2 PC, Xbox, and Wii","PS2","GameCube, PSP, and MUA2 PS2"]
    # Ask which texture format was used
    textureFormat = resources.select("What texture format was used for this asset?", textureFormatList)
    # Set up file names
    XML1Name = XML1Num + "XX (3D Head).igb"
    XML2Name = XML2Num + "XX (3D Head).igb"
    # #################################################################### #
    # ADDITION NEEDED - Need to verify that the file exists before copying #
    # #################################################################### #
    # ################################################ #
    # ADDITION NEEDED - If numbers match, need to skip #
    # ################################################ #
    # Copy the files
    for num, name in zip([XML1Num, XML2Num], [XML1Name, XML2Name]):
        # Determine if the number is used
        if not(num == ""):
            # Number isn't empty, need to copy
            # Perform the copying
            shutil.copy("123XX (3D Head).igb", name)
    # Copy the hex editing batch file
    shutil.copy("Scripts/hexManOrHead.bat", "./")
    # Perform the hex editing
    for num, name in zip([XML1Num, XML2Num], [XML1Name, XML2Name]):
        # Determine if the file exists
        if os.path.exists(name):
        # the file exists
        # Determine the length of the character number
            if len(num) == 2:
                # 2-digit character number
                # Establish hex editing values
                hexNum = "3" + num[0] + " 3" + num[1] + " 30 31"
                hexOther = hexNum + " 5F 5F"
            else:
                # 3-digit character number
                # Establish hex editing values
                hexNum = "3" + num[0] + " 3" + num[1] + " 3" + num[2] + " 30 31"
                hexOther = hexNum + " 5F"
        # Hex edit
        os.system('hexManOrHead.bat "' + name + '" "31 32 33 30 31 5F" "' + hexOther + '" "31 32 33 30 31" "' + hexNum + '"')
    # Delete the hex editing file
    if os.path.isfile("hexManOrHead.bat"):
        os.remove("hexManOrHead.bat")
    # Filter remaining operations based on texture type
    if textureFormat == "PC, PS2, Xbox, and MUA1 360":
        # 256x256 or less, main texture
        copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
    elif textureFormat == "PS2":
        # PS2 only (secondary skin with texture size 256x256 or less, or any skin with texture size over 256x256)
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (PS2)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PS2)")
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2)")
    elif textureFormat == "GameCube, PSP, and MUA2 PS2":
        # GameCube, PSP, and MUA2 PS2
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
    else:
        # XML2 PC, Xbox, and Wii
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PC and Xbox)")
    # Delete the lingering files
    deleteLingering(["123XX (3D Head).igb", XML1Name, XML2Name])

# Define the function to process conversation portraits
def convoProcessing(XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath):
    # Determine the portrait type
    portraitType = resources.select("What is the portrait type?", ["Standard", "Next-Gen Style"])
    # Determine if it's necessary to ask about texture size
    if portraitType == "Standard":
        # Standard portrait, need to determine texture size
        # Determine the texture size
        textureSize = resources.select("What is the original size of the main texture?", ["128x128 or less", "Over 128x128"])
    else:
        # Next-gen style portrait, size doesn't matter
        textureSize = "128x128 or less"
    # Create the list of texture formats based on the texture size
    if textureSize == "128x128 or less":
        # Standard size
        # Main texture is always used
        textureFormatList = ["Main"]
        # Determine if MUA1/MUA2-specific formats are needed
        if (not(MUA1Num == "")) or (not(MUA2Num == "")):
            # MUA1 or MUA2 are in use
            # Determine the portrait type
            if portraitType == "Standard":
                # Standard portrait
                # MUA1 and MUA2 both use the PSP and Wii textures
                textureFormatList.extend(["PSP","Wii"])
            else:
                # Next-gen style portrait
                # MUA1 and MUA2 both use the PSP texture
                textureFormatList.append("PSP")
    else:
        # Oversized
        # start with the common format
        textureFormatList = ["GC, PS2, Xbox"]
        # Determine if the XML2-specific format is needed
        if not(XML2Num == ""):
            # XML2 is in use
            # Add the XML2-specific format
            textureFormatList.append("XML2 PC")
        # Determine if the MUA-specific formats are needed
        if (not(MUA1Num == "")) or (not(MUA2Num == "")):
            # MUA1 or MUA2 are in use
            if not(MUA1Num == ""):
                # MUA1 is in use
                # MUA1-specific format is needed
                textureFormatList.append("MUA1 PC")
            # MUA-specific formats are needed
            textureFormatList.extend(["Wii","PSP"])
    # Ask which texture format was used
    textureFormat = resources.select("What texture format was used for this asset?", textureFormatList)
    # Filter based on texture type
    if portraitType == "Next-Gen":
        # Next-Gen texture
        # Set up file names
        XML1Name = "hud_head_" + XML1Num + "XX (Next-Gen Style).igb"
        XML2Name = "hud_head_" + XML2Num + "XX (Next-Gen Style).igb"
        MUA1Name = "hud_head_" + MUA1Num + "XX (Next-Gen Style).igb"
        MUA2Name = "hud_head_" + MUA2Num + "XX (Next-Gen Style).igb"  
    else:
        # other texture formats
        # Determine the portrait type
        portraitType = resources.select("What type of portrait is being used?", ["Hero Outline/General", "Villain Outline"])
        # Filter based on outline type
        if portraitType == "Hero Outline/General":
            # Hero outline/general
            # Create the descriptor for the file name
            portraitNameAppend = ""
        else:
            # Villain outline
            # Create the descriptor for the file name
            portraitNameAppend = " (Villain)"
        # Set up file names
        XML1Name = "hud_head_" + XML1Num + "XX" + portraitNameAppend + ".igb"
        XML2Name = "hud_head_" + XML2Num + "XX" + portraitNameAppend + ".igb"
        MUA1Name = "hud_head_" + MUA1Num + "XX" + portraitNameAppend + ".igb"
        MUA2Name = "hud_head_" + MUA2Num + "XX" + portraitNameAppend + ".igb"
    # #################################################################### #
    # ADDITION NEEDED - Need to verify that the file exists before copying #
    # #################################################################### #
    # ################################################ #
    # ADDITION NEEDED - If numbers match, need to skip #
    # ################################################ #
    # Copy the files
    for num, name in zip([XML1Num, XML2Num, MUA1Num, MUA2Num], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
        # Determine if the number is used
        if (not(num == "") and not(name == None)):
            # Number and name aren't empty, need to copy
            # Perform the copying
            shutil.copy("hud_head_123XX.igb", name)
    # Copy the hex editing batch file
    shutil.copy("Scripts/hexConvo.bat", "./")
    # Perform the hex editing
    for num, name in zip([XML1Num, XML2Num, MUA1Num, MUA2Num], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
        # Determine if the file exists
        if os.path.exists(name):
        # the file exists
        # Determine the length of the character number
            if len(num) == 2:
                # 2-digit character number
                # Establish hex editing values
                hexNum = "3" + num[0] + " 3" + num[1] + " 30 31 5F 63 6F 6E 76 65 72 73 61 74 69 6F 6E 2E 70 6E 67 00"
            else:
                # 3-digit character number
                # Establish hex editing values
                hexNum = "3" + num[0] + " 3" + num[1] + " 3" + num[2] + " 30 31 5F 63 6F 6E 76 65 72 73 61 74 69 6F 6E 2E 70 6E 67"
        # Hex edit
        os.system('hexConvo.bat "' + name + '" "31 32 33 30 31 5F 63 6F 6E 76 65 72 73 61 74 69 6F 6E 2E 70 6E 67" "' + hexNum + '"')
    # Delete the hex editing file
    if os.path.isfile("hexConvo.bat"):
        os.remove("hexConvo.bat")
    # Filter remaining operations based on texture type
    if textureFormat == "Main":
        # Main texture type
        # Copy any files that don't need optimization.
        copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2 and Xbox)")
        # Determine if next-gen Wii portraits are needed
        if portraitType == "Next-Gen Style":
            # Next-gen style
            # Detremine if the numbers are the same
            if MUA1Num == MUA2Num:
                # MUA1 and MUA2 are the same
                # Copy the files
                copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
            else:
                # MUA1 and MUA2 are not the same
                # Copy the files
                copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
                copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
        # Run first Alchemy operation
        # ################################################################ #
        # ADDITION NEEDED - Need to add the alchemy optimization step here #
        # ################################################################ #
        # Copy the first optimized alchemy file
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
        # Run the second Alchemy operation
        # ################################################################ #
        # ADDITION NEEDED - Need to add the alchemy optimization step here #
        # ################################################################ #
        # Copy the second optimized alchemy file
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
    elif textureFormat == "Wii":
        # Wii
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    else:
        # PSP
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PS2 and PSP)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (PS2 and PSP)")
    # Delete the lingering files
    deleteLingering(["hud_head_123XX.igb", XML1Name, XML2Name, MUA1Name, MUA2Name])

# Define the function for processing character select portraits
def CSPProcessing(XML1Num, XML2Num, XMLPath):
    # Determine the portrait type
    portraitType = resources.select("What type of portrait is being used?", ["XML1-style","XML2-style"])
    # Filter based on portrait type
    if portraitType == "XML1-style":
        # XML1-style
        # Set up file names
        XML1Name = XML1Num + "XX (Character Select Portrait).igb"
        XML2Name = None
    else:
        # XML2-style
        # Set up file names
        XML1Name = None
        XML2Name = XML2Num + "XX (Character Select Portrait).igb"
    # #################################################################### #
    # ADDITION NEEDED - Need to verify that the file exists before copying #
    # #################################################################### #
    # ################################################ #
    # ADDITION NEEDED - If numbers match, need to skip #
    # ################################################ #
    # Copy the files
    for num, name in zip([XML1Num, XML2Num], [XML1Name, XML2Name]):
        # Determine if the number is used
        if (not(num == "") and not(name == None)):
            # Number and name aren't empty, need to copy
            # Perform the copying
            shutil.copy("123XX (Character Select Portrait).igb", name)
    # Filter the remaining operations based on portrait type
    if portraitType == "XML1-style":
        # XML1-style
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
    else:
        # XML2-style
        # Copy the files
        copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
    # Delete the lingering files
    deleteLingering(["123XX (Character Select Portrait).igb", XML1Name, XML2Name])

# Define the function for processing other assets
def otherProcessing(XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath):
    # Determine the texture size
    textureSize = resources.select("What is the original size of the main texture?", ["256x256 or less", "Over 256x256"])
    # Ask additional questions based on texture size
    if textureSize == "256x256 or less":
        # Standard Texture
        # Initialize list with main format
        textureFormatList = ["PC, PS2, Xbox, and MUA1 360", "Wii", "GameCube, PSP, and MUA2 PS2"]
    else:
        # Texture size is over 256x256
        # Initialize a list to store the options in
        textureFormatList = ["MUA1 PC, Steam, 360, and PS3","XML2 PC, Xbox, and Wii","PS2","GameCube, PSP, and MUA2 PS2"]
    # Ask which texture format was used
    textureFormat = resources.select("What texture format was used for this asset?", textureFormatList)
    # Individually determine the file names through user input
    genericName = otherModelNameInput("NA", "the general exported file")
    XML1Name = otherModelNameInput(XML1Num, "XML1")
    XML2Name = otherModelNameInput(XML2Num, "XML2")
    MUA1Name = otherModelNameInput(MUA1Num, "MUA1")
    MUA2Name = otherModelNameInput(MUA2Num, "MUA2")
    # #################################################################### #
    # ADDITION NEEDED - Need to verify that the file exists before copying #
    # #################################################################### #
    # ################################################ #
    # ADDITION NEEDED - If numbers match, need to skip #
    # ################################################ #
    # Copy the files
    for num, name in zip([XML1Num, XML2Num, MUA1Num, MUA2Num], [XML1Name, XML2Name, MUA1Name, MUA2Name]):
        # Determine if the number is used
        if not(num == ""):
            # Number isn't empty, need to copy
            # Perform the copying
            shutil.copy(genericName, name)
    # Filter remaining operations based on texture type
    if textureFormat == "PC, PS2, Xbox, and MUA1 360":
        # 256x256 or less, main texture, primary or secondary skin
        # Copy any files that don't need optimization.
        copyToDestination(XML1Name, XMLPath, "for XML1 (PS2 and Xbox)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PC, PS2, and Xbox)")
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2 and Xbox)")
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/mann1-1.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" mann1-1.ini')
        # Copy the first optimized alchemy file
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC and 360)")
        # Run the second Alchemy operation
        # Copy the Alchemy ini file
        shutil.copy("Scripts/mann1-2.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" mann1-2.ini')
        # Copy the second optimized alchemy file
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (Steam and PS3)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "mann1-1.ini", "mann1-2.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    elif textureFormat == "Wii":
        # Wii
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    elif textureFormat == "PS2":
        # PS2 only (any skin with texture size over 256x256)
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (PS2)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PS2)")
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PS2)")
    elif textureFormat == "GameCube, PSP, and MUA2 PS2":
        # GameCube, PSP, and MUA2 PS2
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (GC)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (GC)")
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/mann3.ini", "./")
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Call the Alchemy batch file
            os.system('Alchemy.bat "' + MUA1Name + '" mann3.ini')
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP) and MUA2 (PS2 and PSP)")
        else:
            # MUA1 and MUA2 are not the same
            # Call the Alchemy batch file
            os.system('Alchemy.bat "' + MUA1Name + '" mann3.ini')
            os.system('Alchemy.bat "' + MUA2Name + '" mann3.ini')
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (PSP)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (PS2 and PSP)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "mann3.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    elif textureFormat == "MUA1 PC, Steam, 360, and PS3":
        # MUA1 PC, Steam, 360, and PS3 (over 256x256)
        # Copy the Alchemy batch file
        shutil.copy("Scripts/Alchemy.bat", "./")
        # Copy the Alchemy ini file
        shutil.copy("Scripts/mann1-1.ini", "./")
        # Call the Alchemy batch file
        os.system('Alchemy.bat "' + MUA1Name + '" mann1-1.ini')
        # Copy the files
        copyToDestination(MUA1Name, MUAPath, "for MUA1 (PC, Steam, 360, and PS3)")
        # Pick out the Alchemy files to delete
        for file in ["Alchemy.bat", "mann1-1.ini"]:
            # Check if the file exists
            if os.path.isfile(file):
                # the file exists
                # delete it
                os.remove(file)
    else:
        # XML2 PC, Xbox, and Wii
        # Copy the files
        copyToDestination(XML1Name, XMLPath, "for XML1 (Xbox)")
        copyToDestination(XML2Name, XMLPath, "for XML2 (PC and Xbox)")
        # Check if the MUA1 and MUA2 numbers are the same
        if MUA1Num == MUA2Num:
            # MUA1 and MUA2 are the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox) and MUA2 (Wii)")
        else:
            # MUA1 and MUA2 are not the same
            # Copy the files
            copyToDestination(MUA1Name, MUAPath, "for MUA1 (Wii and Xbox)")
            copyToDestination(MUA2Name, MUAPath, "for MUA2 (Wii)")
    # Delete the lingering files
    deleteLingering([genericName, XML1Name, XML2Name, MUA1Name, MUA2Name])

# Define the function for getting other model names
def otherModelNameInput(charNum, gameName):
    # determine what to do based on whether or not the character number is defined.
    if charNum == "":
        # Not used with this game
        # no file name is needed
        fileName = None
    else:
        # used with this game
        # Create the question
        prompt = "What is the name of this file for " + gameName + "? Do not include the file extension."
        # Ask the question
        fileName = resources.path(message, fileNameValidator)
        # add the file extension
        fileName += ".igb"
    # return the collected value
    return fileName

# Define the validator for the file name
def fileNameValidator(fileName):
    if len(fileName) == 0:
        return "Please enter a file name."
    elif ".igb" in fileName:
        return "Do not include the file extension."
    else:
        return True

# Define the function to copy files to the necessary destination
def copyToDestination(fileName, releasePath, folderName):
    # Verify that the file name is not a None
    if not(fileName == None):
        # File name is not none
        # Verify that the file exists before copying
        if os.path.isfile(fileName):
            # The file exists
            # Create the path to the game-specific release folder
            gamePath = os.path.join(releasePath, folderName)
            # Verify if the folder already exists
            if not(os.path.exists(gamePath)):
                # Folder does not yet exist
                # Create the folder
                os.mkdir(gamePath)
            # Copy the file
            shutil.copy(fileName, gamePath)

# Define the function to delete lingering igb files
def deleteLingering(fileList):
    # Delete the lingering files
    for file in fileList:
        # Check if the file name is not a none type
        if not(file == None):
            # File is not a none type
            # Check if the file exists
            if os.path.isfile(file):
                # File exists
                # Delete the file
                os.remove(file)


# ############## #
# MAIN EXECUTION #
# ############## #
# Set the window title
ctypes.windll.kernel32.SetConsoleTitleW("BaconWizard17's igb Finisher")
# Display the title
resources.printPlain("██╗ ██████╗ ██████╗ ███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗███████╗██████╗ ")
resources.printPlain("██║██╔════╝ ██╔══██╗██╔════╝██║████╗  ██║██║██╔════╝██║  ██║██╔════╝██╔══██╗")
resources.printPlain("██║██║  ███╗██████╔╝█████╗  ██║██╔██╗ ██║██║███████╗███████║█████╗  ██████╔╝")
resources.printPlain("██║██║   ██║██╔══██╗██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║██╔══╝  ██╔══██╗")
resources.printPlain("██║╚██████╔╝██████╔╝██║     ██║██║ ╚████║██║███████║██║  ██║███████╗██║  ██║")
resources.printPlain("╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝")
# Print relevant info
resources.printPlain("\nVersion 1.0.0")
resources.printPlain("https://marvelmods.com/forum/index.php\n")
# Print the welcome message
resources.printImportant("Welcome to BaconWizard17's igb Finisher!\n")
# Read the settings
settings = parseConfig()
# Get the character numbers
XML1Num = settings[0]
XML2Num = settings[1]
MUA1Num = settings[2]
MUA2Num = settings[3]
# Get the other settings
hexEditChoice = settings[4]
runAlchemyChoice = settings[5]
multiPose = settings[6]
# Determine if hex editing is needed
if hexEditChoice == "True":
    # Hex editing is needed
    # Verify existence of XVI32
    verifyXVI32Existence()
# Check if the asset can be recognized from the file name
assetType = getAssetTypeFromName()
# Determine if the asset type is unknown
if assetType == "Unknown":
    # Asset type could not be identified from the name
    # Print a warning message
    resources.printWarning("WARNING: Asset type could not be identified from the file name. Please choose the asset type.")
    # Check which assets should be asked about
    assetChoices = getAssetChoices(XML1Num, XML2Num, MUA1Num, MUA2Num)
    # Get the asset type
    assetType = resources.select("Which asset type are you finishing?", assetChoices)
    # Determine if the asset is not "Other"
    if not(assetType == "Other"):
        # Asset is not "Other", need to get the file name
        # Ask for the file name
        fileName = resources.path("What is the name of the file that you are processing?", fileNameValidatorStart)
        # add the file extension
        fileName += ".igb"
else:
    # asset could be identified from the name
    fileName = "Known"
# Determine if an XML-compatible asset is being used
if not(assetType == "Mannequin"):
    # XML-compatible asset is being used
    # Get the XML file path
    XMLPath = getFilePath(XML1Num, XML2Num, "XML1", "XML2")
# Determine if an MUA-compatible asset is being used
if not((assetType == "Character Select Portrait") or (assetType == "3D Head")):
    # MUA-compatible asset is being used
    # Get the MUA file path
    MUAPath = getFilePath(MUA1Num, MUA2Num, "MUA1", "MUA2")
# Begin processing
if assetType == "Skin":
    # Skin
    # Determine if the file name needs to be updated
    if not(fileName == "Known"):
        # Name unknown, need to update
        os.rename(fileName, "igActor01_Animation01DB.igb")
    # Call the skin processing function
    skinProcessing(XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath)
elif assetType == "Mannequin":
    # Mannequin
    # Determine if the file name needs to be updated
    if not(fileName == "Known"):
        # Name unknown, need to update
        os.rename(fileName, "123XX (Mannequin).igb")
    # Call the mannequin processing function
    mannequinProcessing(MUA1Num, MUA2Num, MUAPath, multiPose)
elif assetType == "3D Head":
    # 3D Head
    # Determine if the file name needs to be updated
    if not(fileName == "Known"):
        # Name unknown, need to update
        os.rename(fileName, "123XX (3D Head).igb")
    # Call the 3D head processing function
    headProcessing(XML1Num, XML2Num, XMLPath)
elif assetType == "Conversation Portrait":
    # Conversation portrait
    # Determine if the file name needs to be updated
    if not(fileName == "Known"):
        # Name unknown, need to update
        os.rename(fileName, "hud_head_123XX.igb")
    # Call the conversation portrait processing function
    convoProcessing(XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath)
elif assetType == "Character Select Portrait":
    # Character select portrait
    # Determine if the file name needs to be updated
    if not(fileName == "Known"):
        # Name unknown, need to update
        os.rename(fileName, "123XX (Character Select Portrait).igb")
    # Call the mannequin processing function
    CSPProcessing(XML1Num, XML2Num, XMLPath)
else:
    # Other models
    otherProcessing(XML1Num, XML2Num, MUA1Num, MUA2Num, XMLPath, MUAPath)