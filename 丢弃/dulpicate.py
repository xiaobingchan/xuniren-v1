from difflib import SequenceMatcher

target_text = "我们公司是与云计算伴生的一项基于超级计算机系统对外提供计算资源、存储资源等服务的机构或单位，以高性能计算机为基础面向各界提供高性能计算服务。"
input_text = "计算机系统对外提供计算资源、存储资源等服务的机构或单位"

similarity_ratio = SequenceMatcher(None, target_text, input_text).ratio()
print(similarity_ratio)
if similarity_ratio >= 0.3:
    print('False')
else:
    print('true')
