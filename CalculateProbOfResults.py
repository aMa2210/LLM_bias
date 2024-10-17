import pandas as pd

# 读取CSV文件
# df = pd.read_csv('result/FinetuneData_combination_withoutAnswer_result.csv')
df = pd.read_csv('result/combination_correct_options_result_temperature0.csv')

column_values = df['answer_original_temperature:0']
value_counts = column_values.value_counts(normalize=True)
selected_values = value_counts.reindex([0, 1, 2, 3], fill_value=0)

print(selected_values)

column_values = df['answer_fine-tuned_temperature:0']
value_counts = column_values.value_counts(normalize=True)
selected_values = value_counts.reindex([0, 1, 2, 3], fill_value=0)

# 输出结果
print(selected_values)

