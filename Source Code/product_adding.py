'''
Created on 2018-11-3

@author: LYF
'''

import tkinter as tk
from tkinter import ttk
import sys
import pymysql

connection = pymysql.connect(user='root',
                             password='',
                             db='all pos', 
                             cursorclass=pymysql.cursors.DictCursor)

class Gui:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Product Adding")
        self.root.geometry('600x500')
        
        self.label0 = tk.Label(self.root,text = 'Please input with the following data to add Product.')
        self.label0.place(x=5,y=5)

        
        self.label2 = tk.Label(self.root,text = 'Product Name :')
        self.label2.place(x = 5,y = 105)
        self.entry2 = tk.Entry(self.root,width= 25)
        self.entry2.place(x = 100, y = 105)
        
        self.label3 = tk.Label(self.root,text = 'Product Brand :')
        self.label3.place(x = 5,y = 155)
        self.entry3 = tk.Entry(self.root,width= 25)
        self.entry3.place(x = 100, y = 155)
        
        self.label4 = tk.Label(self.root,text = 'Product Price :')
        self.label4.place(x = 5,y = 205)
        self.entry4 = tk.Entry(self.root,width= 25)
        self.entry4.place(x = 100, y = 205)
        
        self.label5 = tk.Label(self.root,text = 'Quanitiy :')
        self.label5.place(x = 5,y = 255)
        self.entry5 = tk.Entry(self.root,width= 25)
        self.entry5.place(x = 100, y = 255)
        
        self.label6 = tk.Label(self.root,text = 'Type :')
        self.label6.place(x = 5,y = 305)
        
        type = tk.StringVar()
        self.option1= ttk.Combobox(root, width=12, textvariable=type)
        self.option1['values'] = ('','Food', 'Drink') 
        self.option1.grid(column=1, row=1)
        self.option1.current(0)
        self.option1.place(x = 100, y = 305)
        
       
        type2 = tk.StringVar()
        self.label7 = tk.Label(self.root,text = 'Subtype :')
        self.label7.place(x = 5,y = 355)
        self.option2= ttk.Combobox(root, width=12, textvariable=type2)
        self.option2['values'] = ('','Bread','Cup noodle','Ice cream', 'Frozen food', 'Snack') 
        self.option2.grid(column=1, row=2)
        self.option2.current(0)
        self.option2.place(x = 100, y = 355)

        tk.Label(self.root,text = '/').place(x = 250,y = 355)

        type3 = tk.StringVar()
        self.option3= ttk.Combobox(root, width=12, textvariable=type3)
        self.option3['values'] = ('','Tea','Carbonated drink','Other','Coffee','Juice','Beer'  ) 
        self.option3.grid(column=1, row=2)
        self.option3.current(0)
        self.option3.place(x = 300, y = 355)
           
        tk.Button(self.root, text='submit', \
            command=lambda: self.adding()).place(x = 25, y = 405)
        
        self.label8= tk.Label(self.root,text = 'Status : Ready')
        self.label8.place(x = 100,y = 405)
            
    def adding(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute('''INSERT INTO product (`product_id`, `product_name`, `product_brand`, `product_price`, `quantity`, `product_type`, `product_subtype`) VALUES(%d,'%s','%s',%f,%d,'%s',"%s"'''%(int(0),self.entry2.get(),self.entry3.get(),float(self.entry4.get()),int(self.entry5.get()),self.option1.get(),(self.option2.get()+','+self.option3.get()))+')')
                connection.commit()
                self.label8.config(text='Status :Success')
                
        except Exception as error:
            print(error)
            self.label8.config(text='Status :ERROR Data')
            

            
            
def main():
    root = tk.Tk()
    Gui(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()        
        