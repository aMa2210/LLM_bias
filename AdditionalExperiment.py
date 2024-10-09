import os
import pandas as pd
from groq import Groq
import re


# df = pd.read_csv('combinations_file.csv')
df = pd.read_csv('50questions_invented_options.csv')
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
model_list = ['llama3-groq-8b-8192-tool-use-preview', 'mixtral-8x7b-32768', 'llama-3.1-70b-versatile', 'gemma2-9b-it']
for model_name in model_list:
    for i in range(10):
        for index, row in df.iterrows():
            question = row['question']
            choices = row['choices'].replace('[', '').replace(']', '')
            choices_list = choices.split(',,')
            letters = ['a) ', 'b) ', 'c) ', 'd) ']
            choices_with_letters = zip(letters, choices_list)
            labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]
            choices = " ".join(labeled_choices)
            systemMessage = r"Please respond with only the letter of the solution, in the format {{'sol': 'solution'}}. If " \
                            r"you do not know the answer please select one of the letters a/b/c/d randomly with equal " \
                            r"probability "
            message_content = f"{question} Choices: {choices}. "
            print(message_content)
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
                # logprobs=True
            )
            match = re.search(r"\{'sol': '([a-z])'\}", chat_completion.choices[0].message.content)
            # print(str(index) + chat_completion.choices[0].message.content)
            if match:
                answer = match.group(1)
                df.at[index, 'answer_' + model_name + '_'+str(i)] = answer
            else:
                if (chat_completion.choices[0].message.content.startswith(
                        r"I'm sorry but I do not have the capability to perform this task for you")):  # For Llama3-Groq-8B, it works well. For other models, you may need to redesign this line.
                    answer = 'error'
                    df.at[index, 'answer_' + model_name + '_'+str(i)] = answer
                else:
                    answer = 'error ' + chat_completion.choices[
                        0].message.content  # To replace the answers manually, cause sometimes models just answer 'a' or similar unexpected answers.
                    # print(answer)
                    df.at[index, 'answer_' + model_name + '_'+str(i)] = answer
    df.to_csv('50questions_invented_options_answers.csv', index=False)


