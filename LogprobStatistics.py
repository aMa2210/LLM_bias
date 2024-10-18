import os
import pandas as pd
import re
from openai import OpenAI

client = OpenAI()
mapping = {'a': 0, 'b': 1, 'c': 2, 'd': 3}

message_system = "Please respond with only the letter of the solution, in the format {'sol': 'solution'}. If you do not know the answer you should pick one option randomly"
# message_system = "Please respond with only the letter of the solution, in the format {'sol': 'solution'}."
# model_name = 'gpt-4o-mini-2024-07-18'
##### model_names = ['gpt-4o-mini-2024-07-18','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIwcOVxj'] #model fined tuned by 1056 data
model_names = ['gpt-4o-mini-2024-07-18','ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIu9SNHG'] #model fined tuned by 176 data
# model_names = ['ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIu9SNHG'] #model fined tuned by 176 data
# model_names = ['ft:gpt-4o-mini-2024-07-18:ging-upm:tairan:AIwcOVxj'] #model fined tuned by 1056 data


file_name = 'FinetuneData_combination_withoutAnswer'
# file_name = 'tmp'
# file_name = 'combination_invented_options'
data_name = 'csv/'+file_name+'.csv'
result_name = 'result/'+file_name+'_logprob_temperature0.csv'
df = pd.read_csv(data_name)
print(message_system)
assistant_content = "{'sol': '"
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
                        {"role": "user", "content": message_content},
                        {"role": "assistant", "content": assistant_content}
                    ],
                    temperature=0,
                    logprobs=True,
                    top_logprobs=4,
                    # max_tokens=1
                )
                # match = re.search(r"([a-d])", completion.choices[0].message.content)
                # print(str(index) + completion.choices[0].message.content)
                choice = completion.choices[0]
                logprobs = choice.logprobs.content[4].top_logprobs
                probabilities = [pow(10, logprob.logprob) for logprob in logprobs if logprob is not None]
                text = [logprob.token for logprob in logprobs if logprob is not None]
                a = sum(probabilities)
                probabilities = [probability/a for probability in probabilities]
                print(sum(probabilities))
                for i in range(4):
                    print(str(text[i]) + "  probability  " + str(probabilities[i]))
                    if model_name == 'gpt-4o-mini-2024-07-18':
                        df.at[index,str(text[i])+'_ori'] = str(probabilities[i])
                    else:
                        df.at[index, str(text[i])+'_ft'] = str(probabilities[i])
            except Exception as row_e:
                print(f"Error processing index {index} with model {model_name}: {row_e}")
                df.at[index, 'processing_error'] = str(row_e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    df.to_csv(result_name, index=False)
    print(f"Results have been saved to {result_name}")
