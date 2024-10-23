import pandas as pd

splits = {'test': 'college_biology/test-00000-of-00001.parquet', 'validation': 'college_biology/validation-00000-of-00001.parquet', 'dev': 'college_biology/dev-00000-of-00001.parquet'}
df = pd.read_parquet("hf://datasets/cais/mmlu/" + splits["test"])
# df = pd.read_parquet("hf://datasets/cais/mmlu/" + 'auxiliary_train')
# df = df.head(6000)
df.to_excel('csv/college_biology.xlsx', index=False)# college_biology anatomy