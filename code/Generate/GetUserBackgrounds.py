import pandas as pd
import os
import RespondSolver as rs
from openai import OpenAI

client = OpenAI(
    api_key="sk-3D1QcNEVz3EwxCmZyRUABm3VvmK4bxnVTNq3sst09Of8KPxZ",
    base_url="https://api.chatanywhere.tech/v1"
 )
project_directory = "F:/SCIR/1210"

excel_path = os.path.join(project_directory, 'data/Original/Data2.xlsx')
sheet_name = 'Sheet1'  

data = pd.read_excel(excel_path, sheet_name=sheet_name)
promptPath = os.path.join(project_directory, 'code/prompts/GetUserBackgrounds.txt')

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

for row in range(80,100):
    prompt = create_prompt(promptPath)
    prompt = prompt.replace("[用户画像]", data.iat[row, 1])
    history = ""
    counselCount = 0
    for col in range(2,10): 
        if not pd.isna(data.iat[row, col]):
            counselCount += 1
            history += f"\n\n第{counselCount}次咨询:\n"
            history += data.iat[row, col]
            #thisPrompt = prompt.replace("[咨询过程]", data.iat[row, col])
    thisPrompt = prompt.replace("[咨询过程]", history)
    respond = gen_summary(client=client, prompt=thisPrompt)
    txtName = f'out_{row}.txt'
    data_dir = os.path.join(project_directory, "data/Generate")
    txtPath = os.path.join((data_dir), txtName)
    with open(txtPath, 'w', encoding='utf-8') as file:
        file.write(respond)
    rs.RespondIntoJson(res=respond, index=row, directory=os.path.join(project_directory, "data/UserCards"))
    #print()

