from pydantic import BaseModel, Field
from typing import List
import json
from openai import OpenAI

class AgentBlueprint(BaseModel):
    agent_name: str = Field(description="A catchy, professional name for the agent")
    role_description: str = Field(description="A short 1-sentence role definition")
    target_user: str = Field(description="Who is this agent for?")
    core_mission: str = Field(description="What is the primary goal of this agent?")
    input_needed: str = Field(description="What information does the user need to provide?")
    output_format: str = Field(description="What does the agent output?")
    risk_level: str = Field(description="Low, Medium, or High risk")
    human_confirmation: str = Field(description="Actions that strictly require a human to say 'Yes' before proceeding")
    constraints: List[str] = Field(description="3-5 absolute constraints the agent MUST NOT violate")
    failure_modes: List[str] = Field(description="3-5 scenarios where the agent might fail or give bad advice")

def enhance_idea(api_key: str, model: str, raw_idea: str, language: str, base_url: str = None) -> str:
    if base_url:
        client = OpenAI(api_key=api_key, base_url=base_url)
    else:
        client = OpenAI(api_key=api_key)
    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are an expert AI product manager. Expand the user's simple agent idea into a detailed, professional feature specification. Output ONLY the expanded description text. You MUST reply in this language: {language}"},
            {"role": "user", "content": f"Make this idea 10x better and more professional: {raw_idea}"}
        ]
    )
    return res.choices[0].message.content

def enhance_idea_stream(api_key: str, model: str, raw_idea: str, language: str, base_url: str = None):
    if base_url:
        client = OpenAI(api_key=api_key, base_url=base_url)
    else:
        client = OpenAI(api_key=api_key)
    res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are an expert AI product manager. Expand the user's simple agent idea into a detailed, professional feature specification. Output ONLY the expanded description text. You MUST reply in this language: {language}"},
            {"role": "user", "content": f"Make this idea 10x better and more professional: {raw_idea}"}
        ],
        stream=True
    )
    for chunk in res:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content

