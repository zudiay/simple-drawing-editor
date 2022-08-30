from tkinter import *
from tkinter.colorchooser import *
from idlelib.tooltip import Hovertip

LINE = 0
SQUARE = 1
CIRCLE = 2
COLOR_PICKER = 3

# class that defines the editor with whiteboard, tools, icons and UI
class DrawingEditor:
    def __init__(self, whiteboard):
        self.whiteboard = whiteboard
        self.current_tool = None
        # define icons for the tools
        self.icons = [PhotoImage(file="pencil.png"), PhotoImage(file="square.png"),
                      PhotoImage(file="circle.png"), PhotoImage(file="colors.png")]

        # define TK labels for the tools
        frame = Frame(width=50)
        for button in [COLOR_PICKER, LINE, SQUARE, CIRCLE]:
            label = Label(frame, relief='groove', image=self.icons[button], height=30, width=30)
            label._tool = button
            label.pack(padx=10, pady=5)

            # connect label clicks with tool choose function and descriptive tooltips
            if not button == 3:  # color picker
                Hovertip(label, f'Draw a {"line" if button==0 else "square" if button==1 else "circle"}')
                label.bind('<Button>', self.choose_tool)
            else:  # line, square and circle
                Hovertip(label, 'Choose color')
                label.bind('<Button>', self.choose_color)
        # pack the labels into a frame on the left hand side of the editor
        frame.pack(side='left', fill='y', pady=5)

    # open color dialog and ask for color, change editor's current color
    def choose_color(self, event):
        color = askcolor()
        self.whiteboard.choose_color(color[1])

    # change editor's current color
    # update the previous and new tool's buttons' appearance
    def choose_tool(self, event):
        current_tool = self.current_tool
        if current_tool is not None:
            current_tool['relief'] = 'groove'
        label = event.widget
        label['relief'] = 'sunken'
        self.current_tool = label
        self.whiteboard.choose_tool(label._tool)

# class that defines the drawing actions on the canvas with a tool, at a coordinate x,y
class Draw:
    def __init__(self, canvas):
        self.canvas = canvas
        self.tool = LINE
        self.color = '#000000'
        self.item = None
        self.coordinates = (None, None)
        self.canvas.bind('<Button>', self.click)
        self.canvas.bind('<B1-Motion>', self.draw)

    def draw(self, event):
        self.canvas.coords(self.item, (self.coordinates[0], self.coordinates[1], event.x, event.y))

    def click(self, event):
        if self.tool == LINE:
            self.item = self.canvas.create_line((event.x, event.y, event.x, event.y), width=10, fill=self.color)
        elif self.tool == SQUARE:
            self.item = self.canvas.create_rectangle((event.x, event.y, event.x, event.y), width=10,  outline=self.color, fill=self.color)
        elif self.tool == CIRCLE:
            self.item = self.canvas.create_oval((event.x, event.y, event.x, event.y), width=10, outline=self.color, fill=self.color)
        self.coordinates = (event.x, event.y)

    def choose_color(self, color):
        self.color = color

    def choose_tool(self, tool):
        self.tool = tool


if __name__ == '__main__':
    root = Tk()
    root.title("CMPE 496 - HOMEWORK 1")
    canvas = Canvas(highlightbackground='black', width=700, height=700)
    DrawingEditor(Draw(canvas))
    canvas.pack()
    root.mainloop()
