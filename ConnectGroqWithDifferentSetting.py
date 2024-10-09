import os
import pandas as pd
from groq import Groq
import re

df = pd.read_csv('combination_correct_options.csv')
# df = pd.read_csv('combination_invented_options.csv') #change the file name manually or add another loop, plz. And you also need to change the file name in line72
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
temperatures = ['0','default']
messages = ["Please respond with only the letter of the solution, in the format {'sol': 'solution'}' "
            '''
            The following are multiple choice questions (with answers) about abstract algebra.

            Question: Statement 1 | If aH is an element of a factor group, then |aH| divides |a|. Statement 2 | If H and K are subgroups of G then HK is a subgroup of G.
            a. True, True
            b. False, False
            c. True, False
            d. False, True
            'sol': 'b'
            
            Question: Find all c in Z_3 such that Z_3[x]/(x^2 + c) is a field.
            a. 0
            b. 1
            c. 2
            d. 3
            'sol': 'b'
            
            Question: Find the characteristic of the ring 2Z.
            a. 0
            b. 3
            c. 12
            d. 30
            'sol': 'a'
            
            Question: Statement 1| Every function from a finite set onto itself must be one to one. Statement 2 | Every subgroup of an abelian group is abelian.
            a. True, True
            b. False, False
            c. True, False
            d. False, True
            'sol': 'a'
            
            Question: Statement 1 | Every element of a group generates a cyclic subgroup of the group. Statement 2 | The symmetric group S_10 has 10 elements.
            a. True, True
            b. False, False
            c. True, False
            d. False, True
            'sol': 'c'
                        ''',
            "Please respond and include in the end the letter of the solution, in the format {'sol': 'solution'}"]
            # "Here is an example:'Question: Statement 1 | If aH is an element of a factor group, then |aH| divides |a|. Statement 2 | If H and K are subgroups of G then HK is a subgroup of G."
            # "a) True, True b) False, False c) True, False d) False, True"
            # " {'sol': 'b'}",
            # "Please respond and include in the end the letter of the solution, in the format {'sol': 'solution'}"]
print(messages[0])
column_name = ['direct', 'afterReasoning']
# model_name = 'llama3-groq-8b-8192-tool-use-preview'
model_name = 'mixtral-8x7b-32768'
for index_message, systemMessage in enumerate(messages):
    for temperature in temperatures:
        for index, row in df.iterrows():
            question = row['question']
            choices = row['choices'].replace('[', '').replace(']', '')
            choices_list = choices.split(',,')
            letters = ['a) ', 'b) ', 'c) ', 'd) ']
            choices_with_letters = zip(letters, choices_list)
            labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]
            choices = " ".join(labeled_choices)
            message_content = f"{question} Choices: {choices}."
            # print(message_content)
            if temperature == '0':
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": systemMessage
                        },
                        {
                            "role": "user",
                            "content": message_content
                        }
                    ],
                    model=model_name,
                    temperature=0,
                )
            else:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": systemMessage
                        },
                        {
                            "role": "user",
                            "content": message_content
                        }
                    ],
                    model=model_name,
                )
            match = re.search(r"\{'sol': '([a-z])'\}", chat_completion.choices[0].message.content)
            print(str(index) + chat_completion.choices[0].message.content)
            if match:
                answer = match.group(1)
                df.at[index, 'answer_' + column_name[index_message]+'_temperature_'+temperature] = answer
            else:
                if (chat_completion.choices[0].message.content.startswith(
                        r"I'm sorry but I do not have the capability to perform this task for you")): #For Llama3-Groq-8B, it works well. For other models, you may need to redesign this line.
                    answer = 'error'
                    df.at[index, 'answer_' + column_name[index_message]+'_temperature_'+temperature] = answer
                else:
                    answer = 'error ' + chat_completion.choices[0].message.content  #To replace the answers manually, cause sometimes models just answer 'a' or similar unexpected answers.
                    # print(answer)
                    df.at[index, 'answer_' + column_name[index_message]+'_temperature_'+temperature] = answer
        df.to_csv('combinations_correct_options_multiple_setting.csv', index=False) #Save after every 2400 petitions, so if an error occurs, we won't lose all the current results.
        # df.to_csv('combinations_invented_options_multiple_setting.csv', index=False)


