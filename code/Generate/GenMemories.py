import pandas as pd
import os
import RespondSolver as rs
from openai import OpenAI

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

def gen_memories(client, prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content":prompt}
        ],
        max_tokens=6000
    )
    return response.choices[0].message.content.strip()

'''
for row in range(1,3):
    prompt = create_prompt(promptPath)
    prompt = prompt.replace("[用户画像]", data.iat[row, 1])
    for col in range(2,10): 
        if not pd.isna(data.iat[row, col]):
            thisPrompt = prompt.replace("[咨询过程]", data.iat[row, col])
            print(gen_summary(client=client, prompt=thisPrompt))
'''
def genMemories(x, y, client):
    txt_path = os.path.join(project_directory, 'data/dialogues')
    memory_path = os.path.join(project_directory, 'data/Memories/Original')
    promptPath = os.path.join(project_directory, 'code/prompts/GenMemories.txt')
    for index in range(x, y):
        prompt = create_prompt(promptPath)
        history = ""
        counselCount = 1
        diaName = f'dialogue_{index}.txt'
        memName = f'memory_{index}.txt'
        myDiaPath = os.path.join(txt_path, diaName)
        myMemPath = os.path.join(memory_path, memName)
        with open(myDiaPath, "r", encoding="utf-8") as file: content = file.read() 
        consultant = content.split('################')[:-1]
        for str in consultant:
            history += f"\n\n第{counselCount}次咨询:\n"
            history += str
            counselCount += 1
        thisPrompt = prompt.replace("@对话历史", history)
        #print(thisPrompt)
        respond = gen_memories(client=client, prompt=thisPrompt)
        with open(myMemPath, 'w', encoding='utf-8') as file:
            file.write(respond)
            print(f"合成进度:{index}")

genMemories(1200, 1500, client=client)