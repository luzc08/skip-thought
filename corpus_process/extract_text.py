#import xml.etree.ElementTree as ET
from lxml import etree as ET
from test_heading import *


def get_text(filename):
    ### TODO: RE for dealing with ? marks
    tree1 = ET.parse(filename)

    root = tree1.getroot()

    # word_exempt = ['HCI','ACM']

    # b = root[1];

    pages = root.findall("./pages/page")
    chunks = root.findall("./pages/page/chunks/chunk")

    title = ''
    fId_title = 0
    sId_title = 0
    h_title = '9'

    fId_a = 0
    sId_a = 0
    h_a = 0

    fId_p = 0
    sId_p = 0
    h_p = pages[0].get('mostPopWordHeight')

    heading_list = []
    subheading_list = []

    str0 = ''
    str_p = ''
    str_a = ''

    flag_sub = 0
    flag_widx = 0
    flag_sec = 0

    # collections = ET.Element('collections')

    paper = ET.Element('paper')
    paper.set('filename', filename.split('/')[-1])
    t = ET.SubElement(paper, 'title')
    # auth_node = ET.SubElement(paper, 'author')

    flag_auth = 0
    flag_conf = 0

    for idx, chunk in enumerate(chunks):
        if chunk.get('type') == 'title':
            words = chunk.findall("./words/wd")
            for word in words:
                if len(title) > 0:
                    title += ' ' + word.get('t')
                else:
                    title += word.get('t')
            t.set('text', replace_qm(title))
        elif chunk.get('type') == 'header' and flag_conf == 0:
            # get conference
            header = chunk.findall("./words/wd")
            for idx,tmpheader in enumerate(header):
                header_text = tmpheader.get('t')
                if header_text in ['CHI', 'UIST']:
                    flag_conf = 1
                    if idx<len(header)-1:
                        paper.set('conference', header_text + header[idx+1].get('t'))
                    else:
                        paper.set('conference', header_text)
                    #print header_text + header[idx+1].get('t')
        elif chunk.get('fontSize') == '13' or chunk.get('fontSize') == '14' and flag_auth == 0:
            author_raw = chunk.findall("./words/wd")
            flag_auth = 1
            for idx, auth in enumerate(author_raw):
                auth_text = auth.get('t')
                if idx == 0:
                    fId_a = auth.get('fId')
                    sId_a = auth.get('sId')
                    h_a = auth.get('h')
                    str_a = auth_text
                elif is_heading(auth, fId_a, sId_a, h_a):
                    str_a = str_a + ' ' + auth_text
                elif not is_heading(auth, fId_a, sId_a, h_a):
                    str_a = ''.join([i for i in str_a if not i.isdigit()])
                    paper.set('author', str_a)
                    break
        if chunk.get('type') == 'body' or (chunk.get('type') == 'unclassified' and (
                        abs(int(chunk.get('fontSize')) - int(h_p)) <= 2 or chunk.get('fontSize') == h_p)) or (
                chunk.get('type') == 'heading' and all(
            word.get('t').isupper() for word in chunk.findall("./words/wd"))):
            words = chunk.findall("./words/wd")
            for widx, word in enumerate(words):
                text = word.get('t');
                if text == 'ABSTRACT':
                    fId_title = word.get('fId');
                    sId_title = word.get('sId');
                    h_title = word.get('h');
                    if widx < len(words) - 1:
                        fId_p = words[widx + 1].get('fId');
                        sId_p = words[widx + 1].get('sId');
                    else:
                        fId_p = chunk.find("./words/wd").get('fId');
                        sId_p = chunk.find("./words/wd").get('sId');
                    # h_p = words[widx + 1].get('h');
                if word.get('h') == h_p or word.get('h') == h_title:
                    if is_heading(word, fId_title, sId_title, h_title):
                        # print text
                        if len(str0) > 0:
                            str0 = str0 + ' ' + text
                        else:
                            str0 = text
                        if widx < len(words) - 1 and (test_split_str(str0, words[widx + 1].get('t')) or test_split1(word, words[widx + 1]) or not is_heading(words[widx + 1], fId_title, sId_title, h_title)):
                            # and (test_split1(word, words[widx + 1]) or (not is_heading(words[widx + 1], fId_title, sId_title, h_title))))
                            # test heading1
                            if is_heading1(str0) and is_heading1_str(str0) and 'ACM' not in str0:  # section
                                #print str0
                                #print words[widx + 1].get('t')
                                heading_list.append(str0)
                                section = ET.SubElement(paper, 'section')
                                section.set('heading', replace_qm(str0))
                                flag_sec = 1
                                flag_widx = widx + 1
                                flag_sub = 0
                                str0 = ''
                            elif len(str0) >= 3:  # subsection
                                if str0 != 'ACM':
                                    subheading_list.append(str0)
                                    #print str0
                                    subsection = ET.SubElement(section, 'subsection')
                                    subsection.set('heading', replace_qm(str0))
                                    flag_sub = 1
                                    flag_widx = widx + 1
                                    str0 = ''
                        elif widx == len(words) - 1:
                            heading_list.append(str0)
                            section = ET.SubElement(paper, 'section')
                            section.set('heading', replace_qm(str0))
                            flag_sec = 1
                            flag_widx = widx+1   ##??
                            flag_sub = 0
                            str0 = ''
                    elif is_text(word, fId_p, sId_p, h_p):
                        if len(str_p) > 0:
                            str_p = str_p + ' ' + text
                        else:
                            str_p = text
                        #print str_p
                        if widx < len(words) - 1 and is_text(words[widx + 1], fId_p, sId_p, h_p) and (
                                    abs(int(words[widx + 1].get('y')) - int(words[widx].get('y'))) < 14):
                            # next one is text and text close enough
                            next_word = words[widx + 1].get('t')
                            if '?' in text and len(next_word) > 0 and not next_word[0].isupper():
                                # dealing with question mark
                                text = text.replace('?', '\'')
                                # print text
                                # if text in ['There']:
                                # 	print text, "true",widx

                        else:
                            # if text in ['imaging.']:
                            # 	print text, flag_sub
                            if flag_sub == 1:
                                # if text in ['scene.']:
                                # 	print str_p,flag_sec,flag_sub
                                # parsing the para for subsection
                                if (len(str_p) > 0 and str_p[0].isupper()) or (
                                                flag_widx > 0 and flag_widx<len(words) and is_heading(words[flag_widx - 1], fId_title, sId_title,
                                                                             h_title)):
                                    # subsection.set('text',str_p)
                                    para = ET.SubElement(subsection, 'para')
                                    para.set('text', replace_qm(replace_space(str_p)))
                                    flag_widx = 0
                                else:
                                    vardict = dir()
                                    if 'para' in vardict:
                                        tmp = para.get('text') + ' ' + str_p
                                        para.set('text', replace_qm(replace_space(tmp)))
                                if widx < len(words) - 1 and is_heading(words[widx + 1], fId_title, sId_title, h_title):
                                    flag_sub = 0
                            elif flag_sec == 1:
                                #print str_p
                                if (len(str_p) > 0 and str_p[0].isupper()) or (
                                                flag_widx >= 1 and flag_widx<len(words) and is_heading(words[flag_widx - 1], fId_title, sId_title,
                                                                             h_title)):
                                    # print str_p
                                    para = ET.SubElement(section, 'para')
                                    para.set('text', replace_qm(replace_space(str_p)))
                                    flag_widx = 0
                                else:
                                    #print flag_widx
                                    vardict = dir()
                                    if 'para' in vardict:
                                        tmp = para.get('text') + ' ' + str_p
                                        para.set('text', replace_qm(replace_space(tmp)))
                            str_p = ''

    # ET.dump(paper)
    # tree = ET.ElementTree(paper)
    return paper
