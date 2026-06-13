import streamlit as st
from openai import OpenAI
import re

def render_sandbox(api_key: str, model: str, system_prompt: str, agent_name: str, lang: str, base_url: str):
    t = {
        "English": {"title": "Live Sandbox", "info": "Test your agent directly here! If it misbehaves, you'll know you need to tweak the prompt.", "vars": "💡 Dynamic Variables Detected:", "chat": "Chat with your agent...", "err": "Please set your API Key in the sidebar."},
        "简体中文": {"title": "在线试聊", "info": "在这里直接和生成的智能体对话！如果它胡言乱语，说明需要重新修改提示词。", "vars": "💡 检测到动态插槽（请先填写上下文）：", "chat": "和你的智能体聊天...", "err": "请在左侧配置API Key。"},
        "繁體中文": {"title": "線上試聊", "info": "在這裡直接和生成的智能體對話！如果它胡言亂語，說明需要重新修改提示詞。", "vars": "💡 檢測到動態插槽（請先填寫上下文）：", "chat": "和你的智能體聊天...", "err": "請在左側配置API Key。"},
        "日本語": {"title": "オンライン試用", "info": "ここで生成されたエージェントと直接チャットできます！", "vars": "💡 動的変数スロットが検出されました：", "chat": "エージェントとチャット...", "err": "API Keyを設定してください。"}
    }.get(lang, {"title": "Live Sandbox", "info": "Test your agent!", "vars": "Template Variables detected:", "chat": "Chat with your agent...", "err": "Error"})

    st.markdown(f"### 🎮 {t['title']}: {agent_name}")
    st.info(t['info'])

    # Dynamic Variables parser (e.g. {{Topic}}, {{Product Name}})
    slots = list(set(re.findall(r'\{\{(.*?)\}\}', system_prompt)))

    filled_prompt = system_prompt
    if slots:
        st.markdown(f"**{t['vars']}**")
        cols = st.columns(len(slots) if len(slots) <= 3 else 3)
        slot_values = {}
        for i, slot in enumerate(slots):
            with cols[i % 3]:
                slot_values[slot] = st.text_input(slot, key=f"slot_{slot}_{agent_name}")

        # Replace slots in the prompt
        for slot, val in slot_values.items():
            if val.strip():
                filled_prompt = filled_prompt.replace(f"{{{{{slot}}}}}", val)
            else:
                # If empty, just put a generic placeholder so it doesn't break
                filled_prompt = filled_prompt.replace(f"{{{{{slot}}}}}", f"[{slot}]")

    # Reset chat history if agent changes
    if "sandbox_messages" not in st.session_state or st.session_state.get('sandbox_agent') != agent_name:
        st.session_state.sandbox_messages = []
        st.session_state.sandbox_agent = agent_name

    for msg in st.session_state.sandbox_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(t['chat']):
        if not api_key:
            st.error(t['err'])
            return

        st.session_state.sandbox_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                if base_url:
                    client = OpenAI(api_key=api_key, base_url=base_url)
                else:
                    client = OpenAI(api_key=api_key)
                messages = [{"role": "system", "content": filled_prompt}] + st.session_state.sandbox_messages
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.markdown(reply)
                st.session_state.sandbox_messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Execution Error: {e}")