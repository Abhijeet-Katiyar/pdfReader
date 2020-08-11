#pip install PyPDF2

import PyPDF2
import re
import sqlite3


def initiateDatabase():
    """Function to create connection and Table in database"""
    conn=sqlite3.connect('pdfReader.db')
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS PDFDATA(FileName Text Unique, FileText TEXT)''')
    # conn.execute('''REINDEX pdfReader.PDFDATA''')
    c.execute("""create unique index FileName_index on PDFDATA(FileName)""")
    return c,conn


def clean(text):
    reg=re.compile('[A-Za-z0-9 .]')
    return ''.join(re.findall(reg,text))


def read_pdf_file(file_path,filename,c):
    """Function to extract text and store it in database"""
    pdf_obj=open(file_path,'rb')
    pdfReader=PyPDF2.PdfFileReader(pdf_obj)
    pdf_text=""        # this string will store text of every page from pdf
    query=c.execute("""Select FileName from PDFDATA""")
    fileNamesInDataBase=query.fetchall()
    filenameList=[i[0] for i in fileNamesInDataBase]
    #print("files:",filenameList)
    if(filename not in filenameList):
        for i in range(pdfReader.numPages):
            page_obj=pdfReader.getPage(i)
            pdf_text+=clean(page_obj.extractText())
            pdf_text+="PAGESPLIT"
        insertQuery="""Insert or Ignore Into PDFDATA(FileName,FileText) Values(?,?)"""
        print("writing to database")
        c.execute(insertQuery,(filename,pdf_text))


def search_keyword(keyword,c,dirFileList):      # c is database cursor
    """function to search page and sentence which contains the keyword"""
    # approach: fetch all the rows from database 
    # loop over all the rows fetched from database and check if file is present in directory(dirFileList is a list with all filenames presented in selected directory)
    # if file name presented in directory the get whole text of pdf and split it by "PAGESPLIT" keyword into pages
    # Break pages into sentences and loop over sentences to check if keyword is present in sentence or not
    # if key word present in sentence the append it into aq list
    # After scanning whole page make a dictionary as {page_number : sentence_list}
    # After scanning all the pages make a dictionary as {filename : {page_number : sentence_list}}
    filname=c.execute("""select FileName,FileText from PDFDATA""")
    a=filname.fetchall()    #type of a is list
    found=False
    filename_list={}
    for i in a:     #type of i is tuple
        if(i[0] in dirFileList):
            print("reading from database")
            filetext=i[1].split("PAGESPLIT")
            page={}
            for j in range(len(filetext)):         # j represents PAges, type of j is int
                sentences=filetext[j].split(".")
                s=[]
                for k in sentences:     #type of k is str
                    if keyword in k:
                        found=True
                        s.append(k.replace("\n", " ").strip())     
                if(found and len(s)>0):
                    page[j+1]=s            
            if(found and len(page)>0):
                filename_list[i[0]]=page
    print("Scanning...")
    if(len(page)==0):
        return False
    return filename_list
#     return [{"page_number": i, "sentence": "some text sjajadn snajksjakdna djajakj"}]

def commitAndClose(c,conn):  # C is cursor
    conn.commit()
    c.execute("""DROP INDEX IF EXISTS FileName_index""")
    # conn.execute("""VACUUM""")
    c.close()
    conn.close()


import os

def getResults(path,keyword):
    files=os.listdir(path)
    #print(type(files))
    findings={}
    c,conn=initiateDatabase()
    for i in files:
        fpath=path+"/"+i
        if(i.endswith(".pdf")):
            read_pdf_file(fpath,i,c)
    findings=search_keyword(keyword,c,files)
    commitAndClose(c,conn)
    return findings                     # returning format is {filename : {page : sentence}, filename : {page : sentence} }







