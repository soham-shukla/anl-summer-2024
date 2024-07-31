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
    
def chunk_text(text, chunksize):
        return [text[i:i + chunksize] for i in range(0, len(text), chunksize)]
         
#defines pdf path
pdf_path = input("enter pdf path here:")

#extracts pdf content
pdf_content = read_file(pdf_path)
pdf_content = pdf_content

chunks = chunk_text(pdf_content, 2000)

all_responses = []
context = "summarize the information given, preserving key data, figures, and details"
for i, chunk in enumerate(chunks):
    try:
        response = ollama.chat(model='llama3custom', messages=[
            {
                'role': 'system',
                'content': 'You are an assistant helping to answer questions based on a provided document.'
            },
            {
                'role': 'user',
                'content': f'This is the content of the document chunk {i + 1}: {chunk}'
            },
            {
                'role':'user',
                'content': f'This is the question about the document: {context}'
            }
        ])

        # Add the response to the list
        all_responses.append(f"chunk {i+1} response: {response['message']['content']}")
    except Exception as e:
        all_responses.append(f'An error has occurred while chatting with the model for chunk {i + 1}: {str(e)}')

combined_responses = "\n".join(all_responses) 

while True: 
    question = input("what can I help you with? ('quit' to exit)")
    if question.lower() == 'quit':
            print("exiting...")
            break

    try:
        final_response = ollama.chat(model='llama3custom', messages=[
            {
                'role': 'system',
                'content': 'You are an assistant helping to answer questions based on a provided document based on information dervived from the provided chunks'
            },
            {
                'role': 'user',
                'content': f'This is a combined summary of document chunks, placed in reading order" {combined_responses}'
            },
            {
                'role': 'user',
                'content': f'This is the question about the document which should be answered from the chunks: {question}'
            }
        ])

        # Print the final response
        print("Final Response:")
        print(final_response['message']['content'])
    except Exception as e:
        print(f'An error has occurred while getting the final response: {str(e)}') 

