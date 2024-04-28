# ########### #
# INFORMATION #
# ########### #


# ####### #
# IMPORTS #
# ####### #
# Resources for this program
import resources
# To be able to copy and move files
import os.path


# ######### #
# FUNCTIONS #
# ######### #

# Define the function for checking numbers
def numCheck(num1, num2, numList, name1, name2, nameList):
    # Add the first number to the number list
    numList.append(num1)
    # Add the first name to the name list
    nameList.append(name1)
    # Determine if the numbers are the same
    if num1 != num2:
        # The numbers are not the same
        # Add the second number to the number list
        numList.append(num2)
        # Add the second name to the name list
        nameList.append(name2)

    return numList, nameList

# Define the function for getting the hex editing string
def getReplaceList(num: str, assetType: str, geomNames: list, texPathList: list) -> list:
    # Set up the new value for the new skin number
    b_Num = bytearray(num, 'utf-8')
    # Initialize a list to hold the hex string pairs
    b_List = []
    # Loop through the texture paths
    for path in texPathList:
        # Determine if the character name is in the texture path
        if "12301" in path:
            # The texture path has the character number in it
            # Convert the texture path to hex
            b_12301_tex = bytearray(path, 'utf-8')
            # Replace the generic number with the character-specific number in the texture path and convert it to hex.
            b_tex = bytearray(path.replace("12301", num), 'utf-8')
            # Add the hex strings to the list of hex strings.
            b_List.append([b_12301_tex, b_tex])
    # Determine the asset type
    if assetType == "Conversation Portrait":
        # Conversation portrait
        # Set up the default string
        b_12301_conversationpng = bytearray('12301_conversation.png', 'utf-8')
        # Set up the new string
        b_Num_conversationpng = b_Num + bytearray('_conversation.png', 'utf-8')
        # Build the list
        b_List.append([b_12301_conversationpng, b_Num_conversationpng])
    else:
        # 3D asset
        # Set the pre-determined value for the main geometry
        b_12301 = bytearray('12301', 'utf-8')
        # Loop through the remaining geometry names
        for geomName in geomNames:
            # Determine if the geometry has the character number in it.
            if "12301" in geomName:
                # The geometry has the character number in it.
                # Verify that this is secondary geometry and not the main geometry. The strings for the main geometry have already been defined and need to be last in the list.
                if not(geomName == "12301"):
                    # This is secondary geometry.
                    # Convert the geometry name to hex.
                    b_12301_geom = bytearray(geomName, 'utf-8')
                    # Replace the generic number with the character-specific number in the geometry name and convert it to hex.
                    b_geom = bytearray(geomName.replace("12301", num), 'utf-8')
                    # Add the hex strings to the list of hex strings.
                    b_List.append([b_12301_geom, b_geom])
        # Determine if this is a skin
        if assetType == "Skin":
            # This is a skin.
            # Set up the default appearance string.
            b_igActor01_Appearance = bytearray('igActor01Appearance', 'utf-8')
            # Add the appearance string to the list of hex strings, along with the character number (which will replace the appearance string).
            b_List.append([b_igActor01_Appearance, b_Num])
        # Append the hex strings for the main geometry.
        b_List.append([b_12301, b_Num])
    # Return the list of hex strings.
    return b_List

def hexEditor(filename: str, replace: list):
    # Read the file in byte mode
    with open(filename, 'rb') as f:
        byte = f.read()

    for b in replace:
        # Verify that the replace string is not longer
        if len(b[0]) >= len(b[1]):
            r = b[1] + bytearray(([0] * (len(b[0]) - len(b[1]))))
            byte = byte.replace(b[0], r)

    # Replace the same file with the new byte data
    with open(filename, 'wb') as f:
        f.write(byte)

# Define the function for hex editing
def hexEdit(numList, nameList, assetType):
        # Determine the length of the character number
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
                # Get the geometry names from the file using Alchemy
                geomNames = resources.GetModelStats(name)
                # Get the texture paths from the file using Alchemy
                (texPathList, texFormatList) = resources.GetTexPath(name)
                # Perform the hex editing
                hexEditor(name, getReplaceList(num, assetType, geomNames, texPathList))