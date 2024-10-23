import pandas as pd
import itertools
import re
# Read the CSV file
df = pd.read_excel('csv/anatomy.xlsx')# college_biology anatomy
# df = pd.read_csv('test_dataset.csv')
# df = pd.read_csv('updated_file.csv')

# Define a function to generate all possible combinations of answers for a given question
def generate_combinations(options, correct_answer):
    # options_list = re.findall(r"'(.*?)'", options)# for correct options
    options_list = [opt.strip() for opt in options.split(',,')]# for generated options
    correct_answer_indices = list(map(int, str(correct_answer).split(',')))
    combinations = list(itertools.permutations(options_list))

    answer_positions = []
    for combo in combinations:
        new_correct_answer = [combo.index(options_list[i]) for i in correct_answer_indices]
        answer_positions.append(','.join(map(str, new_correct_answer)))
    return combinations, answer_positions



# Apply the function to each row in the DataFrame
df['choices'] = df['choices'].apply(lambda x: x.strip('[]').replace("' ", "',"))
df['choices'] = df['choices'].apply(lambda x: x.strip(','))
df['combinations_and_answers'] = df.apply(lambda row: generate_combinations(row['choices'], row['answer']), axis=1)

df['combinations'] = df['combinations_and_answers'].apply(lambda x: x[0])
df['new_answer'] = df['combinations_and_answers'].apply(lambda x: x[1])

df = df.explode(['combinations', 'new_answer'])

df['answer'] = df['new_answer'].apply(lambda x: ','.join(map(str, x)))

df['choices'] = df['combinations'].apply(lambda x: '[{}]'.format(',, '.join(x)))

df.drop(columns=['combinations_and_answers', 'new_answer', 'combinations'], inplace=True)
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
df.to_csv('csv/anatomy_combinations.csv', index=False)# college_biology
# df.to_csv('combination_invented_options.csv', index=False)