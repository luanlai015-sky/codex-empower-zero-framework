import streamlit as st
import json
import zipfile
import io
from core.generator import generate_agent_package, enhance_idea
from core.evaluator import evaluate_agent
from components.blueprint_card import render_blueprint_card
from components.sandbox import render_sandbox
from components.arena import render_arena

st.set_page_config(
    page_title="Codex Empower Zero",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/luanlai015-sky/codex-empower-zero-framework',
        'Report a bug': "https://github.com/luanlai015-sky/codex-empower-zero-framework/issues",
        'About': "# Codex Empower Zero Framework\nFrom idea to Agent Package in seconds."
    }
)

st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0; }
    .sub-header { font-size: 1.2rem; color: #4B5563; margin-bottom: 2rem; }
    .btn-primary { width: 100%; border-radius: 8px; font-weight: bold; background-color: #2563EB; color: white; }
    .score-card { background-color: #F8FAFC; border-left: 4px solid #3B82F6; padding: 15px; border-radius: 8px; margin-top: 10px; }
    .stAppDeployButton {display:none;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# i18n Configuration - Updated Subtitles for extreme beginner-friendliness
translations = {
    "English": {
        "title": "Codex Empower Zero Framework ⚡",
        "subtitle": "Just describe your idea in plain English. We'll build your custom AI agent in 30 seconds, complete with anti-fail guardrails and copy-paste code!",
        "config": "### ⚙️ Configuration",
        "templates_title": "### 📚 Templates Gallery",
        "custom": "Custom...",
        "input_label": "Describe what you want your AI Agent to do:",
        "input_ph": "e.g., I want an agent that automatically reviews my Python code...",
        "btn_gen": "🚀 Generate Agent Package",
        "btn_enh": "✨ Make It 10x Better",
        "err_key": "⚠️ Please enter your OpenAI API Key.",
        "err_desc": "⚠️ Please describe your agent idea.",
        "spin_enh": "🧠 Expanding your idea into a pro-level spec...",
        "spin_gen": "🤖 Architecting Agent Package...",
        "spin_eval": "🔍 Running Security & Readiness Scan...",
        "succ_gen": "✅ Agent Package successfully engineered and evaluated!",
        "recent": "### 🕒 Recent Agents",
        "score_title": "### 📊 Agent Readiness Score",
        "tab_sand": "🎮 Sandbox", "tab_arena": "⚖️ A/B Arena", "tab_prompt": "📝 Prompt", "tab_risk": "⚠️ Risks", "tab_test": "🧪 Tests", "tab_code": "🐍 Code", "tab_docs": "📖 How to Use",
        "dl_btn": "📥 Download Full Agent Package (.zip)",
        "btn_fetch": "🔄 Import Models",
        "succ_fetch": "✅ Successfully imported {count} models!",
        "err_fetch": "❌ Failed to fetch: {error}",
        "enh_title": "✨ Enhanced Pro-Level Idea:",
        "btn_use_enh": "🚀 Generate Agent using this Enhanced Idea",
        "docs_content": """
### 🤷‍♂️ What do I do with these generated files?
1. **🧪 Test it first**: Use the **Sandbox** or **A/B Arena** tabs right here in your browser to chat with your agent.
2. **📥 Download**: Click the ZIP download button below to save all assets.
3. **🛠️ Where to paste them**:
   - **For ChatGPT / Claude Web**: Copy the text from `system_prompt.md` and paste it into ChatGPT's "Custom Instructions" or Claude's "Projects" system prompt.
   - **For Python Developers**: Run the `starter_openai.py` script locally to get a terminal-based chatbot.
   - **For Cursor / Windsurf Users**: Drop the `AGENTS.md` file into your project's root folder. The AI IDE will read it and automatically follow the agent rules.
"""
    },
    "简体中文": {
        "title": "Codex 零代码赋能框架 ⚡",
        "subtitle": "只要会说大白话，30秒帮你捏出一个专属 AI 助手。防翻车规则、测试边界、傻瓜式启动代码一次性全打包！",
        "config": "### ⚙️ 全局配置",
        "templates_title": "### 📚 经典模板库",
        "custom": "自定义输入...",
        "input_label": "用大白话描述你需要一个什么样的 AI 助手帮你干活：",
        "input_ph": "例如：我想做一个能自动帮我检查 Python 代码漏洞，并且语气很毒舌的审查员。",
        "btn_gen": "🚀 一键生成智能体工程",
        "btn_enh": "✨ 魔法扩写 (变强10倍)",
        "err_key": "⚠️ 请在左侧栏输入 OpenAI API Key。",
        "err_desc": "⚠️ 请先描述一下你的想法。",
        "spin_enh": "🧠 正在使用产品经理思维扩写你的需求...",
        "spin_gen": "🤖 正在为你构建智能体架构 (提示词、边界、代码)...",
        "spin_eval": "🔍 正在进行越狱风险与安全合规扫描...",
        "succ_gen": "✅ 智能体工程构建并评估完毕！",
        "recent": "### 🕒 最近生成的智能体",
        "score_title": "### 📊 智能体防翻车健康度",
        "tab_sand": "🎮 在线试聊", "tab_arena": "⚖️ A/B 竞技场", "tab_prompt": "📝 核心提示词", "tab_risk": "⚠️ 风险扫描", "tab_test": "🧪 测试用例", "tab_code": "🐍 傻瓜代码", "tab_docs": "📖 使用说明 (必看)",
        "dl_btn": "📥 一键下载完整助手包 (.zip)",
        "btn_fetch": "🔄 导入大模型列表",
        "succ_fetch": "✅ 成功导入 {count} 个大模型！",
        "err_fetch": "❌ 导入失败: {error}",
        "enh_title": "✨ 魔法扩写后的专业级需求：",
        "btn_use_enh": "🚀 采用这个扩写版本生成智能体",
        "docs_content": """
### 🤷‍♂️ 拿到这些文件后我该怎么用？
1. **🧪 先测一下**: 别着急走，直接在左侧的 **在线试聊** 或者 **A/B 竞技场** 里跟它聊聊天，看看它听不听话。
2. **📥 下载保存**: 点击最下方的“一键下载”按钮，把全套装备保存到电脑。
3. **🛠️ 具体怎么用**:
   - **如果你用网页版 ChatGPT / Kimi / Claude**: 点开 `核心提示词 (system_prompt)`，把里面的所有文字复制下来，粘贴到你的 AI 对话框里（或者粘贴到 ChatGPT 的“自定义指令” / Claude 的“Project 设定”里）。
   - **如果你懂一点点代码**: 电脑里装好 Python，直接运行 `starter_openai.py`，你就能在黑框框里拥有一个专属小助手。
   - **如果你是用 Cursor / Windsurf 编程**: 把 `AGENTS.md` 文件丢进你的项目根目录里，AI 编程工具会自动读取并遵守这个“监工”的规矩！
"""
    },
    "繁體中文": {
        "title": "Codex 零代碼賦能框架 ⚡",
        "subtitle": "只要會說白話文，30秒幫你捏出一個專屬 AI 助手。防翻車規則、測試邊界、傻瓜式啟動代碼一次性全打包！",
        "config": "### ⚙️ 全局配置",
        "templates_title": "### 📚 經典模板庫",
        "custom": "自定義輸入...",
        "input_label": "用白話文描述你需要一個什麼樣的 AI 助手幫你幹活：",
        "input_ph": "例如：我想做一個能自動幫我檢查 Python 代碼漏洞的審查員。",
        "btn_gen": "🚀 一鍵生成智能體工程",
        "btn_enh": "✨ 魔法擴寫 (變強10倍)",
        "err_key": "⚠️ 請在左側欄輸入 OpenAI API Key。",
        "err_desc": "⚠️ 請先描述一下你的想法。",
        "spin_enh": "🧠 正在使用產品經理思維擴寫你的需求...",
        "spin_gen": "🤖 正在為你構建智能體架構 (提示詞、邊界、代碼)...",
        "spin_eval": "🔍 正在進行越獄風險與安全合規掃描...",
        "succ_gen": "✅ 智能體工程構建並評估完畢！",
        "recent": "### 🕒 最近生成的智能體",
        "score_title": "### 📊 智能體防翻車健康度",
        "tab_sand": "🎮 線上試聊", "tab_arena": "⚖️ A/B 競技場", "tab_prompt": "📝 核心提示詞", "tab_risk": "⚠️ 風險掃描", "tab_test": "🧪 測試案例", "tab_code": "🐍 傻瓜代碼", "tab_docs": "📖 使用說明 (必看)",
        "dl_btn": "📥 一鍵下載完整助手包 (.zip)",
        "btn_fetch": "🔄 導入大模型列表",
        "succ_fetch": "✅ 成功導入 {count} 個大模型！",
        "err_fetch": "❌ 導入失敗: {error}",
        "enh_title": "✨ 魔法擴寫後的專業級需求：",
        "btn_use_enh": "🚀 採用這個擴寫版本生成智能體",
        "docs_content": """
### 🤷‍♂️ 拿到這些文件後我該怎麼用？
1. **🧪 先測一下**: 別著急走，直接在左側的 **線上試聊** 或者 **A/B 競技場** 裡跟它聊聊天，看看它聽不聽話。
2. **📥 下載保存**: 點擊最下方的“一鍵下載”按鈕，把全套裝備保存到電腦。
3. **🛠️ 具體怎麼用**:
   - **如果你用網頁版 ChatGPT / Claude**: 點開 `核心提示詞`，把裡面的所有文字複製下來，粘貼到你的 AI 對話框裡（或者粘貼到 ChatGPT 的“自定義指令”裡）。
   - **如果你懂一點代碼**: 電腦裡裝好 Python，直接運行 `starter_openai.py`，你就能在終端擁有一個專屬小助手。
   - **如果你是用 Cursor / Windsurf 寫代碼**: 把 `AGENTS.md` 文件丟進你的專案根目錄裡，AI 會自動讀取並遵守這個規矩！
"""
    },
    "日本語": {
        "title": "Codex ゼロコード・エンパワー ⚡",
        "subtitle": "日常語でアイデアを伝えるだけ。30秒であなた専用のAIエージェントを構築し、フェイルセーフ規則から起動コードまで一式パッケージ化！",
        "config": "### ⚙️ 設定",
        "templates_title": "### 📚 テンプレートギャラリー",
        "custom": "カスタム入力...",
        "input_label": "作成したいAIエージェントを説明してください：",
        "input_ph": "例：Pythonコードの脆弱性を自動的にレビューするエージェントを作りたい。",
        "btn_gen": "🚀 エージェント・パッケージを生成",
        "btn_enh": "✨ 魔法の拡張 (アイデアを10倍強化)",
        "err_key": "⚠️ OpenAI APIキーを入力してください。",
        "err_desc": "⚠️ エージェントのアイデアを説明してください。",
        "spin_enh": "🧠 アイデアを専門的な仕様に拡張中...",
        "spin_gen": "🤖 エージェントの設計図、プロンプト、コードを構築中...",
        "spin_eval": "🔍 セキュリティと準備状況のスキャンを実行中...",
        "succ_gen": "✅ エージェント・パッケージの生成と評価が完了しました！",
        "recent": "### 🕒 最近生成したエージェント",
        "score_title": "### 📊 エージェント完成度スコア",
        "tab_sand": "🎮 サンドボックス", "tab_arena": "⚖️ A/B アリーナ", "tab_prompt": "📝 プロンプト", "tab_risk": "⚠️ リスク", "tab_test": "🧪 テスト", "tab_code": "🐍 コード", "tab_docs": "📖 使い方",
        "dl_btn": "📥 フルパッケージをダウンロード (.zip)",
        "btn_fetch": "🔄 モデルをインポート",
        "succ_fetch": "✅ {count} 個のモデルのインポートに成功しました！",
        "err_fetch": "❌ インポート失敗: {error}",
        "enh_title": "✨ 拡張されたプロレベルのアイデア:",
        "btn_use_enh": "🚀 このアイデアで生成する",
        "docs_content": """
### 🤷‍♂️ 生成されたファイルの使い方は？
1. **🧪 まずはテスト**: この画面の「サンドボックス」タブでエージェントとチャットしてテストしてください。
2. **📥 ダウンロード**: 下のZIPダウンロードボタンをクリックしてファイルを保存します。
3. **🛠️ 活用方法**:
   - **ChatGPT等を使う場合**: `プロンプト` の内容をコピーして、ChatGPTのカスタム指示に貼り付けます。
   - **Pythonを実行する場合**: ローカルで `starter_openai.py` を実行するとチャットボットが起動します。
   - **Cursor等のAI IDEを使う場合**: `AGENTS.md` をプロジェクトのルートに配置すると、AIがルールを読み取ります。
"""
    }
}

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []
if "current_pkg" not in st.session_state:
    st.session_state.current_pkg = None
if "current_eval" not in st.session_state:
    st.session_state.current_eval = None
if "idea_input" not in st.session_state:
    st.session_state.idea_input = ""
if "enhanced_idea" not in st.session_state:
    st.session_state.enhanced_idea = ""

if "available_models" not in st.session_state:
    st.session_state.available_models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
if "prev_template" not in st.session_state:
    st.session_state.prev_template = ""

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg", width=150)

    # Language Selector
    lang = st.selectbox("🌐 Language / 语言 / 言語", ["English", "简体中文", "繁體中文", "日本語"])
    t = translations[lang]

    st.markdown(t["config"])
    api_key = st.text_input("API Key", type="password", placeholder="sk-...")
    base_url = st.text_input("Base URL (Optional)", placeholder="e.g., https://api.deepseek.com/v1")

    if st.button(t["btn_fetch"], use_container_width=True):
        if not api_key:
            st.error(t["err_key"])
        else:
            with st.spinner("Fetching..."):
                try:
                    from openai import OpenAI
                    if base_url:
                        client = OpenAI(api_key=api_key, base_url=base_url)
                    else:
                        client = OpenAI(api_key=api_key)
                    models_response = client.models.list(timeout=10.0)
                    fetched_models = sorted([m.id for m in models_response.data])
                    if fetched_models:
                        preferred = [m for m in fetched_models if "gpt-4o" in m or "deepseek" in m or "claude" in m or "qwen" in m]
                        others = [m for m in fetched_models if m not in preferred]
                        st.session_state.available_models = preferred + others
                        st.success(t["succ_fetch"].format(count=len(fetched_models)))
                    else:
                        st.warning("Connected, but returned 0 models.")
                except Exception as e:
                    st.error(t["err_fetch"].format(error=str(e)))

    # Let user select from fetched models
    model_choice = st.selectbox("Select Model", st.session_state.available_models)

    st.markdown("---")
    st.markdown(t["templates_title"])

    # Templates specific to languages
    if lang == "简体中文":
        templates = {
            t["custom"]: "",
            "GitHub PR 审查员": "一个审查GitHub PR、检查安全风险并提出代码改进建议的智能体。",
            "零代码 App 规划师": "帮助小白规划移动App，生成UI布局和数据库表结构的智能体。",
            "Python 脚本小助手": "编写初学者绝对安全的Python小脚本，并耐心解释如何运行它。",
            "Bug 复现追踪者": "把模糊的Bug描述转化为精确的复现步骤和最小测试用例的智能体。",
            "会议纪要整理员": "将杂乱的会议记录整理成结构化的行动项清单和总结。"
        }
    elif lang == "日本語":
        templates = {
            t["custom"]: "",
            "GitHub PR レビュアー": "GitHub PRをレビューし、セキュリティリスクを確認し、改善を提案するエージェント。",
            "ゼロコード App プランナー": "初心者のアプリ企画を支援し、UIレイアウトとデータベース構造を生成するエージェント。",
            "Python スクリプトアシスタント": "初心者向けの安全なPythonスクリプトを記述し、実行方法を説明するエージェント。",
            "バグ再現テスター": "曖昧なバグレポートから正確な再現手順と最小限のテストケースを生成するエージェント。"
        }
    else:
        templates = {
            t["custom"]: "",
            "GitHub PR Reviewer": "An agent that reviews GitHub PRs, checks for security risks, and suggests code improvements.",
            "Zero-Code App Planner": "An agent that helps absolute beginners plan a mobile app, generating UI layouts and database schemas.",
            "Python Script Helper": "An agent that writes small, beginner-safe Python scripts and explains how to run them.",
            "Bug Reproducer": "An agent that takes a vague bug report and generates precise steps to reproduce it along with a minimal test case."
        }

    selected_template = st.selectbox("", list(templates.keys()), label_visibility="collapsed")
    if selected_template != t["custom"] and selected_template != st.session_state.prev_template:
        st.session_state.idea_input = templates[selected_template]
        st.session_state.prev_template = selected_template

    if st.session_state.history:
        st.markdown("---")
        st.markdown(t["recent"])
        for i, h in enumerate(reversed(st.session_state.history[-5:])):
            if st.button(f"Load: {h['blueprint']['agent_name']}", key=f"hist_{i}"):
                st.session_state.current_pkg = h['pkg']
                st.session_state.current_eval = h.get('eval')

st.markdown(f'<p class="main-header">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{t["subtitle"]}</p>', unsafe_allow_html=True)

# Main Input Area
# To bypass the "cannot be modified after instantiated" error cleanly in Streamlit,
# we control the component via 'value', not via a 'key' mutation.
# When a user types, it doesn't immediately update session state, but we capture it via the return value.
user_input = st.text_area(
    t["input_label"],
    value=st.session_state.idea_input,
    placeholder=t["input_ph"],
    height=120
)

# Sync the user's manual edits back to session state so they aren't lost on rerun
if user_input != st.session_state.idea_input:
    st.session_state.idea_input = user_input

col1, col2 = st.columns([1, 1])
with col1:
    enhance_btn = st.button(t["btn_enh"], use_container_width=True)
with col2:
    generate_btn = st.button(t["btn_gen"], type="primary", use_container_width=True)

if enhance_btn:
    if not api_key:
        st.error(t["err_key"])
    elif not st.session_state.idea_input.strip():
        st.warning(t["err_desc"])
    else:
        # Create an empty placeholder for the streaming text
        st.markdown(f"### {t['enh_title']}")
        stream_placeholder = st.empty()
        full_text = ""
        try:
            from core.generator import enhance_idea_stream
            for chunk in enhance_idea_stream(api_key, model_choice, st.session_state.idea_input, lang, base_url):
                full_text += chunk
                stream_placeholder.info(full_text + "▌")

            # Final output without the cursor
            stream_placeholder.info(full_text)
            st.session_state.enhanced_idea = full_text
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Display the Enhanced Idea block below the buttons if it exists and wasn't just streamed
elif st.session_state.enhanced_idea:
    st.markdown(f"### {t['enh_title']}")
    st.info(st.session_state.enhanced_idea)

if st.session_state.enhanced_idea:
    if st.button(t["btn_use_enh"], type="secondary", use_container_width=True):
        st.session_state.idea_input = st.session_state.enhanced_idea
        st.session_state.enhanced_idea = "" # Clear the enhanced block after adopting
        st.rerun()

st.markdown("---")

if generate_btn:
    if not api_key:
        st.error(t["err_key"])
    elif not st.session_state.idea_input.strip():
        st.error(t["err_desc"])
    else:
        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(percent, msg):
            progress_bar.progress(percent)
            status_text.write(f"🔄 {msg}")

        try:
            update_progress(5, t["spin_gen"])
            pkg = generate_agent_package(api_key, model_choice, st.session_state.idea_input, lang, base_url, step_callback=update_progress)

            update_progress(90, t["spin_eval"])
            eval_data = evaluate_agent(api_key, model_choice, pkg['system_prompt'], lang, base_url)

            update_progress(100, "Done!")
            status_text.empty()
            progress_bar.empty()

            st.session_state.current_pkg = pkg
            st.session_state.current_eval = eval_data

            st.session_state.history.append({"blueprint": pkg['blueprint'], "pkg": pkg, "eval": eval_data})
            st.success(t["succ_gen"])
        except Exception as e:
            status_text.empty()
            progress_bar.empty()
            st.error(f"❌ Error: {str(e)}")

# Display Results
if st.session_state.current_pkg:
    pkg = st.session_state.current_pkg
    eval_data = st.session_state.current_eval
    bp = pkg['blueprint']

    st.markdown("---")

    c_blue, c_score = st.columns([2, 1])
    with c_blue:
        render_blueprint_card(bp, lang)

    with c_score:
        if eval_data:
            st.markdown(t["score_title"])
            score = eval_data['total_score']
            color = "green" if score >= 85 else "orange" if score >= 70 else "red"
            st.markdown(f"<h1 style='text-align: center; color: {color}; font-size: 4rem; margin: 0;'>{score}/100</h1>", unsafe_allow_html=True)

            # Simple UI for scores
            st.markdown("<div class='score-card'>", unsafe_allow_html=True)
            st.markdown(f"🎯 Role Clarity: **{eval_data['role_clarity_score']}**")
            st.markdown(f"🛡️ Safety: **{eval_data['safety_score']}**")
            st.markdown(f"🧪 Testability: **{eval_data['testability_score']}**")
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    tab_sand, tab_arena, tab_prompt, tab_risks, tab_tests, tab_agents, tab_code, tab_docs = st.tabs([
        t["tab_sand"], t["tab_arena"], t["tab_prompt"], t["tab_risk"], t["tab_test"], "📄 AGENTS.md", t["tab_code"], t["tab_docs"]
    ])

    with tab_sand:
        render_sandbox(api_key, model_choice, pkg['system_prompt'], bp['agent_name'], lang, base_url)

    with tab_arena:
        render_arena(api_key, pkg['system_prompt'], bp['agent_name'], lang, base_url, st.session_state.available_models)

    with tab_prompt:
        st.code(pkg['system_prompt'], language="markdown")

    with tab_risks:
        for f in bp['failure_modes']:
            st.markdown(f"- ⚠️ {f}")
        if eval_data:
            st.markdown("---")
            st.success("✅\n" + "\n".join([f"- {c}" for c in eval_data['risk_scan']['passed_checks']]))
            if eval_data['risk_scan']['warnings']:
                st.warning("⚠️\n" + "\n".join([f"- {w}" for w in eval_data['risk_scan']['warnings']]))

    with tab_tests:
        st.code(pkg['test_cases'], language="markdown")

    with tab_agents:
        st.code(pkg['agents_md'], language="markdown")

    with tab_code:
        st.code(pkg['starter_code'], language="python")

    with tab_docs:
        st.markdown(t["docs_content"])

    st.markdown("---")
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("system_prompt.md", pkg['system_prompt'])
        zip_file.writestr("test_cases.md", pkg['test_cases'])
        zip_file.writestr("AGENTS.md", pkg['agents_md'])
        zip_file.writestr("starter_openai.py", pkg['starter_code'])
        zip_file.writestr("agent_config.json", json.dumps(bp, indent=4, ensure_ascii=False))

    st.download_button(
        label=t["dl_btn"],
        data=zip_buffer.getvalue(),
        file_name=f"{bp['agent_name'].replace(' ', '_').lower()}_package.zip",
        mime="application/zip",
        use_container_width=True,
        type="primary"
    )