import os
os.environ.setdefault("PYTHONIOENCODING", "utf-8")  # 文字化け・asciiエラー対策
import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

# .env を読み込み（このファイルと同じフォルダに置く）
load_dotenv(override=True)

st.set_page_config(page_title="専門家AIアシスタント", page_icon="🤖")

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    st.error(".env に OPENAI_API_KEY が見つかりません。")
    st.stop()

system_prompts = {
    "料理人": "あなたはミシュラン三ツ星レストランのシェフです。料理や食の質問に専門的に答えてください。",
    "心理カウンセラー": "あなたは経験豊富な心理カウンセラーです。相手に寄り添い、心理学に基づいて助言してください。",
    "フィットネストレーナー": "あなたは実績のあるフィットネストレーナーです。運動・栄養・健康管理を専門的に助言してください。",
}

st.title("専門家AIアシスタント")
st.write(
    "1) 専門家を選ぶ → 2) 相談内容を入力 → 3) 送信"
)

expert = st.radio("相談したい専門家：", list(system_prompts.keys()))
user_text = st.text_area("ご相談内容：", height=120)

def get_ai_response(text: str, expert_type: str) -> str:
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",      # お好みで変更可（gpt-4o / gpt-4.1-mini 等）
            temperature=0.7,
            api_key=API_KEY,          # langchain-openai 0.3系は api_key 引数名
        )
        msgs = [
            SystemMessage(content=system_prompts[expert_type]),
            HumanMessage(content=text),
        ]
        resp = llm.invoke(msgs)
        return resp.content
    except Exception as e:
        return f"エラーが発生しました: {e}"

if st.button("送信"):
    if not user_text.strip():
        st.warning("相談内容を入力してください。")
    else:
        with st.spinner("AIが考え中..."):
            answer = get_ai_response(user_text.strip(), expert)
        st.subheader("回答")
        st.write(answer)
