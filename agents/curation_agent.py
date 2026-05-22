"""
고객 조건(예산, 목적, 선호 국가)을 분석하여
최적의 국가 + 매물 유형 조합을 추천하는 에이전트.
"""
from base_agent import ask
import json

SYSTEM = """
You are Onearth's investment advisor. Analyze the client's profile and recommend:
1. Top 3 countries that match their criteria
2. For each country: property type, expected price range, ROI potential, residency/visa benefits
3. Risk factors to be aware of
4. Suggested next steps

Available countries on Onearth: USA, Hawaii, France, Portugal, Italy, UK,
Japan, South Korea, Singapore, Thailand, Philippines, Australia, Dubai.

Output as structured JSON with this shape:
{
  "recommendations": [
    {
      "rank": 1,
      "country": "...",
      "property_type": "...",
      "price_range_usd": "...",
      "annual_yield": "...",
      "visa_benefit": "...",
      "risk_level": "low|medium|high",
      "rationale": "..."
    }
  ],
  "warnings": ["..."],
  "next_steps": ["..."]
}
"""

def curate(client_profile: dict) -> dict:
    """
    client_profile 예시:
    {
        "budget_usd": 500000,
        "purpose": "investment",           # investment / vacation_home / relocation
        "preferred_regions": ["Europe", "Asia"],
        "requirements": ["residency visa", "rental income potential"],
        "risk_tolerance": "medium",
        "timeline_months": 12
    }
    """
    prompt = f"Client profile:\n{json.dumps(client_profile, ensure_ascii=False, indent=2)}"
    raw = ask(SYSTEM, prompt, max_tokens=1500)

    # JSON 파싱 시도
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        return json.loads(raw[start:end])
    except (ValueError, json.JSONDecodeError):
        return {"raw_response": raw}


if __name__ == "__main__":
    profile = {
        "budget_usd": 400000,
        "purpose": "investment",
        "preferred_regions": ["Europe", "Asia"],
        "requirements": ["golden visa", "rental income"],
        "risk_tolerance": "medium",
        "timeline_months": 6
    }

    print("=== 매물 추천 테스트 ===")
    result = curate(profile)
    print(json.dumps(result, ensure_ascii=False, indent=2))
