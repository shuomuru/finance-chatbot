import requests
import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder

os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

API_KEY = "sk-kywukyiplhdhmnbkegbmqcfvqzgfixmtmhymwgqbmtffdvjx"
API_URL = "https://api.siliconflow.cn/v1/chat/completions"

BASE_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
FINE_TUNED_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

embedding = HuggingFaceEmbeddings(model_name="BAAI/bge-large-zh-v1.5")
db = FAISS.load_local(
    "faiss_db",
    embedding,
    allow_dangerous_deserialization=True
)
retriever = db.as_retriever(search_kwargs={"k": 5})

rerank_model = CrossEncoder("BAAI/bge-reranker-base")

SYSTEM_PROMPT_WITH_CONTEXT = """
你是专业的金融领域助手。

## 回答规则：
1. 优先根据提供的参考资料回答问题。
2. 如果参考资料中有相关信息，请结合资料进行回答，确保准确。
3. 如果参考资料与问题无关或信息不足，可以使用你自身的金融知识进行回答。
4. 回答要简洁、专业、准确。

## 参考资料：
{context}
"""

SYSTEM_PROMPT_WITHOUT_CONTEXT = """
你是专业的金融领域助手。

## 回答规则：
1. 请根据你自身的金融知识回答问题。
2. 回答要简洁、专业、准确。
3. 如果不确定，可以说明。
"""

def get_context_with_score(question):
    """获取检索到的上下文及相关性分数"""
    docs = retriever.invoke(question)
    texts = [doc.page_content for doc in docs]
    
    if not texts:
        return "", 0.0
    
    pairs = [[question, t] for t in texts]
    scores = rerank_model.predict(pairs)
    ranked = sorted(zip(texts, scores), key=lambda x: x[1], reverse=True)
    
    top_context = "\n".join([t for t, s in ranked[:2]])
    highest_score = ranked[0][1] if ranked else 0.0
    
    return top_context, highest_score

def chat_with_cloud_model(question, model_name):
    context, score = get_context_with_score(question)
    
    # 判断是否有有效上下文（相关性分数阈值设为 0.5）
    has_valid_context = score > 0.5 and context.strip()
    
    if has_valid_context:
        system_prompt = SYSTEM_PROMPT_WITH_CONTEXT.format(context=context)
    else:
        system_prompt = SYSTEM_PROMPT_WITHOUT_CONTEXT
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": 0.1,
        "top_p": 0.9
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    return result["choices"][0]["message"]["content"]

def chat_finance(question):
    return chat_with_cloud_model(question, FINE_TUNED_MODEL_NAME)

def chat_finance_base(question):
    return chat_with_cloud_model(question, BASE_MODEL_NAME)

def chat_finance_compare(question):
    base_answer = chat_finance_base(question)
    fine_tuned_answer = chat_finance(question)
    return {
        "base_model": base_answer,
        "fine_tuned_model": fine_tuned_answer
    }

if __name__ == "__main__":
    question = input("请输入金融问题：")
    print("\n📊 正在进行模型对比...")
    result = chat_finance_compare(question)
    print("\n🔵 基座模型：", result["base_model"])
    print("\n🟢 微调模型：", result["fine_tuned_model"])
