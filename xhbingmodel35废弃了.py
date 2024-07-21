# 开发文档：https://www.xfyun.cn/doc/spark/Web.html#%E5%BF%AB%E9%80%9F%E8%B0%83%E7%94%A8%E9%9B%86%E6%88%90%E6%98%9F%E7%81%AB%E8%AE%A4%E7%9F%A5%E5%A4%A7%E6%A8%A1%E5%9E%8B%EF%BC%88python%E7%A4%BA%E4%BE%8B%EF%BC%89
# 控制台：https://console.xfyun.cn/services/bm35
# pip install --upgrade spark_ai_python
# pip install spark-ai-python
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import argparse
import re

#星火认知大模型v3.5的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = 'da15ae5e'
SPARKAI_API_SECRET = 'Mzg4MDBmYzZjMWY1YjE1ODIwOTI4YzRj'
SPARKAI_API_KEY = '96e4dfe7579d46b8cf09c993499c6883'
#星火认知大模型v3.5的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'

def remove_special_chars(text):
    # 定义需要删除的特殊字符集
    special_chars = r'[*\n\-\(\)\~\:\.\”\“\： ]'
    # 使用正则表达式替换特殊字符
    text = re.sub(special_chars, '', text)
    cleaned_text = re.sub(r'、', ',', text)
    return cleaned_text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("textcontent", help="The path to the audio file")
    args = parser.parse_args()
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content=args.textcontent
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    result = remove_special_chars(a.generations[0][0].text)
    print(result)

