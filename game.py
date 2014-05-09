from Tkinter import *
import tkFont

top = Tk()
top.overrideredirect(True)
top.geometry("{0}x{1}+0+0".format(top.winfo_screenwidth(), top.winfo_screenheight()))

font = tkFont.Font(family="Helvetica", size=36, weight="bold")
typefont = tkFont.Font(family="Arial", size=18)
typed = Text(top, font=typefont)
textbox = Text(top, font=font)

mainframe = Frame(top)

lineindex = 1.0

typed.insert(END, "Word: \n")
typed.pack()
typed.place(relx = 0.0, rely=0.3)
mainframe.update()

def deletetk():
  textbox.delete(1.0, END)

def writeletter(letter):
  typed.insert(END, letter)
  typed.pack()
  typed.place(relx = 0.0, rely=0.3)
  mainframe.update()

def writetk(tktext):
  deletetk()
  textbox.insert(END, tktext) 
  textbox.insert(END, '\n') 
  textbox.pack()
  textbox.place(relx = 0.0, rely=0.5)
  mainframe.update()

def inlinetk(tktext):
  textbox.insert(END, tktext) 
  textbox.pack()
  textbox.place(relx = 0.0, rely=0.5)
  mainframe.update()

def addlinetk(tktext):
  textbox.insert(END, tktext) 
  textbox.insert(END, '\n') 
  textbox.pack()
  textbox.place(relx = 0.0, rely=0.5)
  mainframe.update()
