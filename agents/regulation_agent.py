"""
특정 국가의 최신 부동산 규정 변경사항을 분석하고
regulations.html 업데이트에 필요한 내용을 생성하는 에이전트.
"""
from base_agent import ask

SYSTEM = """
You are a legal researcher specializing in international real estate regulations.
Given a country and a description of a regulatory change or update request,
produce a comprehensive, accurate section for a buyer's guide including:

- Foreign ownership restrictions (percentages, zone types, approval requirements)
- Acquisition taxes and fees (exact % where known)
- Annual property taxes
- Capital gains tax for foreigners
- Visa/residency programs linked to property purchase
- Restrictions on property types (land, agricultural, heritage, coastal zones)
- Recent legal changes (last 2 years if known)

Format as structured text suitable for a website help section.
Be specific with numbers. Note when figures are approximate or subject to change.
"""

def research_regulations(country: str, specific_question: str = "") -> str:
    query = f"Country: {country}\n"
    if specific_question:
        query += f"Focus area: {specific_question}\n"
    query += "\nProvide a complete buyer's guide regulation section."
    return ask(SYSTEM, query, max_tokens=2000)


def generate_html_section(country: str) -> str:
    """regulations.html에 바로 붙여넣을 수 있는 HTML 섹션 생성."""
    content = research_regulations(country)
    prompt = f"""
Convert this regulation content into clean HTML for the Onearth regulations page.
Use these exact CSS classes (already defined in the stylesheet):
- <div class="reg-section" id="{country.lower().replace(' ','-')}">
- <h3 class="reg-h3"> for main headings
- <div class="reg-grid"> with <div class="reg-item"> for tax/fee grids
- <p> for body text
- <div class="reg-tag tag-open"> or <div class="reg-tag tag-restricted"> for status

Content to convert:
{content}
"""
    return ask(
        "You are an HTML developer. Output only valid HTML, no markdown fences.",
        prompt,
        max_tokens=2000
    )


if __name__ == "__main__":
    print("=== 규정 조사 테스트 ===")
    result = research_regulations("Portugal", "Golden Visa program 2024 changes")
    print(result)
