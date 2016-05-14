from lxml import etree as ET
import os
#from test_heading import is_heading
from extract_text import get_text
#import json as JSON

import re

def process_text_from_xml(filename, out_dir):
    paper = get_text(filename)
    out_filename = out_dir+'/'+filename.split('/')[-1].split('.')[-2]+'.xml'
    # root = paper.get
    text_tree = ET.ElementTree(paper)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    text_tree.write(out_filename)
    #str = ET.tostring(text_tree)
    #file = open(out_filename, 'w')
    # file.write(str)
    # file.close()
    print out_filename, 'text extracted'

def process_textdata(filename, collections):
# process Files, add data to existing.xml
    #collections = ET.Element('collections')
    #papers = collections.findall("./paper")
    #num = len(papers)

    # for idx, filename in enumerate(filelist):
    #
    #     if filename in '.DS_Store':
    #         continue

        dir_xml = filename

        print idx,dir_xml

        paper = get_text(dir_xml)

        paper.set('id',str(num+idx))

        #collections.insert(num+idx,paper)

        #print i

    #tree = ET.ElementTree(collections)

    #tree.write(output)
