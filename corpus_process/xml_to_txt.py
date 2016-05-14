from lxml import etree as ET


def get_raw_text(filename, t_filename):

    f = open(t_filename, "a")

    data = ET.parse(filename)

    root = data.getroot()

    sections = root.findall("./section")

    for sec in sections:
        if sec.get('heading')=='ABSTRACT':
            f.write(sec.get('heading')+'\n')
            abstract = sec.find("./para")
            f.write(abstract.get('text')+'\n')
        elif 'REFERENCE' not in sec.get('heading'):
            f.write(sec.get('heading')+'\n')
            paras = sec.findall("./para")
            for para in paras:
                f.write(para.get('text')+'\n')

    #print paper

    f.close()
