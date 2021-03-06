from tkinter import *
from tkinter import filedialog
from pdfReader import getResults
from tkinter import ttk
import threading

root=Tk()
root.title("PDF Explorer")

# To open window as maximized
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width,height))


def select():
    """Function to select directory"""
    global pathLabel
    #global root.filepath
    root.filepath=filedialog.askdirectory(initialdir="./",title="select a folder")  # root.filepath will have the absolute path of choosen directory
    pathLabel=Label(inputFrame,text=root.filepath)
    pathLabel.grid(row=0,column=0)

# GUI for selecting directory
inputFrame=LabelFrame(root,padx=30,pady=30)
pathLabel=Label(inputFrame,text="Directory path...")
pathLabel.grid(row=0,column=0)
BrowseButton=Button(inputFrame,text="Select Folder",command=select)
BrowseButton.grid(row=0,column=1)

var=StringVar() # var will store the filename 


def viewDetails(results,filename):
    """Function to show page and sentences of findings"""
    top=Toplevel()
    top.geometry('%dx%d+0+0' % (width,height))
    top.lift()

    # Canvas for scrollable frame
    container1 = ttk.Frame(top)
    canvas1 = Canvas(container1,width=1493,height=820)
    # Adding Scroll bar
    outputFrame1 = ttk.Frame(canvas1)
    scrollbar1 = ttk.Scrollbar(container1, orient="vertical", command=canvas1.yview)
    outputFrame1.bind(
        "<Configure>",
        lambda e: canvas1.configure(
            scrollregion=canvas1.bbox("all")
        )
    )

    #myLabel=Label(top,text=filename).pack()
    for index,i in enumerate(results[filename]):
        pagenum="page: "+str(i)
        sentence="Sentence: "+results[filename][i]
        pageLabel=ttk.Label(outputFrame1,text=pagenum,anchor="w")
        pageLabel.grid(row=index,column=0,padx=10,pady=10,sticky="w")
        sentenceLabel=ttk.Label(outputFrame1,text=sentence,anchor="w",wraplength=1400,justify=LEFT)
        sentenceLabel.grid(row=index,column=1,padx=10,pady=10,sticky="w")
    canvas1.create_window((0, 0), window=outputFrame1, anchor="nw")
    canvas1.configure(yscrollcommand=scrollbar1.set)

    container1.pack()
    canvas1.pack(side="left", fill="both", expand=True)
    # outputFrame.pack(padx=10,pady=5,fill="both")
    scrollbar1.pack(side="right", fill="y")


def Search():
    """Function to search keyword in files of a directory and display them using GUI"""
    global outputLabel
    global var
    keyword=keywordEntry.get()
    var=StringVar()
    results=getResults(root.filepath,keyword)
    for index,i in enumerate(results):
        filename="File Name: "+str(i)
        pagenum="pagenumbers: "+str(list(results[i].keys()))
        filename_outputLabel=ttk.Label(outputFrame,text=filename,anchor="w",wraplength=300)
        filename_outputLabel.grid(row=index,column=0,padx=10,pady=10,sticky="w")
        pagenum_outputLable=ttk.Label(outputFrame,text=pagenum,anchor="w",wraplength=1000,justify=LEFT)
        pagenum_outputLable.grid(row=index,column=1,padx=10,pady=10,sticky="w")
        #adding radio buttons
        Radiobutton(outputFrame,variable=var,value=i).grid(row=index,column=2)
    detailButton=Button(outputFrame,text="view Details",command= lambda: viewDetails(results,var.get()))
    detailButton.grid(row=len(results),column=0)
   

keywordEntry=Entry(inputFrame,width=50,borderwidth=5)
searchButton=Button(inputFrame,text="search",command= lambda: threading.Thread(target=Search).start())
keywordEntry.grid(row=1,column=0,padx=10,pady=5)
searchButton.grid(row=1,column=1,padx=10,pady=5)

inputFrame.pack(padx=10,pady=20)




# Canvas for scrollable frame
container = ttk.Frame(root)
canvas = Canvas(container,width=1493,height=675)

 # Adding Scroll bar
outputFrame = ttk.Frame(canvas)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)


outputFrame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=outputFrame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

container.pack()
canvas.pack(side="left", fill="both", expand=True)
# outputFrame.pack(padx=10,pady=5,fill="both")
scrollbar.pack(side="right", fill="y")





mainloop()