def generate_agent_package(api_key: str, model: str, user_description: str, language: str, base_url: str = None, step_callback=None) -> dict:
    if base_url:
        client = OpenAI(api_key=api_key, base_url=base_url)
    else:
        client = OpenAI(api_key=api_key)

    # Step 1: Generate Blueprint
    if step_callback: step_callback(15, "Architecting Agent Blueprint...")
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are an AI Agent Architect. Create an agent blueprint based on the user's idea. The contents of all fields MUST be written in this language: {language}. You MUST output ONLY valid JSON matching this exact schema: {{ \"agent_name\": str, \"role_description\": str, \"target_user\": str, \"core_mission\": str, \"input_needed\": str, \"output_format\": str, \"risk_level\": \"Low\"|\"Medium\"|\"High\", \"human_confirmation\": str, \"constraints\": [str], \"failure_modes\": [str] }}"},
                {"role": "user", "content": f"Create an agent blueprint for this idea: {user_description}"}
            ],
            response_format={"type": "json_object"}
        )
        import json
        bp_dict = json.loads(completion.choices[0].message.content)
    except Exception as e:
        raise Exception(f"Failed to generate valid JSON blueprint. Model might not support json_object. Error: {e}")

    # Step 2: Generate System Prompt
    if step_callback: step_callback(40, "Engineering System Prompt...")
    sys_prompt_res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are an elite prompt engineer. Write a high-quality system prompt in Markdown based on the provided blueprint. The ENTIRE prompt must be written in this language: {language}.\n\nIMPORTANT: If the agent needs dynamic context from the user (e.g., Product Name, Target Audience, Topic), you MUST use template variables like {{{{Product_Name}}}} or {{{{Topic}}}} in the prompt."},
            {"role": "user", "content": f"Generate the System Prompt for this blueprint: {json.dumps(bp_dict, ensure_ascii=False)}"}
        ]
    )
    system_prompt = sys_prompt_res.choices[0].message.content

    # Step 3: Generate Test Cases
    if step_callback: step_callback(65, "Writing Evaluation Test Cases...")
    test_cases_res = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": f"You are a QA engineer for AI Agents. Generate 3 test cases in Markdown. They MUST be written in this language: {language}."},
            {"role": "user", "content": f"Generate Test Cases for: {json.dumps(bp_dict, ensure_ascii=False)}"}
        ]
    )
    test_cases = test_cases_res.choices[0].message.content

    # Step 4: Generate AGENTS.md
    if step_callback: step_callback(85, "Drafting AGENTS.md and Starter Code...")
    if language == "简体中文":
        labels = {"ctx": "上下文", "role": "🎯 角色", "mission": "🛠️ 使命", "const": "⚠️ 核心边界 (AI必须遵守)", "fail": "🛑 已知失败场景", "handoff": "🤝 人工接管协议", "wait": "如果用户要求执行", "stop": "，AI必须停止并等待明确的人工批准。"}
    elif language == "繁體中文":
        labels = {"ctx": "上下文", "role": "🎯 角色", "mission": "🛠️ 使命", "const": "⚠️ 核心邊界 (AI必須遵守)", "fail": "🛑 已知失敗場景", "handoff": "🤝 人工接管協議", "wait": "如果用戶要求執行", "stop": "，AI必須停止並等待明確的人工批准。"}
    elif language == "日本語":
        labels = {"ctx": "コンテキスト", "role": "🎯 役割", "mission": "🛠️ ミッション", "const": "⚠️ コア制約 (AIは厳守)", "fail": "🛑 既知の失敗パターン", "handoff": "🤝 人間へのハンドオフプロトコル", "wait": "ユーザーが", "stop": "を要求した場合、AIは停止し、人間の明示的な承認を待たなければならない。"}
    else:
        labels = {"ctx": "Context", "role": "🎯 Role", "mission": "🛠️ Mission", "const": "⚠️ Core Constraints (AI MUST FOLLOW)", "fail": "🛑 Known Failure Modes", "handoff": "🤝 Handoff Protocol", "wait": "If the user asks for", "stop": ", the AI must stop and wait for explicit human approval."}

    agents_md = f"""# {bp_dict['agent_name']} {labels['ctx']}

## {labels['role']}
{bp_dict['role_description']}

## {labels['mission']}
{bp_dict['core_mission']}

## {labels['const']}
{chr(10).join([f'- {c}' for c in bp_dict['constraints']])}

## {labels['fail']}
{chr(10).join([f'- {f}' for f in bp_dict['failure_modes']])}

## {labels['handoff']}
{labels['wait']} {bp_dict['human_confirmation']}{labels['stop']}
"""

    # Step 5: Generate Starter Python Code (Comments in selected language)
    starter_code = f"""import os
from openai import OpenAI

# ==========================================
# 🤖 {bp_dict['agent_name']}
# 🎯 {bp_dict['core_mission']}
# ==========================================

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run_agent(user_input: str):
    system_prompt = \"\"\"\\
Insert the content of system_prompt.md here.
Constraint to remember: {bp_dict['constraints'][0]}
\"\"\"

    try:
        response = client.chat.completions.create(
            model="{model}",
            messages=[
                {{"role": "system", "content": system_prompt}},
                {{"role": "user", "content": user_input}}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {{e}}"

if __name__ == "__main__":
    print("🚀 {bp_dict['agent_name']}...")
    print("Input needed: {bp_dict['input_needed']}")
    print("-" * 40)

    test_input = input("Enter prompt: ")
    result = run_agent(test_input)
    print("\\n🤖 Response:\\n", result)
"""

    return {
        "blueprint": bp_dict,
        "system_prompt": system_prompt,
        "test_cases": test_cases,
        "agents_md": agents_md,
        "starter_code": starter_code
    }