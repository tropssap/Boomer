from tkinter import *
from tkinter import filedialog as fd
import functions as func

class RootWindow(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.geometry('400x250+250+250')
        self.resizable(False, False)
        
        self.title('Voice Identificator')
        canvas = Canvas(self, width=400, height=250, bg='#1b1d1c')
        canvas.pack()
        label = Label(self, text='Hello and Welcome!',bg='#1b1d1c',relief=FLAT,fg="white",font="Verdana 15 bold")
        label.place(x=25,y=25)

        label = Label(self, text='This is a program to identify your voice',bg='#1b1d1c',relief=FLAT,fg="white",font="Verdana 10 bold")
        label.place(x=25,y=60)      

        label = Label(self, text='Please choose one of these following options',bg='#1b1d1c',relief=FLAT,fg="white",font="Verdana 10 bold")
        label.place(x=25,y=80) 
 
        button_Create = Button(self, text='Create new user', command=self.create_window,relief=FLAT,overrelief=FLAT,bg='#32c0b4',activebackground='#32c0b4',bd=0,fg="white",activeforeground="white",font="Verdana 12 bold")
        button_Create.place(x=25,y=180)

        button_Id = Button(self, text='Identification user', command=self.id_window,relief=FLAT,overrelief=FLAT,bg='#32c0b4',activebackground='#32c0b4',bd=0,fg="white",activeforeground="white",font="Verdana 12 bold")
        button_Id.place(x=205,y=180)

    def create_window(self):
        self.withdraw()
        Create_Window().mainloop()
        
    def id_window(self):
        self.withdraw()
        Id_Window().mainloop()

        

class Create_Window(Tk):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.geometry('600x300+250+250')
        self.resizable(False, False)
        self.path_wav = ''
        self.sex = StringVar()
        self.username = StringVar()
        self.title('Voice Identificator')
        canvas = Canvas(self, width=600, height=300, bg='#1b1d1c')
        canvas.pack()
        fileOpen = fd.askopenfile(filetypes=[("WAV Files","*.wav")])
        if fileOpen!=None:
            self.path_wav=fileOpen.name
        button_go_back2 = Button(self, text='Back to menu', command=self.back_window,relief=FLAT,overrelief=FLAT,bg='#32c0b4',activebackground='#32c0b4',bd=0,fg="white",activeforeground="white",font="Verdana 10 bold")
        button_go_back2.place(x=5,y=5)
        self.entry_user= Entry(self)
        self.entry_user.place(x=240,y=75)
        
        rbutton_men=Radiobutton(self,text='Male',command=self.set_men,value='0')
        rbutton_women=Radiobutton(self,text='Female',command=self.set_women,value='1')
        rbutton_men.place(x=220,y=120)
        rbutton_women.place(x=310,y=120)
        button_submit = Button(self, text="Submit Form", command=self.submit_message)
        button_submit.place(x=260,y=225)
        button_change = Button(self, text="Change Directory", command=self.change_dir)
        button_change.place(x=260,y=170)    


    def back_window(self):
        self.withdraw()
        RootWindow().mainloop()
        self.deiconify()

    def set_men(self):
        self.sex='man'
        
    def set_women(self):
        self.sex='woman'

    def submit_message(self):
        if self.path_wav != "" and self.entry_user.get() != "":
            func.user_insert(self.path_wav, self.entry_user.get(), self.sex)
        self.withdraw()
        RootWindow().mainloop()
        self.deiconify()

    def change_dir(self):
        fileOpen = fd.askopenfile(filetypes=[("WAV Files","*.wav")])
        if fileOpen!=None:
            path_wav=fileOpen.name
        


class Id_Window(Tk): 
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.geometry('600x300+250+250')
        self.resizable(False, False)

        self.title('Voice Identificator')
        canvas = Canvas(self, width=600, height=300, bg='#1b1d1c')
        canvas.pack()

        self.path_wav = ''
        self.sex = StringVar()
        self.username = StringVar()

        fileOpen = fd.askopenfile(filetypes=[("WAV Files","*.wav")])
        if fileOpen!=None:
            self.path_wav=fileOpen.name
        
        button_go_back = Button(self, text='Back to menu', command=self.back_window2,relief=FLAT,overrelief=FLAT,bg='#32c0b4',activebackground='#32c0b4',bd=0,fg="white",activeforeground="white",font="Verdana 10 bold")
        button_go_back.place(x=5,y=5)

        button_go_back = Button(self, text='Identify', command=self.identify_user)
        button_go_back.place(x=5,y=45)

        self.result_sex=Label(self,text='')
        self.result_sex.place(x=5,y=85)
        self.result_name=Label(self,text='')
        self.result_name.place(x=5,y=125)

    def back_window2(self):
        self.withdraw()
        RootWindow().mainloop()
        self.deiconify()

    def identify_user(self):
        self.sex, self.username = func.voice_identify(self.path_wav)
        self.result_sex.config(text=self.sex)
        self.result_name.config(text=self.username)
        
        

if __name__ == '__main__':
    RootWindow().mainloop()
