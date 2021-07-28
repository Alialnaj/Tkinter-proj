from tkinter import Tk, Label, Button, Frame, simpledialog
from tkinter.ttk import Progressbar
# from PIL import Image, ImageTk
import requests
import re
import os
import threading

def passUrldata():
    url = simpledialog.askstring("Enter Url", "Please Enter an URL")
    downloadthread = threading.Thread(target=lambda: addDownloadURL(url))
    downloadthread.start()

def getStandardsize(size):
    items = ['bytes', 'KB', 'MB', 'GB', 'TB']
    for x in itmes:
        if size < 1024.0:
            return "%3.1f %s" % (size, x)
    return size


def addDownloadURL(url):
    

    if url != None:
        req = requests.get(url, stream=True)

        if "Content-Length" in req.headers:
            total_size = req.headers['Content-Length']
        else:
            total_size = None
        
        filename = ""

        if "Content-Disposition" in req.headers.keys():
            fname = re.findall("filename=(.+)", req.headers['Content-Disposition'])[0]
        else:
            fname = url.split("/")[-1]
        
        fname.replace(" ", "")
        frame2 = Frame(frame, bg="#E67E22")
        # img = Image.open("Img.png")
        # render = ImageTk.PhotoImage(img)
    # 
        # label = Label(frame2, image=render).grid(row=0, column=0)

        title = Label(frame2, text=fname, padx=5, bg="#E67E22", fg="white", anchor='w')
        title.config(font=("Helvetica", 14))
        title.grid(row=0, column=1, sticky="nsew")

        labelPercentage = Label(frame2, text="0 %", padx=5, anchor='w', bg="#E67E22", fg="white")
        labelPercentage.grid(row=0, column=2)
        labelSize = Label(frame2, text="0 KB", padx=5, anchor='w', bg="#E67E22", fg="white")
        labelSize.grid(row=1, column=2)

        progress = Progressbar(frame2)
        progress['value'] = 50
        progress.grid(row=1, column=1, sticky="nsew")

        frame2.pack(fill="x", expand=True)
        frame2.columnconfigure(1, weight=1)



        with open(fname, "wb") as fileobj:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    fileobj.write(chunk)
                    current_size = os.path.getsize(fname)
                    labelSize.config(text=str(getStandardsize(current_size)))
                    if total_size != None:
                        percentage = round((int(current_size) / int(total_size))*100)    
                        labelPercentage.config(text=str(percentage) + " %")
                        progress['value'] = percentage
                    else:
                        percentage = "Infinte"
                        progress.config(mode="indeterminate")
                        progress.start()   
                        labelPercentage.config(text=str(percentage) + " %")


        if total_size != None:
            current_size = os.path.getsize(fname)
            labelSize.config(text=str(getStandardsize(current_size)))
            labelPercentage.config(text=str(percentage) + " %")
            percentage = round((int(current_size) / int(total_size))*100)         
            progress['value'] = percentage
        else:
            current_size = os.path.getsize(fname)
            labelSize.config(text=str(getStandardsize(current_size)))
            labelPercentage.config(text="100 %")
            progress['value'] = 100



window = Tk()
window.title("File Download Manager")
window.geometry("900x600")
frame = Frame(window, bg="#212F3C")
frame.pack(fill="both", expand=True)


rowframe = Frame(frame, bg="grey")
button = Button(rowframe, text="Add download URL", bg="#27AE60", fg="white", padx=10, pady=10, activebackground="light blue", activeforeground="black", command=passUrldata)
button.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
button1 = Button(rowframe, text="Exit program", bg="#C0392B", fg="white", padx=10, pady=10, activebackground="light blue", activeforeground="black", command=window.quit)
button1.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
rowframe.grid_columnconfigure(0, weight=1)
rowframe.grid_columnconfigure(1, weight=1)


rowframe.pack(fill="x")

window.mainloop()
