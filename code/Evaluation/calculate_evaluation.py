import pandas as pd
import re

# 读取CSV文件
df = pd.read_csv('gpt4_responses_en.csv')

# 定义一个函数来提取分数
def extract_scores(column):
    pattern = re.compile(r'(\w+): (\d)')
    scores_dict = {}
    
    for text in df[column].dropna():
        if not text.strip():
            continue
        
        matches = pattern.findall(text)
        for match in matches:
            key, score = match
            if key not in scores_dict:
                scores_dict[key] = []
            scores_dict[key].append(int(score))
    
    return scores_dict


score_columns = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6']
all_scores = {}


for column in score_columns:
    column_scores = extract_scores(column)
    

    for key, values in column_scores.items():
        if key not in all_scores:
            all_scores[key] = []  
        all_scores[key].extend(values)  


average_scores = {key: sum(values) / len(values) for key, values in all_scores.items()}


for key, avg in average_scores.items():
    print(f"{key}: {avg:.2f}")


