import tkinter as tk

class quitButton(tk.Button):
    '''
    setup quit button
    '''
    def __init__(self, parent):
        tk.Button.__init__(self, parent)
        self['text'] = 'Quit'
        self['command'] = parent.destroy
        self.pack(side=tk.BOTTOM)
        
def main():
    root = tk.Tk()
    quitButton(root)
    root.mainloop()

if __name__ == '__main__':
    main()