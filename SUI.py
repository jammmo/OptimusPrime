
import tkinter
tk = tkinter.Tk()

def callback():
    tk.wm_attributes('-transparentcolor', )
    w = tkinter.Label(tk,text="Helvetica", font=("Times", 50),bg="#27ae60")
    w.configure(text="dsad")
    w.place(relx=.5, rely=.5, anchor="center")
    # w['bg'] = w.master['bg']
    # w.place(x=0, y=250, anchor="center")
    # w.place(x=0, y=0)
    w.pack()
# tk.geometry("500x700")
C = tkinter.Canvas(tk, height=500, width=700)
background_image=tkinter.PhotoImage(file = "C:/Users/Chau Do/Downloads/download1.gif")
background_label = tkinter.Label(tk, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# C.create_text(0,20,text="My text")

callback()



C.pack()
tk.mainloop()
