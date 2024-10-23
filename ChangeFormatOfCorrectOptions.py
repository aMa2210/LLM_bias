import pandas as pd
import re
file_name = 'csv/college_biology.xlsx'#anatomy college_biology

df = pd.read_excel(file_name)

def process_string(s):
    # Remove brackets and split by spaces
    elements = s.strip("[]")
    elements = re.findall(r"'(.*?)'|\"(.*?)\"", elements)
    elements = [e[0] if e[0] else e[1] for e in elements]
    # Join elements using ',, ' separator
    return ',, '.join(elements)

# Apply the function to the column
df['choices'] = df['choices'].apply(process_string)
df.to_excel('csv/college_biology_2.xlsx', index=False)
# df.to_excel(file_name)