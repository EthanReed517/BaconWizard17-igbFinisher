# ########### #
# INFORMATION #
# ########### #
# This module is used to write Alchemy optimizations


# ####### #
# IMPORTS #
# ####### #
# External modules
import os
from pathlib import Path


# ################ #
# GLOBAL VARIABLES #
# ################ #
# This dictionary defines various alchemy optimizations.
optimization_dict = {
    'Alchemy 3.2': {
        # Generate collision.
        'igCollideHullRaven': ['name = igCollideHullRaven', 'maxTrianglesPerLeaf = -1', 'mergeTriangles = false', 'ignoreIsCollidable = false', 'notifyOfError = true', 'totalBeforeVerts = -1', 'totalAfterVerts = -1'],
        # Resize images to their original size (dummy optimization that allows the skin to be run through Alchemy 3.2, slightly reducing file size).
        'igResizeImage (Full)': ['name = igResizeImage', 'widthFactor = 1.0', 'heightFactor = 1.0', 'minHeight = 1', 'minWidth = 1', 'maxHeight = -1', 'maxWidth = -1', 'resizeMipmap = false', 'useNextPowerOfTwo = true', 'filterType = 6'],
        # Resize images to half their original size.
        'igResizeImage (Half)': ['name = igResizeImage', 'widthFactor = 0.5', 'heightFactor = 0.5', 'minHeight = 1', 'minWidth = 1', 'maxHeight = -1', 'maxWidth = -1', 'resizeMipmap = false', 'useNextPowerOfTwo = true', 'filterType = 6'],
        # Resize images to half their original size.
        'igResizeImage (Quarter)': ['name = igResizeImage', 'widthFactor = 0.25', 'heightFactor = 0.25', 'minHeight = 1', 'minWidth = 1', 'maxHeight = -1', 'maxWidth = -1', 'resizeMipmap = false', 'useNextPowerOfTwo = true', 'filterType = 6'],
        # Resize images to one eighth their original size.
        'igResizeImage (Eighth)': ['name = igResizeImage', 'widthFactor = 0.125', 'heightFactor = 0.125', 'minHeight = 1', 'minWidth = 1', 'maxHeight = -1', 'maxWidth = -1', 'resizeMipmap = false', 'useNextPowerOfTwo = true', 'filterType = 6'],
        # Resize images to one sixteenth their original size.
        'igResizeImage (Sixteenth)': ['name = igResizeImage', 'widthFactor = 0.0625', 'heightFactor = 0.0625', 'minHeight = 1', 'minWidth = 1', 'maxHeight = -1', 'maxWidth = -1', 'resizeMipmap = false', 'useNextPowerOfTwo = true', 'filterType = 6'],
        # Convert textures to DXT1 (preserves transparent textures).
        'igConvertImage (DXT1)': ['name = igConvertImage', 'format = DXT1', 'order = DEFAULT', 'isExclude = exclude', 'convertIfSmaller = true', 'preserveAlpha = true', 'imageListFilename = '],
        # Convert textures to PNG8, including alpha PNG8.
        'igQuantizeRaven': ['name = igQuantizeRaven', 'imageList = ', 'imageListFilename = ', 'isExclude = true', 'isReduce = false', 'alphaPallete = true', 'eightBitTofourBitOnly = false'],
        # Convert textures to PNG8 but skips any textures in the texture list.
        'igQuantizeRaven (skip)': ['name = igQuantizeRaven', 'imageList = ', f'imageListFilename = {Path(os.environ['temp']) / 'temp.txt'}', 'isExclude = true', 'isReduce = false', 'alphaPallete = true', 'eightBitTofourBitOnly = false'],
        # Convert textures to PNG8 (uses the worse format, only used on environment maps).
        'igConvertImage (PNG8)': ['name = igConvertImage', 'format = x_8', 'order = DEFAULT', 'isExclude = exclude', 'convertIfSmaller = true', 'preserveAlpha = true', f'imageListFilename = {Path(os.environ['temp']) / 'temp.txt'}']
    },
    'Alchemy 5': {
        # Get statistics for textures.
        'igStatisticsTexture': ['name = igStatisticsTexture', 'useFullPath = true', 'separatorString = ^|', 'columnMaxWidth = -1', 'showColumnsMask = 0x00000117', 'sortColumn = -1'],
        # Get statistics for geometry.
        'igStatisticsGeometry': ['name = igStatisticsGeometry', 'separatorString = ^|', 'columnMaxWidth = -1', 'showColumnsMask = 0x00100001', 'sortColumn = -1'],
        # Generate global color.
        'igGenerateGlobalColor': ['name = igGenerateGlobalColor'],
        # Convert igGeometryAttr to igGeometryAttr2 (standard method)
        'igConvertGeometryAttr': ['name = igConvertGeometryAttr', 'accessMode = 3', 'storeBoundingVolume = false'],
        # Convert opaque textures to DXT1.
        'igConvertImage (DXT1)': ['name = igConvertImage', 'format = IG_GFX_TEXTURE_FORMAT_RGBA_DXT1', 'sourceFormat = rgb_888_24', 'order = IG_GFX_IMAGE_ORDER_DEFAULT', 'isExclude = exclude', 'convertIfSmaller = false', 'imageListFilename = '],
        # Convert opaque textures to PNG4.
        'igConvertImage (PNG4)': ['name = igConvertImage', 'format = IG_GFX_TEXTURE_FORMAT_X_4', 'sourceFormat = rgb_888_24', 'order = IG_GFX_IMAGE_ORDER_DEFAULT', 'isExclude = exclude', 'convertIfSmaller = false', 'imageListFilename = '],
        # Convert opaque textures to PNG8.
        'igConvertImage (PNG8)': ['name = igConvertImage', 'format = IG_GFX_TEXTURE_FORMAT_X_8', 'sourceFormat = rgb_888_24', 'order = IG_GFX_IMAGE_ORDER_DEFAULT', 'isExclude = exclude', 'convertIfSmaller = false', 'imageListFilename = '],
        # Calls the secondary optimization for XML2 PSP.
        'igOptimizeActorSkinsInScenes': ['name = igOptimizeActorSkinsInScenes', f'{Path(os.environ['temp']) / 'opt2.ini'}', 'applySkinLocal = true'],
        # Convert igGeometryAttr to igGeometryAttr2 (XML2 PSP method).
        'igConvertGeometryAttr (PSP)': ['name = igConvertGeometryAttr', 'accessMode = 0', 'storeBoundingVolume = false'],
        # Various additional XML2 PSP optimizations.
        'igConvertTransform': ['name = igConvertTransform', 'firstNodeName = ', 'scaleMax = 0.001', 'transMax = 0.001', 'rotMax = 0.00001', 'eulerMax = 0.00001'],
        'igCollapseAllHierarchies': ['name = igCollapseAllHierarchies', 'nodesToIgnore = ', 'preserveOrder = false'],
        'igPromoteAllAttrs': ['name = igPromoteAllAttrs', 'attrsToIgnore = igGeometryAttr, igGeometryAttr1_5, igGeometryAttr2, igParticleAttr, igLightAttr, igLightStateAttr, igClearAttr, igCopyRenderDestinationAttr, igSetRenderDestination, igDisplayListAttr, igTextureUnloadAttr, igTextureAttr, igVertexShaderAttr, igPixelShaderAttr'],
        'igCollapseGeometry': ['name = igCollapseGeometry', 'useNewMethod = true', 'traversalName = igNodeTraversal'],
        'igCollapseHierarchy (igGeometry)': ['name = igCollapseHierarchy', 'nodeType = igGeometry', 'preserveOrder = false'],
        'igLimitActorBlendPalettes': ['name = igLimitActorBlendPalettes', 'maxBlendMatrixCount = 6'],
        'igCollapseHierarchy (igBlendMatrixSelect)': ['name = igCollapseHierarchy', 'nodeType = igBlendMatrixSelect', 'preserveOrder = false'],
        'igMSStripTriangles': ['name = igMSStripTriangles', 'minNumberOfTriangle = 0', 'stitch = false', 'strip = true', 'index = false', 'compactGeometry = true'],
        'igSetVertexStreamAccessMode': ['name = igSetVertexStreamAccessMode', 'accessMode = 3'],
        'igBuildNativeGeometry': ['name = igBuildNativeGeometry', 'targetPlatform = 4', 'removeOriginalVertexData = true', 'doubleBonePalette = false', 'scaleAlphaPsx2 = true']
    }
}

# ######### #
# FUNCTIONS #
# ######### #
# This function is used to write an optimization.
def WriteOptimization(optimization_list, **kwargs):
    # Set up the optimization path.
    optimization_path = kwargs.get('optimization_path', Path(os.environ['temp']) / 'opt.ini')
    # Open the optimization path to begin writing the file.
    with open(optimization_path, 'w') as file:
        # Loop through the opening lines.
        for line in ['[OPTIMIZE]', f'optimizationCount = {len(optimization_list)}', 'hierarchyCheck = true']:
            # Write the opening lines.
            file.write(f'{line}\n')
        # Start a counter for the current optimization.
        optimization_count = 0
        # Loop through the optmiizations in the optimization list.
        for optimization in optimization_list:
            # Increment the counter.
            optimization_count += 1
            # Write the optimization's opening line.
            file.write(f'[OPTIMIZATION{optimization_count}]\n')
            # Loop through the list of lines from the optimization dictionary.
            for line in optimization_dict[kwargs.get('alchemy_version', 'Alchemy 5')][optimization]:
                # Write the line.
                file.write(f'{line}\n')