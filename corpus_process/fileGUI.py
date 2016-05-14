from Tkinter import *
import tkFileDialog
#from get_title_list import *
from process_text import *
import subprocess
import xml.etree.ElementTree as ET
import os.path

class Application(Frame):
    # def say_hi(self):
    #     print "hi there, everyone!"
    file_path_list = []
    collections_output = 'static/collections1.xml'
    idx = 0
    file_folder = ''
    file_list = []
    #file_n = ''
    dir_str = ''

    def open_file(self):
        file_path = tkFileDialog.askopenfilenames()
        self.file_path_list =  list(file_path)
        #print self.file_path_list
        self.listbox.delete(0,END)
        for item in self.file_path_list:
            self.listbox.insert(END,item)

    def clear_file(self):
        self.file_path_list = []
        self.listbox.delete(0,END)

    def call_lapdf(self,file_name, tmp_str):
        subprocess.call(['java', '-classpath', 'lapdftext.jar', 'edu.isi.bmkeg.lapdf.bin.BlockifyClassify', file_name,'corpusxml/'+ tmp_str])

    def extract_and_show(self):
        if self.idx < len(self.file_list):
            file_name = self.file_folder + '/' +self.file_list[self.idx]
            self.call_lapdf(file_name, self.dir_str)
            self.idx += 1
        xxx = 'sdsdsdd'
        print self.idx
        return xxx

    # def examine_window(self):
    #     self.idx = 0
    #     self.file_list = os.listdir(self.file_folder)
    #
    #     t = Toplevel(self)
    #     t.wm_title("Test extraction results")
    #     t.next_text_btn = Button(t, command = self.extract_and_show)
    #     t.next_text_btn["text"] = "Extract"
    #     # t.next_text_btn["command"] = self.extract_and_show(file_folder, file_list[self.idx], tmp_str)
    #     #t.next_text_btn.pack({"side": "left"})
    #     #l = Button(t, text="This is window #%s"
    #     t.next_text_btn.pack(side="top", fill="both", expand=True, padx=100, pady=100)

        #self.extract_and_show(file_folder, file_list[self.idx], tmp_str)
        #self.idx += 1

        #l = Label(t, text="This is window")
        #l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    def process(self):
        self.file_folder = tkFileDialog.askdirectory()
        self.dir_str = self.file_folder.split('/')[-1]
        tmp_str = self.file_folder.split('/')[-1]
        print 'processing '+self.file_folder
        #self.examine_window()
        #print tmp_str
        #get_headings_list(self.file_path_list,'output.json')
        #process_textdata(self.file_path_list,'output.xml')
        filename_list = os.listdir(self.file_folder)
        filename_list = [ x for x in filename_list if '.pdf' in x]
        for filename in filename_list:
            print 'processing', filename
            subprocess.call(['java', '-classpath', 'lapdftext.jar', 'edu.isi.bmkeg.lapdf.bin.BlockifyClassify', self.file_folder+'/'+filename,'corpusxml/'+ tmp_str])
        # #print self.file_path_list

    def extract_text_batch(self):
        print 'extracting text'
        if os.path.isfile('static/collections1.xml'):
            tree = ET.parse(self.collections_output)
            collections = tree.getroot()
            print 'file founded!'
        else:
            collections = ET.Element('collections')
            print 'file created!'
        process_textdata(self.file_path_list,self.collections_output)

    def delete_file(self):
        items = map(int, self.listbox.curselection())
        for item in reversed(items):
            #print self.listbox.get(item)
            #self.file_path_list.remove(self.listbox.get(item))
            self.listbox.delete(item)
            del self.file_path_list[item]
        print self.file_path_list

    def add_file(self):
        file_path = tkFileDialog.askopenfilenames()
        for item in file_path:
            self.file_path_list.append(item)
        for item in self.file_path_list:
            self.listbox.insert(END,item)
        #print ANCHOR
        #del self.file_path_list[ANCHOR]

    def createWidgets(self):
        # self.QUIT = Button(self)
        # self.QUIT["text"] = "QUIT"
        # self.QUIT["fg"]   = "red"
        # self.QUIT["command"] =  self.quit
        #
        # self.QUIT.pack({"side": "left"})
        self.listbox = Listbox(self,selectmode=EXTENDED)
        self.listbox.config(width = 100)
        self.listbox.pack({"side": "top"})

        self.listbox.insert(END, "a list entry")

        self.open_file_btn = Button(self)
        self.open_file_btn["text"] = "Open Files"
        self.open_file_btn["command"] = self.open_file

        self.open_file_btn.pack({"side": "left"})

        self.add_file_btn = Button(self)
        self.add_file_btn["text"] = "Add Files"
        self.add_file_btn["command"] = self.add_file

        self.add_file_btn.pack({"side": "left"})

        self.delete_file_btn = Button(self)
        self.delete_file_btn["text"] = "Delete File"
        self.delete_file_btn["command"] = self.delete_file

        self.delete_file_btn.pack({"side": "left"})

        self.clear_btn = Button(self)
        self.clear_btn["text"] = "Clear all"
        self.clear_btn["command"] = self.clear_file

        self.clear_btn.pack({"side": "left"})

        self.PROC = Button(self)
        self.PROC["text"] = "Process"
        self.PROC["command"] = self.process

        self.PROC.pack({"side": "left"})

        self.EXTRACT = Button(self)
        self.EXTRACT["text"] = "Extract text from xml"
        self.EXTRACT["command"] = self.extract_text_batch

        self.EXTRACT.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        # self.entrythingy = Entry()
        # self.entrythingy.pack()

        # here is the application variable
        # self.contents = StringVar()
        # # set it to some value
        # self.contents.set("this is a variable")
        # # tell the entry widget to watch this variable
        # self.entrythingy["textvariable"] = self.contents
        #
        # # and here we get a callback when the user hits return.
        # # we will have the program print out the value of the
        # # application variable when the user hits return
        # self.entrythingy.bind('<Key-Return>',
        #                       self.print_contents)

    # def print_contents(self, event):
    #     print "hi. contents of entry is now ---->", \
    #           self.contents.get()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()



# root = tk.Tk()
# root.withdraw()
# file_path = tkFileDialog.askopenfilenames()
# file_path_list = list(file_path)
#
# print file_path_list
