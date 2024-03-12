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
def getReplaceList(num: str, assetType: str) -> list:
    # Initialize the hex string
    hexString = ""
    # Set the pre-determined values
    b_12301 = bytearray('12301', 'utf-8')
    b_igActor01_Appearance = bytearray('igActor01Appearance', 'utf-8')
    b_12301_outline = bytearray('12301_outline', 'utf-8')
    b_12301_other = bytearray('12301_', 'utf-8')
    b_12301_conversationpng = bytearray('12301_conversation.png', 'utf-8')
    # Establish hex editing values
    b_Num = bytearray((num + '01'), 'utf-8')
    b_Appearance = b_Num
    b_Outline = b_Num + bytearray('_outline', 'utf-8')
    b_Other = b_Num + bytearray(('_' * (4 - len(num))), 'utf-8')
    b_Num_conversationpng = b_Num + bytearray('_conversation.png', 'utf-8')
    # Determine the asset type
    # since Python 3.10 we can use the switch statement with match assetType: ... case "Skin":
    if assetType == "Skin":
        # Skin
        # Build the list
        b_List = [[b_igActor01_Appearance, b_Appearance], [b_12301_outline, b_Outline], [b_12301_other, b_Other], [b_12301, b_Num]]
    elif (assetType == "Mannequin") or (assetType == "3D Head"):
        # Mannequin or 3D Head
        # Build the list
        b_List = [[b_12301_other, b_Other], [b_12301, b_Num]]
    elif assetType == "Conversation Portrait":
        # Conversation portait
        # Build the list
        b_List = [[b_12301_conversationpng, b_Num_conversationpng]]

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
                # Perform the hex editing
                hexEditor(name, getReplaceList(num, assetType))