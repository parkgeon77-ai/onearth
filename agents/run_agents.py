"""
Onearth 에이전트 메뉴 — 터미널에서 대화형으로 실행.
"""
import sys
import os

def menu():
    print("\n" + "="*50)
    print("  ONEARTH AI AGENTS")
    print("="*50)
    print("1. 고객 문의 응답 (Inquiry Agent)")
    print("2. 매물 설명 생성 (Listing Agent)")
    print("3. 투자 추천 (Curation Agent)")
    print("4. 국가 규정 조사 (Regulation Agent)")
    print("0. 종료")
    print("-"*50)
    return input("선택: ").strip()

def run_inquiry():
    from inquiry_agent import answer_inquiry
    q = input("고객 질문 입력: ").strip()
    lang = input("언어 (ko/en, 기본 ko): ").strip() or "ko"
    print("\n[응답 생성 중...]\n")
    print(answer_inquiry(q, lang))

def run_listing():
    from listing_agent import generate_listing
    print("매물 정보 입력 (Enter로 기본값 사용):")
    data = {
        "country": input("국가: ") or "Japan",
        "city": input("도시: ") or "Tokyo",
        "type": input("매물 유형: ") or "Modern apartment",
        "size_sqm": int(input("면적(㎡): ") or "80"),
        "bedrooms": int(input("침실 수: ") or "2"),
        "price_usd": int(input("가격(USD): ") or "500000"),
        "features": input("특징 (쉼표 구분): ").split(",") or ["city view", "new build"],
    }
    langs = input("언어 (ko,en,ja 등 쉼표 구분, 기본 ko,en): ").strip() or "ko,en"
    lang_list = [l.strip() for l in langs.split(",")]
    print("\n[설명 생성 중...]\n")
    results = generate_listing(data, lang_list)
    for lang, text in results.items():
        print(f"\n--- {lang.upper()} ---\n{text}")

def run_curation():
    from curation_agent import curate
    import json
    print("고객 투자 조건 입력:")
    profile = {
        "budget_usd": int(input("예산(USD): ") or "500000"),
        "purpose": input("목적 (investment/vacation_home/relocation): ") or "investment",
        "preferred_regions": input("선호 지역 (Europe,Asia 등): ").split(",") or ["Europe"],
        "requirements": input("요구사항 (visa,rental 등): ").split(",") or ["rental income"],
        "risk_tolerance": input("리스크 허용도 (low/medium/high): ") or "medium",
    }
    print("\n[추천 분석 중...]\n")
    result = curate(profile)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def run_regulation():
    from regulation_agent import research_regulations
    country = input("국가 이름 (영어): ").strip() or "Thailand"
    focus = input("특정 질문 (선택): ").strip()
    print("\n[규정 조사 중...]\n")
    print(research_regulations(country, focus))

if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("오류: ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        sys.exit(1)

    while True:
        choice = menu()
        if choice == "0":
            break
        elif choice == "1":
            run_inquiry()
        elif choice == "2":
            run_listing()
        elif choice == "3":
            run_curation()
        elif choice == "4":
            run_regulation()
        else:
            print("잘못된 입력입니다.")
