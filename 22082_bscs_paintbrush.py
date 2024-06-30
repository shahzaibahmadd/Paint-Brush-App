import tkinter.colorchooser as colorchooser
from distutils.cmd import Command
from tkinter import *
from tkinter import colorchooser
import math
from tkinter import filedialog
from PIL import ImageGrab
from PIL import Image,ImageTk
from tkinter import filedialog
import PIL.ImageGrab as ImageGrabe
from tkinter import messagebox
class PaintApp:
    def __init__(self, width, height, title):
        self.screen = Tk()
        self.screen.title(title)
        self.screen.geometry(str(width) + 'x' + str(height))
        self.brushwidth=5
        self.image = ImageGrab.grab()  # Grab the initial screenshot
 
        self.selected_item = None
        self.fill_color = None
        self.selection_rectangle= None


        self.brushcolor = 'black'
        self.erasercolor = 'white'
       

        self.lastx, self.lasty = None, None
        self.shapeid = None

     
     # button area
        self.buttonarea = Frame(self.screen, width=width, height=100, bg="grey")
        self.buttonarea.pack()

     
     # create canvas
        self.canvas = Canvas(self.screen, width=width, height=height, bg="white")
        self.canvas.pack()

     
     # clear screen button
        self.clearbutton = Button(self.buttonarea, text="clear screen", bg="blue", command=self.clearcanvas)
        self.clearbutton.place(x=5, y=5)
     
     # brush button
        self.brushbutton = Button(self.buttonarea, text="brush", bg="pink", command=self.onbrushbuttonpressed)
        self.brushbutton.place(x=85, y=5)
       
      
     # eraser button
        self.eraserbutton = Button(self.buttonarea, text="eraser", bg="orange", command=self.oneraserbuttonpressed)
        self.eraserbutton.place(x=225, y=5)
      
      # select color button
        self.selectcolorbutton = Button(self.buttonarea, text="select color", bg="green", command=self.selectcolor)
        self.selectcolorbutton.place(x=155, y=5)
      
      # circle button
        self.circlebutton = Button(self.buttonarea, text="circle", bg="light blue", command=self.oncirclebuttonpressed)
        self.circlebutton.place(x=433, y=35)
      
      # rectangle button
        self.rectanglebutton = Button(self.buttonarea, text="rectangle", bg="light blue",
                                     command=self.onrectanglebuttonpressed)
        self.rectanglebutton.place(x=525, y=35)
       
      # oval button
        self.ovalbutton = Button(self.buttonarea, text="oval", bg="light blue",
                                     command=self.onovalbuttonpressed)
        self.ovalbutton.place(x=587, y=35)
       
      #hexagon button
        self.hexagonbutton = Button(self.buttonarea, text="hexagon", bg="light blue",
                                     command=self.onhexagonbuttonpressed)
        self.hexagonbutton.place(x=623, y=35)
       
      # pentagon button
        self.pentagonbutton = Button(self.buttonarea, text="pentagon", bg="light blue",
                                     command=self.onpentagonbuttonpressed)
        self.pentagonbutton.place(x=680, y=35)
       
      # triangle button
        self.trianglebutton = Button(self.buttonarea, text="triangle", bg="light blue",
                                     command=self.ontrianglebuttonpressed)
        self.trianglebutton.place(x=560, y=65)
        
       #square button
        self.squarebutton = Button(self.buttonarea, text="square", bg="light blue",
                                     command=self.onsquarebuttonpressed)
        self.squarebutton.place(x=475, y=35)
        
       #line button
        self.linebutton = Button(self.buttonarea, text="line", bg="light blue",
                                     command=self.onlinebuttonpressed)
        self.linebutton.place(x=500, y=65)
       #star button
        self.starbutton = Button(self.buttonarea, text="star", bg="light blue",
                                     command=self.onstarbuttonpressed)
        self.starbutton.place(x=530, y=65)
       #n-polygon button
        self.polygonbutton = Button(self.buttonarea, text="n-polygon", bg="light blue",
                                     command=self.onpolygonbuttonpressed)
        self.polygonbutton.place(x=610, y=65)
     # magnify
        self.magnifybutton = Button(self.buttonarea, text="magnify", bg="yellow",
                                     command=self.onmagnifybuttonpressed)
        self.magnifybutton.place(x=270, y=35)
     # get pixel
        self.colorpickbutton = Button(self.buttonarea, text="color pick", bg="yellow",
                                     command=self.oncolorpickbuttonpressed)
        self.colorpickbutton.place(x=330, y=35)
     # Create the Fill button
        self.fill_button = Button(self.buttonarea, text="Fill", bg="yellow",command=self.on_FillButtonPress)
        self.fill_button.place(x=400,y=35)
    # buttons
        self.fill_button = Button(self.buttonarea, text="                                           SHAPES                                             ", bg="pink")
        self.fill_button.place(x=430,y=5)



        
       
        # magnify binding 
       
       
        self.save_button = Button(self.buttonarea, text="Save Canvas", command=self.save_canvas)
        self.save_button.place(x=5,y=30)

        self.load_button = Button(self.buttonarea, text="Load Canvas", command=self.load_canvas)
        self.load_button.place(x=5,y=55)
        
        self.selectwholeshapetool = Button(self.buttonarea, text="select whole tool", command=self.onselectbuttonpressed)
        self.selectwholeshapetool.place(x=270,y=60)
        
        self.selecttool = Button(self.buttonarea, text="select tool", command=self.on_selection_pressed)
        self.selecttool.place(x=155,y=30)
        self.movetool = Button(self.buttonarea, text="move selected", command=self.on_move_pressed)
        self.movetool.place(x=155,y=55)
    

    def on_FillButtonPress(self):

            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
                    
            selectedcolor = colorchooser.askcolor()
            self.brushcolor = selectedcolor[1]

            

            self.canvas.bind("<Button-1>", self.start_fill)
   
    def start_fill(self, event):
        x, y = event.x, event.y
        boundary_color = self.get_pixel_color(x, y)
        if boundary_color != self.fill_color:
            self.flood_fill(x, y, boundary_color)

    def flood_fill(self, x, y, boundary_color):
        stack = [(x, y)]
        while stack:
            x, y = stack.pop()
            if self.is_within_boundary(x, y) and self.get_pixel_color(x, y) == boundary_color:
                self.set_pixel_color(x, y, self.fill_color)
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))

    def is_within_boundary(self, x, y):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        return 0 <= x < canvas_width and 0 <= y < canvas_height

    def get_pixel_color(self, x, y):
        items = self.canvas.find_overlapping(x, y, x, y)
        if items:
            item_id = items[-1]  # Get the top-most item
            return self.canvas.itemcget(item_id, "fill")
        return ""

    def set_pixel_color(self, x, y, color):
        items = self.canvas.find_overlapping(x, y, x, y)
        if items:
            item_id = items[-1]  # Get the top-most item
            

            self.canvas.itemconfig(item_id, fill=self.brushcolor)
   

    def on_selection_pressed(self):
      self.canvas.unbind("<Button-1>")
      self.canvas.unbind("<Button-3>")
      self.canvas.unbind("<ButtonRelease-1>")
      self.canvas.unbind("<ButtonRelease-3>")
      self.canvas.unbind("<B1-Motion>")
      self.canvas.bind("<B1-Motion>", self.move_selection)
      self.canvas.bind("<ButtonRelease-1>", self.move_selection_end)

    def on_move_pressed(self):
      self.canvas.unbind("<Button-1>")
      self.canvas.unbind("<Button-3>")
      self.canvas.unbind("<ButtonRelease-1>")
      self.canvas.unbind("<ButtonRelease-3>")
      self.canvas.unbind("<B1-Motion>")
      self.canvas.bind("<B1-Motion>", self.move_items)
      self.canvas.bind("<ButtonRelease-1>", self.move_items_end)  


    def move_selection(self, event):
      if not self.lastx:
         self.lastx, self.lasty = event.x, event.y
         self.selection_rectangle = self.canvas.create_rectangle(self.lastx, self.lasty, self.lastx, self.lasty, dash=(2, 2))
      else:
         x1, y1 = self.canvas.coords(self.selection_rectangle)[:2]
         x2, y2 = event.x, event.y
         self.canvas.coords(self.selection_rectangle, x1, y1, x2, y2)

    def move_selection_end(self,event):
      x1, y1, x2, y2 = self.canvas.coords(self.selection_rectangle)
      items = self.canvas.find_enclosed(x1, y1, x2, y2)
      for item in items:
         self.canvas.addtag_withtag("selected", item)
      self.canvas.delete(self.selection_rectangle)
      self.lastx, self.lasty = None, None    

   

    def move_items(self, event):
      if not self.lastx:
        self.lastx, self.lasty = event.x, event.y
      else:
        x, y = event.x - self.lastx, event.y - self.lasty
        self.canvas.move("selected", x, y)
        self.lastx, self.lasty = event.x, event.y

    def move_items_end(self, event):
      self.lastx, self.lasty = None, None
            # old sai wala
    def select_shape(self, event):
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)[0]
        self.selected_item = item
        self.startx, self.starty = x, y

    def onselectbuttonpressed(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.select_shape)
        self.canvas.bind("<ButtonRelease-1>", self.pick_clrend)
        self.canvas.bind("<B1-Motion>", self.move_shape)



    

    def move_shape(self, event):
        if self.selected_item:
            x, y = event.x, event.y
            dx = x - self.startx
            dy = y - self.starty
            self.canvas.move(self.selected_item, dx, dy)
            self.startx, self.starty = x, y


    def save_canvas(self):
        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        image = ImageGrab.grab(bbox=(x, y, x1, y1))
        filename = filedialog.asksaveasfilename(defaultextension=".jpg")
        if filename:
            image.save(filename)

    def load_canvas(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg")])
        if filename:
            image = Image.open(filename)
            width, height = image.size
            self.canvas.config(width=width, height=height)
            self.canvas.delete("all")
            self.image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.image)
   

    

    def paintbrush(self,event):
        x, y = self.event.x, self.event.y
        color = self.canvas.itemcget(self.canvas.find_closest(x, y), "fill")
        fill_color = colorchooser.askcolor(color)[1]
        self.fill_region(x, y, color, fill_color)
    # Function to fill the region
    # def fill_region(self,x, y, target_color, fill_color):
    #     current_color = self.canvas.itemcget(self.canvas.find_closest(x, y), "fill")
    #     if current_color == target_color:
    #         self.canvas.create_rectangle(x, y, x+1, y+1, fill=fill_color, outline=fill_color)
    #         self.fill_region(x+1, y, target_color, fill_color)
    #         self.fill_region(x-1, y, target_color, fill_color)
    #         self.fill_region(x, y+1, target_color, fill_color)
    #         self.fill_region(x, y-1, target_color, fill_color)

    # # Function to handle button click event
    # def fill_button_click(self):
    #     color = self.canvas.itemcget(self.canvas.find_closest(1, 1), "fill")
    #     fill_color = colorchooser.askcolor(color)[1]
    #     self.fill_region(1, 1, color, fill_color)

    
    def pick_clr(self, event):
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)[0]
        pixel_color = self.canvas.itemcget(item, 'fill')
        self.brushcolor = pixel_color
        
    def oncolorpickbuttonpressed(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<Button-1>", self.pick_clr)
        self.canvas.bind("<ButtonRelease-1>", self.pick_clrend)    


    def pick_clrend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None    
        # magnify
   
   
    def do_zoom(self,event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.canvas.scale(ALL, x, y, factor, factor)
    def dozoomend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
    def onmagnifybuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<MouseWheel>", self.do_zoom)
        self.canvas.bind('<ButtonPress-1>', lambda event: self.canvas.scan_mark(event.x, event.y))
        self.canvas.bind("<B1-Motion>", lambda event: self.canvas.scan_dragto(event.x, event.y, gain=1))
        self.canvas.bind("<B1-Motion>", self.do_zoom)
        self.canvas.bind("<ButtonRelease-1>", self.dozoomend)    

        # bursh
    def onbrushbuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawbrush)
        self.canvas.bind("<ButtonRelease-1>", self.drawbrushend)
          # brushsize10 button
        self.brushbutton10 = Button(self.buttonarea, text="brush10", bg="pink", command=self.onbrushbuttonpressedsize10)
        self.brushbutton10.place(x=85, y=80)
         # brushsize15 button
        self.brushbutton15 = Button(self.buttonarea, text="brush15", bg="pink", command=self.onbrushbuttonpressedsize15)
        self.brushbutton15.place(x=85, y=30)
          # brushsize5 button
        self.brushbutton5 = Button(self.buttonarea, text="brush5", bg="pink", command=self.onbrushbuttonpressedsize5)
        self.brushbutton5.place(x=85, y=55)

    def onbrushbuttonpressedsize10(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.brushbutton10.destroy()
        self.brushbutton15.destroy()
        self.brushbutton5.destroy()
        self.canvas.bind("<B1-Motion>", self.drawbrushsize10)
        self.canvas.bind("<ButtonRelease-1>", self.drawbrushendsize10)

    def onbrushbuttonpressedsize5(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.brushbutton15.destroy()
        self.brushbutton5.destroy()
        self.brushbutton10.destroy()
        self.canvas.bind("<B1-Motion>", self.drawbrush)
        self.canvas.bind("<ButtonRelease-1>", self.drawbrushend)

    def onbrushbuttonpressedsize15(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.brushbutton15.destroy()
        self.brushbutton5.destroy()
        self.brushbutton10.destroy()
        self.canvas.bind("<B1-Motion>", self.drawbrushsize15)
        self.canvas.bind("<ButtonRelease-1>", self.drawbrushendsize15)
        #eraser
    def oneraserbuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<B1-Motion>", self.eraser)
        self.canvas.bind("<ButtonRelease-1>", self.eraserend)
           # brushsize10 button
        self.eraserbutton10 = Button(self.buttonarea, text="eraser10", bg="pink", command=self.oneraserbuttonpressedsize10)
        self.eraserbutton10.place(x=255, y=80)
         # brushsize15 button
        self.eraserbutton15 = Button(self.buttonarea, text="eraser15", bg="pink", command=self.oneraserbuttonpressedsize15)
        self.eraserbutton15.place(x=255, y=30)
          # brushsize5 button
        self.eraserbutton5 = Button(self.buttonarea, text="eraser5", bg="pink", command=self.oneraserbuttonpressedsize5)
        self.eraserbutton5.place(x=255, y=55)

    def oneraserbuttonpressedsize10(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.eraserbutton10.destroy()
        self.eraserbutton15.destroy()
        self.eraserbutton5.destroy()
        self.canvas.bind("<B1-Motion>", self.erasersize10)
        self.canvas.bind("<ButtonRelease-1>", self.eraserendsize10)

    def oneraserbuttonpressedsize5(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.eraserbutton10.destroy()
        self.eraserbutton15.destroy()
        self.eraserbutton5.destroy()
        self.canvas.bind("<B1-Motion>", self.eraser)
        self.canvas.bind("<ButtonRelease-1>", self.eraserend)

    def oneraserbuttonpressedsize15(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.eraserbutton10.destroy()
        self.eraserbutton15.destroy()
        self.eraserbutton5.destroy()
        self.canvas.bind("<B1-Motion>", self.erasersize15)
        self.canvas.bind("<ButtonRelease-1>", self.eraserendsize15)
        #circle
    def oncirclebuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawcircle)
        self.canvas.bind("<ButtonRelease-1>", self.drawcircleend)

    # rectangle
    def onrectanglebuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawrectangle)
        self.canvas.bind("<ButtonRelease-1>", self.drawrectangleend)
        # oval
    def onovalbuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawoval)
        self.canvas.bind("<ButtonRelease-1>", self.drawovalend)

    # hexagon
    def onhexagonbuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawhexagon)
        self.canvas.bind("<ButtonRelease-1>", self.drawhexagonend)
    # pentagon
    def onpentagonbuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawpentagon)
        self.canvas.bind("<ButtonRelease-1>", self.drawpentagonend)
        # trianagle 
    def ontrianglebuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawtriangle)
        self.canvas.bind("<ButtonRelease-1>", self.drawtriangleend)
        # square
    def onsquarebuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawsquare)
        self.canvas.bind("<ButtonRelease-1>", self.drawsquareend)
    # line
    def onlinebuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawline)
        self.canvas.bind("<ButtonRelease-1>", self.drawlineend)
    # star
    def onstarbuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawstar)
        self.canvas.bind("<ButtonRelease-1>", self.drawstarend)

        # n side polygon
    def onpolygonbuttonpressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<B1-Motion>", self.drawpolygon)
        self.canvas.bind("<ButtonRelease-1>", self.drawpolygonend)
    
    # n side polygon
    def drawpolygon(self, event):
        if self.shapeid is not None:
            self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return

        # Prompt the user to enter the number of sides for the polygon
        sides = int(input("Enter the number of sides for the polygon: "))

        radius = min(abs(event.x - self.lastx), abs(event.y - self.lasty))
        x_center, y_center = self.lastx, self.lasty

        # Calculate the angle between each point
        angle = 2 * math.pi / sides

        # Calculate the coordinates for the points of the polygon
        vertices = []
        for i in range(sides):
            x = x_center + radius * math.cos(i * angle)
            y = y_center + radius * math.sin(i * angle)
            vertices.extend([x, y])

        self.shapeid = self.canvas.create_polygon(vertices, outline=self.brushcolor, width=5,fill="")

    def drawpolygonend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
    
        # circle
    def drawcircle(self, event):
        if self.shapeid is not None:
            self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        radius = abs(self.lastx - event.x) + abs(self.lasty - event.y)
        x1, y1 = (self.lastx - radius), (self.lasty - radius)
        x2, y2 = (self.lastx + radius), (self.lasty + radius)
        self.shapeid = self.canvas.create_oval(x1, y1, x2, y2, outline=self.brushcolor, width=5)
        
    def drawcircleend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
        # rectangle
    def drawrectangle(self, event):
        if self.shapeid is not None:
            self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        x1, y1 = self.lastx, self.lasty
        x2, y2 = event.x, self.lasty
        x3, y3 = event.x, event.y
        x4, y4 = self.lastx, event.y

        vertices = [x1, y1, x2, y2, x3, y3, x4, y4]
        self.shapeid = self.canvas.create_polygon(vertices, outline=self.brushcolor, width=5,fill="")
        
    def drawrectangleend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None

        # square 
    def drawsquare(self,event):
             if self.shapeid is not None:
                self.canvas.delete(self.shapeid)

             if self.lastx is None:
                self.lastx, self.lasty = event.x, event.y
                return
             radius = abs(self.lastx - event.x) + abs(self.lasty - event.y)
             x1, y1 = (self.lastx - radius), (self.lasty - radius)
             x2, y2 = (self.lastx + radius), (self.lasty + radius)
             self.shapeid = self.canvas.create_rectangle( x1,y1, x2, y2, outline=self.brushcolor, width=5,fill="")
    def drawsquareend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
        # oval
    def drawoval(self, event):
        if self.shapeid is not None:
            self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        x1, y1 = self.lastx, self.lasty
        x2, y2 = event.x, event.y

        self.shapeid = self.canvas.create_oval(x1, y1, x2, y2, outline=self.brushcolor, width=5,fill="")

        
    def drawovalend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
        # hexagon
    def drawhexagon(self, event):
        if self.shapeid is not None:
           self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return

     # Calculate the coordinates for the six vertices of the hexagon
        x_center, y_center = self.lastx, self.lasty 
        side_length = abs(event.x - self.lastx)
  
        x1 = x_center - side_length
        y1 = y_center
        x2 = x_center - side_length / 2
        y2 = y_center - (side_length * (3 ** 0.5)) / 2
        x3 = x_center + side_length / 2
        y3 = y_center - (side_length * (3 ** 0.5)) / 2
        x4 = x_center + side_length
        y4 = y_center
        x5 = x_center + side_length / 2
        y5 = y_center + (side_length * (3 ** 0.5)) / 2
        x6 = x_center - side_length / 2
        y6 = y_center + (side_length * (3 ** 0.5)) / 2

        # Create the hexagon using the six vertices
        vertices = [x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6]
        self.shapeid = self.canvas.create_polygon(vertices, outline=self.brushcolor, width=5,fill="")
       
    def drawhexagonend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
        # pentagon
    def drawpentagon(self, event):
        if self.shapeid is not None:
            self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return

        # Calculate the coordinates for the five vertices of the pentagon
        x_center, y_center = self.lastx, self.lasty
        side_length = abs(event.x - self.lastx)

        angle = 360 / 5  # Angle between adjacent vertices of the pentagon
        vertices = []    # List to store the coordinates of the vertices

        for i in range(5):
            # Calculate the x and y coordinates for each vertex
            angle_rad = math.radians(72 + i * angle)  # Add 72 degrees to rotate the pentagon
            x = x_center + side_length * math.cos(angle_rad)
            y = y_center + side_length * math.sin(angle_rad)
            vertices.extend([x, y])

        # Create the pentagon using the five vertices
        self.shapeid = self.canvas.create_polygon(vertices, outline=self.brushcolor, width=5,fill="")

    def drawpentagonend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
        # triangle
    def drawtriangle(self, event):
        if self.shapeid is not None:
            self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return

        x1, y1 = self.lastx, self.lasty
        x2, y2 = event.x, event.y
        x3, y3 = 2 * self.lastx - event.x, event.y

        vertices = [x1, y1, x2, y2, x3, y3]
        self.shapeid = self.canvas.create_polygon(vertices, outline=self.brushcolor, width=5,fill="")

    def drawtriangleend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
        # star
    def drawstar(self, event):
        if self.shapeid is not None:
            self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return

        radius = min(abs(event.x - self.lastx), abs(event.y - self.lasty))
        x_center, y_center = self.lastx, self.lasty

        # Number of points in the star
        points = 5
        # Calculate the angle between each point
        angle = 2 * math.pi / (2 * points)

        # Calculate the coordinates for the points of the star
        vertices = []
        for i in range(points * 2):
            radius_value = radius if i % 2 == 0 else radius * 0.5
            x = x_center + radius_value * math.cos(i * angle)
            y = y_center + radius_value * math.sin(i * angle)
            vertices.extend([x, y])

        self.shapeid = self.canvas.create_polygon(vertices, outline=self.brushcolor, width=5,fill="")

    def drawstarend(self, event):
         self.lastx, self.lasty = None, None 
         self.shapeid = None
         # line
    def drawline(self, event):
        if self.shapeid is not None:
            self.canvas.delete(self.shapeid)

        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return

        x1, y1 = self.lastx, self.lasty
        x2, y2 = event.x, event.y
        x3, y3 = (self.lastx + event.x) / 2, (self.lasty + event.y) / 2

        vertices = [x1, y1, x2, y2, x3, y3]
        self.shapeid = self.canvas.create_polygon(vertices, outline=self.brushcolor, width=5,fill="")

    def drawlineend(self, event):
        self.lastx, self.lasty = None, None
        self.shapeid = None
        # select color
    def selectcolor(self):
        selectedcolor = colorchooser.askcolor()
        self.brushcolor = selectedcolor[1]
        # clear canvas
    def clearcanvas(self):
        self.canvas.delete("all")
        # main function
    def run(self):
        self.screen.mainloop()
        # brush
    def drawbrush(self, event):
        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        self.canvas.create_line(self.lastx, self.lasty, event.x, event.y, width=self.brushwidth, capstyle=ROUND,
                                fill=self.brushcolor)
        self.lastx, self.lasty = event.x, event.y

    def drawbrushend(self, event):
        self.lastx, self.lasty = None, None
    

    def drawbrushsize10(self, event):
        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        self.canvas.create_line(self.lastx, self.lasty, event.x, event.y, width=10, capstyle=ROUND,
                                fill=self.brushcolor)
        self.lastx, self.lasty = event.x, event.y

    def drawbrushendsize10(self, event):
        self.lastx, self.lasty = None, None

    def drawbrushsize15(self, event):
        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        self.canvas.create_line(self.lastx, self.lasty, event.x, event.y, width=15, capstyle=ROUND,
                                fill=self.brushcolor)
        self.lastx, self.lasty = event.x, event.y

    def drawbrushendsize15(self, event):
        self.lastx, self.lasty = None, None
        # eraser
    def eraser(self, event):
        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        self.canvas.create_line(self.lastx, self.lasty, event.x, event.y, width=5, capstyle=ROUND,
                                fill=self.erasercolor)
        self.lastx, self.lasty = event.x, event.y

    def eraserend(self, event):
        self.lastx, self.lasty = None, None
    def erasersize10(self, event):
        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        self.canvas.create_line(self.lastx, self.lasty, event.x, event.y, width=10, capstyle=ROUND,
                                fill=self.erasercolor)
        self.lastx, self.lasty = event.x, event.y

    def eraserendsize10(self, event):
        self.lastx, self.lasty = None, None

    def erasersize15(self, event):
        if self.lastx is None:
            self.lastx, self.lasty = event.x, event.y
            return
        self.canvas.create_line(self.lastx, self.lasty, event.x, event.y, width=15, capstyle=ROUND,
                                fill=self.erasercolor)
        self.lastx, self.lasty = event.x, event.y

    def eraserendsize15(self, event):
        self.lastx, self.lasty = None, None




PaintApp(800, 600, "Paint App").run()
