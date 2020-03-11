import xml.etree.ElementTree as ET
import os

base_dir = '../glyph_definitions'

specification_glyphs = {}

all_params = set()
param_combinations = {}

for file_name in os.listdir(base_dir):
    (base_name, extension) = os.path.splitext(file_name)
    extension = os.path.splitext(file_name)[1]

    if extension != ".svg":
        continue

    tree = ET.parse(os.path.join(base_dir, file_name))
    svg_tree = tree.getroot()

    param_string = svg_tree.attrib['{https://parametric-svg.github.io/v0.2}defaults']
    params = [ param.split('=')[0] for param in param_string.split(';') ]
    all_params = all_params.union(params)

    params.sort()
    params_list_string = ", ".join(params)
    if params_list_string in param_combinations.keys():
        param_combinations[params_list_string].append(base_name)
    else:
        param_combinations[params_list_string] =[base_name]

print(f"Complete list of glyphs is {', '.join(all_params)}")

for params_list_string in param_combinations.keys():
    glyph_list = param_combinations[params_list_string]
    print(f"\nUsed by {len(glyph_list)} glyphs ({', '.join(glyph_list)}):")
    print(params_list_string)

#print(len(param_combinations))