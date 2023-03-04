# -*- coding: utf-8 -*-
import regex as re
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import filedialog
import threading
import tkinter.ttk
import DataProcessing
import PDF2image
import Recognition_V2
import convert
import rotate


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartMenu)
        self.title('Sleep study system')
        self.geometry("600x380")
        self.resizable(False,False)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill="both", expand=True)

class StartMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Start Menu").place(x=250, y=50)
        tk.Button(self, text="Recognition",
                  command=lambda: master.switch_frame(Recognition_Page)).place(x=250, y=100)
        tk.Button(self, text="Generate Report",
                  command=lambda: master.switch_frame(Generate_Page_A)).place(x=236, y=200)
        tk.Button(self, text="Recognition and generate",
                  command=lambda: master.switch_frame(Generate_Page_B)).place(x=210, y=300)

class Recognition_Page(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="File Path：").place(x=50, y=50)
        self.var_name = tk.StringVar()
        self.progressbarOne = tkinter.ttk.Progressbar(self, length=400, mode='indeterminate')
        self.progressbarOne.pack(pady=20)
        self.progressbarOne['maximum'] = 100
        self.progressbarOne['value'] = 0
        self.progressbarOne.place(x=100, y=100)
        self.text = Text(self, width=60, height=10, state="disabled")
        self.text.place(x=90, y=150)

        self.entry_name = tk.Entry(self, textvariable=self.var_name, width=55)
        self.entry_name.place(x=120, y=50)
        tk.Button(self, text="choose", command=lambda: self.thread_it(self.selectPath_file)).place(x=525, y=45)
        tk.Button(self, text="transcript", command=lambda: self.thread_it(self.convert_)).place(x=250, y=300)
        tk.Label(self, text="Recognition").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to StartMenu",
                  command=lambda: master.switch_frame(StartMenu)).place(x=400, y=300)

    # input file path
    def selectPath_file(self):
        picpath = filedialog.askopenfilename(filetypes=[("table", [".pdf", ".png", ".jpg", "jpeg"])])
        self.var_name.set(picpath)
        self.text.configure(state='normal')
        self.text.insert('insert', 'The selected file:' + picpath + '\n')
        self.text.configure(state='disabled')

    def convert_(self):
        picpath = self.var_name.get()
        list_index = [i.start() for i in re.finditer("/", picpath)]
        filename = picpath[list_index[-1] + 1:picpath.find(".")]
        self.progressbarOne.start()
        if picpath[-3:] == "pdf":
            self.text.configure(state='normal')
            self.text.insert('insert', 'Converting the pdf file into images...' + '\n')
            self.text.configure(state='disabled')
            file = PDF2image.to_image(picpath, filename)
            self.text.configure(state='normal')
            self.text.insert('insert', 'Convert complete!' + '\n')
            self.text.configure(state='disabled')
        else:
            file = [picpath]
        for i in file:
            self.text.configure(state='normal')
            self.text.insert('insert', 'Rotating the image ' + i + '...' + '\n')
            self.text.configure(state='disabled')
            rotate.rotate_till_align(i)
            self.text.configure(state='normal')
            self.text.insert('insert', 'Rotate complete!' + '\n')
            self. text.configure(state='disabled')
            self.text.configure(state='normal')
            self.text.insert('insert', 'Dividing the cells...' + '\n')
            self.text.configure(state='disabled')
            convert.divide_into_parts(i)
            self.text.configure(state='normal')
            self.text.insert('insert', 'Divide file ' + i + ' complete!' + '\n')

            self.text.configure(state='disabled')
            Recognition_V2.output_file(i[:-3]+".csv")
            self.text.configure(state='normal')
            self.text.insert('insert', 'recognize the file ' +i+ ' complete! CSV file is generated!'+'\n')
            self.text.configure(state='disabled')

        self.progressbarOne.stop()
        messagebox.showinfo("message", "transcription complete!")

    def thread_it(self,func, *args):
        '''use thread to run the GUI'''
        # create
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        # start
        t.start()

class Generate_Page_A(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="obs csv Path：").place(x=50, y=45)
        tk.Label(self, text="sleep data Path：").place(x=50, y=85)
        self.var_name_1 = tk.StringVar()
        self.var_name_2 = tk.StringVar()
        self.progressbarOne = tkinter.ttk.Progressbar(self, length=400, mode='indeterminate')
        self.progressbarOne.pack(pady=20)
        self.progressbarOne['maximum'] = 100
        self.progressbarOne['value'] = 0
        self.progressbarOne.place(x=100, y=120)
        self.text = Text(self, width=60, height=10, state="disabled")
        self.text.place(x=90, y=150)

        self.entry_name = tk.Entry(self, textvariable=self.var_name_1, width=50)
        self.entry_name.place(x=140, y=45)
        self.entry_name_1 = tk.Entry(self, textvariable=self.var_name_2, width=45)
        self.entry_name_1.place(x=160, y=85)
        tk.Button(self, text="choose", command=lambda: self.thread_it(self.selectPath_file)).place(x=525, y=40)
        tk.Button(self, text="choose", command=lambda: self.thread_it(self.selectPath_file_1)).place(x=525, y=80)
        tk.Button(self, text="generate", command=lambda: self.thread_it(self.convert_)).place(x=250, y=300)
        tk.Label(self, text="Generate report").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to StartMenu",
                  command=lambda: master.switch_frame(StartMenu)).place(x=400, y=300)

    # input file path
    def selectPath_file(self):
        picpath = filedialog.askopenfilename(filetypes=[("obs file", [".csv"])])
        self.var_name_1.set(picpath)
        self.text.configure(state='normal')
        self.text.insert('insert', 'The selected file:' + picpath + '\n')
        self.text.configure(state='disabled')

    def selectPath_file_1(self):
        picpath = filedialog.askopenfilename(filetypes=[("sleep data", [".txt"])])
        self.var_name_2.set(picpath)
        self.text.configure(state='normal')
        self.text.insert('insert', 'The selected file:' + picpath + '\n')
        self.text.configure(state='disabled')

    def convert_(self):
        picpath_1 = self.var_name_1.get()
        picpath_2 = self.var_name_2.get()
        print(picpath_2,picpath_1)
        self.text.configure(state='normal')
        self.text.insert('insert', 'Report generating... ' + '\n')
        self.text.configure(state='disabled')
        self.progressbarOne.start()
        filename = DataProcessing.read_table(picpath_2,picpath_1)
        self.progressbarOne.stop()
        self.text.configure(state='normal')
        self.text.insert('insert', 'Report generated! ' + '\n')
        self.text.configure(state='disabled')
        messagebox.showinfo("message", "Generation complete! The file name is: {0}".format(filename))

    def thread_it(self,func, *args):
        '''use thread to run the GUI'''
        # create
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        # start
        t.start()
