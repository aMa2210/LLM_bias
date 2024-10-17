import pandas as pd

df = pd.read_csv('result/combination_correct_options_result_temperature0.csv', encoding='ISO-8859-1')

column1 = 'answer'
column2 = 'answer_original_temperature:0'
column3 = 'answer_fine-tuned_temperature:0'
column4 = 'answer_fine-tuned_temperature:0ftby1056data'
column5 = 'answer_original_temperature:0_promptNoRandomHint'
column6 = 'answer_fine-tuned_temperature:0_promptNoRandomHint'


equal_values_ori = df[column1] == df[column2]
equal_values_ft = df[column1] == df[column3]
equal_values_ftby1056 = df[column1] == df[column4]
equal_values_ori_noHint = df[column1] == df[column5]
equal_values_ft_noHint = df[column1] == df[column6]
# for index, row in df.iterrows():
#     if row[column2] != row[column3]:
#         print(str(index)+': '+'ori: '+str(row[column2])+'  ft: '+str(row[column3]))

count_ori = equal_values_ori.sum()
count_ft = equal_values_ft.sum()
count_ftby1056 = equal_values_ftby1056.sum()
count_ori_noHint = equal_values_ori_noHint.sum()
count_ft_noHint = equal_values_ft_noHint.sum()


prob_ori = count_ori / len(df)
prob_ft = count_ft / len(df)
prob_ftby1056 = count_ftby1056 / len(df)
prob_ori_noHint = count_ori_noHint / 2398
prob_ft_noHint = count_ft_noHint / 2399


print('correct num of original model: '+str(count_ori))
print('correct num of finetuned model: '+str(count_ft))
print('correct num of finetunedby1056 model: '+str(count_ftby1056))
print('correct num of ori_noHint model: '+str(count_ori_noHint))
print('correct num of ft_noHint model: '+str(count_ft_noHint))

print('correct probability of original model: '+str(prob_ori))
print('correct probability of finetuned model: '+str(prob_ft))
print('correct probability of finetunedby1056 model: '+str(prob_ftby1056))
print('correct probability of ori_noHint model: '+str(prob_ori_noHint))
print('correct probability of ft_noHint model: '+str(prob_ft_noHint))