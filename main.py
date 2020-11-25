from tkinter import *
from tkinter import ttk
import PIL
from PIL import ImageTk, Image
from tkinter import filedialog

pro_select = 0
ac_select = 0

root = Tk()
root.title('BTS Unifi Heatmap')
root.iconbitmap('pics/bts.ico')
root.geometry('700x600')
root.config(bg='#292929')

main_canvas = Canvas(root, width=600, height=400, bg='white')
main_canvas.pack(pady=10)

right_canvas = Canvas(root, width=600, height=120, bg='#383838')
right_canvas.pack()


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

def move(e):
    x = 600//2
    y = 400//2

    global img5
    global img6
    global count

    img5 = PhotoImage(file='pics/heatmap2.png')
    my_image2 = canvas6.create_image(e.x,e.y, image=img5)

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


def importsite():
    apps = []
    filename = filedialog.askopenfilename(initialdir="C:", title="Select File")
    filetypes=(("executables","*.exe"), ("all files", "*.*"))
    apps.append(filename)
    
    global canvas6
    global photo6
    canvas6 = Canvas(main_canvas, height=8, width=12, bg='white')
    photo6 = ImageTk.PhotoImage(file=apps[0])
    item6 = canvas6.create_image(310, 210, image=photo6)
    canvas6.place(relx=0,rely=0,relheight=1,relwidth=1)


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

ac_label = Label(right_canvas, text='Unifi AC-AP lite', font=('helvetica', 10), bg='#383838', fg='white')
ac_label.place(relx=0.25, rely=0.7)

blankpage = Label(main_canvas, text='Start by importing building floor plans\n Then Select your AP and drag onto the site photo to see the range', font=('helvetica', 12), bg='white')
blankpage.place(relx=0.1, rely=0.5)

root.mainloop()
