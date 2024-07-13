from gensim import corpora, similarities, models
import jieba
import pandas as pd
from fuzzywuzzy import fuzz
import time
import openpyxl

start_time = time.time()

# 加载Excel文件
workbook = openpyxl.load_workbook('知识库问答模板-骏宇文博-4ab96e6a-4749-4495-adbb-3c217441e161.xlsx')
sheet = workbook.active
# 初始化问题和答案列表
questions = []
answers = []
videoimg_list = []
excel_length = 0
# 遍历Excel中的数据
for row in sheet.iter_rows(min_row=2, values_only=True):
   if isinstance(row[0], str) and isinstance(row[1], str):
      questions.append(row[0].replace("\n", ""))
      answers.append(row[1])
      videoimg_list.append("stop")
      excel_length=excel_length+1

question = '公司在什么位置'
# excel = pd.ExcelFile("知识库问答模板-骏宇文博-4ab96e6a-4749-4495-adbb-3c217441e161.xlsx")
# data = excel.parse(0)
data = pd.DataFrame({'question': questions, 'answer': answers})
a = data.question.apply(lambda user: fuzz.ratio(user, question))
a = a.nlargest(5).reset_index()
a.columns = ["question", "similar"]
a.question = data.question[a.question].values
df = pd.DataFrame(a)
first_row_values = df.iloc[0, [0, 1]]
if float(first_row_values['similar'])>40.0:
    print("第一行的 'question' 数据：", first_row_values['question'])
    print("相似度：", first_row_values['similar'])

    df = pd.DataFrame(data)
    result = df.loc[df['question'] == first_row_values['question'], 'answer'].values[0]
    print(result)



# 记录程序结束时间
end_time = time.time()
# 计算程序运行时间
run_time = end_time - start_time
print(f"程序运行时间为： {run_time:.4f} 秒")