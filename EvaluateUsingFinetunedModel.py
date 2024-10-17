import os
import pandas as pd
import re
from openai import OpenAI

client = OpenAI()
mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
message_system = "Please respond with only the letter of the solution, in the format {'sol': 'solution'}. If you do not know the answer you should pick one option randomly"
# model_name = 'gpt-4o-mini-2024-07-18'
##### model_names = ['gpt-4o-mini-2024-07-18','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIwcOVxj'] #model fined tuned by 1056 data
model_names = ['gpt-4o-mini-2024-07-18','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIu9SNHG'] #model fined tuned by 176 data
# model_names = ['ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIu9SNHG'] #model fined tuned by 176 data


file_name = 'combination_correct_options'
# file_name = 'combination_invented_options'
data_name = 'csv/'+file_name+'.csv'
result_name = 'result/'+file_name+'_result_temperature0.csv'
df = pd.read_csv(data_name)
print(message_system)
try:
    for model_name in model_names:
        for index, row in df.iterrows():
            try:
                question = row['question']
                choices = row['choices'].replace('[', '').replace(']', '')
                choices_list = choices.split(',,')
                letters = ['a) ', 'b) ', 'c) ', 'd) ']
                choices_with_letters = zip(letters, choices_list)
                labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]
                choices = " ".join(labeled_choices)
                message_content = f"{question} Choices: {choices}."
                print(message_content)
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": message_system},
                        {"role": "user", "content": message_content}
                    ],
                    temperature=0
                )
                match = re.search(r"\{'sol': '([a-z])'\}", completion.choices[0].message.content)
                print(str(index) + completion.choices[0].message.content)
                if match:
                    answer = match.group(1)
                    answer = mapping[answer]
                    if model_name == 'gpt-4o-mini-2024-07-18':
                        df.at[index, 'answer_original_temperature:0'] = answer
                    else:
                        df.at[index, 'answer_fine-tuned_temperature:0'] = answer
                    # else:
                    #     raise ValueError('wrong model name')

                else:
                    answer = 'error ' + completion.choices[
                        0].message.content  # To replace the answers manually, cause sometimes models just answer 'a' or similar unexpected answers.
                    print(answer)
                    if model_name == 'gpt-4o-mini-2024-07-18':
                        df.at[index, 'answer_original_temperature:0'] = answer
                    else:
                        df.at[index, 'answer_fine-tuned_temperature:0'] = answer
            except Exception as row_e:
                print(f"Error processing index {index} with model {model_name}: {row_e}")
                # 可选：在DataFrame中记录错误信息
                df.at[index, 'processing_error'] = str(row_e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    df.to_csv(result_name, index=False)
    print(f"Results have been saved to {result_name}")
