import pandas as pd
import itertools
import re
import random

random.seed(613)
# Read the CSV file
df = pd.read_csv('csv/FinetuneData.csv')
# df = pd.read_csv('test_dataset.csv')
# df = pd.read_csv('updated_file.csv')

# Define a function to generate all possible combinations of answers for a given question
def generate_combinations(options):
    # options_list = re.findall(r"'(.*?)'", options)# for correct options
    options_list = [opt.strip() for opt in options.split(',,')]# for generated options
    all_combinations = list(itertools.permutations(options_list))  # 生成所有选项组合
    if len(all_combinations) > 4:
        combinations = random.sample(all_combinations, 4)  # 随机选取4种组合
    else:
        combinations = all_combinations
    # combinations = all_combinations
    # combinations = combinations[:4]
    return combinations



# Apply the function to each row in the DataFrame
df['choices'] = df['choices'].apply(lambda x: x.strip('[]').replace("' ", "',"))
df['choices'] = df['choices'].apply(lambda x: x.strip(','))
df['combinations'] = df.apply(lambda row: generate_combinations(row['choices']), axis=1)



df = df.explode('combinations')
df = df.reset_index(drop=True)
df_new = []
for _, row in df.iterrows():
    for i in range(4):
        new_row = row.copy()  # 复制原始行
        new_row['answer'] = i  # 修改目标列为 0-3
        df_new.append(new_row)

df = pd.DataFrame(df_new)
df['choices'] = df['combinations'].apply(lambda x: '[{}]'.format(',, '.join(x)))

# df_new.drop(columns=['combinations'], inplace=True)
df.drop(columns=['combinations'], inplace=True)
# df.drop(columns=['answer'], inplace=True)
#
#
# df['choices'] = df['combinations_and_answers'].apply(lambda x: x[0])
# df['answer'] = df['combinations_and_answers'].apply(lambda x: x[1])
#
# # Explode the combinations into new rows
# df = df.explode('choices')
# df['answer'] = df['answer'].apply(lambda x: x[0] if isinstance(x, list) else x)
#
# # Convert the combinations to a string (optional)
# df['choices'] = df['choices'].apply(lambda x: '[{}]'.format(',, '.join(x)))

# Save the updated DataFrame to a new CSV file
# df.to_csv('csv/FinetuneData_combination_withoutAnswer.csv', index=False)
df.to_csv('csv/FinetuneData_combination_176.csv', index=False)
# df.to_csv('combination_correct_options.csv', index=False)
# df.to_csv('combination_invented_options.csv', index=False)