class Generate_Page_B(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="raw obs Path：").place(x=50, y=45)
        tk.Label(self, text="sleep data Path：").place(x=50, y=85)
        self.var_name_1 = tk.StringVar()
        self.var_name_2 = tk.StringVar()
        self.progressbarOne = tkinter.ttk.Progressbar(self, length=400, mode='indeterminate')
        self.progressbarOne.pack(pady=20)
        self.progressbarOne['maximum'] = 100
        self.progressbarOne['value'] = 0
        self.progressbarOne.place(x=100, y=120)
        self.text = Text(self, width=60, height=10, state="disabled")
        self.text.place(x=90, y=150)

        self.entry_name = tk.Entry(self, textvariable=self.var_name_1, width=50)
        self.entry_name.place(x=140, y=45)
        self.entry_name_1 = tk.Entry(self, textvariable=self.var_name_2, width=45)
        self.entry_name_1.place(x=160, y=85)
        tk.Button(self, text="choose", command=lambda: self.thread_it(self.selectPath_file)).place(x=525, y=40)
        tk.Button(self, text="choose", command=lambda: self.thread_it(self.selectPath_file_1)).place(x=525, y=80)
        tk.Button(self, text="generate", command=lambda: self.thread_it(self.convert_)).place(x=250, y=300)
        tk.Label(self, text="Recognize and Generate report").pack(side="top", fill="x", pady=10)
        tk.Button(self, text="Return to StartMenu",
                  command=lambda: master.switch_frame(StartMenu)).place(x=400, y=300)
    def selectPath_file(self):
        picpath = filedialog.askopenfilename(filetypes=[("obs file", [".pdf", ".png", ".jpg", "jpeg"])])
        self.var_name_1.set(picpath)
        self.text.configure(state='normal')
        self.text.insert('insert', 'The selected file:' + picpath + '\n')
        self.text.configure(state='disabled')

    def selectPath_file_1(self):
        picpath = filedialog.askopenfilename(filetypes=[("sleep data", [".txt"])])
        self.var_name_2.set(picpath)
        self.text.configure(state='normal')
        self.text.insert('insert', 'The selected file:' + picpath + '\n')
        self.text.configure(state='disabled')

    def convert_(self):
        picpath_1 = self.var_name_1.get()
        picpath_2 = self.var_name_2.get()
        list_index = [i.start() for i in re.finditer("/", picpath_1)]
        filename = picpath_1[list_index[-1] + 1:picpath_1.find(".")]
        self.progressbarOne.start()
        if picpath_1[-3:] == "pdf":
            self.text.configure(state='normal')
            self.text.insert('insert', 'Converting the pdf file into images...' + '\n')
            self.text.configure(state='disabled')
            file = PDF2image.to_image(picpath_1, filename)
            self.text.configure(state='normal')
            self.text.insert('insert', 'Convert complete!' + '\n')
            self.text.configure(state='disabled')
        else:
            file = [picpath_1]
        for i in file:
            self.text.configure(state='normal')
            self.text.insert('insert', 'Rotating the image ' + i + '...' + '\n')
            self.text.configure(state='disabled')
            rotate.rotate_till_align(i)
            self.text.configure(state='normal')
            self.text.insert('insert', 'Rotate complete!' + '\n')
            self. text.configure(state='disabled')
            self.text.configure(state='normal')
            self.text.insert('insert', 'Dividing the cells...' + '\n')
            self.text.configure(state='disabled')
            convert.divide_into_parts(i)
            self.text.configure(state='normal')
            self.text.insert('insert', 'Divide file ' + i + ' complete!' + '\n')

            self.text.configure(state='disabled')
            name = Recognition_V2.output_file(i[:-3]+"csv")
            self.text.configure(state='normal')
            self.text.insert('insert', 'recognize the file ' +i+ ' complete! CSV file is generated!'+'\n')
            self.text.configure(state='disabled')
            self.text.configure(state='normal')
            self.text.insert('insert', 'Report generating... ' + '\n')
            self.text.configure(state='disabled')
            self.progressbarOne.start()
            filename = DataProcessing.read_table(picpath_2, name)
            self.progressbarOne.stop()
            self.text.configure(state='normal')
            self.text.insert('insert', 'Report generated! ' + '\n')
            self.text.configure(state='disabled')
        self.progressbarOne.stop()
        messagebox.showinfo("message", "Generation complete! The file name is: {0}".format(filename))

    def thread_it(self,func, *args):
        '''use thread to run the GUI'''
        # create
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        # start
        t.start()
if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()