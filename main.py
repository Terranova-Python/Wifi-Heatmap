from tkinter import *
from PIL import ImageTk, Image, ImageDraw
from tkinter import filedialog
import scapy.all as scapy
import re
import argparse
import cv2
import numpy as np
import subprocess
import webbrowser

MRX, MRX2, MRX3 = 250, 250, 250       # static Sizes of Wifi frequency
CANVW, CANVH = 675,300

root = Tk()
root.title('Heatwave | Version 1.0.0 | Terranova Technology')
root.iconbitmap('heatmapicon.ico')
root.geometry('1400x800')
root.config(bg='#1F1F1F')

###### COLORS FOR USE ######
DGRAY = '#262626'
LGRAY = '#383838'
PBLUE = '#01255c'
OWHITE = '#d4d4d4'

def change_pro(e):
    img = Image.open('pics/apicon.png')
    smaller_ap = img.resize((95,65), Image.ANTIALIAS)
    new_small = ImageTk.PhotoImage(smaller_ap)
    imglabel.config(image=new_small)
    imglabel.image = new_small

def changeback_pro(e):
    img = PhotoImage(file='pics/apicon.png')  # PRO
    imglabel.config(image=img)
    imglabel.image = img

def change_lr(e):
    img2 = Image.open('pics/macpro.png')
    smaller_ap2 = img2.resize((55,38), Image.ANTIALIAS)
    new_small2 = ImageTk.PhotoImage(smaller_ap2)
    imglabel2.config(image=new_small2)
    imglabel2.image = new_small2

def changeback_lr(e):
    img2 = PhotoImage(file='pics/macpro.png')  # PRO
    imglabel2.config(image=img2)
    imglabel2.image = img2

def change_ubg(e):
    img3 = Image.open('pics/UWB-XG.png')
    smaller_ap3 = img3.resize((93,85), Image.ANTIALIAS)
    new_small3 = ImageTk.PhotoImage(smaller_ap3)
    imglabel3.config(image=new_small3)
    imglabel3.image = new_small3

def changeback_ubg(e):
    img3 = PhotoImage(file='pics/UWB-XG.png')  # PRO
    imglabel3.config(image=img3)
    imglabel3.image = img3

uwb_list = [0,0,0]
def uwb_wifi_adjust(event):
    global bg5,resized_bg5, new_bg5, canvas6, uwb_location, uwb_location2, img5, my_image, MRX3

    uwb_list.append(int(event))
    e4 = uwb_list[-1]
    pe4 = uwb_list[-2]
    if e4 > pe4:          # if the last value added is more than the previous, then increase the amount of rx, ry to add to the pic
        MRX3 += 10
    if e4 < pe4:          # if the last value added is more than the previous, then increase
        MRX3 -= 10

    if len(uwb_list) >= 3:
        uwb_list.pop(0)

    bg5 = Image.open('pics/heatmap2.png')
    resized_bg5 = bg5.resize((MRX3,MRX3), Image.ANTIALIAS)
    new_bg5 = ImageTk.PhotoImage(resized_bg5)
    canvas6.create_image(uwb_location,uwb_location2,image=new_bg5)
    img5 = PhotoImage(file='pics/UWB-XG.png')
    my_image = canvas6.create_image(uwb_location, uwb_location2, image=img5)

pro_list = [0,0,0]
def pro_wifi_adjust(event):
    global bg2,resized_bg2, new_bg2, canvas6, pro_ap_locationx, pro_ap_locationy, img6, my_image, MRX

    pro_list.append(int(event))

    e3 = pro_list[-1]
    pe3 = pro_list[-2]
    if e3 > pe3:          # if the last value added is more than the previous, then increase the amount of rx, ry to add to the pic
        MRX += 10
    if e3 < pe3:          # if the last value added is more than the previous, then increase
        MRX -= 10
    if len(pro_list) >= 3:
        pro_list.pop(0)

    bg2 = Image.open('pics/heatmap2.png')
    resized_bg2 = bg2.resize((MRX,MRX), Image.ANTIALIAS)
    new_bg2 = ImageTk.PhotoImage(resized_bg2)
    canvas6.create_image(pro_ap_locationx,pro_ap_locationy,image=new_bg2)
    img6 = PhotoImage(file='pics/macpro.png')
    my_image = canvas6.create_image(pro_ap_locationx, pro_ap_locationy, image=img6)

