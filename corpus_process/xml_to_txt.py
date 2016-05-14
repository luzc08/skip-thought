from lxml import etree as ET


def get_raw_text(filename, t_filename):

    f = open(t_filename, "a+")

    data = ET.parse(filename)

    print data

    root = data.getroot()

    sections = root.findall("./section")

    #print sections

    for sec in sections:
        #print sec.get('heading')
        if sec.get('heading')=='ABSTRACT':
            f.write(sec.get('heading')+'\n')
            abstract = sec.find("./para")
            print abstract.get('text')
            f.write(abstract.get('text')+'\n')
        elif 'REFERENCE' not in sec.get('heading'):
            f.write(sec.get('heading')+'\n')
            paras = sec.findall("./para")
            for para in paras:
                print para.get('text')
                f.write(para.get('text')+'\n')

    #print paper

    f.close()
