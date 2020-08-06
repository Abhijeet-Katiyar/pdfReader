from tkinter import *
from tkinter import filedialog
from pdfReader import getResults

root=Tk()
root.title("PDF Explorer")

# To open window as maximized
width, height = root.winfo_screenwidth(), root.winfo_screenheight()

root.geometry('%dx%d+0+0' % (width,height))


def select():
    global pathLabel
    #global root.filepath
    root.filepath=filedialog.askdirectory(initialdir="./",title="select a folder")
    pathLabel=Label(inputFrame,text=root.filepath)
    pathLabel.grid(row=0,column=0)

inputFrame=LabelFrame(root,padx=30,pady=30)
pathLabel=Label(inputFrame,text="Directory path...")
pathLabel.grid(row=0,column=0)
BrowseButton=Button(inputFrame,text="Select Folder",command=select)
BrowseButton.grid(row=0,column=1)

def Search(keyword):
    global outputLabel
    results=getResults(root.filepath,keyword)
    for index,i in enumerate(results):
        filename="File Name: "+str(i)
        pagenum="pagenumbers: "+str(list(results[i].keys()))
        filename_outputLabel=Label(outputFrame,text=filename,anchor="w")
        filename_outputLabel.grid(row=index,column=0,padx=5,pady=5,sticky="w")
        pagenum_outputLable=Label(outputFrame,text=pagenum,anchor="w",wraplength=800,justify=LEFT)
        pagenum_outputLable.grid(row=index,column=1,padx=5,pady=5,sticky="w")


keywordEntry=Entry(inputFrame,width=50,borderwidth=5)
searchButton=Button(inputFrame,text="search",command= lambda: Search(keywordEntry.get()))
keywordEntry.grid(row=1,column=0)
searchButton.grid(row=1,column=1)


inputFrame.pack(padx=10,pady=5)



outputFrame=LabelFrame(root,padx=30,pady=30)
outputFrame.pack(padx=10,pady=5,fill="both")


mainloop()