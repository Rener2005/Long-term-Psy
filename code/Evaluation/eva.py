import pandas as pd
import os
from itertools import zip_longest
#import RespondSolver as rs
from openai import OpenAI
import csv
client = OpenAI(
    api_key="sk-3D1QcNEVz3EwxCmZyRUABm3VvmK4bxnVTNq3sst09Of8KPxZ",
    base_url="https://api.chatanywhere.tech/v1"
 )
project_directory = "F:/SCIR/1210"


#promptPath = os.path.join(project_directory, 'code/prompts/GenMemories.txt')

def create_prompt(path):
    with open(path, "r", encoding="utf-8") as file: prompt = file.read() 
    return prompt


#txt_path = os.path.join(project_directory, 'data/dialogues')

def genRespond(client, prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content":prompt}
        ],
        max_tokens=6000,
        temperature=0
    )
    return response.choices[0].message.content.strip()

def genEva(index, client):
    txt_path = os.path.join(project_directory, 'data/dialogues')
    promptPath = os.path.join(project_directory, 'code/prompts/prompt_evaluation1.txt')
    
    if True:
        prompt = create_prompt(promptPath)
        #history = ""
        counselCount = 1
        diaName = f'dialogue_{index}.txt'
        myDiaPath = os.path.join(txt_path, diaName)
        with open(myDiaPath, "r", encoding="utf-8") as file: content = file.read() 
        consultant = content.split('################')[:-1]
        respond_list = []
        for str in consultant:
            counselCount += 1
            thisPrompt = prompt.replace("{diag}", str)
            #print(thisPrompt)
            res = genRespond(client=client, prompt=thisPrompt)
            respond_list.append(res)
        return respond_list

with open('gpt4_responses_en.csv', 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Index', 'S1','S2','S3','S4','S5','S6','S7','S8','S9']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:
        writer.writeheader()
    

    for index in range(205, 300):
        gpt4_response = genEva(index, client)
        print(gpt4_response)
        row = {'Index': index}
        for i, response in enumerate(zip_longest(gpt4_response, fillvalue='')):
            row[f'S{i+1}'] = response[0]  # 将空位填充为默认值

        writer.writerow(row)