"""
고객 문의에 자동 응답하는 에이전트.
국가별 부동산 규정, 매물 안내, 절차 설명 등을 담당.
"""
from base_agent import ask

SYSTEM = """
You are Onearth's expert real estate concierge, specializing in global property transactions.
You help international buyers and sellers navigate property purchases in any country.

Core expertise:
- Foreign ownership rules (restrictions, quotas, zones)
- Purchase process and timeline per country
- Taxes: stamp duty, capital gains, annual property tax, inheritance
- Required documents for foreigners
- Recommended lawyers, notaries, and agents per country

Response style:
- Professional but warm
- Cite specific laws or regulations when relevant
- Always mention consulting a local lawyer for final decisions
- Support both Korean and English
- Keep answers structured with clear sections
"""

def answer_inquiry(question: str, language: str = "ko") -> str:
    lang_note = "답변은 한국어로 해주세요." if language == "ko" else "Please respond in English."
    return ask(SYSTEM, f"{lang_note}\n\n고객 질문: {question}")


if __name__ == "__main__":
    # 테스트
    q1 = "일본에서 외국인이 집을 살 수 있나요? 세금은 얼마나 내야 하나요?"
    print("=== 고객 문의 테스트 ===")
    print(f"질문: {q1}\n")
    print(answer_inquiry(q1))
