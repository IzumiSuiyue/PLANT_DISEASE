import os
from dashscope import Generation
from dotenv import load_dotenv
from difflib import get_close_matches
from app.disease_data import get_disease_dict

load_dotenv()

def get_advice(disease: str) -> str:
    prompt = f"请简要介绍“{disease}”病害的症状和发病原因，并提供3-5条控制措施，控制在500字以内。"
    try:
        response = Generation.call(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}],
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            timeout=10
        )
        return response["output"]["text"].strip()
    except Exception as e:
        return f"❗ 千问调用失败：{str(e)}"

def query_disease(name: str) -> tuple[str, str]:
    disease_dict = get_disease_dict()
    if name in disease_dict:
        info = disease_dict[name]
        return (
            f"🌿 病害名：{name}\n"
            f"🦠 症状：{info['symptom']}\n"
            f"📌 发病原因：{info['cause']}\n"
            f"🧪 防治措施：\n" + "\n".join([f"- {c}" for c in info['control']]),
            "local"
        )
    
    close = get_close_matches(name, disease_dict.keys(), n=3, cutoff=0.4)
    if close:
        suggestions = "\n".join([
            f"- {m}：{disease_dict[m]['symptom']}" for m in close
        ])
        return f"❗ 未找到“{name}”。你可能想输入：\n{suggestions}", "local"

    gpt_response = get_advice(name)
    return f"🤖 以下为AI生成内容（非本地知识库）：\n\n{gpt_response}", "gpt"
