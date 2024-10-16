import pandas as pd
import json

mapping = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}
output_json = []
output_file = 'output_finetune_data.jsonl'
# df = pd.read_csv('100invented_options.csv')
df = pd.read_csv('csv/FinetuneData_combination.csv')
messages = "Please respond with only the letter of the solution, in the format {'sol': 'solution'}. If you do not know the answer you should pick one option randomly"
print(messages)
with open(output_file, 'w') as outfile:
    for index, row in df.iterrows():
        question = row['question']
        choices = row['choices'].replace('[', '').replace(']', '')
        choices_list = choices.split(',,')
        letters = ['a) ', 'b) ', 'c) ', 'd) ']
        choices_with_letters = zip(letters, choices_list)
        labeled_choices = [f"{letter}{choice.strip()}" for letter, choice in choices_with_letters]
        choices = " ".join(labeled_choices)
        message_content = f"{question} Choices: {choices}."
        print(message_content)
        answer = r"{'sol': '" + mapping[row['answer']]+r"'}"
        print(answer)
        json_line = {
            "messages": [
                {"role": "system", "content": messages},
                {"role": "user", "content": message_content},
                {"role": "assistant", "content": answer}
            ]
        }

        # Write each JSON object as a line
        outfile.write(json.dumps(json_line) + '\n')

