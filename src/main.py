import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
import os
import re
import numpy as np
import PyPDF2
#import cv2
import os
directory ="C:\\Users\\anuvr\\PycharmProjects\\insights\\pdf_folder"
categories = {'MDA': ['management discussion and analysis', 'MD & A', 'MD&A'], }
def extract_pdf_text(file_path, categories):
    # Open the PDF file
    with open(file_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f) #PyPDF2.PdfFileReader(f)
        pdf_info =  pdf.metadata #pdf.getDocumentInfo()

        # Extract the metadata fields
        title = pdf_info.title
        author = pdf_info.author
        creator = pdf_info.creator
        producer = pdf_info.producer
        title = pdf_info.title
        f_name = os.path.basename(file_path)


        # Create an empty DataFrame to store the results
        df = pd.DataFrame(columns=['page_number', 'text'])

        # Iterate through each page of the PDF
        for i in range(0, len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text().lower() #page.extractText().lower()

            # Iterate through the categories dictionary
            for key, values in categories.items():
                for val in values:
                    # Check if the current page contains any of the words in the categories dictionary
                    if val.lower() in text:
                        # If a match is found, add a new row to the DataFrame
                        df = df.append({ 'page_number': i+1, 'text': text}, ignore_index=True)
                        df['author'] = author
                        df['creator'] = creator
                        df['producer'] = producer
                        df['title'] = title
                        df['File Name'] = f_name

    #drop 1st record (index)
    df = df.tail(-1)
    return df

#file_path = 'C:\\Users\\anuvr\\PycharmProjects\\insights\\pdf_folder\\astral.pdf'
file_path = '../pdf_folder/astral.pdf'
df = extract_pdf_text(file_path, categories)

df = extract_pdf_text(file_path,categories)

page_numbers_lst = df['page_number'].tolist()

# Fn to get only md&a page numbers
def first_sequence(lst):
    result = []
    for i in range(1, len(lst)):
        if lst[i] == lst[i-1] + 1:
            result.append(lst[i-1])
        else:
            result.append(lst[i-1])
            break
    return result

mda_page_numbers = first_sequence(page_numbers_lst)

filtered_df = df[df['page_number'].isin(mda_page_numbers)]

prompt_df = pd.DataFrame(columns=['page_number', 'positive_prompt', 'negative_prompt', 'summary_prompt'])

for index, row in filtered_df.iterrows():
    p = row['page_number']
    chunk = row['text']
    print(len(chunk))
    positive_prompt = (
        f"{chunk}\n\n As an investor of company , what are important positive bullet pointers about the company in short ? ")
    negative_prompt = (
        f"{chunk}\n\n As an investor of company, what are important negative bullet pointers about the company in short ? ")
    summary_prompt = (f"{chunk} \n\nTl;dr")
    prompt_df = prompt_df.append(
        {'page_number': p, 'positive_prompt': positive_prompt, 'negative_prompt': negative_prompt,
         'summary_prompt': summary_prompt}, ignore_index=True)

