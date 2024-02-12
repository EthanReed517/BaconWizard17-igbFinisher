# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Resources for this program
import resources
# To be able to copy and move files
import os


# ######### #
# FUNCTIONS #
# ######### #
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

# Define the function for checking numbers
def numCheck(num1, num2, numList, name1, name2, nameList):
    # Determine if the numbers are the same
    if num1 == num2:
        # The numbers are the same
        # Only add one number to the number list
        numList.append(num1)
        # Only add one name to the name list
        nameList.append(name1)
    else:
        # The numbers are not the same
        # Add both numbers to the number list
        numList.append(num1)
        numList.append(num2)
        # Add both names to the name list
        nameList.append(name1)
        nameList.append(name2)
    return numList, nameList

# Define the function for getting the hex editing string
def getHexString(num, assetType):
    # Initialize the hex string
    hexString = ""
    # Determine the asset type
    if assetType == "Skin":
        # Skin
        # Set the pre-determined values
        hexigActor01_Appearance = "69 67 41 63 74 6F 72 30 31 41 70 70 65 61 72 61 6E 63 65"
        hex12301_outline = "31 32 33 30 31 5F 6F 75 74 6C 69 6E 65"
        hex12301_other = "31 32 33 30 31 5F"
        hex12301 = "31 32 33 30 31"
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
        # Loop through the values
        for hexItem in [hexigActor01_Appearance, hexAppearance, hex12301_outline, hexOutline, hex12301_other, hexOther, hex12301, hexNum]:
            # Add to the hex string
            hexString += ("\"" + hexItem + "\" ")
        # Set the hex script name
        hexScript = "hexSkin"
    elif (assetType == "Mannequin") or (assetType == "3D Head"):
        # Mannequin or 3D Head
        # Set the pre-determined values
        hex12301_other = "31 32 33 30 31 5F"
        hex12301 = "31 32 33 30 31"
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
        # Loop through the values
        for hexItem in [hex12301_other, hexOther, hex12301, hexNum]:
            # Add to the hex string
            hexString += ("\"" + hexItem + "\" ")
        # Set the hex script name
        hexScript = "hexMannOrHead"
    elif assetType == "Conversation Portrait":
        # Conversation portait
        # Set the pre-determined values
        hex12301_conversationpng = "31 32 33 30 31 5F 63 6F 6E 76 65 72 73 61 74 69 6F 6E 2E 70 6E 67"
        # Determine the length of the character number
        if len(num) == 2:
            # 2-digit character number
            # Establish hex editing values
            hexNum_conversationpng = "3" + num[0] + " 3" + num[1] + " 30 31 5F 63 6F 6E 76 65 72 73 61 74 69 6F 6E 2E 70 6E 67 00"
        else:
            # 3-digit character number
            # Establish hex editing values
            hexNum_conversationpng = "3" + num[0] + " 3" + num[1] + " 3" + num[2] + " 30 31 5F 63 6F 6E 76 65 72 73 61 74 69 6F 6E 2E 70 6E 67"
        # Loop through the values
        for hexItem in [hex12301_conversationpng, hexNum_conversationpng]:
            # Add to the hex string
            hexString += ("\"" + hexItem + "\" ")
        # Set the hex script name
        hexScript = "hexConvo"
    return hexString, hexScript

# Define the function for hex editing
def hexEdit(numList, nameList, assetType):
    # Initialize a list for the character numbers
    hexNumList = []
    # Initialize a list for the character names
    hexNameList = []
    # Get the numbers to add to the list
    (hexNumList, hexNameList) = numCheck(numList[0], numList[1], hexNumList, nameList[0], nameList[1], hexNameList)
    # Determine if this is something used by all 4 games
    if len(numList) == 4:
        # This is used by all 4 games
        # Add the other numbers to the list
        (hexNumList, hexNameList) = numCheck(numList[2], numList[3], hexNumList, nameList[2], nameList[3], hexNameList)
    # Loop through the character numbers and file names
    for num, name in zip(hexNumList, hexNameList):
        # Determine if the name is defined
        if not(name == None):
            # The name is defined
            # Determine if the file exists
            if os.path.exists(name):
                # The file exists
                # Determine the hex editing string
                (hexString, hexScript) = getHexString(num, assetType)
                # Perform the hex editing
                os.system("START /W XVI32\\xvi32.exe \"" + name + "\" /S=Scripts\\" + hexScript + ".xsc " + hexString)