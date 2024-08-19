import pandas as pd
import json

def add_id_to_records(data):
    """
    Add ID to each record in a list of dictionaries. The ID will have a string "t" followed by a number starting from 1.

    :param data: List of dictionaries
    :return: List of dictionaries with IDs added
    """
    for i, record in enumerate(data, start=1):
        record['ID'] = f"s{i}"
    return data

# 读取CSV文件
df = pd.read_csv('songci_with_popularity.csv')

# 过滤掉 PoemGoogleCounts 为 0 的行
df = df[df['PoemGoogleCounts'] > 0]

# 根据 PoemGoogleCounts 降序排序
df = df.sort_values(by='PoemGoogleCounts', ascending=False)

# 保留每首诗的 PoemAnalysis 列的前五分之一
def shorten_poem_analysis(poem_analysis):
    if pd.isna(poem_analysis):  # 处理缺失值
        return poem_analysis
    length = len(poem_analysis)
    return poem_analysis[:length // 5]

df['PoemAnalysis'] = df['PoemAnalysis'].apply(shorten_poem_analysis)
df = df[['Title', 'Author', 'Poem', 'PoemAnalysis', 'PoemGoogleCounts']]

# 将 DataFrame 转换为字典列表
data = df.to_dict(orient='records')

# 为每个记录添加 ID
data_with_id = add_id_to_records(data)

# 将处理后的数据保存到 JSON 文件
output_json_path = 'songci.json'
with open(output_json_path, 'w', encoding='utf-8') as file:
    json.dump(data_with_id, file, ensure_ascii=False, indent=4)

print(f"处理完成，结果已保存到 {output_json_path}")
