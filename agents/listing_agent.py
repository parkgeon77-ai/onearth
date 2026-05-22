"""
매물 기본 정보를 받아 고급스러운 매물 설명문을 생성하고,
한국어/영어/일본어로 번역까지 처리하는 에이전트.
"""
from base_agent import ask

SYSTEM = """
You are a luxury real estate copywriter for Onearth, a global property brokerage.
Given raw property details, write compelling, premium descriptions that:
- Open with an evocative headline
- Highlight lifestyle and investment value
- Mention location advantages specifically
- Include key specs naturally (not as a dry list)
- End with a subtle call to action
- Tone: sophisticated, aspirational, never salesy
Write in the requested language. Keep under 300 words.
"""

def generate_listing(
    property_data: dict,
    languages: list = ["ko", "en"]
) -> dict:
    """
    property_data 예시:
    {
        "country": "Japan",
        "city": "Kyoto",
        "type": "Traditional machiya townhouse",
        "size_sqm": 120,
        "bedrooms": 3,
        "price_usd": 480000,
        "features": ["garden", "tea room", "renovated kitchen", "near Gion"],
        "investment_notes": "Popular for short-term rental, Airbnb allowed"
    }
    """
    raw = str(property_data)
    results = {}

    lang_map = {
        "ko": "Korean",
        "en": "English",
        "ja": "Japanese",
        "zh": "Simplified Chinese",
        "fr": "French",
    }

    for lang_code in languages:
        lang_name = lang_map.get(lang_code, "English")
        prompt = f"Write in {lang_name}.\n\nProperty details:\n{raw}"
        results[lang_code] = ask(SYSTEM, prompt, max_tokens=600)

    return results


if __name__ == "__main__":
    sample = {
        "country": "Portugal",
        "city": "Lisbon",
        "type": "Renovated apartment",
        "size_sqm": 95,
        "bedrooms": 2,
        "price_usd": 620000,
        "features": ["river view", "original azulejo tiles", "private terrace", "Alfama district"],
        "investment_notes": "Golden Visa eligible, high rental yield area"
    }

    print("=== 매물 설명 생성 테스트 ===")
    descriptions = generate_listing(sample, languages=["ko", "en"])
    for lang, text in descriptions.items():
        print(f"\n--- {lang.upper()} ---")
        print(text)
