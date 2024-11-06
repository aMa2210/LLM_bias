import os
import pandas as pd
import re
from openai import OpenAI

client = OpenAI()
mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
# message_system = "Please respond with only the letter of the solution, in the format {'sol': 'solution'}. If you do not know the answer you should pick one option randomly"
# message_system = "Please respond with only the letter of the solution, in the format {'sol': 'solution'}."
# message_system = "Por favor, responde solo con la letra de la solución, en el formato {'sol': 'solución'}." #Spanish
message_system = "请仅以字母形式回复答案，格式为 {'sol': 'solution'}。"   #Chinese
model_names = ['gpt-4o-mini-2024-07-18']
##### model_names = ['gpt-4o-mini-2024-07-18','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIwcOVxj'] #model fined tuned by 1056 data
# model_names = ['gpt-4o-mini-2024-07-18','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIu9SNHG'] #model fined tuned by 176 data
# model_names = ['gpt-4o-mini-2024-07-18','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan-3kdata:AKgiQ1hk'] #model fined tuned by 3k data
# model_names = ['ft:gpt-4o-mini-2024-07-18:ging-upm:tairan-3kdata:AKgiQ1hk'] #model fined tuned by 3k data
# model_names = ['ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIwcOVxj'] #model fined tuned by 1056 data
# model_names = ['gpt-4o-mini-2024-07-18','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIu9SNHG','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan-3kdata:AKgiQ1hk'] #ori ftBy176 ftBy3k
# model_names = ['ft:gpt-4o-mini-2024-07-18:ging-upm:tairan-176data:AQSJvx45'] #ft by 176 with (n_epochs=3, batch_size=3, learning_rate_multiplier=0.05)
# file_name = 'college_biology_combinations'
# file_name = 'combination_correct_options'
file_name = 'MMLU_chinese_randomOptions_combinations'
# file_name = 'Dataset_3k_randomOptions'
# file_name = 'combination_invented_options'
data_name = 'csv/'+file_name+'.xlsx'
result_name = 'result/'+file_name+'_result.csv'
df = pd.read_excel(data_name)
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
                # message_content = f"{question} Choices: {choices}."
                # message_content = f"{question} Opciones: {choices}."  # for Spanish
                message_content = f"{question} 选项: {choices}."  # for Chinese
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
                    elif model_name == 'ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIu9SNHG':
                        df.at[index, 'answer_fine-tuned_temperature:0_ftby176'] = answer
                    elif model_name == 'ft:gpt-4o-mini-2024-07-18:ging-upm:tairan-3kdata:AKgiQ1hk':
                        df.at[index, 'answer_fine-tuned_temperature:0_ftby3k'] = answer
                    elif model_name == 'ft:gpt-4o-mini-2024-07-18:ging-upm:tairan-176data:AQSJvx45':
                        df.at[index, 'answer_fine-tuned_temperature:0_ftby176_para:3_3_0.05'] = answer
                    # else:
                    #     raise ValueError('wrong model name')

                else:
                    answer = 'error ' + completion.choices[
                        0].message.content  # To replace the answers manually, cause sometimes models just answer 'a' or similar unexpected answers.
                    print(answer)
                    if model_name == 'gpt-4o-mini-2024-07-18':
                        df.at[index, 'answer_original_temperature:0'] = answer
                    elif model_name == 'ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIu9SNHG':
                        df.at[index, 'answer_fine-tuned_temperature:0_ftby176'] = answer
                    elif model_name == 'ft:gpt-4o-mini-2024-07-18:ging-upm:tairan-3kdata:AKgiQ1hk':
                        df.at[index, 'answer_fine-tuned_temperature:0_ftby3k'] = answer
                    elif model_name == 'ft:gpt-4o-mini-2024-07-18:ging-upm:tairan-176data:AQSJvx45':
                        df.at[index, 'answer_fine-tuned_temperature:0_ftby176_para:3_3_0.05'] = answer
            except Exception as row_e:
                print(f"Error processing index {index} with model {model_name}: {row_e}")
                df.at[index, 'processing_error'] = str(row_e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    df.to_csv(result_name, index=False)
    print(f"Results have been saved to {result_name}")
