# -*- coding: utf-8 -*-
import re
import json
import os
project_directory = "F:/SCIR/1210"
dataPath = os.path.join(project_directory, 'data/Generate/out_2.txt')
#dataPath = os.path.join(project_directory, 'out.txt')
with open(dataPath, "r", encoding="utf-8") as file: text = file.read() 


# 正则表达式模式
#pattern = r"## 用户背景\n\[基本信息\]\s*(.*?)\s*\[近期生活事件\]\s*(.*?)\s*\[心理状态\]\s*(.*?)\s*\[此次咨询的目的\]\s*(.*?)\s*## 咨询策略\n\[咨询计划\]\s*(.*?)\s*\[咨询目标\]\s*(.*?)\n"
pattern = r"## 用户背景\s*\[基本信息\]\s*(.*?)\s*\[近期生活事件\]\s*(.*?)\s*\[心理状态\]\s*(.*?)\s*\[此次咨询的目的\]\s*(.*?)\s*## 咨询策略\s*\[咨询目标\]\s*(.*?)\s*\[咨询计划\]\s*([^\n#]+)"
matches = re.findall(pattern, text, re.DOTALL)
#print(matches)

def RespondIntoJson(res, index, directory):
    sessions = []
    matches = re.findall(pattern, res, re.DOTALL)
    for i, match in enumerate(matches, 1):
        basic_info, recent_events, psychological_state, purpose, plan, goal = match

        session_data = {
            "session": f"第{i}次咨询",
            "user_background": {
                "basic_info": basic_info.strip(),
                "recent_events": recent_events.strip(),
                "psychological_state": psychological_state.strip(),
                "purpose": purpose.strip(),
            },
        "strategy": {
            "plan": plan.strip(),
            "goal": goal.strip(),
            }
        }

        sessions.append(session_data)

    filename = f"consultations_{index}.json"
    filepath = os.path.join(directory, filename)
    #json_data = json.dumps({"consultations": sessions}, ensure_ascii=False, indent=4)
    with open(filepath, 'w', encoding='utf-8') as json_file:
        json.dump({"consultations": sessions}, json_file, ensure_ascii=False, indent=4)


#RespondIntoJson(text, 0, "data/UserCards")