lr_eifi_list = [0,0,0]
def lr_wifi_size(event):
    global bg3,resized_bg3, new_bg3, canvas6, lt_location, lt_location2, img7, my_image, MRX2

    lr_eifi_list.append(int(event))

    e2 = lr_eifi_list[-1]
    pe2 = lr_eifi_list[-2]
    if e2 > pe2:          # if the last value added is more than the previous, then increase the amount of rx, ry to add to the pic
        MRX2 += 10
    if e2 < pe2:          # if the last value added is more than the previous, then increase
        MRX2 -= 10
    if len(event_list) >= 3:
        event_list.pop(0)

    bg3 = Image.open('pics/heatmap2.png')
    resized_bg3 = bg3.resize((MRX2,MRX2), Image.ANTIALIAS)
    new_bg3 = ImageTk.PhotoImage(resized_bg3)
    canvas6.create_image(lt_location,lt_location2,image=new_bg3)
    img7 = PhotoImage(file='pics/macpro.png')
    my_image = canvas6.create_image(lt_location, lt_location2, image=img7)

event_list = [0,0,0]
def adjust_size(event):                                         # map size
    global bg1, resized_bg, new_bg, rx, ry, filename

    event_list.append(int(event))
    rxz, ryz = CANVW, CANVH
    bg1 = Image.open(filename)
    max_threshold = 1000        # Set the max threshold of an image
    e = event_list[-1]
    pe = event_list[-2]
    if e > pe:       # if the last value added is more than the previous, then increase the amount of rx, ry to add to the pic
        rx += 40
        ry += 25
    if e < pe:     # if the last value added is more than the previous, then increase
        rx -= 40
        ry -= 25

    if len(event_list) >= 3:
        event_list.pop(0)

    resized_bg = bg1.resize((rx,ry), Image.ANTIALIAS)
    new_bg = ImageTk.PhotoImage(resized_bg)
    canvas6.create_image(rxz,ryz,image=new_bg)

def move3(e):                                                               # UWB
    x = 600//2
    y = 400//2
    global bg5, resized_bg5, new_bg5, img5, MRX3, uwb_location, uwb_location2

    uwb_location = e.x
    uwb_location2 = e.y

    bg5 = Image.open('pics/heatmap2.png')
    resized_bg5 = bg5.resize((MRX3,MRX3), Image.ANTIALIAS)
    new_bg5 = ImageTk.PhotoImage(resized_bg5)
    canvas6.create_image(e.x,e.y,image=new_bg5)
    img5 = PhotoImage(file='pics/UWB-XG.png')
    my_image = canvas6.create_image(e.x,e.y, image=img5)

def move2(e):                                                               # LR
    x = 600//2
    y = 400//2
    global bg3, resized_bg3, new_bg3, img7, MRX2, lt_location, lt_location2

    lt_location = e.x
    lt_location2 = e.y

    bg3 = Image.open('pics/heatmap2.png')
    resized_bg3 = bg3.resize((MRX2,MRX2), Image.ANTIALIAS)
    new_bg3 = ImageTk.PhotoImage(resized_bg3)
    canvas6.create_image(e.x,e.y,image=new_bg3)
    img7 = PhotoImage(file='pics/macpro.png')
    my_image = canvas6.create_image(e.x,e.y, image=img7)

def move(e):                                                                # PRO
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

def pro_func(event):                                            # PRO
    global gg, green_glow
    canvas6.bind('<B1-Motion>', move)
    gg = PhotoImage(file='pics/dot.png') 
    green_glow = Label(right_canvas, image=gg, bg=LGRAY)
    green_glow.place(relx=0.084, rely=0.65)

def pro_func2(event):                                           # LR
    global gg, green_glow
    canvas6.bind('<B1-Motion>', move2)
    gg = PhotoImage(file='pics/dot.png')
    green_glow = Label(right_canvas, image=gg, bg=LGRAY)
    green_glow.place(relx=0.302, rely=0.65)

