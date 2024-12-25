import pandas as pd
import os
import RespondSolver as rs
from openai import OpenAI

client = OpenAI(
    api_key="sk-3D1QcNEVz3EwxCmZyRUABm3VvmK4bxnVTNq3sst09Of8KPxZ",
    base_url="https://api.chatanywhere.tech/v1"
 )
project_directory = "F:/SCIR/1210"

original_path = os.path.join(project_directory, 'data/Original/data_original.csv')
data = pd.read_csv(original_path, usecols=[0])  # 只读取第一列

data_list = []

for index, row in data.iterrows():
    data_list.append(row[0])

promptPath = os.path.join(project_directory, 'code/prompts/GenUserBackgrounds.txt')

def create_prompt(path):
    with open(path, "r", encoding="utf-8") as file: prompt = file.read() 
    return prompt



def gen_summary(client, prompt):
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

for row in range(1100,1400):
    prompt = create_prompt(promptPath)
    thisPrompt = prompt.replace("[用户画像]", data_list[row])
    
    respond = gen_summary(client=client, prompt=thisPrompt)
    txtName = f'out_{row+100}.txt'
    data_dir = os.path.join(project_directory, "data/Generate")
    txtPath = os.path.join((data_dir), txtName)
    with open(txtPath, 'w', encoding='utf-8') as file:
        file.write(respond)
    rs.RespondIntoJson(res=respond, index=row+100, directory=os.path.join(project_directory, "data/UserCards"))
    #print()

