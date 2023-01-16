'''
Filename  :payment_DB.py
Author    :Vincent,LYF
Date      :19-11-2018

Description: This module defines the functions in pos
'''
import tkinter as tk

import tkinter.scrolledtext as tkst
import pymysql

from tkinter.constants import ACTIVE, DISABLED, NORMAL
from tkinter.constants import LEFT, BOTTOM
from tkinter import Button, Frame, Tk
from faulthandler import disable
import datetime  
from tkinter import ttk
import warnings
from insertionsort import  *
import insertionsort
import matplotlib
import staff_logon
import staff_logon_loop
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import numpy as np


x = np.arange(4)


class Gui:
    def __init__(self, root,id):
        
        self.list=[]
        self.basket=[]
        self.vipId=0
        self.vipFlag=False
        self.total=0 
        self.vipPoints=0
        self.productList=[]
        self.customerPay=''
        
        self.staffId=id
        
        self.wholeDayTotal=0
        self.wholeDayProductList=[]
        self.wholeDayProductList2=[]
        
        self.qtyId=0
        self.qtyFlag=False
        self.priceId=0
        self.priceFlag=False
        
        self.root = root
        self.root.geometry('760x650')
        
        self.root.title("GUI POS System")
        self.nb = ttk.Notebook(root)
        self.page0 = ttk.Frame(self.nb)
        self.page1 = ttk.Frame(self.nb)
        self.page2 = ttk.Frame(self.nb)
        self.page3 = ttk.Frame(self.nb)
        self.page4 = ttk.Frame(self.nb)
        self.page5 = ttk.Frame(self.nb)
        self.page6 = ttk.Frame(self.nb)
        self.page7 = ttk.Frame(self.nb)
        self.page8 = ttk.Frame(self.nb)
        
        
        self.paySign=False
        
        self.add=False
        self.dele=False
        self.addData=[]
        self.delData=[]
        
        self.frame = Frame(root)
        self.frame.pack()
        
        self.dot=False
        self.xFlag=False
        
        self.bind_flag=True
        
        
        self.db = pymysql.connect('localhost','root','','ALL POS')
        self.cursor = self.db.cursor()
        
        self.connection = pymysql.connect(user='root',
                             password='',
                             db='all pos', 
                             cursorclass=pymysql.cursors.DictCursor)
        
        
        self.date=datetime.datetime.now()
        self.date_label=tk.Label(root,text='mkyStore       '+str(self.date.strftime('%Y/%m/%d')) + '       '+str(self.staffId))
        self.date_label.pack()
        
      
        
        self.rootFrame = tk.Frame(self.root)
        
        self.rootFrame.pack()
        
        self.btnLogout=tk.Button(self.rootFrame, text='Logout' , command=lambda: self.logout() )
        self.btnLogout.pack(side=tk.LEFT)
        self.btnLogout.config(state=NORMAL)
        
        self.btnLogoutCancel=tk.Button(self.rootFrame, text='Cancel' , command=lambda: self.logoutCancel() )
        self.btnLogoutCancel.pack(side=tk.LEFT)
        self.btnLogoutCancel.config(state=DISABLED)
        
        self.btnLogoutConfirm=tk.Button(self.rootFrame, text='Confirm' , command=lambda: self.logoutConfirm()() )
        self.btnLogoutConfirm.pack(side=tk.LEFT)
        self.btnLogoutConfirm.config(state=DISABLED)
        
        self.nb.add(self.page0, text='Main')        
        self.nb.add(self.page1, text='Update product')
        self.nb.add(self.page2, text='Add product')
        self.nb.add(self.page3, text='Delete product')
        self.nb.add(self.page4, text='Cash in machine')
        self.nb.add(self.page5, text='Report & reset')
        self.nb.add(self.page6, text='Help')
        
       
        '''
        setup main in POS
        '''
        self.label = tk.Label(self.page0, bg='grey93', text='enter product code')
        self.label.pack()
        
        self.editArea2 = tkst.ScrolledText(self.page0,height=5)
        self.editArea2.pack( fill="both") 
        self.editArea2.config(state="disabled")
        
        self.editArea = tkst.ScrolledText(self.page0,height=5)
        self.editArea.pack(expand=1, fill="both") 
        self.editArea.config(state="disabled")
            
        
        
        
        self.frame4 = tk.Frame(self.page0)
        
        self.frame4.pack()
        
        self.frame5 = tk.Frame(self.page0)
        
        self.frame5.pack()
        
        self.frame6 = tk.Frame(self.page0)
        
        self.frame6.pack()

        self.frame7 = tk.Frame(self.page0)
        
        self.frame7.pack()
        
        
        tk.Button(self.frame7, text='',width=6,height=2).pack(side=tk.LEFT)
       
        tk.Button(self.frame7, text='',width=6,height=2).pack(side=tk.LEFT)
        tk.Button(self.frame7, text='',width=6,height=2).pack(side=tk.LEFT)
        
        self.btnReceive=tk.Button(self.frame7, text='Receive',width=6,height=2, command= lambda:self.pressed_button_a('receive') )
        self.btnReceive.pack(side=tk.LEFT)
        self.btnReceive.config(state=DISABLED)
        
        self.btnPay=tk.Button(self.frame7, text='Pay',width=6,height=2, command=lambda: self.pressed_button_a('pay'))
        self.btnPay.pack(side=tk.LEFT)
        self.btnPay.config(state=NORMAL)
        tk.Button(self.frame7, text=0,  width=3,height=2, command=lambda: self.pressed_button(0)).pack(side=tk.LEFT)
        
        self.btnDot=tk.Button(self.frame7, text='.',width=3,height=2 , command=lambda: self.pressed_button(11))
        self.btnDot.pack(side=tk.LEFT)
        self.btnDot.config(state=NORMAL)
        tk.Button(self.frame7, text='<x',width=3,height=2, command=lambda: self.pressed_button(20)).pack(side=tk.LEFT)
        
        
        tk.Button(self.frame6, text='',width=6,height=2).pack(side=tk.LEFT)
        tk.Button(self.frame6, text='',width=6,height=2).pack(side=tk.LEFT)
        tk.Button(self.frame6, text='',width=6,height=2).pack(side=tk.LEFT)
        tk.Button(self.frame6, text='',width=6,height=2).pack(side=tk.LEFT)
       
        
        self.btnAdd=tk.Button(self.frame6, text='Add',  width=6,height=2, command=lambda: self.pressed_button_a('add'))
        self.btnAdd.pack(side=tk.LEFT)
        self.btnAdd.config(state=NORMAL)
        
        
        tk.Button(self.frame6, text=1,width=3,height=2, command=lambda: self.pressed_button(1)).pack(side=tk.LEFT)
        tk.Button(self.frame6, text=2,width=3,height=2, command=lambda: self.pressed_button(2)).pack(side=tk.LEFT)
        tk.Button(self.frame6, text=3,width=3,height=2, command=lambda: self.pressed_button(3)).pack(side=tk.LEFT)
        
        self.btn_confirm=tk.Button(self.frame5, text='Confirm',width=6,height=2, command=lambda: self.pressed_button_a('confirm'))
        self.btn_confirm.pack(side=tk.LEFT)
        self.btn_confirm.config(state=DISABLED)
       
        self.btnKeyOff=tk.Button(self.frame5, text='Key Off',width=6,height=2,command=lambda: self.pressed_button_a('off'))
        self.btnKeyOff.pack(side=tk.LEFT)
        self.btnKeyOff.config(state=DISABLED)
        
        self.btnDiscount=tk.Button(self.frame5, text='-$5',width=6,height=2, command=lambda: self.pressed_button_a('discount'))
        self.btnDiscount.pack(side=tk.LEFT)
        self.btnDiscount.config(state=DISABLED)
        tk.Button(self.frame5, text='',width=6,height=2).pack(side=tk.LEFT)
       
        
        self.btnDel=tk.Button(self.frame5, text='Delete',  width=6,height=2, command=lambda: self.pressed_button_a('del'))
        self.btnDel.pack(side=tk.LEFT)
        self.btnDel.config(state=NORMAL)
        
        tk.Button(self.frame5, text=4, width=3,height=2,command=lambda: self.pressed_button(4)).pack(side=tk.LEFT)
        tk.Button(self.frame5, text=5,width=3,height=2, command=lambda: self.pressed_button(5)).pack(side=tk.LEFT)
        tk.Button(self.frame5, text=6, width=3,height=2,command=lambda: self.pressed_button(6)).pack(side=tk.LEFT)
        
       
        
        self.btnCancel=tk.Button(self.frame4, text='Cancel',width=6,height=2, command=lambda: self.pressed_button_a('cancel'))
        self.btnCancel.pack(side=tk.LEFT)
        self.btnCancel.config(state=NORMAL)
        
        self.btnKeyOn=tk.Button(self.frame4, text='Key On',width=6,height=2,command=lambda: self.pressed_button_a('on'))
        self.btnKeyOn.pack(side=tk.LEFT)
        self.btnKeyOn.config(state=NORMAL)
        
        
        self.btnVip=tk.Button(self.frame4, text='VIP',width=6,height=2,command=lambda: self.pressed_button_a('vip'))
        self.btnVip.pack(side=tk.LEFT)
        self.btnVip.config(state=NORMAL)
        
        self.btnNew=tk.Button(self.frame4, text='New',width=6,height=2,command=lambda: self.pressed_button_a('new'))
        self.btnNew.pack(side=tk.LEFT)
        self.btnNew.config(state=DISABLED)
        
        self.btnX=tk.Button(self.frame4, text='x',width=6,height=2,command=lambda: self.pressed_button(40))
        self.btnX.pack(side=tk.LEFT)
        self.btnX.config(state=NORMAL)
        
        tk.Button(self.frame4, text=7,width=3,height=2, command=lambda: self.pressed_button(7)).pack(side=tk.LEFT)
        tk.Button(self.frame4, text=8,width=3,height=2, command=lambda: self.pressed_button(8)).pack(side=tk.LEFT)
        tk.Button(self.frame4, text=9,width=3,height=2, command=lambda: self.pressed_button(9)).pack(side=tk.LEFT)
        
        
        
        '''
        setup update page
        '''
        
        self.updateLabel1 = tk.Label(self.page1, bg='grey93',text = 'Please input the Product ID if you want to update that Product :')
        self.updateLabel1.place(x=5,y=5)
        
        self.updateLabel2 = tk.Label(self.page1, bg='grey93',text = 'Product ID :')
        self.updateLabel2.place(x = 5,y = 55)
        self.updateEntry2 = tk.Entry(self.page1,width= 15)
        self.updateEntry2.place(x = 100, y = 55)
        
        self.updateSearch=tk.Button(self.page1, text='Search',command=lambda: self.showData())
        self.updateSearch.place(x = 250, y = 55)
        self.updateSearch.config(state=NORMAL)
        
        tk.Label(self.page1, bg='grey93',text = '-'*89).place(x = 5, y = 105)
        
        self.updateLabel3 = tk.Label(self.page1, bg='grey93',text = ' ')
        self.updateLabel3.place(x=5,y=155)
        
        self.updateLabel4 = tk.Label(self.page1, bg='grey93',text = 'Which item you what to alter?')
        self.updateLabel4.place(x = 350,y = 200)
        type = tk.StringVar()
        self.updateOption1= ttk.Combobox(self.page1, width=12, textvariable=type)
        self.updateOption1['values'] = ('product_name', 'product_brand', 'product_price', 'quantity', 'product_type', 'product_subtype') 
        self.updateOption1.grid(column=1, row=1)
        self.updateOption1.current(0)
        self.updateOption1.place(x = 350, y = 225)
        
        
        self.updateLabel6 = tk.Label(self.page1, bg='grey93',text = 'New data:')
        self.updateLabel6.place(x = 350,y = 265)
        self.updateEntry6 = tk.Entry(self.page1,width= 15)
        self.updateEntry6.place(x = 350, y = 290)
        
        self.updateSubmit=tk.Button(self.page1, text='submit', \
            command=lambda: self.alter())
        self.updateSubmit.place(x = 350, y=325)
        self.updateSubmit.config(state=NORMAL)
        
        self.updateLabel7= tk.Label(self.page1, bg='grey93',text = 'Status : Ready')
        self.updateLabel7.place(x = 350,y = 405)
        
        self.updateUnlock=tk.Button(self.page1, text='Unlock / Start',command=lambda: self.buttonState(2))
        self.updateUnlock.place(x = 5, y = 500)
        self.updateUnlock.config(state=DISABLED)
        
        self.updateEntry2.config(state=NORMAL)
        self.updateEntry6.config(state=NORMAL)
        self.updateOption1.config(state=NORMAL)
        '''
        setup add page
        '''
        
        self.addLabel0 = tk.Label(self.page2, bg='grey93',text = 'Please input with the following data to add Product.')
        self.addLabel0.place(x=5,y=5)

        
        self.addLabel2 = tk.Label(self.page2, bg='grey93',text = 'Product Name :')
        self.addLabel2.place(x = 5,y = 105)
        self.addEntry2 = tk.Entry(self.page2,width= 25)
        self.addEntry2.place(x = 115, y = 105)
        
        self.addLabel3 = tk.Label(self.page2, bg='grey93',text = 'Product Brand :')
        self.addLabel3.place(x = 5,y = 155)
        self.addEntry3 = tk.Entry(self.page2,width= 25)
        self.addEntry3.place(x = 115, y = 155)
        
        self.addLabel4 = tk.Label(self.page2, bg='grey93',text = 'Product Price :')
        self.addLabel4.place(x = 5,y = 205)
        self.addEntry4 = tk.Entry(self.page2,width= 25)
        self.addEntry4.place(x = 115, y = 205)
        
        self.addLabel5 = tk.Label(self.page2, bg='grey93',text = 'Quanitiy :')
        self.addLabel5.place(x = 5,y = 255)
        self.addEntry5 = tk.Entry(self.page2,width= 25)
        self.addEntry5.place(x = 115, y = 255)
        
        self.addLabel6 = tk.Label(self.page2, bg='grey93',text = 'Type :')
        self.addLabel6.place(x = 5,y = 305)
        
        
        self.addOption1= ttk.Combobox(self.page2, width=12, textvariable=type)
        self.addOption1['values'] = ('Food', 'Drink') 
        self.addOption1.grid(column=1, row=1)
        self.addOption1.current(0)
        self.addOption1.place(x = 115, y = 305)
        
       
        type2 = tk.StringVar()
        self.addLabel7 = tk.Label(self.page2, bg='grey93',text = 'Subtype :')
        self.addLabel7.place(x = 5,y = 355)
        self.addOption2= ttk.Combobox(self.page2, width=12, textvariable=type2)
        self.addOption2['values'] = ('Bread','Cup noodle','Ice cream', 'Frozen food', 'Snack','Tea','Carbonated drink','Other','Coffee','Juice','Beer'  ) 
        self.addOption2.grid(column=1, row=2)
        self.addOption2.current(0)
        self.addOption2.place(x = 115, y = 355)
            
        self.addSubmit=tk.Button(self.page2, text='submit', \
            command=lambda: self.adding())
        self.addSubmit.place(x = 20, y = 405)
        self.addSubmit.config(state=NORMAL)
        
        self.addLabel8= tk.Label(self.page2, bg='grey93',text = 'Status : Ready')
        self.addLabel8.place(x = 115,y = 405)
        
        self.addUnlock=tk.Button(self.page2, text='Unlock / Start',command=lambda: self.buttonState(2))
        self.addUnlock.place(x = 5, y = 500)
        self.addUnlock.config(state=DISABLED)
        
        self.addEntry2.config(state=NORMAL)
        self.addEntry3.config(state=NORMAL)
        self.addEntry4.config(state=NORMAL)
        self.addEntry5.config(state=NORMAL)
        self.addOption1.config(state=NORMAL)
        self.addOption2.config(state=NORMAL)
        '''
        setup delete page
        '''
        self.delLabel1 = tk.Label(self.page3, bg='grey93',text = 'Please input the Product ID if you want to delete that Product :')
        self.delLabel1.place(x=5,y=5)
        
        self.delLabel2 = tk.Label(self.page3, bg='grey93',text = 'Product ID :')
        self.delLabel2.place(x = 5,y = 55)
        self.delEntry2 = tk.Entry(self.page3,width= 15)
        self.delEntry2.place(x = 100, y = 55)
        
        self.delLabel3 = tk.Label(self.page3, bg='grey93',text = ' ')
        self.delLabel3.place(x=5,y=155)
        
        self.delSearch=tk.Button(self.page3, text='Search', \
            command=lambda: self.deleteShowData())
        self.delSearch.place(x = 250, y = 55)
        self.delSearch.config(state=NORMAL)
        
        
        self.delDel=tk.Button(self.page3, text='Delete', \
            command=lambda: self.delete())
        self.delDel.place(x = 20, y=405)
        self.delDel.config(state=NORMAL)   
        
        self.delLabel7= tk.Label(self.page3, bg='grey93',text = 'Status : Ready')
        self.delLabel7.place(x = 115,y = 405)
        
        self.delUnlock=tk.Button(self.page3, text='Unlock / Start',command=lambda: self.buttonState(2))
        self.delUnlock.place(x = 5, y = 500)
        self.delUnlock.config(state=DISABLED)
        
        
        self.delEntry2.config(state=NORMAL)
        
        
        '''
        setup cash in machine page
        '''
        
        self.cashLabel1 = tk.Label(self.page4, bg='grey93',text = 'Please input the total value of cash initially:')
        self.cashLabel1.place(x=5,y=5)
        
       
        self.cashEntry = tk.Entry(self.page4,width= 15)
        self.cashEntry.place(x = 5, y = 50)
        self.cashEntry.config(state=NORMAL)
        
        self.cashConfirm1=tk.Button(self.page4, text='Confirm', \
            command=lambda: self.cashInMachine(1) )
        self.cashConfirm1.place(x = 155, y=50)
        self.cashConfirm1.config(state=NORMAL)
        
        self.cashChange1=tk.Button(self.page4, text='Change', \
            command=lambda: self.cashInMachineChange(1))
        self.cashChange1.place(x = 220, y=50)
        self.cashChange1.config(state=DISABLED)
            
            
        self.cashLabel2 = tk.Label(self.page4, bg='grey93',text = 'Please input the total value of cash finally:')
        self.cashLabel2.place(x=5,y=100)
        
       
        self.cashEntry2 = tk.Entry(self.page4,width= 15)
        self.cashEntry2.place(x = 5, y = 150)
        
        
        
        self.cashConfirm2=tk.Button(self.page4, text='Confirm', \
            command=lambda: self.cashInMachine(2))
        self.cashConfirm2.place(x = 155, y=150)
        self.cashConfirm2.config(state=NORMAL)
        
        self.cashChange2=tk.Button(self.page4, text='Change', \
            command=lambda: self.cashInMachineChange(2))
        self.cashChange2.place(x = 220, y=150)
        self.cashChange2.config(state=DISABLED)
        
        self.cashUnlock=tk.Button(self.page4, text='Unlock / Start',command=lambda: self.buttonState(2))
        self.cashUnlock.place(x = 5, y = 500)
        self.cashUnlock.config(state=DISABLED)
        
        self.cashLabel3= tk.Label(self.page4, bg='grey93',text='')
        self.cashLabel3.place(x = 5, y = 300)
        
        self.cashEntry.config(state=NORMAL)
        self.cashEntry2.config(state=NORMAL)
        
        '''
        setup report and reset
        '''
        tk.Label(self.page5, bg='grey93',text='Print Z report:').place(x = 5, y=5)
        tk.Button(self.page5,text='Z report',command=lambda: self.Z()).place(x = 5, y=50)
        
        tk.Label(self.page5, bg='grey93',text='Create bar chart to show how many product have been sold today:').place(x = 5, y=100)
        tk.Button(self.page5,text='Bar chart',command=lambda: self.barChart()).place(x = 5, y=150)
        
        tk.Label(self.page5, bg='grey93',text='Reset the whole system:').place(x = 5, y=200)
        self.btnReset=tk.Button(self.page5,text='Reset',command=lambda: self.buttonStateChange())
        self.btnReset.place(x = 5, y=250)
        self.btnResetConfirm=tk.Button(self.page5,text='Confirm',command=lambda: self.reset())
        self.btnResetConfirm.place(x = 60, y=250)
        self.btnResetConfirm.config(state=DISABLED)
        
        
        '''
        setup help page
        '''
        self.editArea3 = tkst.ScrolledText(self.page6,height=5)
        self.editArea3.pack( expand=1,fill="both") 
        self.editArea3.insert(tk.INSERT, 'comming soon...')
        self.editArea3.config(state="disabled")
        
        
        '''
        pack self.nb
        '''
        
        self.nb.pack(expand=1, fill="both")
        
        
        
    def pressed_button(self,number):
        if len(self.list)>100:
            self.list=self.list[:99]
        if number in range(0,10)  :
            self.list.append(str(number))
            
        elif number ==11:
            self.list.append('.')
            self.dot=True
            
        elif number == 20 and not (len(self.list) == 0):
            var=len(self.list)
            self.list.pop(var-1)
        elif number ==40:
            self.list.append('x')
            self.xFlag=True
        if '.' not in self.list:
            self.dot= False  
             
        if self.dot == True:
            self.btnDot.config(state=DISABLED)
        else:
            self.btnDot.config(state=NORMAL)
            
        if 'x' not in self.list:
            self.xFlag= False  
            
       
        if self.xFlag == True:
            self.btnX.config(state=DISABLED)
            self.btnDot.config(state=DISABLED)
        else:
            self.btnX.config(state=NORMAL)
            self.btnDot.config(state=NORMAL)
        
        
        self.label.config(text=self.list)
        
        
    def pressed_button_a(self, value):
        if value == 'pay':
            self.pay()
            
        elif value =='add':
            self.addProduct()
            
        elif value == 'del':
            self.delProduct()
        
        elif value == 'receive':
            self.receive()
        
        elif value == 'new':
            self.new()
            
      
        
        elif value == 'vip':
            self.vip()
            
    
        elif value == 'cancel':
            self.cancel()
            
        elif value == 'confirm':
        
            self.new()
            
        elif value == 'discount':
            self.discount()
            
        elif value == 'on':
            self.buttonState(1)
            
        elif value == 'off':
            self.buttonState(2)
     
            
        self.label.config(text=self.list)
    
    
    def buttonState(self,number):
        if number == 1:
            self.root.bind('1', lambda event: self.pressed_button(1))
            self.root.bind('2', lambda event: self.pressed_button(2))
            self.root.bind('3', lambda event: self.pressed_button(3))
            self.root.bind('4', lambda event: self.pressed_button(4))
            self.root.bind('5', lambda event: self.pressed_button(5))
            self.root.bind('6', lambda event: self.pressed_button(6))
            self.root.bind('7', lambda event: self.pressed_button(7))
            self.root.bind('8', lambda event: self.pressed_button(8))
            self.root.bind('9', lambda event: self.pressed_button(9))
            self.root.bind('0', lambda event: self.pressed_button(0))
            self.root.bind('.', lambda event: self.pressed_button(11))
            self.root.bind('<BackSpace>', lambda event: self.pressed_button(20))
            self.root.bind('<x>', lambda event: self.pressed_button(40))
            
            self.btnKeyOn.config(state=DISABLED)
            self.btnKeyOff.config(state=NORMAL)
            
            self.updateEntry2.config(state=DISABLED)
            self.updateEntry6.config(state=DISABLED)
            self.updateOption1.config(state=DISABLED)
            self.updateSearch.config(state=DISABLED)
            self.updateSubmit.config(state=DISABLED)
            
            self.addEntry2.config(state=DISABLED)
            self.addEntry3.config(state=DISABLED)
            self.addEntry4.config(state=DISABLED)
            self.addEntry5.config(state=DISABLED)
            self.addOption1.config(state=DISABLED)
            self.addOption2.config(state=DISABLED)
            self.addSubmit.config(state=DISABLED)
            
            self.delEntry2.config(state=DISABLED)
            self.delSearch.config(state=DISABLED)
            self.delDel.config(state=DISABLED)
            
            self.cashEntry.config(state=DISABLED)
            self.cashEntry2.config(state=DISABLED)
            
            self.cashUnlock.config(state=NORMAL)
            self.updateUnlock.config(state=NORMAL)
            self.addUnlock.config(state=NORMAL)
            self.delUnlock.config(state=NORMAL)
            
        elif number == 2:
            self.root.unbind('1')
            self.root.unbind('2')
            self.root.unbind('3')
            self.root.unbind('4')
            self.root.unbind('5')
            self.root.unbind('6')
            self.root.unbind('7')
            self.root.unbind('8')
            self.root.unbind('9')
            self.root.unbind('0')
            self.root.unbind('.')
            self.root.unbind('<BackSpace>')
            
            self.btnKeyOff.config(state=DISABLED)
            self.btnKeyOn.config(state=NORMAL)
            
            self.updateEntry2.config(state=NORMAL)
            self.updateEntry6.config(state=NORMAL)
            self.updateOption1.config(state=NORMAL)
            self.updateSubmit.config(state=NORMAL)
            self.updateSearch.config(state=NORMAL)
            
            self.addEntry2.config(state=NORMAL)
            self.addEntry3.config(state=NORMAL)
            self.addEntry4.config(state=NORMAL)
            self.addEntry5.config(state=NORMAL)
            self.addOption1.config(state=NORMAL)
            self.addOption2.config(state=NORMAL)
            self.addSubmit.config(state=NORMAL)
            
            self.delEntry2.config(state=NORMAL)
            self.delSearch.config(state=NORMAL)
            self.delDel.config(state=NORMAL)
            
            self.cashEntry.config(state=NORMAL)
            self.cashEntry2.config(state=NORMAL)
            
            self.cashUnlock.config(state=DISABLED)
            self.updateUnlock.config(state=DISABLED)
            self.addUnlock.config(state=DISABLED)
            self.delUnlock.config(state=DISABLED)
            
            
            
        
    def addProduct(self):
        try:
            self.add=True
            pss=False
        
            xLocation=len(self.list)
            xFlag=False
            loop=1
        
            x=0 
            while x < len(self.list) and xFlag==False:
                if self.list[x]=='x':
                    xLocation=x
                    xFlag=True
                x+=1
        
            str1=''.join(self.list[:xLocation])
        
            if xFlag ==True:
                i=''.join(self.list[xLocation+1:])
                loop=int(i)
            
        
            i=0
            while i< loop:
                str_qt='SELECT quantity FROM Product WHERE product_id ='
                self.cursor.execute(str_qt + str1 )
        
                quantity=[]
                quantity=self.cursor.fetchone()
                #print(quantity)
        
                if int(quantity[0]) <1:
                    self.editArea2.config(state="normal")
                    self.editArea2.delete(1.0, tk.END) 
                    self.editArea2.insert(tk.INSERT ,'error: no inventory id '+str1)
                    self.editArea2.insert(tk.INSERT ,'\n')
                    self.editArea2.config(state="disabled")
                    pss=True
            
            
                if pss == False:
                    str2= 'SELECT product_id, product_name, product_brand , product_price FROM Product WHERE product_id ='
        
                    self.cursor.execute(str2 + str1 )
                    data = self.cursor.fetchone()
                    #print(data)
                    self.editArea.config(state="normal")
                    self.editArea.insert(tk.INSERT ,data)
                    self.editArea.insert(tk.INSERT ,'\n')
                    self.editArea.config(state="disabled")
                    self.list=[]
            
                    self.productList.append(data)
            
                    self.basket.append(str1)
                    #print(self.basket)
        
                    str3='SELECT product_price FROM Product WHERE product_id ='
                    self.cursor.execute(str3 + str1 )
                    value=[]
                    value=self.cursor.fetchone()
                    self.total+=value[0]
                    #print(self.total)
        
        
        
                    quantity_n=int(quantity[0])-1
                    str_qt_n_1= 'UPDATE Product SET quantity = '
                    str_qt_n_2= ' WHERE product_id ='
                    self.cursor.execute(str_qt_n_1 +str(quantity_n)+ str_qt_n_2+ str1 )
                    self.db.commit()
            
            
                    self.addData.append(str1)
                else:
                    self.list=[]
                i+=1
        except TypeError as error:
            self.editArea2.config(state="normal")
            self.editArea2.insert(tk.INSERT ,'Invalid data input')
            self.editArea2.insert(tk.INSERT ,'\n')
            self.editArea2.config(state="disabled")
        
    def delProduct(self):
        self.dele=True
        
        
        xLocation=len(self.list)
        xFlag=False
        loop=1
        
        x=0 
        while x < len(self.list) and xFlag==False:
            if self.list[x]=='x':
                xLocation=x
                xFlag=True
            x+=1
        
        str1=''.join(self.list[:xLocation])
        
        if xFlag ==True:
            i=''.join(self.list[xLocation+1:])
            loop=int(i)
        
        
        i=0
        while i< loop:
            if str1 in self.basket:
        
                str2= 'SELECT product_id, product_name, product_brand , product_price FROM Product WHERE product_id ='
        
                self.cursor.execute(str2 + str1 )
                data = self.cursor.fetchone()
        
                self.editArea.config(state="normal")
                self.editArea.insert(tk.INSERT ,'del:')
                self.editArea.insert(tk.INSERT ,data)
                self.editArea.insert(tk.INSERT ,'\n')
                self.editArea.config(state="disabled")
        
                self.list=[]
        
                str3='SELECT product_price FROM Product WHERE product_id ='
                self.cursor.execute(str3 + str1 )
                value=[]
                value=self.cursor.fetchone()
                self.total-=value[0]
            
                str_qt='SELECT quantity FROM Product WHERE product_id ='
                self.cursor.execute(str_qt + str1 )
        
                quantity=[]
                quantity=self.cursor.fetchone()
            
                quantity_n=int(quantity[0])+1
                str_qt_n_1= 'UPDATE Product SET quantity = '
                str_qt_n_2= ' WHERE product_id ='
                self.cursor.execute(str_qt_n_1 +str(quantity_n)+ str_qt_n_2+ str1 )
                self.db.commit()
            
                self.basket.remove(str1)
                self.delData.append(str1)
                self.productList.remove(data)
            
            else:
                self.editArea2.config(state="normal")
                self.editArea2.delete(1.0, tk.END) 
                self.editArea2.insert(tk.INSERT ,'error: no product in basket id '+str1)
                self.editArea2.insert(tk.INSERT ,'\n')
                self.editArea2.config(state="disabled")
                self.list=[]
                    
            i+=1

        
    def vip(self):
        try:
            self.vipId=0
        
            str1=''.join(self.list)
            self.list=[]
        
            str_qt='SELECT customer_id FROM customer WHERE telephone_no ='
            self.cursor.execute(str_qt + str1 )
            self.vipId = (self.cursor.fetchone())[0]
        
        
            self.editArea.config(state="normal")
            self.editArea.insert(tk.INSERT ,'Membership add') 
            self.editArea.insert(tk.INSERT ,'\n')
            self.editArea.config(state="disabled")
        
            self.vipFlag=True
        
            self.vipPoints=0
            str_qt2='SELECT collecting_points FROM customer WHERE customer_id ='
            self.cursor.execute(str_qt2 + str(self.vipId ))
            self.vipPoints= (self.cursor.fetchone())[0]
        
            if self.vipPoints >= 200:
                self.btnDiscount.config(state=NORMAL)
            
        except pymysql.err.ProgrammingError as error:
            self.editArea2.config(state="normal")
            self.editArea2.insert(tk.INSERT ,'Invalid membership telephone number') 
            self.editArea2.insert(tk.INSERT ,'\n')
            self.editArea2.config(state="disabled")
        except TypeError as error:
            self.editArea2.config(state="normal")
            self.editArea2.insert(tk.INSERT ,'Invalid membership telephone number') 
            self.editArea2.insert(tk.INSERT ,'\n')
            self.editArea2.config(state="disabled")
        
    def discount(self):
        
        
        self.editArea.config(state="normal")
        self.editArea.insert(tk.INSERT ,'Discount: ')
        self.editArea.insert(tk.INSERT ,'5.00')
        self.editArea.insert(tk.INSERT ,'\n')
        self.editArea.config(state="disabled")
        
        self.btnCancel.config(state=DISABLED)
        self.btnDiscount.config(state=DISABLED)
        self.total-=5
        
        
        str_qt_n_1= 'UPDATE customer SET collecting_points = '
        str_qt_n_2= ' WHERE customer_id ='
        self.cursor.execute(str_qt_n_1 +str(self.vipPoints-200)+ str_qt_n_2+ str(self.vipId ))
        self.db.commit()
        
    def pay(self):
        self.btnCancel.config(state=DISABLED)
        if self.total >=0 :
            self.btnPay.config(state=DISABLED)
            self.btnAdd.config(state=DISABLED)
            self.btnX.config(state=DISABLED)
            self.btnDel.config(state=DISABLED)
            self.btnVip.config(state=DISABLED)
        
            if self.paySign == False:
                self.editArea.config(state="normal")
                self.editArea.insert(tk.INSERT ,'\n')
                self.editArea.insert(tk.INSERT ,'please pay:')
                self.editArea.insert(tk.INSERT ,str(round(float(self.total),2)))
                self.editArea.insert(tk.INSERT ,'\n')
                self.editArea.config(state="disabled")
        
        
                self.editArea2.config(state="normal")
                self.editArea2.insert(tk.INSERT ,'Input customer pay') 
                self.editArea2.insert(tk.INSERT ,'\n')
                self.editArea2.config(state="disabled")
        
            self.btnReceive.config(state=NORMAL)
            self.list=[]
        else: 
            self.new()
            
    def receive(self):   
        self.btnReceive.config(state=DISABLED)
        
        self.customerPay=''.join(self.list)
        self.list=[]
        
        if (float(self.customerPay) - self.total) <0 :
            self.editArea2.config(state="normal")
            self.editArea2.insert(tk.INSERT ,'Customer pay not enough') 
            self.editArea2.insert(tk.INSERT ,'\n')
            self.editArea2.config(state="disabled")
            self.paySign=True
            self.pay()
        else:
            self.editArea2.config(state="normal")
            self.editArea2.delete(1.0, tk.END) 
            self.editArea2.config(state="disabled")
        
            self.editArea.config(state="normal")
            self.editArea.insert(tk.INSERT ,'\n')
            self.editArea.insert(tk.INSERT ,'Customer pay:')
            self.editArea.insert(tk.INSERT ,self.customerPay)
            self.editArea.insert(tk.INSERT ,'\n')
        
            self.editArea.insert(tk.INSERT ,'\n')
            self.editArea.insert(tk.INSERT ,'Change:')
            self.editArea.insert(tk.INSERT ,str(round(float(self.customerPay) - self.total,2)))
            self.editArea.insert(tk.INSERT ,'\n')
        
            self.editArea.insert(tk.INSERT ,'\n')
            self.editArea.insert(tk.INSERT ,'\n')
            self.editArea.insert(tk.INSERT ,'Payment success')
            self.editArea.insert(tk.INSERT ,'\n')
            
            if self.vipFlag == True:
                points=0
                str_qt='SELECT collecting_points FROM customer WHERE customer_id = '
                self.cursor.execute(str_qt +str(self.vipId)  )
                points=((self.cursor.fetchone())[0])+int(self.total)
                
                str_qt_n_1= 'UPDATE customer SET collecting_points = '
                str_qt_n_2= ' WHERE customer_id ='
                self.cursor.execute(str_qt_n_1 +str(points)+ str_qt_n_2+ str(self.vipId ))
                self.db.commit()
                
            self.editArea.config(state="disabled")
            
            self.paySign=False
            
            self.btnNew.config(state=NORMAL)
            
            date_string=datetime.datetime.now()
        
            
            file_full=(str(date_string))+'.txt'
    
            fileIn = open(file_full, 'w')
            
    
    
            fileIn.write('mkyStore OFFICAL RECEIPT:')
            
            fileIn.write('\n')
            fileIn.write(str(date_string.strftime('%Y/%m/%d %H:%M:%S')))
            fileIn.write('\n')
            fileIn.write(str(self.staffId)+'\n')
            fileIn.write('---------------------------------------------------------------------------------------------------------------')   
            fileIn.write('\n')
            i=0
            while i < len(self.productList):
                fileIn.write(str(self.productList[i]))
                fileIn.write('\n')
                i+=1
            fileIn.write('\n')
            fileIn.write('\n')
            fileIn.write('total: '+str(round(self.total,2)))
            fileIn.write('\n')
            
            fileIn.write('Customer pay: '+self.customerPay)
            fileIn.write('\n')
           
           
            fileIn.write('Change: '+  str(round(float(self.customerPay) - self.total,2)))
            fileIn.write('\n')
            
            if self.vipFlag == True:
                vp=0
                str_qt2='SELECT collecting_points FROM customer WHERE customer_id ='
                self.cursor.execute(str_qt2 + str(self.vipId ))
                vp= (self.cursor.fetchone())[0]
            
                fileIn.write('\n')
                fileIn.write('Membership no.'+str(self.vipId ))
                fileIn.write('\n')
                fileIn.write('Original points: '+str(self.vipPoints))
                fileIn.write('\n')
                fileIn.write('Updated points: '+str(vp))
                fileIn.write('\n')
            fileIn.close()
            
            
            fileIn=open('z_datasource.txt','a')
            x=0
            while x <len(self.productList):
                fileIn.write(str(self.productList[x]))
                fileIn.write('\n')
                x+=1
            fileIn.close()
            
            
            
    def new(self):
        self.editArea.config(state="normal")
        self.editArea.delete(1.0, tk.END) 
        self.editArea.config(state="disabled")
        
        self.editArea2.config(state="normal")
        self.editArea2.delete(1.0, tk.END) 
        self.editArea2.config(state="disabled")
        
        self.total=0
        self.list=[]
        self.basket=[]
        self.vipFlag=False
        self.vipId=0
        self.paySign=False
        self.add=False
        self.dele=False
        self.addData=[]
        self.delData=[]
        self.vipPoints=0
        self.qtyId=0
        self.qtyFlag=False
        self.priceId=0
        self.priceFlag=False
        self.productList=[]
        self.customerPay=''
        self.xFlag=False
        
        self.btnNew.config(state=DISABLED)
        self.btnPay.config(state=NORMAL)
        self.btnDel.config(state=NORMAL)
        self.btnAdd.config(state=NORMAL)
        self.btn_confirm.config(state=DISABLED)
        self.btnCancel.config(state=NORMAL)
        self.btnX.config(state=NORMAL)
        self.cursor = self.db.cursor()
    
   
        
    def cancel(self):
        
        
        
        if self.add ==True:
            i=0
            while i < len(self.addData):
                str_qt='SELECT quantity FROM Product WHERE product_id ='
                self.cursor.execute(str_qt + self.addData[i] )
        
                quantity=[]
                quantity=self.cursor.fetchone()
                
                quantity_n=0
                quantity_n=int(quantity[0])+1
                str_qt_n_1= 'UPDATE Product SET quantity = '
                str_qt_n_2= ' WHERE product_id ='
                self.cursor.execute(str_qt_n_1 +str(quantity_n)+ str_qt_n_2+ self.addData[i] )
                self.db.commit()
                i+=1
            
            
        
        if self.dele ==True:
            i=0
            while i < len(self.delData):
                str_qt='SELECT quantity FROM Product WHERE product_id ='
                self.cursor.execute(str_qt + self.delData[i] )
        
                quantity=[]
                quantity=self.cursor.fetchone()
                
                quantity_n=0
                quantity_n=int(quantity[0])-1
                str_qt_n_1= 'UPDATE Product SET quantity = '
                str_qt_n_2= ' WHERE product_id ='
                self.cursor.execute(str_qt_n_1 +str(quantity_n)+ str_qt_n_2+ self.delData[i] )
                self.db.commit()
                i+=1
                
        self.editArea2.config(state="normal")
        self.editArea2.delete(1.0, tk.END) 
        self.editArea2.insert(tk.INSERT ,'Cancel sucess')
        self.editArea2.insert(tk.INSERT ,'\n')
        self.editArea2.config(state="disabled")
        self.new()
    
    

    '''
    Z report
    '''
    def Z(self):
        fileImport=open('Z_datasource.txt','r')
        line= fileImport.readline()
        self.wholeDayProductList2=[]
        DT=['productID','productName','productBrand','productPrice']
        
        while line != '':
            productRec=line.split(',')
            length=len(productRec[3])
            
            self.wholeDayProductList.append(dict(zip(DT,[int(productRec[0][1:]),productRec[1],productRec[2],float(productRec[3][:(length-2)]) ])))
            self.wholeDayProductList2.append(productRec[0][1:]+' '+productRec[1]+' '+productRec[2]+' '+productRec[3][:(length-2)])
            line= fileImport.readline()
            
        
            
        all_product=[]
        self.cursor.execute('SELECT product_id FROM Product')
        row = self.cursor.fetchone()
        while row is not None:
            
            length2=len(str(row))
            
            all_product.append(int(str(row)[1:(length2-2)]))
            row = self.cursor.fetchone()
            
        #print(all_product) 
        #print(self.wholeDayProductList2)
        insertionsort.main(self.wholeDayProductList2)
        #print(self.wholeDayProductList2)
        date_string=datetime.datetime.now()
        
        
        
        file_full='Z report '+str(date_string)+'.txt'
    
        fileIn = open(file_full, 'w')
            
    
    
        fileIn.write('mkyStore Z report:')
            
        fileIn.write('\n')
        fileIn.write('Created '+str(date_string.strftime('%Y/%m/%d %H:%M:%S')))
        fileIn.write('\n')
        fileIn.write('\n')
        fileIn.write(str(self.staffId)+'\n')
        fileIn.write('\n')
        fileIn.write('---------------------------------------------------------------------------------------------------------------')  
       
        x=0
        pSalesTotal=0
        while x < len(self.wholeDayProductList):
          
            pSalesTotal+=float(self.wholeDayProductList[x]['productPrice'])
            x+=1
      
       
        fileIn.write('\n')   
        fileIn.write('Total sales on this day:'+str(round(pSalesTotal,2)))
        fileIn.write('\n')   
        
        fileImport2 = open('cashInMachineInitial.txt', 'r')
        
        cashInitial=fileImport2.readline()
        
        fileIn.write('\n')   
        fileIn.write('Cash in machine initially:'+str(cashInitial))
        fileIn.write('\n')   
        
        fileImport2.close
        
        fileImport3 = open('cashInMachineNow.txt', 'r')
        
        cashFinal=fileImport3.readline()
        
        fileIn.write('Cash in machine finally:'+str(cashFinal))
        fileIn.write('\n')   
        
        fileImport3.close
        
        fileIn.write('Difference: ')   
        fileIn.write(str(round(float(cashInitial)-float(cashFinal)-pSalesTotal,2)))
        
        fileIn.write('\n') 
        fileIn.write('---------------------------------------------------------------------------------------------------------------')  
        fileIn.write('\n') 
        fileIn.write('pID, productName, sold')
        fileIn.write('\n')
          
        i=0
        x=0
        
        while i< len(all_product):
            number_v=0
            for e in self.wholeDayProductList:
                e['productID']
                if all_product[i] == e['productID']:
                    number_v+=1
            if number_v!=0:
                
                
                
                fileIn.write(str(all_product[i]))
                
                str_qt='SELECT product_name FROM Product WHERE product_id ='
                self.cursor.execute(str_qt + str(all_product[i]) )
                
                pname=str(self.cursor.fetchone())
                pname_length=len(pname)
                
                fileIn.write('  '+pname[1:pname_length-2]+'  ')
                                         
                fileIn.write (str(number_v))
                
                
              
                fileIn.write('\n')
            i+=1
            
            x=0
       
        fileIn.write('\n') 
        fileIn.write('---------------------------------------------------------------------------------------------------------------')  
        fileIn.write('\n') 
        fileIn.write('pID, productName, brand, price')
        fileIn.write('\n') 
        
        while x < len(self.wholeDayProductList2):
            fileIn.write(self.wholeDayProductList2[x])
            fileIn.write('\n')
            x+=1
        fileIn.close() 
    
    
    
    
    
    '''
    functions of update data
    '''
        
    def showData(self):
        
        found=False
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * from product where 1')
            
            for e in cursor.fetchall():
            
                if str(e['product_id'])==self.updateEntry2.get():
                    found=True
                    self.updateLabel3.config(text="ID:"+str(e['product_id'])+'\r\n'+
                                        "Name:"+e['product_name']+'\r\n'+
                                        "Brand:"+e['product_brand']+'\r\n'+
                                        "Price:"+str(e['product_price'])+'\r\n'+
                                        "Quantity:"+str(e['quantity'])+'\r\n'+
                                        "Type:"+e['product_type']+'\r\n')
                   
                    
            if not found:
                self.updateLabel3.config(text="Not Found!")
    
    
    def alter(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                if self.updateOption1.get() != 'product_price' or self.updateOption1.get() != 'quantity':
                    with self.connection.cursor() as cursor:
                        cursor.execute("UPDATE product SET %s= '%s' where product.product_id=%d "%(self.updateOption1.get(),self.updateEntry6.get(),int(self.updateEntry2.get())))
                        self.connection.commit()
                        self.updateLabel7.config(text='Status : Success')
                
                        cursor.execute('SELECT * from product where 1')
                        for e in cursor.fetchall():
                            if str(e['product_id'])==self.updateEntry2.get():
                                self.updateLabel3.config(text="ID:"+str(e['product_id'])+'\r\n'+
                                        "Name:"+e['product_name']+'\r\n'+
                                        "Brand:"+e['product_brand']+'\r\n'+
                                        "Price:"+str(e['product_price'])+'\r\n'+
                                        "Quantity:"+str(e['quantity'])+'\r\n'+
                                        "Type:"+e['product_type']+'\r\n'+
                                        "Subtype:"+e['product_subtype']+'\r\n')
        
                elif self.updateOption1.get()== 'product_price':
                    with self.connection.cursor() as cursor:
                        cursor.execute("UPDATE product SET '%s'= %f where product.product_id=%d "%(self.updateOption1.get(),float(self.updateEntry6.get()),int(self.updateEntry2.get())))
                        self.connection.commit()
                        self.updateLabel7.config(text='Status : Success') 
                
                        cursor.execute('SELECT * from product where 1')
                        for e in cursor.fetchall():
                            if str(e['product_id'])==self.updateEntry2.get():
                                self.updateLabel3.config(text="ID:"+str(e['product_id'])+'\r\n'+
                                        "Name:"+e['product_name']+'\r\n'+
                                        "Brand:"+e['product_brand']+'\r\n'+
                                        "Price:"+str(e['product_price'])+'\r\n'+
                                        "Quantity:"+str(e['quantity'])+'\r\n'+
                                        "Type:"+e['product_type']+'\r\n'+
                                        "Subtype:"+e['product_subtype']+'\r\n')

                elif self.updateOption1.get()== 'quantity':
                    with self.connection.cursor() as cursor:
                        cursor.execute("UPDATE product SET '%s'= %d where product.product_id=%d "%(self.updateOption1.get(),int(self.updateEntry6.get()),int(self.updateEntry2.get())))
                        self.connection.commit()
                        self.updateLabel7.config(text='Status : Success')  
                
                        cursor.execute('SELECT * from product where 1')
                        for e in cursor.fetchall():
                            if str(e['product_id'])==self.updateEntry2.get():
                                self.updateLabel3.config(text="ID:"+str(e['product_id'])+'\r\n'+
                                        "Name:"+e['product_name']+'\r\n'+
                                        "Brand:"+e['product_brand']+'\r\n'+
                                        "Price:"+str(e['product_price'])+'\r\n'+
                                        "Quantity:"+str(e['quantity'])+'\r\n'+
                                        "Type:"+e['product_type']+'\r\n'+
                                        "Subtype:"+e['product_subtype']+'\r\n') 
            
            except Exception:
                self.updateLabel7.config(text='Status :ERROR Data')
    
    
    
    '''
    functions of add data
    ''' 
                
    def adding(self):
        try:
            if float(self.addEntry4.get()) <0 or int(self.addEntry5.get()) <0:
                raise ValueError
            with self.connection.cursor() as cursor:
                cursor.execute('''INSERT INTO product VALUES(%d,'%s','%s',%f,%d,'%s',"%s"'''%(int(0),self.addEntry2.get(),self.addEntry3.get(),float(self.addEntry4.get()),int(self.addEntry5.get()),self.addOption1.get(),self.addOption2.get())+')')
                self.connection.commit()
                self.addLabel8.config(text='Status : Success')
                
        except Exception as error:
            #print(error)
            self.addLabel8.config(text='Status :ERROR Data')
        except ValueError as error:
            self.addLabel8.config(text='Status :ERROR Data')
    
    '''
    functions of delete data
    '''
    
    def deleteShowData(self):
        found=False
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * from product where 1')
            for e in cursor.fetchall():
                if str(e['product_id'])==self.delEntry2.get():
                    found=True
                    self.delLabel3.config(text="ID:"+str(e['product_id'])+'\r\n'+
                                        "Name:"+e['product_name']+'\r\n'+
                                        "Brand:"+e['product_brand']+'\r\n'+
                                        "Price:"+str(e['product_price'])+'\r\n'+
                                        "Quantity:"+str(e['quantity'])+'\r\n'+
                                        "Type:"+e['product_type']+'\r\n'+
                                        "Subtype:"+e['product_subtype']+'\r\n')
                   
                    
            if not found:
                self.delLabel3.config(text="Not Found!")
    
    
    def delete(self):
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute("DELETE FROM product WHERE product.product_id ='%s'"%(int(self.delEntry2.get())))
                    self.connection.commit()
                    self.delLabel7.config(text='Status : Success')

            except Exception:
                self.delLabel7.config(text='Status :ERROR Data')
                
                
    '''
    functions of cash in machine
    '''
    
    def cashInMachine(self,number):
        try:
            if number == 1:
                if float(self.cashEntry.get()) <0:
                    raise ValueError
                
                fileIn = open('cashInMachineInitial.txt', 'w')

                fileIn.write(str(float(self.cashEntry.get())))
                fileIn.write('\n')
                fileIn.close()
            
                self.cashConfirm1.config(state=DISABLED)
                self.cashChange1.config(state=NORMAL)
            elif number == 2:
                if float(self.cashEntry2.get()) <0:
                    raise ValueError
                fileIn = open('cashInMachineNow.txt', 'w')

                fileIn.write(str(float(self.cashEntry2.get())))
                fileIn.write('\n')
                fileIn.close()
                self.cashConfirm2.config(state=DISABLED)
                self.cashChange2.config(state=NORMAL)
            self.cashLabel3.config(text='Success')
        except ValueError as error:
            
            self.cashLabel3.config(text='ERROR data')
    
    def cashInMachineChange(self,number):
        if number == 1:
            self.cashConfirm1.config(state=NORMAL)
            self.cashChange1.config(state=DISABLED)
        elif number == 2:
            self.cashConfirm2.config(state=NORMAL)
            self.cashChange2.config(state=DISABLED)
        
    '''
    reset data of sold product and cash in machine
    '''
    def buttonStateChange(self):
        self.btnResetConfirm.config(state=NORMAL)
        
    def reset(self):
        fileIn = open('cashInMachineInitial.txt', 'w')

        fileIn.write('0')
        fileIn.write('\n')
        fileIn.close()
        
        fileIn2 = open('cashInMachineNow.txt', 'w')

        fileIn2.write('0')
        fileIn2.write('\n')
        fileIn2.close()
        
        fileIn3 = open('z_datasource.txt', 'w')

        fileIn3.write('')
        
        fileIn3.close()
        self.btnResetConfirm.config(state=DISABLED)
        
        
    '''
    bar chart
    '''
    def barChart(self):
        
        i=0
        x=0
        
        data=[]
        datavalue=[]
        
        all_product=[]
        
        
        fileImport=open('Z_datasource.txt','r')
        line= fileImport.readline()
        self.wholeDayProductList2=[]
        DT=['productID','productName','productBrand','productPrice']
        
        while line != '':
            productRec=line.split(',')
            length=len(productRec[3])
            
            self.wholeDayProductList.append(dict(zip(DT,[int(productRec[0][1:]),productRec[1],productRec[2],float(productRec[3][:(length-2)]) ])))
          
            line= fileImport.readline()
            
        all_product=[]
        self.cursor.execute('SELECT product_id FROM Product')
        row = self.cursor.fetchone()
        while row is not None:
            
            length2=len(str(row))
            
            all_product.append(int(str(row)[1:(length2-2)]))
            row = self.cursor.fetchone()
        
        while i< len(all_product):
            number_v=0
            
            for e in self.wholeDayProductList:
                e['productID']
                if all_product[i] == e['productID']:
                    number_v+=1
            if number_v!=0:
                
                
                str_qt='SELECT product_name FROM Product WHERE product_id ='
                self.cursor.execute(str_qt + str(all_product[i]) )
                
                pname=str(self.cursor.fetchone())
                pname_length=len(pname)
                
                data.append(str(all_product[i])+'  '+pname[1:pname_length-2]+'  ')
                datavalue.append(number_v)        
                
           
            i+=1
        print(data)
        print(datavalue)
        
        x = np.arange(len(datavalue))
        
        
        
        
        plt.bar(x, datavalue)
        plt.xticks(x, data)
        plt.show()
      
        
    '''
    logout
    '''
    def logout(self):
        self.btnLogoutCancel.config(state=NORMAL)
        self.btnLogoutConfirm.config(state=NORMAL)
        self.btnLogout.config(state=DISABLED)
        
    def logoutCancel(self):  
        self.btnLogoutCancel.config(state=DISABLED)
        self.btnLogoutConfirm.config(state=DISABLED)
        self.btnLogout.config(state=NORMAL)
    
    def logoutConfirm(self):
        staff_logon_loop.main(self.root)
    
def main(id, window):
    root = tk.Tk()
    Gui(root,id)
    window.destroy()
    root.mainloop()
    

if __name__ == '__main__':
    main(id)
