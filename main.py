"""
Name : pre_process.py
Author  : Hongliang Liu, Jing Li, Hongling Lei, Aishwarya Kura
Contact : honglian@andrew.cmu.edu
Time    : 2021/9/11 15:57
Desc: used to scrape data from website A
"""
from os import times
from scrape import Scrape_TJ, Scrape_target, Scrape_walmart, chrome
from tkinter.constants import COMMAND, END
from typing import Sized, Text
from tkinter import ttk
from tkinter import *
from matchVersion import *
from selenium import webdriver
import tkinter as tk
import threading
import time


LARGE_FONT= ("Verdana", 12)

class Application(tk.Tk):

    def __init__(self):
        
        super().__init__()

        self.wm_title("Scrape Program")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.show_frame(StartPage)

    def to_scrape(self, cont, entryText, isBrowser):
        '''

        entryText: The input for what users want to buy
        isBrowser: The bool variable for Chrome to display
        '''
        frame = cont(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        # muti-thread
        frame.t_scrape = threading.Thread(target=frame.scraping, args=(entryText, isBrowser)) 
        frame.t_scrape.start()
        
        
    def to_table(self, cont, tablelist, entryText):
        '''
        tablelist: The array for category data
        '''
        frame = cont(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        frame.display(tablelist, entryText)
        
    def show_frame(self, cont):
        frame = cont(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()
        t = threading.Thread(target=frame.checkChromeDriverUpdate)
        t.start()
        
class StartPage(tk.Frame):
    '''
    indexPage
    The Entry Page for users
    This page is also for matching the chrome version
    '''
    def __init__(self, parent, root):
        super().__init__(parent)
        label_welcome = tk.Label(self, text="Welcome", font=(LARGE_FONT, 21))
        self.label_match = tk.Label(self, text="This label is for match version", font=(LARGE_FONT, 15))
        

        label_buy = tk.Label(self, text="what do you want to buy?", font=(LARGE_FONT, 15))
        label_welcome.pack(pady=10,padx=10)
        self.label_match.pack(pady=10,padx=10)

        self.checkVar = StringVar(value="0")
        self.Checkbutton1 = ttk.Checkbutton(self, text='Turn on the browser',variable=self.checkVar)
        self.Checkbutton1.pack()

        label_buy.pack(pady=10,padx=10)

        self.Text1 = ttk.Entry(self)
        self.Text1.pack()
        button1 = ttk.Button(self, text="Start Scraping", command=lambda: self.to_Scrape(root)).pack(pady=5)
        button2 = ttk.Button(self, text="Exit", command=lambda: exit(0)).pack(pady=5)
        
        
    def to_Scrape(self, root):
        entry_text = self.Text1.get()
        isBrowser = self.checkVar.get()
        root.to_scrape(Scrape, entry_text, isBrowser)

    def checkChromeDriverUpdate(self):
        chrome_version = getChromeVersion() #current chrome version
        driver_version = getChromeDriverVersion() #driver version
        if chrome_version == driver_version:
            self.label_match.configure(text='Your chrome version is {},And your driver version match.'.format(chrome_version))
        else:
            try:
                self.label_match.configure(text='Chromedriver is being downloading...')
                if getLatestChromeDriver(chrome_version):
                    self.label_match.configure(text='Chromedriver {} is ready...'.format(chrome_version))
            except requests.exceptions.Timeout:
                #Timeout
                self.label_match.configure(text='Chromedriver failed, please exit and restart.')
                return False
            except Exception as e:
                self.label_match.configure(text='Unknow exception: {}'.format(e))
                return False

class Scrape(tk.Frame):
    '''
    The Scrape Page for scraping, where the scraping detail will be avalibale in this Page.
    '''
    def __init__(self, parent, root):
        super().__init__(parent)
        self.label = tk.Label(self, text="On Scraping...", font=(LARGE_FONT, 26))
        self.label2 = tk.Label(self, text="Scraping traderjoe's {} item, error: {}".format(0, None), font=(LARGE_FONT, 15))
        self.label3 = tk.Label(self, text="Scraping walmart {} item, error: {}".format(0, None), font=(LARGE_FONT, 15))
        self.label4 = tk.Label(self, text="Scraping target {} item, error: {}".format(0, None), font=(LARGE_FONT, 15))
        
        self.label.pack(pady=10,padx=10)
        self.label3.pack(pady=5,padx=5)
        self.label2.pack(pady=5,padx=5)
        self.label4.pack(pady=10,padx=5)
        
        self.threading = False
        self.button1 = ttk.Button(self, text="Output Table", command=lambda: self.to_Table(root))
        self.button1.pack()
        
        
    def scraping(self, entryText, isBrowser):
        if entryText:
            self.enrtyText = entryText
            self.all_list = []
            
            '''
            Scraping walmart
            '''
            browser = chrome("Y")
            driver_w = browser.get_driver()
            self.walmart_list = Scrape_walmart()
            self.walmart_list.set_chrome(driver_w)
            self.walmart_list.get_table(entryText, self)
            if self.walmart_list.total_list:
                driver_w.close()
            self.all_list.extend(self.walmart_list.total_list)
            
            '''
            Scraping TJ
            '''
            if isBrowser == '1':
                browser = chrome("Y")
            else:
                browser = chrome("N")
                
            driver = browser.get_driver()
            self.TJ_list = Scrape_TJ()
            self.TJ_list.set_chrome(driver)
            self.TJ_list.get_table(entryText, self)
            self.all_list.extend(self.TJ_list.total_list)
            
            '''
            Scraping target
            '''
            self.target_list = Scrape_target()
            self.target_list.set_chrome(driver)
            self.target_list.get_table(entryText, self)
            self.all_list.extend(self.target_list.total_list)
            self.button1.configure(text='Finished!')
  
        else:
            self.label.configure(text="Please input what you want to buy")
            
    def to_Table(self, root):
        root.to_table(Table, self.all_list, self.enrtyText)

class Table(tk.Frame):
    '''Table Page'''
    def __init__(self, parent, root):
        super().__init__(parent)
        self.label = tk.Label(self, text="title", font=LARGE_FONT)
        self.label.pack(pady=5,padx=5)
        
        button1 = ttk.Button(self, text="search another item", command=lambda: root.show_frame(StartPage)).pack()
        button2 = ttk.Button(self, text="quit", command=lambda: exit(0)).pack()

    def display(self, tablelist, entryText):
        
        self.label.configure(text='Query Name:{}'.format(entryText))
        all_head = []
        row_1 = []
        row_2 = []
        for c in tablelist:
            head = c.keys()
            for _head in head:
                if _head in all_head:
                    pass
                else:
                    all_head.append(_head)
                    if _head != 'name' and _head != 'website': 
                        all_head.append("{}%".format(_head))

        columns = all_head

        self.table = ttk.Treeview(
            master=self,  #
            height=15,  # rows,height
            columns=columns,  #
            show='headings',  #
        )
        xscroll = Scrollbar(self, orient=HORIZONTAL,command=self.table.xview)
        yscroll = Scrollbar(self, orient=VERTICAL,command=self.table.yview)

        self.table.configure(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)

        xscroll.pack(side='top',fill='x')
        yscroll.pack(side='right', fill='y')
        self.table.pack()
        f = open(entryText+"_output.csv", 'w',encoding='utf-8')
        for column in columns:
            self.table.heading(column=column, text=column, anchor=CENTER, command=lambda column=column:self.treeview_sort_column(column,False))  #
            self.table.column(column=column, width=80, minwidth=50, anchor=CENTER, )  #
            f.write(column+",")
        f.write("\n")

        for c in tablelist:
            insert_row = []
            head = c.keys()
            insert_row.append(c['name'])
            insert_row.append(c['website'])

            for key in all_head:
                if key in head:  
                    if key != 'name' and key != 'website':
                        insert_row.append(c[key][0])
                        insert_row.append(c[key][1])
                else:
                    insert_row.append('NULL')
                    insert_row.append('NULL')
            for i in insert_row:
                if i is None:
                    f.write('null,')
                else:
                    f.write(i+',')
            f.write('\n')
            self.table.insert('', END,values=insert_row)
        for i in tablelist:
            print(i)

        f.close()
            

        
    def treeview_sort_column(self,col, reverse):#Treeview、column name
        l = [(self.table.set(k, col), k) for k in self.table.get_children('')]
        print(l)
        l.sort(reverse=reverse)#sort
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):#
            self.table.move(k, '', index)
            
        self.table.column(column=col, width=80, minwidth=50, anchor=CENTER, )  #
        self.table.heading(column=col,text=col,anchor=CENTER, command=lambda col=col: self.treeview_sort_column(col, not reverse))#rename title
        
        self.table.update()



if __name__ == '__main__':
    # implement Application
    app = Application()
    # main loop:
    app.mainloop()
