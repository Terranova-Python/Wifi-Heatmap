from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import scapy.all as scapy
import re
import argparse

MRX = 200
MRX2 = 200

root = Tk()
root.title('Unifi Heatmap')
root.iconbitmap('pics/heatmapicon.ico')
root.geometry('1400x800')
root.config(bg='#292929')

DHEIGHT = 310
DWIDTH = 210

###### COLORS FOR USE ######
DGRAY = '#262626'
LGRAY = '#383838'
PBLUE = '#01255c'
RGRAY = '#292929'
OWHITE = '#d4d4d4'


def change_pro(e):
    img = Image.open('pics/apicon.png')
    smaller_ap = img.resize((90,62), Image.ANTIALIAS)
    new_small = ImageTk.PhotoImage(smaller_ap)
    imglabel.config(image=new_small)
    imglabel.image = new_small


def changeback_pro(e):
    img = PhotoImage(file='pics/apicon.png')  # PRO
    imglabel.config(image=img)
    imglabel.image = img


def pro_wifi_adjust():
    global bg2,resized_bg2, new_bg2, canvas6, pro_ap_locationx, pro_ap_locationy, img6, my_image, MRX
    mrx_amount = vertical_wifi.get()

    if MRX <= 650:
        MRX += mrx_amount
        bg2 = Image.open('pics/heatmap2.png')
        resized_bg2 = bg2.resize((MRX,MRX), Image.ANTIALIAS)
        new_bg2 = ImageTk.PhotoImage(resized_bg2)
        canvas6.create_image(pro_ap_locationx,pro_ap_locationy,image=new_bg2)
        img6 = PhotoImage(file='pics/macpro.png')
        my_image = canvas6.create_image(pro_ap_locationx, pro_ap_locationy, image=img6)

    else:
        pass


def lr_wifi_size():
    global bg3,resized_bg3, new_bg3, canvas6, lt_location, lt_location2, img7, my_image, MRX2
    mrx_amount = vertical_lr_wifi.get()

    if MRX2 <= 650:
        MRX2 += mrx_amount
        bg3 = Image.open('pics/heatmap2.png')
        resized_bg3 = bg3.resize((MRX2,MRX2), Image.ANTIALIAS)
        new_bg3 = ImageTk.PhotoImage(resized_bg3)
        canvas6.create_image(lt_location,lt_location2,image=new_bg3)

        img7 = PhotoImage(file='pics/macpro.png')
        my_image = canvas6.create_image(lt_location, lt_location2, image=img7)

    else:
        pass


def move3(e):
    x = 600//2
    y = 400//2
    global bg4, resized_bg4, new_bg4, img4, MRX, ubg_location, ubg_location2

    ubg_location = e.x
    ubg_location2 = e.y

    bg4 = Image.open('pics/heatmap2.png')
    resized_bg4 = bg4.resize((MRX,MRX), Image.ANTIALIAS)
    new_bg4 = ImageTk.PhotoImage(resized_bg4)
    canvas6.create_image(e.x,e.y,image=new_bg4)

    img4 = PhotoImage(file='pics/UWB-XG.png')
    my_image = canvas6.create_image(e.x,e.y, image=img4)


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


def move(e):
    global bg2, resized_bg2, new_bg2, img6, MRX, pro_ap_locationx, pro_ap_locationy
    x = 600//2
    y = 400//2
    pro_ap_locationx = e.x
    pro_ap_locationy = e.y

    bg2 = Image.open('pics/heatmap2.png')
    resized_bg2 = bg2.resize((MRX,MRX), Image.ANTIALIAS)
    new_bg2 = ImageTk.PhotoImage(resized_bg2)
    canvas6.create_image(e.x,e.y,image=new_bg2)

    img6 = PhotoImage(file='pics/macpro.png')
    my_image = canvas6.create_image(e.x,e.y, image=img6)


def pro_func(event):
    canvas6.bind('<B1-Motion>', move)

def pro_func2(event):
    canvas6.bind('<B1-Motion>', move2)

def pro_func3(event):
    canvas6.bind('<B1-Motion>', move3)

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
    global filename, canvas6, bg1, resized_bg, new_bg, rx, ry
    filename = filedialog.askopenfilename(initialdir="C:", title="Select File")
    filetypes=(("executables","*.exe"), ("all files", "*.*"))
    rxz, ryz = 620,300  # Crops Image

    canvas6 = Canvas(main_canvas, height=8, width=12, bg=DGRAY)
    canvas6.place(relx=.0,rely=.0,relheight=1,relwidth=1)

    bg1 = Image.open(filename)
    rx, ry = bg1.size
    resized_bg = bg1.resize((rx,ry), Image.ANTIALIAS)
    new_bg = ImageTk.PhotoImage(resized_bg)
    canvas6.create_image(rxz,ryz,image=new_bg)

