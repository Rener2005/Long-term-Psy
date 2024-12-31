import pandas as pd
import os
import RespondSolver as rs
from openai import OpenAI
import json
import GenMemories

client = OpenAI(
    api_key="sk-3D1QcNEVz3EwxCmZyRUABm3VvmK4bxnVTNq3sst09Of8KPxZ",
    base_url="https://api.chatanywhere.tech/v1"
 )
project_directory = "F:/SCIR/1210"

cards_path = os.path.join(project_directory, 'data/UserCards')

promptPath = os.path.join(project_directory, 'code/prompts/GenDialogues_task1.txt')

def create_prompt(path):
    with open(path, "r", encoding="utf-8") as file: prompt = file.read() 
    return prompt



def gen_dialogue(client, prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content":prompt}
        ],
        max_tokens=20000
    )
    return response.choices[0].message.content.strip()

txt_path = os.path.join(project_directory, 'data/dialogues')
for index in range(1400, 1500):
    
    long_str = ""
    diaName = f'dialogue_{index}.txt'
    myDiaPath = os.path.join(txt_path, diaName)
    fileName = f"consultations_{index}.json"
    filePath = os.path.join(cards_path, fileName)
    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            all_Data = json.load(file)
        sessions = all_Data["consultations"]
        roll = len(sessions)
        for i, consultation in enumerate(sessions):
            promptTemplate = create_prompt(promptPath)
            user_background = consultation["user_background"]
            strategy = consultation["strategy"]
            #@开始前状态
            s1 = f"心理状态:{user_background['psychological_state']}\n已达成的目标:{user_background['purpose']}"
            promptTemplate = promptTemplate.replace("@开始前状态", s1)

            #@结束时状态
            if i < roll-1:
                s2 = f"心理状态:{sessions[i+1]['user_background']['psychological_state']}\n已达成的目标:{sessions[i+1]['user_background']['purpose']}"
            else:
                s2 = f"用户心理问题已经得到解决，此次咨询顺利结案。"

            promptTemplate = promptTemplate.replace("@结束时状态", s2)

            #@用户背景
            s3 = f"原始背景:{user_background['basic_info']}\n近期事件:{user_background['recent_events']}"

            promptTemplate = promptTemplate.replace("@用户背景", s3)

            #@咨询计划
            s4 = f"咨询计划:{strategy['plan']}\n咨询目标:{strategy['goal']}"

            promptTemplate = promptTemplate.replace("@咨询计划", s4)
            #@对话历史
            s5 = long_str
            #promptTemplate = promptTemplate.replace("@对话历史", s5)
            #print(promptTemplate)
            long_str += gen_dialogue(client=client, prompt=promptTemplate)
            long_str += "\n###################\n"

            
        print(f"合成进度:{index}")
        with open(myDiaPath, 'w', encoding='utf-8') as file:
            file.write(long_str)

    except FileNotFoundError:
        print(f"文件 {filePath} 未找到，跳过该轮循环。")
        continue  
            

    