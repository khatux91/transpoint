#!/usr/bin/python
from __future__ import division
import wx
from wx.lib.imagebrowser import *
import Image, os


DEFAULT_WIDTH  = 800
DEFAULT_HEIGHT = 600  #height and width of program window (ratio of 1.33)

TITLE          = "A simple app to convert a color to transparency"
ABOUT_TITLE    = "About"
ABOUT_BODY     = "A simple application to make image background \n" \
            "transparent for incorporation into presentation slides \n" \
            "Author: Raja S. May 2007 \n rajajs@gmail.com"

ID_APP         = wx.NewId()
ID_ABOUT       = wx.NewId()
ID_DISPLAY     = wx.NewId()
ID_SELECT      = wx.NewId()
ID_SAVE        = wx.NewId()
ID_EXIT        = wx.NewId()
ID_CONVERT     = wx.NewId()
ID_INVERT      = wx.NewId()
ID_LOW         = wx.NewId()
ID_MEDIUM      = wx.NewId()
ID_HIGH        = wx.NewId()
ID_RESIZE      = wx.NewId()
ID_NORESIZE    = wx.NewId()

class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent):
        wx.StatusBar.__init__(self, parent, -1)
        self.SetFieldsCount(3)
        self.SetStatusWidths([-4, -2,-1])
        
        # take care when the window is resized
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        # create the static bitmap of the required size
        rect = self.GetFieldRect(2)
        self.bmp_size = rect.GetSize()       
        self.StaticBitmap = wx.StaticBitmap(self,-1,self.MakeBitmap(wx.Color(125,125,125)),\
        (rect.GetTopLeft().Get()[0]+2,rect.GetTopLeft().Get()[1]+2),rect.GetSize())
        
    def Reposition(self):    
        rect = self.GetFieldRect(2)
        self.bmp_size = rect.GetSize()       
        self.StaticBitmap.SetPosition((rect.GetTopLeft().Get()[0]+2,rect.GetTopLeft().Get()[1]+2))
        self.StaticBitmap.SetSize(rect.GetSize())
        self.StaticBitmap.SetBitmap(self.MakeBitmap(self.color))
        
    def OnSize(self, evt):
        self.Reposition()    
    
    def SetSelectedColor(self,color):
        self.color = color
        self.StaticBitmap.SetBitmap(self.MakeBitmap(color))
        self.SetStatusText("Selected Color", 1)
    
    def MakeBitmap(self, colour):
        bmp = wx.EmptyBitmap(self.bmp_size.GetWidth()-2,self.bmp_size.GetHeight()-2)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(colour))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        return bmp         

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):

        self.__lastdir__ = os.getcwd() 
        self.r1 = 255; self.g1 = 255; self.b1 = 255 #initial values for color to remove (white)
        
        wx.Frame.__init__(self, parent, ID_APP, title,wx.DefaultPosition,wx.Size(DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.sb = CustomStatusBar(self)
        self.SetStatusBar(self.sb)
        self.sb.SetSelectedColor(wx.Color(self.r1,self.g1,self.b1))

        FileMenu = wx.Menu()
        FileMenu.Append(ID_DISPLAY,"&Open image","Open an image")
        FileMenu.Append(ID_SAVE,"&Save image","Save the image")
        FileMenu.AppendSeparator()
        FileMenu.Append(ID_EXIT,"E&xit","Terminate the program")
        
        EditMenu = wx.Menu()
        EditMenu.Append(ID_SELECT,"&Select colour","Select colour to make transparent")
        EditMenu.Append(ID_CONVERT,"&Convert","Converting selected color to transparent... Please wait")
        EditMenu.Append(ID_INVERT,"&Convert and invert","Converting selected color to transparent... Please wait")
        
        ChangeMenu = wx.Menu()
        ChangeMenu.AppendRadioItem(ID_LOW,"&Low","Low threshold to identify similar color")
        ChangeMenu.AppendRadioItem(ID_MEDIUM,"&Medium","Medium threshold to identify similar color")
        ChangeMenu.AppendRadioItem(ID_HIGH,"&High","High threshold to identify similar color")

        OutputMenu = wx.Menu()
        OutputMenu.AppendRadioItem(ID_RESIZE,"&Resize","Make image smaller if required")
        OutputMenu.AppendRadioItem(ID_NORESIZE,"&Noresize","Do not change image size")
        
        HelpMenu = wx.Menu()
        HelpMenu.Append(ID_ABOUT,"&About","More information about this program")

        menuBar = wx.MenuBar()
        menuBar.Append(FileMenu, "&File");
        menuBar.Append(EditMenu, "&Edit");
        menuBar.Append(ChangeMenu, "&Threshold");
        menuBar.Append(OutputMenu,"&Size")
        menuBar.Append(HelpMenu, "&Help");
        self.SetMenuBar(menuBar)
        
        tsize = (16,16)
        
        self.toolbar = self.CreateToolBar(wx.TB_HORIZONTAL |
                                          wx.NO_BORDER | wx.TB_FLAT)

        self.toolbar.AddSimpleTool(ID_DISPLAY,
                                   wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize),
                                   "Open")
        self.toolbar.AddSimpleTool(ID_SAVE,
                                   wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize),
                                   "Save")
        self.toolbar.AddSeparator()
        
        self.toolbar.AddSimpleTool(ID_SELECT,
                                   wx.Bitmap("select.png", wx.BITMAP_TYPE_PNG), 
                                   "Select")                
        self.toolbar.AddSimpleTool(ID_CONVERT,
                                   wx.Bitmap("convert.bmp", wx.BITMAP_TYPE_BMP),
                                   "Convert")
        self.toolbar.AddSimpleTool(ID_INVERT,
                                   wx.Bitmap("invert.bmp", wx.BITMAP_TYPE_BMP), 
                                   "Convert and Invert")
        
        self.toolbar.AddSeparator()
        self.toolbar.AddSimpleTool(ID_EXIT,
                           wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, tsize),
                           "Exit")

        self.toolbar.Realize()

        self.__panel__ = wx.Panel(self)

        wx.EVT_MENU(self, ID_ABOUT,   self.About)
        wx.EVT_MENU(self, ID_DISPLAY, self.DisplayImage)
        wx.EVT_MENU(self, ID_EXIT,    self.Quit)
        wx.EVT_MENU(self, ID_SELECT,  self.SelectColor)
        wx.EVT_MENU(self, ID_CONVERT, self.Convert)
        wx.EVT_MENU(self, ID_INVERT, self.Invert)
        wx.EVT_MENU(self, ID_LOW, self.LowThresh)
        wx.EVT_MENU(self, ID_MEDIUM, self.MediumThresh)
        wx.EVT_MENU(self, ID_HIGH, self.HighThresh)
        wx.EVT_MENU(self, ID_SAVE, self.SaveImage)
        wx.EVT_MENU(self, ID_RESIZE, self.Resize)
        wx.EVT_MENU(self, ID_NORESIZE, self.Noresize)
        
        
        self.SELECT_FLAG = "FALSE"  #flag determines if mouse click must be processed
        self.IMAGE_SELECTED = "FALSE" #flags image selection
        self.IMAGE_CONVERTED = "FALSE" #flags image conversion
        self.wildcard = "PNG files (*.png)|*.png|All files (*.*)|*.*"
        self.Threshold = 15    #threshold for medium
        self.RESIZE_FLAG = "TRUE"
        self.BITMAP_FLAG = "NOexists"
        self.SlideHeight = 720
        self.SlideWidth  = 960 #resized figure
                
        ChangeMenu.Check(ID_MEDIUM,1)

    def Alert(self,title,msg="Undefined"):
        dlg = wx.MessageDialog(self, msg,title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def About(self, event):
        self.Alert(ABOUT_TITLE,ABOUT_BODY)
    
    def Quit(self, event):
        self.Close(1)
        
    def LowThresh(self,event):
        self.Threshold = 6
        #print "Low"
        
    def MediumThresh(self,event):
        self.Threshold = 15
        #print "Medium"

    def HighThresh(self,event):
        self.Threshold = 36
        #print "High"
        
    def Resize(self,event):
        self.RESIZE_FLAG = "TRUE"   
    
    def Noresize(self,event):
        self.RESIZE_FLAG = "FALSE"       
        
    def ScaleImage(self,im,width,height): #scale image to smaller than w x h, but maintain aspect ratio
        AspectRatio = width/height
        w,h = im.size
 #       print im.size
        hNorm = h/AspectRatio
        if hNorm < w:
            ShrinkRatio = w/width
        else:
            ShrinkRatio = h/height
#        print ShrinkRatio
        if ShrinkRatio > 1:
            im = im.resize((int(w/ShrinkRatio),int(h/ShrinkRatio)))
  #      print im.size
        return im
        
    def DisplayImage(self,event):
        img = self.ChooseImage()
        if img == None:
           self.SetStatusText("Image select cancelled by user.",0)
           return 0
    
        bmp = self.GetBmpfromPIL(img)
        if bmp == None:
           return 0
        self.IMAGE_SELECTED = "TRUE"
        
        self.__lastdir__ = os.path.dirname(img)
        self.SetStatusText(os.path.basename(img))

        if self.BITMAP_FLAG == "exists":
            self.StaticBitmap.SetBitmap(bmp)
#            print "bitmap updated"
        else:
            self.StaticBitmap = wx.StaticBitmap(self.__panel__,-1,bmp,wx.Point(0,0),
             wx.Size(DEFAULT_WIDTH,DEFAULT_HEIGHT))
            self.BITMAP_FLAG = "exists"
#            print "bitmap created"
                
        wx.EVT_LEFT_UP(self.StaticBitmap, self.OnButtonUp) #mouse left button up is bound to bitmap

    def ChooseImage(self):
        dlg = ImageDialog(self,self.__lastdir__);
        if dlg.ShowModal() == wx.ID_OK:
           return dlg.GetFile()

    def SaveImage(self, event):
        if self.IMAGE_CONVERTED == "FALSE":
            self.Alert("Warning", "Image not processed yet")
        elif self.IMAGE_SELECTED == "FALSE":
            self.Alert("Warning", "No image selected yet")
        else:
            dlg = wx.FileDialog(self, "Save image as...", os.getcwd(),
                               style=wx.SAVE | wx.OVERWRITE_PROMPT,
                               wildcard = self.wildcard)
            if dlg.ShowModal() == wx.ID_OK:
                filename = dlg.GetPath()
                if not os.path.splitext(filename)[1]:
                    filename = filename + '.png'
                self.filename = filename
                self.SaveFile()
            dlg.Destroy()
        
    def SaveFile(self):
        self.im.save(self.filename)
        self.IMAGE_SELECTED = "FALSE" #flags image selection
        self.IMAGE_CONVERTED = "FALSE" 
        self.SetStatusText("Image saved")
    
    def GetBmpfromPIL( self,img ):
        self.im_original = Image.open( img, 'r')
        if self.RESIZE_FLAG == "TRUE":
            self.im_original = self.ScaleImage(self.im_original,self.SlideWidth,self.SlideHeight)
        #self.imsmall = self.im_original.resize((DEFAULT_WIDTH,DEFAULT_HEIGHT))
#        print "before ",self.im_original.size
        self.imsmall = self.ScaleImage(self.im_original,DEFAULT_WIDTH,DEFAULT_HEIGHT)
        #print "before ",self.imsmall.mode
#        print self.imsmall.size
        self.imsmall.convert("RGB") #if it is in greyscale
        #print "after ",self.imsmall.mode
        image = apply( wx.EmptyImage, self.imsmall.size )
        image.SetData( self.imsmall.convert( "RGB").tostring() )
        #image.SetAlphaData(self.imsmall.convert("RGBA").tostring()[3::4])
        return image.ConvertToBitmap() # wxBitmapFromImage(image)
    
    def SelectColor(self,event):
        if self.IMAGE_SELECTED == "FALSE":
            self.Alert("Warning","No image selected yet")
        elif self.IMAGE_CONVERTED == "TRUE":
            self.Alert("Warning","Figure processed already, reopen image or open new image")
        else:
            self.SELECT_FLAG = 1
            self.__panel__.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
        
    def OnButtonUp(self,event):
        pt = event.GetPosition()
                       
        if self.SELECT_FLAG == 1:
#            print self.imsmall.mode
                        
            #if the original image is RGBA, imsmall is still RGBA - therefore...
            try:
                self.r1,self.g1,self.b1 = self.imsmall.getpixel((pt.x,pt.y))
            except ValueError:
                self.r1,self.g1,self.b1,dummy = self.imsmall.getpixel((pt.x,pt.y))
                
            self.sb.SetSelectedColor(wx.Color(self.r1,self.g1,self.b1))
            #print "selected coords ",self.xcoord,self.ycoord
            self.SELECT_FLAG = 0
            self.__panel__.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

    def Invert(self,event):
        self.ConvertTrans(self,"invert")
    
    def Convert(self,event):
        self.ConvertTrans(self,"noinvert")
    
    def ConvertTrans(self,event,invertflag):   # this is where all the action happens
        if self.IMAGE_SELECTED == "FALSE":
            self.Alert("Warning","No image selected yet")
        else:
            self.SetStatusText("please wait, converting...")
            self.im = self.im_original.convert("RGBA") #add an alpha channel
            maxx,maxy = self.im.size
            
            for x in range(maxx):
                for y in range(maxy):
                    r,g,b,a = self.im.getpixel((x,y))
                    if invertflag == "noinvert":
                        if abs(self.r1-r)<self.Threshold and abs(self.g1-g)<self.Threshold and abs(self.b1-b)<self.Threshold:
                            self.im.putpixel((x,y),(r,g,b,0))
                    else:
                        if abs(self.r1-r)<self.Threshold and abs(self.g1-g)<self.Threshold and abs(self.b1-b)<self.Threshold:
                            self.im.putpixel((x,y),(256-r,256-g,256-b,0))
                        else:
                            self.im.putpixel((x,y),(256-r,256-g,256-b,a))
            
            imDisplay = self.ScaleImage(self.im,DEFAULT_WIDTH,DEFAULT_HEIGHT)
           
            bg = Image.open("bg.png",'r')
            bg.paste(imDisplay,(0,0),imDisplay)
            imDisplay = bg
            
            image = apply( wx.EmptyImage, imDisplay.size )
            image.SetData( imDisplay.convert( "RGB").tostring() )
            image.SetAlphaData(imDisplay.convert("RGBA").tostring()[3::4])
            transbmp = image.ConvertToBitmap()
            self.StaticBitmap.SetBitmap(transbmp)
            
            self.SetStatusText("")
            self.IMAGE_CONVERTED = "TRUE"

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, ID_APP, TITLE)
        frame.Show(1)
        self.SetTopWindow(frame)
        return 1

app = MyApp(0)
app.MainLoop()