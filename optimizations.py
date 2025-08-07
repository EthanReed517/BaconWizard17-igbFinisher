# ########### #
# INFORMATION #
# ########### #
# This module is used to write Alchemy optimizations


# ####### #
# IMPORTS #
# ####### #


# ################ #
# GLOBAL VARIABLES #
# ################ #
# This dictionary defines various alchemy optimizations.
optimization_dict = {
    'texture_stats': ['name = igStatisticsTexture', 'useFullPath = true', 'separatorString = ^|', 'columnMaxWidth = -1', 'showColumnsMask = 0x00000117', 'sortColumn = -1']
}

# ######### #
# FUNCTIONS #
# ######### #
# This function is used to write an optimization.
def WriteOptimization(optimization_list, optimization_path):