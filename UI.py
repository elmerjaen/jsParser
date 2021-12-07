from tkinter import *
import re
import jsParser

gui = Tk()
gui.title('Analizador Sintáctico de Javascript')
gui.geometry('545x240')

user_input = Text(gui, width=60, height=5, font=('Consolas',11,'bold'))
lbStart = Label(gui, text="A continuación, ingrese código Javascript:", font=('Helvetica',11,'bold'))
myLabel = Label(gui)
lbTokens = Label(gui)

def myClick():
    global myLabel
    global lbTokens

    myLabel.destroy()
    lbTokens.destroy()

    js_string = user_input.get("1.0","end-1c")
    result, category = jsParser.check_string(js_string)

    if result == 1:
        myLabel = Label(gui, text=f'La sintaxis {category} es correcta.', font=('Helvetica',12,'bold'), bg="RoyalBlue3", fg="white")
        
        #get tokens
        findTokens = re.findall('\w+|\W', js_string)
        tokenDict = jsParser.get_tokens(findTokens)
        a = 'Tokens:\n\n'
        a += '\n'.join('{} {}'.format(k, d) for k, d in tokenDict.items())
        a = a.replace("'", "")
        a = a.replace("[", "")
        a = a.replace("]", "")
        
        gui.geometry('545x390')
        lbTokens = Label(gui, text=a, font=('Helvetica',12,'bold'), justify=LEFT, bg="linen")
        lbTokens.place(x=30, y=240)
    else:
        myLabel = Label(gui, text="Error de sintaxis. Revise nuevamente.", font=('Helvetica',12,'bold'), bg="red", fg="white")
    
    myLabel.place(x=30, y=200)

def on_enter(e):
    btnVerifySql.config(bg='LightBlue', fg='black')

def on_leave(e):
    btnVerifySql.config(bg='DarkOrange4', fg='white')

btnVerifySql = Button(
    gui,text="Verificar sintaxis", command=myClick, 
    font=('Helvetica',12,'bold'), fg="white",
    bg="DarkOrange4", padx=10, pady=8)

# btnVerifySql hover event
btnVerifySql.bind('<Enter>', on_enter)
btnVerifySql.bind('<Leave>', on_leave)

lbStart.place(x=30, y=5)
user_input.place(x=30, y=35)
btnVerifySql.place(x=190, y=140)

gui.configure(bg='linen')
gui.mainloop()