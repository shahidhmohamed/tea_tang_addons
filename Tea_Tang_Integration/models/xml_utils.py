import xml.etree.ElementTree as ET

def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.Element(key)
        child.text = str(val)
        elem.append(child)
    return ET.tostring(elem, encoding='unicode')