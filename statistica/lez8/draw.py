import tkinter

tk=tkinter.Tk()
tk.title('Traffico')
canvas=tkinter.Canvas(tk,width=1920,height=1080,bg='lightgreen')
canvas.create_rectangle(0,0,canvas.winfo_width(),canvas.winfo_height())
canvas.pack()