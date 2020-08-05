from tkinter import *
from tkinter import filedialog
from pdfReader import getResults

root=Tk()
root.title("PDF Explorer")

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
    for i in results:
        s="File Name: "+str(i)+"\t pagenumbers: "+str(list(results[i].keys()))
        outputLabel=Label(outputFrame,text=s)
        outputLabel.pack()


keywordEntry=Entry(inputFrame,width=50,borderwidth=5)
searchButton=Button(inputFrame,text="search",command= lambda: Search(keywordEntry.get()))
keywordEntry.grid(row=1,column=0)
searchButton.grid(row=1,column=1)


inputFrame.pack(padx=10,pady=5)



outputFrame=LabelFrame(root,padx=30,pady=30)
outputLabel=Label(outputFrame)
outputLabel.pack()

outputFrame.pack(padx=10,pady=5)


mainloop()