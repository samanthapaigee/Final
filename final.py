import requests #for http things
import json #for json things
from tkinter import * #for gui things
apikey = 'dc3ec57ee666562a7ccf3d77f2e1eb85' #openweathermap api key
requrl=''

def menuclick(menuvalue): #destroy previous window and allow central menu location for expansion
    global root
    root.destroy()
    if(menuvalue==2):
        setzip()
    if(menuvalue==1):
        setcity()
        
def setcity(): #enter city and link to url joiner
    global root
    root = Tk()
    entercity=Label(text="enter your city")
    entercity.grid(row=0)
    e = Entry(width=50) #entry textbox
    e.grid(row=1,column=0)
    enterbutton = Button(root, text="Enter",command=lambda:[setcityurl(e.get()),root.destroy()]) #kill window
    enterbutton.grid(row=1,column=1)
    
def setcityurl(var1):#city url joiner
    city=var1
    global requrl
    requrlcity=''.join(['https://api.openweathermap.org/data/2.5/forecast?q=',city,'&units=imperial&appid=',apikey]) #joins var city and var apikey to url
    requrl=requrlcity
    
def setzip(): #enter zip and link to url joiner
    global root
    root = Tk()
    enterzip=Label(text="enter your zipcode")
    enterzip.grid(row=0)
    e = Entry(width=50) #entry textbox
    e.grid(row=1,column=0)
    enterbutton = Button(text="Enter",command=lambda: [setzipurl(e.get()),root.destroy()]) #kill window
    enterbutton.grid(row=1,column=1)
    
def setzipurl(var1): #zip url joiner
    zipcode=var1
    global requrl
    requrlzip =''.join(['https://api.openweathermap.org/data/2.5/forecast?zip=',zipcode,'&units=imperial&appid=',apikey])#joins var zipcode and var apikey to url
    requrl=requrlzip

def main():
    global root
    root = Tk()
    citybutton = Button(root, text="city",padx=50,pady=50, command=lambda: menuclick(1)) #add menu option city
    citybutton.grid(row=0,column=0)

    zipbutton = Button(root, text="zipcode",padx=50,pady=50, command=lambda: menuclick(2)) #add menu option zipcode
    zipbutton.grid(row=0,column=1)
    root.mainloop()


    jout=(requests.get(requrl)).json() #getdata as .json

    root = Tk()
    scrollbar = Scrollbar(root)#make tkinter scrollbar container
    scrollbar.pack( side = RIGHT, fill = Y )
    if(jout['cod']=='200'): #check connection is http 200 ("try")
        root.geometry('330x200')
        listlabel = Label(root,text=str(jout['city']['name'])+' weather') #top line label
        listlabel.pack()
        listlabel = Label(root,text='              Date:            Temp:     Weather:',anchor=W, justify=LEFT) #top line label done this way because tkinter Label doesn't ack \t formatting
        listlabel.pack(fill=X)
        mylist = Listbox(root, yscrollcommand = scrollbar.set )
        for x in jout['list']:
            mylist.insert(END, str(x['dt_txt'])+'   '+str(int(x['main']['temp']))+'    '+str(x['weather'][0]['description']))#add human readable date time, temp, & weather description to list
            mylist.insert(END,'') #insert blank line to list since tkinter doesnt recognize \n formatting
        mylist.pack( side = LEFT, fill = BOTH, expand=True ) #pack list
        scrollbar.config( command = mylist.yview ) #move list when scrolled
        TRYAGAIN = Button(root, text="Try again?",command=lambda: [root.destroy(),main()]) #add menu option zipcode
        TRYAGAIN.pack(side=BOTTOM)
    else: #if connection != 200
        listlabel = Label(root,text='connection error: location not found')
        listlabel.pack()
        TRYAGAIN = Button(root, text="Try again?",command=lambda: [root.destroy(),main()]) #add menu option zipcode
        TRYAGAIN.pack(side=BOTTOM)
    root.mainloop()

main()