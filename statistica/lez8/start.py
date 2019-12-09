import objects
import const
import draw
import gametime

def loop():
    print(gametime.gametime.getFormattedTime())
    draw.tk.after(10,loop)
    #sum 10 every time to gametime???


if __name__ == "__main__":
    #draw roads
    draw.drawField()
    loop()
    
    draw.tk.mainloop()