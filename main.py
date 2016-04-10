from Tkinter import *
from PIL import Image, ImageTk
from ttk import Frame, Style, Button
from room import *
from loader import *
# Debugging
import pdb

class Main(Frame):
    # Lol mainframe
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

        # State attributes
        self.room = False


    def initUI(self):

        self.parent.title("Chaos Dungeon Generator")
        self.style = Style()
        self.style.theme_use("default")

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)

        closeButton = Button(self, text="Quit", command=quit)
        closeButton.pack(side=LEFT, padx=5, pady=5)
        okButton = Button(self, text="Start", command=self.generateRoom)
        okButton.pack(side=LEFT)

    def generateRoom(self):
        '''
        Generates the Room() object and displays it in a window.
        '''
        # Up here should be user inputs that pop up first, but right now
        # just making the window and a randomly generated room.

        # Clearing out any previous stuff
        if self.room:
            self.roomframe.destroy()
            self.room = False

        # Setting the lvl variable
        lvl = IntVar()
        lvl.set(1)
        # Button commands (contained here for a reason)
        def upLevel():
            lvl.set(lvl.get() + 1)
            roomframe.update()
            print lvl.get()
        def downLevel(level):
            lvl.set(lvl.get() + 1)

        # Generating the new frame for the room
        self.roomframe = Frame(self.parent, borderwidth=1)
        self.room = True #
        up = Button(self.roomframe, text='+')
        down = Button(self.roomframe, text='-')
        up.pack(side=TOP)
        down.pack(side=TOP)

        # Generating the Room() object and storing it as an attribute
        self.current_room = Room(shape ="Rectangle")
        outstr = self.current_room.roomString(level = lvl.get())
        print self.current_room.size, self.current_room.shape
        room_label = Label(self.roomframe, text = outstr, fg = "white",
                           bg = "black", justify=LEFT, anchor = W,
                           font = ('Courier', '12'))
        room_label.pack()#side=BOTTOM, fill = BOTH)

        # Packing the room's frame
        self.roomframe.pack(side = BOTTOM,fill=BOTH, expand=True)

def main():

    root = Tk()
    ex = Main(root)
    root.mainloop()


if __name__ == '__main__':
    main()