def scan_ip(event):
    T2.delete('1.0', END)

    def scan(ip):
        arp_packet = scapy.ARP(pdst=ip)
        broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_broadcast_packet = broadcast_packet/arp_packet
        answered_list = scapy.srp(arp_broadcast_packet, timeout=1, verbose=False)[0]
        client_list = []

        for element in answered_list:
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
            client_list.append(client_dict)
        
        return client_list


    def print_result(scan_list):
        result_head = "IP\t\tMAC\n---------------------------------"
        T2.insert('end', result_head + '\n')

        if scan_list:
            for client in scan_list:
                scan_results = client["ip"] + "\t\t" + client["mac"]
                T2.insert('end', scan_results + '\n')

                if '04:18:d6' in client['mac']:   # Check condition - If Mac contains x, highlight the line that that Mac is on...
                    c_l = scan_list.index(client) + 3
                    start_cl, end_cl = str(c_l) + ".0" , str(c_l) + ".40"
                    T2.tag_add('start', start_cl, end_cl)
                    T2.tag_configure('start', foreground='#40c773')

        else:
            T2.insert('end', 'No Results!\nCheck subnet format, or scan again.')
            T2.tag_add("start", "3.0", "4.35")
            T2.tag_configure("start", foreground="red")

    result_list = scan(ip_entry.get())
    print_result(result_list)


main_canvas = Canvas(root, width=1350, height=600, bg=DGRAY)
main_canvas.pack(pady=10)

right_canvas = Canvas(root, width=600, height=140, bg=LGRAY)
right_canvas.place(relx=0.3, rely=0.8)

adjust_canvas = Canvas(root, width=300, height=140, bg=LGRAY)
adjust_canvas.place(relx=0.72, rely=0.8)

ip_canvas = Canvas(root, width=300, height=140, bg=LGRAY)
ip_canvas.place(relx=0.08, rely=0.8)

ip_label = Label(ip_canvas, bg=LGRAY, fg=OWHITE, text='Format: x.x.x.x/x')
ip_label.place(relx=0.61, rely=0.0115)

msg = StringVar()  
T2 = Text(ip_canvas, bg=PBLUE, fg='white')
T2.place(relx=0.005, rely=0.13, relheight=0.9, relwidth=0.989)

img = PhotoImage(file='pics/apicon.png')  # PRO
imglabel = Label(right_canvas, image=img, bg=LGRAY)
imglabel.bind('<Button-1>', pro_func)
imglabel.bind('<Enter>', change_pro)
imglabel.bind('<Leave>', changeback_pro)
imglabel.place(relx=0.03, rely=0.13)

img2 = PhotoImage(file='pics/macpro.png')   # LITE
imglabel2 = Label(right_canvas, image=img2, bg=LGRAY)
imglabel2.bind('<Button-1>', pro_func2)
imglabel2.place(relx=0.28, rely=0.26)

img3 = PhotoImage(file='pics/UWB-XG.png')   # UWB-XG
imglabel3 = Label(right_canvas, image=img3, bg=LGRAY)
imglabel3.bind('<Button-1>', pro_func3)
imglabel3.place(relx=0.48, rely=0.13)

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

acpro_label = Label(right_canvas, text='Unifi AC-AP-PRO', font=('helvetica', 10), bg=LGRAY, fg='white')
acpro_label.place(relx=0.02, rely=0.7)

ac_label = Label(right_canvas, text='Unifi AC-AP-LR', font=('helvetica', 10), bg=LGRAY, fg='white')
ac_label.place(relx=0.26, rely=0.7)

blankpage = Label(main_canvas, text='Start by importing building floor plans\n Then Select your AP and drag onto the site photo to see the range', font=('helvetica', 15), fg='white', bg=DGRAY)
blankpage.place(relx=0.27, rely=0.5)

height_entry = Button(adjust_canvas, text=' Apply ', command=adjust_size)
height_entry.place(relx=0.315, rely=.79)

ap_lr_wifi = Button(adjust_canvas, text=' Apply ', command=lr_wifi_size)
ap_lr_wifi.place(relx=0.54, rely=.79)

Wifi_adjust_button = Button(adjust_canvas, text=' Apply ', command=pro_wifi_adjust)
Wifi_adjust_button.place(relx=0.745, rely=.79)

ip_entry = Entry(ip_canvas, width=30)
ip_entry.bind('<Return>', scan_ip)
ip_entry.place(relx=0.001, rely=.001)

vertical_wifi = Scale(adjust_canvas, from_= 50, to=-50)
vertical_wifi.place(relx=0.75, rely=.05)

vertical_lr_wifi = Scale(adjust_canvas, from_= 50, to=-50)
vertical_lr_wifi.place(relx=0.549, rely=.05)

vertical_maps = Scale(adjust_canvas, from_= 600, to=400)
vertical_maps.place(relx=0.32, rely=.05)

root.mainloop()
