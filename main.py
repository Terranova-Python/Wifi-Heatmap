from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import time

pro_select = 0
ac_select = 0
MRX = 200
MRX2 = 200

root = Tk()
root.title('Unifi Heatmap')
root.iconbitmap('pics/bts.ico')
root.geometry('1400x800')
root.config(bg='#292929')

DHEIGHT = 310
DWIDTH = 210


class Fullscreen_Example:
    def __init__(self):
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)  
        self.fullScreenState = False
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)

        self.window.mainloop()

        
main_canvas = Canvas(root, width=1350, height=600, bg='#262626')
main_canvas.pack(pady=10)

right_canvas = Canvas(root, width=600, height=140, bg='#383838')
right_canvas.pack()

adjust_canvas = Canvas(root, width=250, height=140, bg='#383838')
adjust_canvas.place(relx=0.75, rely=0.8)


def change(e):
    print('Hover')

    img = Image.open('pics/apicon.png')
    smaller_ap = img.resize((90,62), Image.ANTIALIAS)
    new_small = ImageTk.PhotoImage(smaller_ap)
    imglabel.config(image=new_small)
    imglabel.image = new_small

def changeback(e):
    print('og')
    img = PhotoImage(file='pics/apicon.png')  # PRO
    imglabel.config(image=img)
    imglabel.image = img

apps = []


def move2(e):
    x = 600//2
    y = 400//2
    global bg3, resized_bg3, new_bg3, img7, MRX, lt_location, lt_location2

    lt_location = e.x
    lt_location2 = e.y

    bg3 = Image.open('pics/heatmap2.png')
    resized_bg3 = bg3.resize((MRX,MRX), Image.ANTIALIAS)
    new_bg3 = ImageTk.PhotoImage(resized_bg3)
    canvas6.create_image(e.x,e.y,image=new_bg3)

    img7 = PhotoImage(file='pics/macpro.png')
    my_image = canvas6.create_image(e.x,e.y, image=img7)
    my_label.config(text='Coordinates: x = ' + str(e.x) + ' y = ' + str(e.y))


def pro_wifi_adjust():
    global MRX
    mrx_amount = vertical_wifi.get()
    print(MRX, mrx_amount)

    if MRX <= 650:
        MRX += mrx_amount
        global bg2,resized_bg2, new_bg2, canvas6, pro_ap_locationx, pro_ap_locationy, img6, my_image
        bg2 = Image.open('pics/heatmap2.png')
        resized_bg2 = bg2.resize((MRX,MRX), Image.ANTIALIAS)
        new_bg2 = ImageTk.PhotoImage(resized_bg2)
        canvas6.create_image(pro_ap_locationx,pro_ap_locationy,image=new_bg2)

        img6 = PhotoImage(file='pics/macpro.png')
        my_image = canvas6.create_image(pro_ap_locationx, pro_ap_locationy, image=img6)

    else:
        pass

def lr_wifi_size():
    global MRX
    mrx_amount = vertical_lr_wifi.get()
    print(MRX, mrx_amount)

    if MRX <= 650:
        MRX += mrx_amount
        global bg3,resized_bg3, new_bg3, canvas6, lt_location, lt_location2, img7, my_image
        bg3 = Image.open('pics/heatmap2.png')
        resized_bg3 = bg3.resize((MRX,MRX), Image.ANTIALIAS)
        new_bg3 = ImageTk.PhotoImage(resized_bg3)
        canvas6.create_image(lt_location,lt_location2,image=new_bg3)

        img7 = PhotoImage(file='pics/macpro.png')
        my_image = canvas6.create_image(lt_location, lt_location2, image=img7)

    else:
        pass

def move(e):
    x = 600//2
    y = 400//2
    global bg2, resized_bg2, new_bg2, img6, MRX, pro_ap_locationx, pro_ap_locationy
    pro_ap_locationx = e.x
    pro_ap_locationy = e.y

    bg2 = Image.open('pics/heatmap2.png')
    resized_bg2 = bg2.resize((MRX,MRX), Image.ANTIALIAS)
    new_bg2 = ImageTk.PhotoImage(resized_bg2)
    canvas6.create_image(e.x,e.y,image=new_bg2)

    img6 = PhotoImage(file='pics/macpro.png')
    my_image = canvas6.create_image(e.x,e.y, image=img6)
    my_label.config(text='Coordinates: x = ' + str(e.x) + ' y = ' + str(e.y))

    
