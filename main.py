from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog

pro_select = 0
ac_select = 0
MRX = 200

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

main_canvas = Canvas(root, width=1350, height=600, bg='white')
main_canvas.pack(pady=10)

right_canvas = Canvas(root, width=600, height=120, bg='#383838')
right_canvas.pack()

apps = []
def move2(e):
    x = 600//2
    y = 400//2

    global img8
    global img55

    img8 = PhotoImage(file='pics/heatmap3.png')

    my_image8 = canvas6.create_image(e.x,e.y, image=img8)

    img55 = PhotoImage(file='pics/macpro.png')
    my_image55 = canvas6.create_image(e.x,e.y, image=img55)

    my_label.config(text='Coordinates: x = ' + str(e.x) + ' y = ' + str(e.y))

def pro_wifi_adjust(e):
    global MRX
    text_num = height_entry2.get()
    mrx_num = int(text_num)
    MRX += mrx_num

def move(e):
    x = 600//2
    y = 400//2
    global bg2, resized_bg2, new_bg2, img6, MRX

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


def adjust_size(event):
    global bg1, resized_bg, new_bg, rx, ry, filename
    rxz, ryz = 620,300  # Crops Image

    rx = int(height_entry.get())
    ry = int(height_entry.get())
    bg1 = Image.open(filename)
    resized_bg = bg1.resize((rx,ry), Image.ANTIALIAS)
    new_bg = ImageTk.PhotoImage(resized_bg)
    canvas6.create_image(rxz,ryz,image=new_bg)

def importsite():
    global filename
    filename = filedialog.askopenfilename(initialdir="C:", title="Select File")
    filetypes=(("executables","*.exe"), ("all files", "*.*"))
    apps.append(filename)
    #rx, ry = 300,250  # resizes image
    rxz, ryz = 620,300  # Crops Image

    global canvas6
    canvas6 = Canvas(main_canvas, height=8, width=12, bg='white')
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

blankpage = Label(main_canvas, text='Start by importing building floor plans\n Then Select your AP and drag onto the site photo to see the range', font=('helvetica', 15), bg='white')
blankpage.place(relx=0.33, rely=0.5)

height_entry = Entry(right_canvas, width=4)
height_entry.bind('<Return>', adjust_size)
height_entry.place(relx=0.9, rely=.1)

height_entry2 = Entry(right_canvas, width=4)
height_entry2.bind('<Return>', pro_wifi_adjust)
height_entry2.place(relx=0.9, rely=.4)

root.mainloop()
