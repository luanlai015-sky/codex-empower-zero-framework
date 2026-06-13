import streamlit as st
from openai import OpenAI
import re

def render_arena(api_key: str, system_prompt: str, agent_name: str, lang: str, base_url: str, available_models: list):
    t = {
        "English": {"title": "A/B Model Arena", "info": "Test how different models interpret your System Prompt simultaneously.", "msg": "Send a message to both models:", "btn": "Fight! 🥊", "err": "Please set your API Key.", "fill": "💡 Fill template variables first:"},
        "简体中文": {"title": "大模型 A/B 竞技场", "info": "同一套提示词，分别发送给两个不同的模型，看看谁更聪明！", "msg": "给两个模型发送相同的指令：", "btn": "开始对决 🥊", "err": "请先配置 API Key。", "fill": "💡 请先填写动态插槽："},
        "繁體中文": {"title": "大模型 A/B 競技場", "info": "同一套提示詞，分別發送給兩個不同的模型，看看誰更聰明！", "msg": "給兩個模型發送相同的指令：", "btn": "開始對決 🥊", "err": "請先配置 API Key。", "fill": "💡 請先填寫動態插槽："},
        "日本語": {"title": "A/B アリーナ", "info": "同じプロンプトを異なるモデルに送信し、結果を比較します。", "msg": "両方のモデルにメッセージを送信：", "btn": "対決 🥊", "err": "API Keyを設定してください。", "fill": "💡 変数を入力してください："}
    }.get(lang, {"title": "A/B Model Arena", "info": "Test models.", "msg": "Message:", "btn": "Fight! 🥊", "err": "API Key missing.", "fill": "Fill variables:"})

    st.markdown(f"### ⚖️ {t['title']}")
    st.info(t['info'])

    # Handle variables for Arena too
    slots = list(set(re.findall(r'\{\{(.*?)\}\}', system_prompt)))
    filled_prompt = system_prompt

    if slots:
        st.markdown(f"**{t['fill']}**")
        cols = st.columns(len(slots) if len(slots) <= 3 else 3)
        slot_values = {}
        for i, slot in enumerate(slots):
            with cols[i % 3]:
                slot_values[slot] = st.text_input(slot, key=f"arena_slot_{slot}_{agent_name}")

        for slot, val in slot_values.items():
            if val.strip():
                filled_prompt = filled_prompt.replace(f"{{{{{slot}}}}}", val)
            else:
                filled_prompt = filled_prompt.replace(f"{{{{{slot}}}}}", f"[{slot}]")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        model_a = st.selectbox("Model A (Red Corner)", available_models, index=0, key="model_a")
    with col2:
        model_b = st.selectbox("Model B (Blue Corner)", available_models, index=min(1, len(available_models)-1), key="model_b")

    user_msg = st.text_area(t['msg'], height=100)

    if st.button(t['btn'], type="primary", use_container_width=True):
        if not api_key:
            st.error(t['err'])
            return
        if not user_msg.strip():
            return

        if base_url:
            client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            client = OpenAI(api_key=api_key)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"<div style='text-align: center; color: #EF4444; font-weight: bold;'>🔴 {model_a}</div>", unsafe_allow_html=True)
            with st.spinner("Generating..."):
                try:
                    res_a = client.chat.completions.create(
                        model=model_a,
                        messages=[{"role": "system", "content": filled_prompt}, {"role": "user", "content": user_msg}],
                        temperature=0.7
                    )
                    st.success(res_a.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")

        with c2:
            st.markdown(f"<div style='text-align: center; color: #3B82F6; font-weight: bold;'>🔵 {model_b}</div>", unsafe_allow_html=True)
            with st.spinner("Generating..."):
                try:
                    res_b = client.chat.completions.create(
                        model=model_b,
                        messages=[{"role": "system", "content": filled_prompt}, {"role": "user", "content": user_msg}],
                        temperature=0.7
                    )
                    st.info(res_b.choices[0].message.content)
                except Exception as e:
                    st.error(f"Error: {e}")