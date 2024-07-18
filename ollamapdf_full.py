import ollama
import urllib.parse, urllib.error
import urllib.request as REQ
import pymupdf
import fitz

def read_file(pdf):
    try:
        pdf_doc = fitz.open(pdf)
        text = ""
        
        for numpage in range(len(pdf_doc)):
            page = pdf_doc.load_page(numpage)
            text += page.get_text()
        return text
    except Exception as e:
        return f'an error has occured while reading the PDF: {str(e)}'
    

#defines pdf path
pdf_path = input("enter pdf path here:")

#extracts pdf content
pdf_content = read_file(pdf_path)
pdf_content = pdf_content[:2000]

#print(pdf_content)

question = input("what can i help you with?")

response = ollama.chat(model='llama3custom', messages=[
    {
        'role': 'system',
        'content': 'You are an assistant helping to answer questions based on a provided document.'
    },
    {
        'role': 'user',
        'content': f'This is the content of the document: {pdf_content}'
    },
    {
        'role': 'user',
        'content': f'This is the question about the document: {question}'
    }
])

print(response['message']['content'])