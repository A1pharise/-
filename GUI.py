import tkinter as tk
from tkinter import messagebox
import numpy as np

def is_boom(a):
    a=a.widget
    print(a)
    if(a.boom):
        for i in a.root.boom:
            x=i.grid_info()
            row=x['row']
            col=x['column']
            L=tk.Label(i.root,text='',width=2,height=1,bg='red')
            L.grid(column=col,row=row)
            i.destroy()
        messagebox.showinfo(":-(", "you die")
        a.root.root.destroy()
    else:
        x=a.grid_info()
        row=x['row']
        col=x['column']
        num=0
        posi=a.root.posi
        for i in range(row-1,row+2):
            for j in range(col-1,col+2):
                if(i in range(0,8) and j in range(0,8)):
                    if(posi[i][j].boom):
                        num=num+1
        L=tk.Label(a.root,text=num,width=2,height=1)
        L.grid(column=col,row=row)
        a.destroy()
        a.root.num=a.root.num+1
        if(a.root.num==54):
            messagebox.showinfo(":-)", "you win")
            a.root.root.destroy()



posi=np.empty((8,8),dtype=object)
Gui=tk.Tk()
Gui.geometry('500x300')
frm=tk.Frame(Gui,width=300,height=250,bg='yellow')
frmright=tk.Frame(Gui,width=100,height=250,bg='green')
frmtop=tk.Frame(Gui,width=50,height=50,bg='black')
frm.root=Gui
frm.posi=posi
frm.num=0
for row in range(8):
    for col in range(8):
        posi[row][col]=tk.Button(frm,width=2,height=1)
        posi[row][col].boom=False
        posi[row][col].root=frm
        posi[row][col].grid(column=col,row=row)
boomlist=np.random.choice(posi.flatten(),10,replace=False)
frm.boom=boomlist
for i in boomlist:
    i.boom=True
posi[0][0].bind_class('Button','<Button-1>',is_boom)
print(boomlist)
frm.place(x=50,y=50)
frmright.place(x=375,y=50)
frmtop.place(x=225,y=0)


Gui.mainloop()