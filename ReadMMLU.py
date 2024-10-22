import pandas as pd

# splits = {'test': 'abstract_algebra/test-00000-of-00001.parquet', 'validation': 'abstract_algebra/validation-00000-of-00001.parquet', 'dev': 'abstract_algebra/dev-00000-of-00001.parquet'}
# df = pd.read_parquet("hf://datasets/cais/mmlu/" + splits["test"])
df = pd.read_parquet("hf://datasets/cais/mmlu/" + 'auxiliary_train')
df = df.head(6000)
df.to_csv('csv/test_dataset_6k.csv', index=False)