def pro_func3(event):                                           # UWB
    global gg, green_glow
    canvas6.bind('<B1-Motion>', move3)
    gg = PhotoImage(file='pics/dot.png')
    green_glow = Label(right_canvas, image=gg, bg=LGRAY)
    green_glow.place(relx=0.54, rely=0.65)

def info():
    webbrowser.open('https://www.terranovatechnology.com/heatwave-s6hd5g1hdgeyd6hfg5h41d6fs')

def importsite():
    global filename, canvas6, bg1, resized_bg, new_bg, rx, ry, image1, draw
    filename = filedialog.askopenfilename(initialdir="C:", title="Select File")
    filetypes=(("executables","*.exe"), ("all files", "*.*"))
    rxz, ryz = CANVW,CANVH                                      # Places cropping image in center of screen (half of the main_canvas size x,y)

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
            ap_mac_list = ['00:15:6D','00:1B:67','00:1B:67','00:27:22','00:15:6D','00:1B:67',
                            '00:27:22','04:18:D6','24:A4:3C','68:72:51','6C:5E:7A','9C:B0:08',
                            'DC:9F:DB','04:4e:5a']

            for client in scan_list:
                scan_results = client["ip"] + "\t\t" + client["mac"]
                T2.insert('end', scan_results + '\n')

                for mac_id in ap_mac_list:
                    if mac_id in client['mac']:             # Check condition - If Mac contains x, highlight the line that that Mac is on...
                        c_l = scan_list.index(client) + 3
                        start_cl, end_cl = str(c_l) + ".0" , str(c_l) + ".40"
                        T2.tag_add('start', start_cl, end_cl)
                        T2.tag_configure('start', foreground='#40c773')
                else:
                    pass

        else:
            T2.insert('end', 'No Results!\nCheck subnet format, or scan again.')
            T2.tag_add("start", "3.0", "4.35")
            T2.tag_configure("start", foreground="red")

    result_list = scan(ip_entry.get())
    print_result(result_list)

def start_vis():
    global filename
    img = cv2.imread(filename)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # detect edges
    edges = cv2.Canny(gray, 150, 300)

    lines = cv2.HoughLinesP(
        edges,
        rho=1.0,
        theta=np.pi/180,
        threshold=20,
        minLineLength=30,
        maxLineGap=10        
    )

    # draw lines
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    line_color = [0, 255, 0]
    line_thickness = 2
    dot_color = [0, 255, 0]
    dot_size = 3

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_img, (x1, y1), (x2, y2), line_color, line_thickness)
            cv2.circle(line_img, (x1, y1), dot_size, dot_color, -1)
            cv2.circle(line_img, (x2, y2), dot_size, dot_color, -1)

    overlay = cv2.addWeighted(img, 0.8, line_img, 1.0, 0.0)
    cv2.imshow("Overlay", overlay)
    cv2.waitKey()
    cv2.destroyAllWindows()

def save_canvas():
    subprocess.Popen('C:\\Windows\\System32\\SnippingTool.exe')

def clear_canvas():
    canvas6.delete("all")
    blankpage = Label(main_canvas, text='Start by importing building floor plans\n Then Select your AP and drag onto the site photo to see the range', font=('helvetica', 15), fg='white', bg=DGRAY)
    blankpage.place(relx=0.29, rely=0.5)

def bugreport():
    webbrowser.open('https://www.terranovatechnology.com/bug-report-lkjbo7960ogbnug869hbubub')

main_canvas = Canvas(root, width=1350, height=600, bg=DGRAY)
main_canvas.pack(pady=10)

right_canvas = Canvas(root, width=600, height=140, bg=LGRAY)
right_canvas.place(relx=0.3, rely=0.8)

adjust_canvas = Canvas(root, width=200, height=120, bg=LGRAY)
adjust_canvas.place(relx=0.76, rely=0.8)

ip_canvas = Canvas(root, width=300, height=140, bg=LGRAY)
ip_canvas.place(relx=0.08, rely=0.8)

ip_label = Label(ip_canvas, bg=LGRAY, fg=OWHITE, text='Format: x.x.x.x/x')
ip_label.place(relx=0.61, rely=0.0114)

msg = StringVar()  
T2 = Text(ip_canvas, bg=PBLUE, fg='white')
T2.place(relx=0.005, rely=0.13, relheight=0.86, relwidth=0.989)
T2.insert('end', '^ Scan a subnet or Single\nIP Address. Unifi APs may be\nHighlighted in Green')

