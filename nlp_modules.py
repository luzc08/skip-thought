from lxml import etree as ET
from nltk.tokenize import sent_tokenize

def test_sentence():
    tree = ET.parse('collections.xml')
    root = tree.getroot()
    find_para = ET.XPath(".//para")

    sections = root.findall("./paper/section")

    sentences = []

    exempt_list = ['Author Keywords','ACM','Classification Keywords','REFERENCES']

    for idx, sec in enumerate(sections):
        paras = find_para(sec)
        for para in paras:
            if para.getparent().get('heading') not in exempt_list:
                #print para.getparent().get('heading')
                sent_tokenize_list = sent_tokenize(para.get('text'))
                sentences += sent_tokenize_list

    return sentences