def pro_func(event):
    global pro_select
    pro_select += 1

    if pro_select >= 1:
        canvas6.bind('<B1-Motion>', move)

        
def pro_func2(event):
    global pro_select
    pro_select += 1

    if pro_select >= 1:
        canvas6.bind('<B1-Motion>', move2)

        
def donothing():
    pass


def adjust_size():   #nMap size
    global bg1, resized_bg, new_bg, rx, ry, filename
    rxz, ryz = 620,300  # Crops Image

    rx = int(vertical_maps.get()) + 100
    ry = int(vertical_maps.get())
    bg1 = Image.open(filename)
    resized_bg = bg1.resize((rx,ry), Image.ANTIALIAS)
    new_bg = ImageTk.PhotoImage(resized_bg)
    canvas6.create_image(rxz,ryz,image=new_bg)

    
def importsite():
    global filename
    filename = filedialog.askopenfilename(initialdir="C:", title="Select File")
    filetypes=(("executables","*.exe"), ("all files", "*.*"))
    apps.append(filename)
    rxz, ryz = 620,300  # Crops Image

    global canvas6
    canvas6 = Canvas(main_canvas, height=8, width=12, bg='#262626')
    canvas6.place(relx=.0,rely=.0,relheight=1,relwidth=1)
    
    global bg1, resized_bg, new_bg, rx, ry
    
    bg1 = Image.open(filename)
    rx, ry = bg1.size
    resized_bg = bg1.resize((rx,ry), Image.ANTIALIAS)
    new_bg = ImageTk.PhotoImage(resized_bg)
    canvas6.create_image(rxz,ryz,image=new_bg)

my_label = Label(root, text='', bg='#292929', fg='white')
my_label.pack(side='bottom')

img = PhotoImage(file='pics/apicon.png')  # PRO
imglabel = Label(right_canvas, image=img, bg='#383838')
imglabel.bind('<Button-1>', pro_func)
imglabel.bind('<Enter>', change)
imglabel.bind('<Leave>', changeback)
imglabel.place(relx=0.03, rely=0.13)

img2 = PhotoImage(file='pics/macpro.png')   # LITE
imglabel2 = Label(right_canvas, image=img2, bg='#383838')
imglabel2.bind('<Button-1>', pro_func2)
imglabel2.place(relx=0.28, rely=0.26)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import", command=importsite)
filemenu.add_command(label="save", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="info", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

acpro_label = Label(right_canvas, text='Unifi AC-AP-PRO', font=('helvetica', 10), bg='#383838', fg='white')
acpro_label.place(relx=0.02, rely=0.7)

ac_label = Label(right_canvas, text='Unifi AC-AP-LR', font=('helvetica', 10), bg='#383838', fg='white')
ac_label.place(relx=0.26, rely=0.7)

blankpage = Label(main_canvas, text='Start by importing building floor plans\n Then Select your AP and drag onto the site photo to see the range', font=('helvetica', 15), fg='white', bg='#262626')
blankpage.place(relx=0.27, rely=0.5)

height_entry = Button(adjust_canvas, text=' Apply ', command=adjust_size)
height_entry.place(relx=0.315, rely=.79)

ap_lr_wifi = Button(adjust_canvas, text=' Apply ', command=lr_wifi_size)
ap_lr_wifi.place(relx=0.54, rely=.79)

Wifi_adjust_button = Button(adjust_canvas, text=' Apply ', command=pro_wifi_adjust)
Wifi_adjust_button.place(relx=0.745, rely=.79)


vertical_wifi = Scale(adjust_canvas, from_= 50, to=-50)
vertical_wifi.place(relx=0.75, rely=.05)

vertical_lr_wifi = Scale(adjust_canvas, from_= 50, to=-50)
vertical_lr_wifi.place(relx=0.549, rely=.05)

vertical_maps = Scale(adjust_canvas, from_= 600, to=400)
vertical_maps.place(relx=0.32, rely=.05)

root.mainloop()
