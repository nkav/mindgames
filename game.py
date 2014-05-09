from Tkinter import *
import tkFont

top = Tk()
top.overrideredirect(True)
top.geometry("{0}x{1}+0+0".format(top.winfo_screenwidth(), top.winfo_screenheight()))

font = tkFont.Font(family="Helvetica", size=36, weight="bold")
textbox = Text(top, font=font)

mainframe = Frame(top)

lineindex = 1.0

def deletetk():
  textbox.delete(1.0, END)

def writetk(tktext):
  deletetk()
  textbox.insert(END, tktext) 
  textbox.insert(END, '\n') 
  textbox.pack()
  textbox.place(relx = 0.0, rely=0.5)
  mainframe.update()

def addlinetk(tktext):
  textbox.insert(END, tktext) 
  textbox.insert(END, '\n') 
  textbox.pack()
  textbox.place(relx = 0.0, rely=0.5)
  mainframe.update()
