'''
Created on 2018-11-5

@author: LYF,Li Yat Long
'''

import tkinter as tk
import pymysql
import payment_DB2
from quitButton import quitButton

connection = pymysql.connect(user='root',
                             password='',
                             db='all pos', 
                             cursorclass=pymysql.cursors.DictCursor)

class Gui:
    
    def __init__(self, root):
        '''
        setup logon page
        '''
        self.root = root
        self.root.title("POS login")
        self.root.geometry('350x200')
        
        self.label0 = tk.Label(self.root,text = 'Please input the username and password.')
        self.label0.place(x=5,y=5)

        
        self.label2 = tk.Label(self.root,text = 'Username:')
        self.label2.place(x = 5,y = 55)
        self.entry2 = tk.Entry(self.root,width= 25)
        self.entry2.place(x = 100, y = 55)
        
        self.label3 = tk.Label(self.root,text = 'Password:')
        self.label3.place(x = 5,y = 105)
        self.entry3 = tk.Entry(self.root,width= 25)
        self.entry3.place(x = 100, y = 105)
        
        tk.Button(self.root, text='submit', \
            command=lambda: self.logon()).place(x = 25, y = 155)
        
        self.label8= tk.Label(self.root,text = 'Status : Ready')
        self.label8.place(x = 105,y = 155)
        
        
        self.qBtn=quitButton(self.root)
    def logon(self):
        try:
            with connection.cursor() as cursor:
                found=False
                cursor.execute('''SELECT * FROM staff WHERE 1 ''')
                for e in cursor.fetchall():
                    if (self.entry2.get()!=e['username'] or self.entry3.get()!=e['password']) and not found:
                        print(type(e['username']))
                        print(type(self.entry2.get()))
                        self.label8.config(text='Status :Invaild username or password')
                    else:
                        str_qt2="SELECT staff_id FROM staff WHERE username = "
                        a = str((self.entry2.get()))
                    
                        cursor.execute(str_qt2 +" '" +a+ "' " )
                        id= (cursor.fetchone())
                        print(id)
                    
                    
                    
                        self.label8.config(text='Status : Success')
                        found=True
                        payment_DB2.main(id,self.root)
        except NameError as error:
            pass           
        
        
        
def main():
    root = tk.Tk()
    Gui(root)
    root.mainloop()
    
if __name__ == '__main__':
    main()           