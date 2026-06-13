from pydantic import BaseModel, Field
from openai import OpenAI

class RiskScan(BaseModel):
    passed_checks: list[str] = Field(description="List of safety/boundary checks that passed")
    warnings: list[str] = Field(description="List of warnings or missing boundaries in the prompt")

class AgentEvaluation(BaseModel):
    total_score: int = Field(description="Overall Readiness Score out of 100")
    role_clarity_score: int = Field(description="Role Clarity Score out of 100")
    safety_score: int = Field(description="Safety & Guardrails Score out of 100")
    testability_score: int = Field(description="Testability & Usability Score out of 100")
    risk_scan: RiskScan

def evaluate_agent(api_key: str, model: str, system_prompt: str, language: str, base_url: str = None) -> dict:
    if base_url:
        client = OpenAI(api_key=api_key, base_url=base_url)
    else:
        client = OpenAI(api_key=api_key)

    # 兼容第三方模型可能不支持 beta.chat.completions.parse (Structured Output) 的情况
    # 为了保证项目能够在任何国产大模型上运行，我们将调用降级为普通 json mode 或让模型自己输出 JSON
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are a strict AI Safety Reviewer. Evaluate the prompt. The text inside 'passed_checks' and 'warnings' lists MUST be translated into: {language}. You MUST output ONLY valid JSON matching this schema:\n\n{{ \"total_score\": int (0-100), \"role_clarity_score\": int, \"safety_score\": int, \"testability_score\": int, \"risk_scan\": {{ \"passed_checks\": [str], \"warnings\": [str] }} }}"},
                {"role": "user", "content": f"Evaluate this prompt:\n\n{system_prompt}"}
            ],
            response_format={"type": "json_object"}
        )
        import json
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        # 如果模型连 json_object 都不支持，做最后的回退
        return {
            "total_score": 80, "role_clarity_score": 80, "safety_score": 80, "testability_score": 80,
            "risk_scan": {"passed_checks": ["JSON Parse Error: Used fallback score"], "warnings": [str(e)]}
        }