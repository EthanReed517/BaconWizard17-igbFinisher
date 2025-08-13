# ########### #
# INFORMATION #
# ########### #
# This module is used to write Alchemy optimizations


# ####### #
# IMPORTS #
# ####### #
# Internal modules
import questions
# External modules
from configparser import ConfigParser
from os import environ
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
        # Convert textures to DXT1 (preserves transparent textures).
        'igConvertImage (DXT1)': ['name = igConvertImage', 'format = DXT1', 'order = DEFAULT', 'isExclude = exclude', 'convertIfSmaller = true', 'preserveAlpha = true', 'imageListFilename = '],
        # Convert textures to PNG8, including alpha PNG8.
        'igQuantizeRaven': ['name = igQuantizeRaven', 'imageList = ', 'imageListFilename = ', 'isExclude = true', 'isReduce = false', 'alphaPallete = true', 'eightBitTofourBitOnly = false'],
        # Convert textures to PNG8 but skips any textures in the texture list.
        'igQuantizeRaven (exclude)': ['name = igQuantizeRaven', 'imageList = ', f'imageListFilename = {Path(environ['temp']) / 'temp.txt'}', 'isExclude = true', 'isReduce = false', 'alphaPallete = true', 'eightBitTofourBitOnly = false'],
        # Convert textures to PNG8 but only on any textures in the texture list.
        'igQuantizeRaven (include)': ['name = igQuantizeRaven', 'imageList = ', f'imageListFilename = {Path(environ['temp']) / 'temp.txt'}', 'isExclude = false', 'isReduce = false', 'alphaPallete = true', 'eightBitTofourBitOnly = false'],
        # Convert textures to PNG8 (uses the worse format, only used on environment maps).
        'igConvertImage (PNG8)': ['name = igConvertImage', 'format = x_8', 'order = DEFAULT', 'isExclude = exclude', 'convertIfSmaller = true', 'preserveAlpha = true', f'imageListFilename = {Path(environ['temp']) / 'temp.txt'}']
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
        # Convert opaque textures to DXT5.
        'igConvertImage (DXT5)': ['name = igConvertImage', 'format = IG_GFX_TEXTURE_FORMAT_RGBA_DXT5', 'sourceFormat = rgba_8888_32', 'order = IG_GFX_IMAGE_ORDER_DEFAULT', 'isExclude = exclude', 'convertIfSmaller = false', 'imageListFilename = '],
        # Convert opaque textures to PNG4.
        'igConvertImage (PNG4)': ['name = igConvertImage', 'format = IG_GFX_TEXTURE_FORMAT_X_4', 'sourceFormat = rgb_888_24', 'order = IG_GFX_IMAGE_ORDER_DEFAULT', 'isExclude = exclude', 'convertIfSmaller = false', 'imageListFilename = '],
        # Convert opaque textures to PNG8.
        'igConvertImage (PNG8)': ['name = igConvertImage', 'format = IG_GFX_TEXTURE_FORMAT_X_8', 'sourceFormat = rgb_888_24', 'order = IG_GFX_IMAGE_ORDER_DEFAULT', 'isExclude = exclude', 'convertIfSmaller = false', 'imageListFilename = '],
        # Calls the secondary optimization for XML2 PSP.
        'igOptimizeActorSkinsInScenes': ['name = igOptimizeActorSkinsInScenes', f'fileName = {Path(environ['temp']) / 'opt2.ini'}', 'applySkinLocal = true'],
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
    optimization_path = kwargs.get('optimization_path', Path(environ['temp']) / 'opt.ini')
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
            try:
                # Check the key.
                optimization_dict[kwargs.get('alchemy_version', 'Alchemy 5')][optimization]
                # Increment the counter.
                optimization_count += 1
                # Write the optimization's opening line.
                file.write(f'[OPTIMIZATION{optimization_count}]\n')
                # Loop through the list of lines from the optimization dictionary.
                for line in optimization_dict[kwargs.get('alchemy_version', 'Alchemy 5')][optimization]:
                    # Write the line.
                    file.write(f'{line}\n')
            except KeyError:
                # An unrecognized optimization was called.
                # Determine what operation this is.
                if optimization == 'igResizeImage':
                    # This is the scaling operation.
                    # Increment the counter.
                    optimization_count += 1
                    # Write the optimization's opening line.
                    file.write(f'[OPTIMIZATION{optimization_count}]\n')
                    # Get the scale factor.
                    scale_factor = kwargs.get('scale_to', 1.0)
                    # Loop thorugh the lines for this optimization.
                    for line in ['name = igResizeImage', f'widthFactor = {scale_factor}', f'heightFactor = {scale_factor}', 'minHeight = 1', 'minWidth = 1', 'maxHeight = -1', 'maxWidth = -1', 'resizeMipmap = false', 'useNextPowerOfTwo = true', 'filterType = 6']:
                        # Write the line.
                        file.write(f'{line}\n')
                elif optimization == 'igRavenSetupMUAMaterial':
                    # This is the advanced texture optimization.
                    # Set up the config parser class.
                    config = ConfigParser()
                    # Read the settings file.
                    try:
                        config.read(kwargs['advanced_texture_ini'])
                    except Exception as e:
                        questions.PrintError(f'Failed to open {kwargs['advanced_texture_ini']}.', error_text = e, system_exit = True)
                    # Access the 'OPTIMIZE' section and get the optimizationCount value.
                    try:
                        advanced_texture_count = int(config['OPTIMIZE']['optimizationCount'])
                    except Exception as e:
                        questions.PrintError(f'Failed to read the "optimizationCount" key from the "OPTIMIZE" section of {kwargs['advanced_texture_ini']}.', error_text = e, system_exit = True)
                    # Loop through the advanced texture.
                    for i in range(advanced_texture_count):
                        # Increment the optimization count.
                        optimization_count += 1
                        # Write the optimization's opening line.
                        file.write(f'[OPTIMIZATION{optimization_count}]\n')
                        # Write the optimization name.
                        file.write('name = igRavenSetupMUAMaterial\n')
                        # Loop through the consistent keys.
                        for key in ['diffuseMapName', 'specularMap', 'reflectionMapRight', 'reflectionMapLeft', 'reflectionMapBack', 'reflectionMapFront', 'reflectionMapUp', 'reflectionMapDown', 'reflectance', 'reflectionMaskMap', 'emissiveMap', 'generateTangentBinormals']:
                            # Get the key's value and write it.
                            try:
                                file.write(f'{key} = {config[f'OPTIMIZATION{i + 1}'][key]}\n')
                            except error as e:
                                questions.PrintError(f'Failed to access key "{key}" from the "OPTIMIZATION{i + 1}" section of {kwargs['advanced_texture_ini']}.', error_text = e, system_exit = True)
                        # Determine which normal map type.
                        if kwargs.get('normal_map_type', 'green') == 'green':
                            # This is a green normal map.
                            # Write the green normal map path.
                            try:
                                file.write(f'normalMap = {config[f'OPTIMIZATION{i + 1}']['normalMapGreen']}\n')
                            except error as e:
                                questions.PrintError(f'Failed to access key "normalMapGreen" from the "OPTIMIZATION{i + 1}" section of {kwargs['advanced_texture_ini']}.', error_text = e, system_exit = True)
                        else:
                            # This is a blue normal map.
                            # Write the green normal map path.
                            try:
                                file.write(f'normalMap = {config[f'OPTIMIZATION{i + 1}']['normalMapBlue']}\n')
                            except error as e:
                                questions.PrintError(f'Failed to access key "normalMapBlue" from the "OPTIMIZATION{i + 1}" section of {kwargs['advanced_texture_ini']}.', error_text = e, system_exit = True)
                else:
                    # The optimization was not recognized.
                    questions.PrintError(f'An unrecognized Alchemy optimization ({optimization}) was called.', contact_creator = True, system_exit = True)