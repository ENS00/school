import tkinter
import const
import objects

tk=tkinter.Tk()
tk.title(const.W_TITLE)
canvas=tkinter.Canvas(tk,width=const.W_WIDTH,height=const.W_HEIGHT,bg=const.W_BACKGROUND)
canvas.pack()

def drawField():
    global tk
    global canvas
    canvas.create_rectangle(0,0,canvas.winfo_width(),canvas.winfo_height(),width=0)
    
    lane_up_entry = objects.Lane(objects.Position(const.W_WIDTH/2-36*0.75,0),
                                objects.Position(const.W_WIDTH/2-36*0.75,const.W_HEIGHT/2-36*1.5))
    lane_up_entry.draw()
    lane_up_exit = objects.Lane(objects.Position(const.W_WIDTH/2+36*0.75,const.W_HEIGHT/2-36*1.5),
                                objects.Position(const.W_WIDTH/2+36*0.75,0))
    lane_up_exit.draw()
    lane_left_entry=objects.Lane(objects.Position(const.W_WIDTH/2-36*1.5,const.W_HEIGHT/2-36*0.75),
                                objects.Position(0,const.W_HEIGHT/2-36*0.75))
    lane_left_entry.draw()
    lane_left_exit=objects.Lane(objects.Position(0,const.W_HEIGHT/2+36*0.75),
                                objects.Position(const.W_WIDTH/2-36*1.5,const.W_HEIGHT/2+36*0.75))
    lane_left_exit.draw()