img = PhotoImage(file='pics/apicon.png')  # PRO
imglabel = Label(right_canvas, image=img, bg=LGRAY)
imglabel.bind('<Button-1>', pro_func)
imglabel.bind('<Enter>', change_pro)
imglabel.bind('<Leave>', changeback_pro)
imglabel.place(relx=0.03, rely=0.13)

img2 = PhotoImage(file='pics/macpro.png')   # LITE
imglabel2 = Label(right_canvas, image=img2, bg=LGRAY)
imglabel2.bind('<Button-1>', pro_func2)
imglabel2.bind('<Enter>', change_lr)
imglabel2.bind('<Leave>', changeback_lr)
imglabel2.place(relx=0.28, rely=0.26)

img3 = PhotoImage(file='pics/UWB-XG.png')   # UWB-XG
imglabel3 = Label(right_canvas, image=img3, bg=LGRAY)
imglabel3.bind('<Button-1>', pro_func3)
imglabel3.bind('<Enter>', change_ubg)
imglabel3.bind('<Leave>', changeback_ubg)
imglabel3.place(relx=0.48, rely=0.1)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import", command=importsite)
filemenu.add_command(label="Ai-Visualizer (beta)", command=start_vis)
filemenu.add_command(label="Save", command=save_canvas)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Clear All", command=clear_canvas)
menubar.add_cascade(label="Edit", menu=helpmenu)
helpmenu2 = Menu(menubar, tearoff=0)
helpmenu2.add_command(label="Info", command=info)
helpmenu2.add_command(label="Report Bug", command=bugreport)
menubar.add_cascade(label="Help", menu=helpmenu2)

root.config(menu=menubar)

acpro_label = Label(right_canvas, text='Unifi AC-AP-PRO', font=('helvetica', 8), bg=LGRAY, fg='white')
acpro_label.place(relx=0.04, rely=0.012)

ac_label = Label(right_canvas, text='Unifi AC-AP-LR', font=('helvetica', 8), bg=LGRAY, fg='white')
ac_label.place(relx=0.26, rely=0.012)

unifi_uwb_label = Label(right_canvas, text='Unifi UWB-XG-US', font=('helvetica', 8), bg=LGRAY, fg='white')
unifi_uwb_label.place(relx=0.49, rely=0.012)

blankpage = Label(main_canvas, text='Start by importing building floor plans\n Then Select your AP and drag onto the site photo to see the range', font=('helvetica', 15), fg='white', bg=DGRAY)
blankpage.place(relx=0.29, rely=0.5)

ip_entry = Entry(ip_canvas, width=30)
ip_entry.bind('<Return>', scan_ip)
ip_entry.place(relx=0.001, rely=.001)

vert_label = Label(adjust_canvas,text='-Scaling Options-', font=('helvetica', 8), bg=LGRAY, fg='white')
vert_label.pack(side = TOP)

vert_label2 = Label(adjust_canvas,text='Pro                LR               UWB            Map', font=('helvetica', 7), bg=LGRAY, fg='white')
vert_label2.pack(side = BOTTOM)

vertical_wifi = Scale(adjust_canvas,width=10,length=100,command=pro_wifi_adjust, highlightbackground=DGRAY, to= -50, from_=50)  # PRO AP SCALE
vertical_wifi.pack(side = LEFT,padx=10)

vertical_lr_wifi = Scale(adjust_canvas,width=10,length=100,command=lr_wifi_size,highlightbackground=DGRAY, to= -50, from_=50)   # LR AP SCALE
vertical_lr_wifi.pack(side = LEFT,padx=10)

uwb_wifi = Scale(adjust_canvas,width=10,length=100,command=uwb_wifi_adjust, highlightbackground=DGRAY, to= -50, from_=50)                        # UWB AP SCALE
uwb_wifi.pack(side = LEFT,padx=10)

vertical_maps = Scale(adjust_canvas, width=10,length=100,command=adjust_size,highlightbackground=DGRAY, from_=20, to=-20)       # MAP SCALE
vertical_maps.pack(side=LEFT, padx=10)

root.mainloop()
