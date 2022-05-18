# block models and textures are from default minecraft assets
# items.json is from prismarine-data

import json
import cv2
import numpy as np
from skimage import io
import os

output_name = "blockColors.json"

def getAverageColor(path):
    if path.startswith("minecraft:block/"):
        path = path[len("minecraft:block/"):]
    img = io.imread(os.path.join("block_textures", path + ".png"))
    avgColor = img.mean(axis=0).mean(axis=0)
    avgColor = avgColor.tolist()
    if (len(avgColor) == 3):
        avgColor.append(255.0)
    return avgColor

blockIndex = []

for filename in os.listdir('block_models'):
    fin = open(os.path.join("block_models", filename))
    model_data = json.load(fin)
    fin.close()

    blockName = filename[:-len(".json")]
    if (blockName.endswith("_inventory")):
        blockName = blockName[:-len("_inventory")]

    if 'parent' in model_data and model_data['parent'] == "minecraft:block/cube_all":
        avgColor = getAverageColor(model_data['textures']['all'])
        if (avgColor[3] != 255.0):
            continue
        blockIndex.append({"name": blockName, "color": avgColor})

fout = open(output_name, 'w', encoding='utf-8')
json.dump(blockIndex, fout)
fout.close()