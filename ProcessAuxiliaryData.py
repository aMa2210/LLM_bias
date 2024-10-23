import pandas as pd
import json
import re

csv_file_path = 'csv/test_dataset_6k.csv'
df = pd.read_csv(csv_file_path)



def clean_data_string(data_str):

    print('before: '+data_str)
    data_str = data_str.replace(', ,', ',')
    data_str = data_str.replace('array(', '').replace('dtype=object),', '')
    data_str = data_str.replace("'answer'","\"answer\"")
    data_str = data_str.replace("'choices'", "\"choices\"")
    data_str = data_str.replace("'question'", "\"question\"")
    data_str = data_str.replace("'subject'", "\"subject\"")
    print('after: '+data_str)
    pattern_answer = r'"answer":\s*(\d+)'
    pattern_choices = r'"choices":\s*(\[.*?\])'
    pattern_question = r'"question":\s*"(.*?)"'
    # pattern_subject = r'"subject":\s*"(.*?)"'
    pattern_question_2 = r'"question":\s*\'(.*?)\''
    # 提取字段
    answer = re.search(pattern_answer, data_str, re.DOTALL).group(1)
    choices = re.search(pattern_choices, data_str, re.DOTALL).group(1)
    if re.search(pattern_question, data_str):
        question = re.search(pattern_question, data_str, re.DOTALL).group(1)
    else:
        question = re.search(pattern_question_2, data_str, re.DOTALL).group(1)
    # subject = re.search(pattern_subject, data_str).group(1)

    # 打印结果
    print("Answer:", answer)
    print("Choices:", choices)
    print("Question:", question)
    # print("Subject:", subject)
    return answer, choices, question


def parse_data(row):
    data_str = row['train']  # 读取 'train' 列的值
    answer, choices, question = clean_data_string(data_str)

    row['answer'] = answer
    row['choices'] = choices
    row['question'] = question

    return row

parsed_df = df.apply(parse_data, axis=1)
parsed_df.drop(columns=['train'], inplace=True)

df_unique = parsed_df.drop_duplicates(subset=['question']) # since for some reason, this dataset contains same questions

df_3k = df_unique.head(3000)

df_3k.to_csv('csv/test_dataset_3k_processed.csv', index=False)
