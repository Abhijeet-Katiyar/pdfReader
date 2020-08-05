#pip install PyPDF2

import PyPDF2
import re

def clean(text):
    reg=re.compile('[A-Za-z0-9. ]')
    return ''.join(re.findall(reg,text))


def read_pdf_file(file_path):
    """Function to extract text"""
    pdf_obj=open(file_path,'rb')
    pdfReader=PyPDF2.PdfFileReader(pdf_obj)
    pdf_text=""        # this string will store text of every page from pdf
    for i in range(pdfReader.numPages):
        page_obj=pdfReader.getPage(i)
        print(clean(page_obj.extractText()))
    return pdf_text


def search_keyword(pdf_file_path, keyword):
    """function to search page and sentence which contains the keyword"""
    # approach: extract text from every page and split by new line character to make a list of sentenes.
    # check every sentence if it contains the keyword.
    # store the page_number and sentence in appropriate list and return it in form of dictionary
    pdf_obj=open(pdf_file_path,'rb')
    pdfReader=PyPDF2.PdfFileReader(pdf_obj)
    page,sentence=[],[] 
    for i in range(pdfReader.numPages):         # i represents page number
        page_obj=pdfReader.getPage(i)
        text=clean(page_obj.extractText())
        l=text.split(".")
        for j in l:             # j represents sentence
            if keyword in j:
                page.append(i+1)
                sentence.append(j.replace("\n", "").strip())
    print("Scanning...")
    if(len(page)==0):
        return False
    return dict(zip(page,sentence))
#     return [{"page_number": i, "sentence": "some text sjajadn snajksjakdna djajakj"}]


import os

def getResults(path,keyword):
    files=os.listdir(path)
    findings={}
    for i in files:
        fpath=path+"/"+i
        if(i.endswith(".pdf")):
            dictionary=search_keyword(fpath,keyword)
            if(dictionary):
                findings[i]=dictionary
    return findings                     # returning format is {filename : {page : sentence}, filename : {page : sentence} }




# file_path=input("Enter absolute file path: ")
# print("PDF Text:\n",read_pdf_file(file_path))

# choice=input("If you want to search a keyword yes/no: ")
# if(choice.lower()=='yes'):
#     keyword=input("Enter Keyword to search: ")
#     d=search_keyword(file_path,keyword)
#     for i in d:
#         print("page no.:",i,"\tSentence:",d[i])
#         print()






