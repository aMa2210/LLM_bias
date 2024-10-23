import pandas as pd

df = pd.read_csv('result/college_biology_combinations_result_temperature0.csv', encoding='ISO-8859-1')
# df = pd.read_csv('result/combination_correct_options_result_temperature0.csv', encoding='ISO-8859-1')


column1 = 'answer'
column2 = 'answer_original_temperature:0'
column3 = 'answer_fine-tuned_temperature:0_ftby176'
column4 = 'answer_fine-tuned_temperature:0_ftby3k'



equal_values_ori = df[column1] == df[column2]
equal_values_ftby176 = df[column1] == df[column3]
equal_values_ftby3k = df[column1] == df[column4]

num_minus1_ori = sum(df[column2] == -1)
print('num_minus1_ori:' + str(num_minus1_ori))
num_minus1_ftby176 = sum(df[column3] == -1)
print('num_minus1_ftby176:'+str(num_minus1_ftby176))
num_minus1_ftby3k = sum(df[column4] == -1)
print('num_minus1_ftby3k:'+str(num_minus1_ftby3k))
# for index, row in df.iterrows():
#     if row[column2] != row[column3]:
#         print(str(index)+': '+'ori: '+str(row[column2])+'  ft: '+str(row[column3]))

count_ori = equal_values_ori.sum()
count_ftby176 = equal_values_ftby176.sum()
count_ftby3k  = equal_values_ftby3k.sum()


prob_ori = count_ori / (len(df)-num_minus1_ori)
prob_ftby176 = count_ftby176 / (len(df)-num_minus1_ftby176)
prob_ftby3k = count_ftby3k / (len(df)-num_minus1_ftby3k)


print('correct num of original model: '+str(count_ori))
print('correct num of ftby176 model: '+str(count_ftby176))
print('correct num of ftby3k model: '+str(count_ftby3k))

print('correct probability of original model: '+str(prob_ori))
print('correct probability of ftby176 model: '+str(prob_ftby176))
print('correct probability of ftby3k model: '+str(prob_ftby3k))


# Acc-H
group_size = 24
total_rows = len(equal_values_ori)
num_groups = total_rows // group_size  # 计算完整的组数

count_all_true_groups = 0

for i in range(num_groups):
    start_idx = i * group_size
    end_idx = start_idx + group_size
    group = equal_values_ori[start_idx:end_idx]
    if group.all():
        # print(i)
        count_all_true_groups += 1
print('acc-h num(ori): ', count_all_true_groups)

count_all_true_groups = 0
for i in range(num_groups):
    start_idx = i * group_size
    end_idx = start_idx + group_size
    group = equal_values_ftby176[start_idx:end_idx]
    if group.all():
        # print(i)
        count_all_true_groups += 1
print('acc-h num(ftby176): ', count_all_true_groups)

count_all_true_groups = 0
for i in range(num_groups):
    start_idx = i * group_size
    end_idx = start_idx + group_size
    group = equal_values_ftby3k[start_idx:end_idx]
    if group.all():
        # print(i)
        count_all_true_groups += 1
print('acc-h num(ftby3k): ', count_all_true_groups)

