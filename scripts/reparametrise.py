import xml.etree.ElementTree as ET

import os
import re
import sympy


def convert_attribute_value(expr_string):
    print(expr_string)
    return re.sub(r'\{(.*?)\}', convert_expression, expr_string)

def convert_expression(matchobj):
    expr_string = matchobj.group(1)
    print("In convert_expression:", expr_string)
    expr = sympy.sympify(expr_string)
    print(expr)
    return '{%s}' % str(expr.subs('arrowhead_width', 'total_width - arrowbody_width'))


base_dir = '../glyph_definitions'
output_dir = '../reparametrised'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

specification_glyphs = {}
bare_glyphs = {}

for file_name in os.listdir(base_dir):
    print(f"Now processing {file_name}")
    base_name = os.path.splitext(file_name)[0]
    extension = os.path.splitext(file_name)[1]

    if extension != ".svg":
        continue

    tree = ET.parse(os.path.join(base_dir, file_name))
    svg_tree = tree.getroot()

    for child in svg_tree:
        parametric_attributes = []
        for attrib in child.attrib:
            if attrib.startswith('{https://parametric-svg.github.io/v0.2}'):
                child.attrib[attrib] = convert_attribute_value(child.attrib[attrib])

    # This ensures that we XML is serialised using the desired namespace names, rather than 'ns0' and 'ns1'
    nsmap = {
        'http://www.w3.org/2000/svg':  '',
        'https://parametric-svg.github.io/v0.2': 'parametric'
    }
    ET._namespace_map.update(nsmap)

    tree.write(os.path.join(output_dir, f"{base_name}.svg"))
