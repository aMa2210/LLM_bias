import pandas as pd


# df = pd.read_csv('result/FinetuneData_combination_withoutAnswer_result.csv')
# df = pd.read_csv('result/combination_correct_options_result_temperature0.csv')
# df = pd.read_csv('result/combination_correct_options_result_temperature0.csv', encoding='ISO-8859-1')
# df = pd.read_csv('result/Dataset_3k_randomOptions_result_temperature0.csv', encoding='ISO-8859-1')
df = pd.read_csv('result/combination_correct_options_result_temperature0_ftBy3kData.csv', encoding='ISO-8859-1')


# column_values = df['answer_original_temperature:0']
# value_counts = column_values.value_counts(normalize=True)
# value_counts_num = column_values.value_counts(normalize=False)
# selected_values = value_counts.reindex([0, 1, 2, 3], fill_value=-1)
# selected_values_num = value_counts_num.reindex([0, 1, 2, 3], fill_value=-1)
# print(selected_values)
# # print(selected_values_num)
# print(sum(selected_values_num))
#
# column_values = df['answer_fine-tuned_temperature:0']
# value_counts = column_values.value_counts(normalize=True)
# value_counts_num = column_values.value_counts(normalize=False)
# selected_values = value_counts.reindex([0, 1, 2, 3], fill_value=-1)
# selected_values_num = value_counts_num.reindex([0, 1, 2, 3], fill_value=-1)
# print(selected_values)
# # print(selected_values_num)
# print(sum(selected_values_num))



# column_values = df['answer_fine-tuned_temperature:0ftby1056data']
# value_counts = column_values.value_counts(normalize=True)
# value_counts_num = column_values.value_counts(normalize=False)
# selected_values = value_counts.reindex([0, 1, 2, 3], fill_value=-1)
# selected_values_num = value_counts_num.reindex([0, 1, 2, 3], fill_value=-1)
# print(selected_values)
# # print(selected_values_num)
#
#

column_values = df['answer_original_temperature:0_promptNoRandomHint']
column_values = column_values[column_values != -1]
value_counts = column_values.value_counts(normalize=True)
value_counts_num = column_values.value_counts(normalize=False)
selected_values = value_counts.reindex([0, 1, 2, 3], fill_value=-1)
selected_values_num = value_counts_num.reindex([0, 1, 2, 3], fill_value=-1)
print(selected_values)
print(sum(selected_values_num))



column_values = df['answer_fine-tuned_temperature:0_promptNoRandomHint']
column_values = column_values[column_values != -1]
value_counts = column_values.value_counts(normalize=True)
value_counts_num = column_values.value_counts(normalize=False)
selected_values = value_counts.reindex([0, 1, 2, 3], fill_value=-1)
selected_values_num = value_counts_num.reindex([0, 1, 2, 3], fill_value=-1)
print(selected_values)
print(sum(selected_values_num))