import pandas as pd

df = pd.read_csv('result/combination_correct_options_result_temperature0_ftBy3kData.csv', encoding='ISO-8859-1')
# df = pd.read_csv('result/combination_correct_options_result_temperature0.csv', encoding='ISO-8859-1')


column1 = 'answer'
column2 = 'answer_original_temperature:0'
column3 = 'answer_fine-tuned_temperature:0'
column5 = 'answer_original_temperature:0_promptNoRandomHint'
column6 = 'answer_fine-tuned_temperature:0_promptNoRandomHint'


equal_values_ori = df[column1] == df[column2]
equal_values_ft = df[column1] == df[column3]
equal_values_ori_noHint = df[column1] == df[column5]
equal_values_ft_noHint = df[column1] == df[column6]
num_minus1_ori_noHint = sum(df[column5] == -1)
print('num_minus1_ori_noHint:' + str(num_minus1_ori_noHint))
num_minus1_ft_noHint = sum(df[column6] == -1)
print('num_minus1_ft_noHint:'+str(num_minus1_ft_noHint))
# for index, row in df.iterrows():
#     if row[column2] != row[column3]:
#         print(str(index)+': '+'ori: '+str(row[column2])+'  ft: '+str(row[column3]))

count_ori = equal_values_ori.sum()
count_ft = equal_values_ft.sum()
count_ori_noHint = equal_values_ori_noHint.sum()
count_ft_noHint = equal_values_ft_noHint.sum()


prob_ori = count_ori / len(df)
prob_ft = count_ft / len(df)
prob_ori_noHint = count_ori_noHint / (len(df)-num_minus1_ori_noHint)
prob_ft_noHint = count_ft_noHint / (len(df)-num_minus1_ft_noHint)


print('correct num of original model: '+str(count_ori))
print('correct num of finetuned model: '+str(count_ft))
print('correct num of ori_noHint model: '+str(count_ori_noHint))
print('correct num of ft_noHint model: '+str(count_ft_noHint))

print('correct probability of original model: '+str(prob_ori))
print('correct probability of finetuned model: '+str(prob_ft))
print('correct probability of ori_noHint model: '+str(prob_ori_noHint))
print('correct probability of ft_noHint model: '+str(prob_ft_noHint))


# Acc-H
group_size = 24
total_rows = len(equal_values_ori)
num_groups = total_rows // group_size  # 计算完整的组数

count_all_true_groups = 0

for i in range(num_groups):
    start_idx = i * group_size
    end_idx = start_idx + group_size
    group = equal_values_ori_noHint[start_idx:end_idx]
    if group.all():
        # print(i)
        count_all_true_groups += 1
print('acc-h num(ori): ', count_all_true_groups)

count_all_true_groups = 0
for i in range(num_groups):
    start_idx = i * group_size
    end_idx = start_idx + group_size
    group = equal_values_ft_noHint[start_idx:end_idx]
    if group.all():
        # print(i)
        count_all_true_groups += 1
print('acc-h num(ft): ', count_all_true_groups)
