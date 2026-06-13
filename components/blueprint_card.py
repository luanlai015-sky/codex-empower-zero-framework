import streamlit as st

def render_blueprint_card(bp: dict, lang: str):
    labels = {
        "English": {"role": "Role", "user": "Target User", "mission": "Mission", "in": "Input Needed", "out": "Output Format", "risk": "Risk Level", "human": "Human Conf."},
        "简体中文": {"role": "角色定位", "user": "目标用户", "mission": "核心使命", "in": "所需输入", "out": "输出格式", "risk": "风险等级", "human": "人工确认"},
        "繁體中文": {"role": "角色定位", "user": "目標用戶", "mission": "核心使命", "in": "所需輸入", "out": "輸出格式", "risk": "風險等級", "human": "人工確認"},
        "日本語": {"role": "役割", "user": "ターゲット", "mission": "ミッション", "in": "必要な入力", "out": "出力形式", "risk": "リスクレベル", "human": "人間による確認"},
    }
    l = labels.get(lang, labels["English"])

    html = f"""
    <div style="background-color: #1E293B; color: white; padding: 20px; border-radius: 12px; font-family: monospace; border: 1px solid #334155; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h3 style="color: #60A5FA; margin-top: 0; border-bottom: 1px solid #334155; padding-bottom: 10px;">🛡️ {bp['agent_name']}</h3>
        <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
            <tr><td style="padding: 8px 0; color: #94A3B8; width: 30%;">{l['role']}</td><td style="padding: 8px 0;">{bp['role_description']}</td></tr>
            <tr><td style="padding: 8px 0; color: #94A3B8;">{l['user']}</td><td style="padding: 8px 0;">{bp['target_user']}</td></tr>
            <tr><td style="padding: 8px 0; color: #94A3B8;">{l['mission']}</td><td style="padding: 8px 0;">{bp['core_mission']}</td></tr>
            <tr><td style="padding: 8px 0; color: #94A3B8;">{l['in']}</td><td style="padding: 8px 0;">{bp['input_needed']}</td></tr>
            <tr><td style="padding: 8px 0; color: #94A3B8;">{l['out']}</td><td style="padding: 8px 0;">{bp['output_format']}</td></tr>
            <tr>
                <td style="padding: 8px 0; color: #94A3B8;">{l['risk']}</td>
                <td style="padding: 8px 0;">
                    <span style="background-color: {'#EF4444' if bp['risk_level'].lower() in ['high', '高'] else '#F59E0B' if bp['risk_level'].lower() in ['medium', '中'] else '#10B981'}; padding: 2px 8px; border-radius: 4px; font-size: 0.9em; font-weight: bold;">
                        {bp['risk_level'].upper()}
                    </span>
                </td>
            </tr>
            <tr><td style="padding: 8px 0; color: #94A3B8;">{l['human']}</td><td style="padding: 8px 0;">⚠️ {bp['human_confirmation']}</td></tr>
        </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)