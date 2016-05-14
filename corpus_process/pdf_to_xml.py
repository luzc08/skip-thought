import subprocess
import xml.etree.ElementTree as ET
import os.path
from process_text import *

dir_path = 'static/proceedings'
target_path = 'corpusxml'
conf_list = ['CHI','CSCW','UIST','Ubicomp']
#conf_list = ['CHI']
#target_conf = 'CHI'

def process(conf):
    file_folder = dir_path+'/'+conf
    #self.file_folder = tkFileDialog.askdirectory()
    #self.dir_str = self.file_folder.split('/')[-1]
    #tmp_str = file_folder.split('/')[-1]
    print 'processing ' + file_folder
    # self.examine_window()
    # print tmp_str
    # get_headings_list(self.file_path_list,'output.json')
    # process_textdata(self.file_path_list,'output.xml')
    filename_list = os.listdir(file_folder)
    filename_list = [x for x in filename_list if '.pdf' in x]
    for filename in filename_list:
        print 'processing', file_folder, filename
        if not os.path.isfile('corpusxml/' + conf +'/'+filename.split('.')[-2]+'_lapdf.xml'):
            subprocess.call(['java', '-classpath', 'lapdftext.jar', 'edu.isi.bmkeg.lapdf.bin.BlockifyClassify',
                         file_folder + '/' + filename, 'corpusxml/' + conf])
        if not os.path.isfile('extracted/' + conf +'/' + filename.split('.')[-2]+'.xml'):
            if os.path.isfile('corpusxml/' + conf +'/'+filename.split('.')[-2]+'_lapdf.xml'):
                process_text_from_xml('corpusxml/' + conf +'/'+filename.split('.')[-2]+'_lapdf.xml','extracted/'+conf)
        # #print self.file_path_list


folders = os.listdir(dir_path)
t_folders = os.listdir(target_path)

for target_conf in conf_list:
    filtered_folders = [ x for x in folders if x != 'Ubicomp2006' and target_conf in x]
    #print filtered_folders

    for conf in filtered_folders:
        process(conf)