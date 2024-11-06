import pandas as pd
from datasets import load_dataset

df = load_dataset("openai/MMMLU", "ES_LA")
df = pd.DataFrame(df['test'])
# splits = {'test': 'college_biology/test-00000-of-00001.parquet', 'validation': 'college_biology/validation-00000-of-00001.parquet', 'dev': 'college_biology/dev-00000-of-00001.parquet'}
# df = pd.read_parquet("hf://datasets/cais/mmlu/" + splits["test"])
# df = pd.read_parquet("hf://datasets/cais/mmlu/" + 'auxiliary_train')
df = df.head(100)
df.to_excel('csv/MMLU_spanish.xlsx', index=False)# college_biology anatomy
# df.to_excel('csv/MMLU_chinese.xlsx', index=False)# college_biology anatomy