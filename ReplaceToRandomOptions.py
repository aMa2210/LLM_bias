import pandas as pd
import json
import random

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('csv/test_dataset_3k_randomOptions.csv')
# df = pd.read_csv('csv/test_dataset_3k_processed.csv')

# Load the words dictionary from the JSON file
with open('words_dictionary.json') as f:
    words_dict = json.load(f)


# Define a function to randomly select a word from the dictionary
def get_random_word():
    return random.choice(list(words_dict.keys()))


# Apply the function to the 'choices' column to replace it with random words
df['choices'] = df['choices'].apply(lambda x: format(',,'.join([get_random_word() for _ in range(4)])))
i = 0
for index, row in df.iterrows():
    df.at[index, 'answer'] = i
    i += 1
    if i > 3:
        i = 0

# Save the updated DataFrame to a new CSV file
df.to_csv('csv/test_dataset_3k_randomOptions.csv', index=False)
