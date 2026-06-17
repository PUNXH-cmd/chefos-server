from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="ChefOS - AI 로봇 셰프 대시보드 v4.1")

# 1. 초정밀 로봇 제어용 50종 밥 요리 데이터베이스
RECIPE_DB = {
    "치킨 마요 덮밥": {"재료": ["밥 200g", "순살치킨 150g", "마요네즈 30g", "데리야끼소스 20g"], "조리법": "1. 180도 유온에서 치킨을 4분 30초간 튀김.\n2. 밥 위에 3cm 크기로 커팅한 치킨 안착.\n3. 데리야끼와 마요네즈 소스를 십자 격자로 분사."},
    "참치 마요 덮밥": {"재료": ["밥 200g", "캔참치 120g", "마요네즈 40g", "조미김 5g"], "조리법": "1. 참치 캔 유분을 200N 압력으로 95% 압착 제거.\n2. 마요네즈와 참치를 30초간 균일 혼합.\n3. 밥 위에 돔 형태로 성형 후 김가루 토핑."},
    "제육 덮밥": {"재료": ["밥 200g", "돼지전지 180g", "고추장양념 50g", "양파 30g"], "조리법": "1. 220도 고온 웍에서 고기와 양파를 2분간 초강불 시어링.\n2. 고추장 소스 투입 후 1분 30초간 가열하여 불맛 흡착.\n3. 밥 측면에 잔여 소스와 함께 서빙."},
    "불고기 덮밥": {"재료": ["밥 200g", "소불고기 150g", "팽이버섯 30g", "간장소스 40g"], "조리법": "1. 160도 회전 팬에 소고기와 간장 소스 투입.\n2. 3분간 졸인 후 데친 팽이버섯 가미.\n3. 밥 상단에 국물과 함께 정갈하게 플레이팅."},
    "돈까스 덮밥(가츠동)": {"재료": ["밥 200g", "돈까스 150g", "계란 1개", "쯔유소스 50g"], "조리법": "1. 170도에서 돈까스 5분간 튀김 후 2cm 간격 커팅.\n2. 쯔유 소스에 양파를 졸인 후 계란물을 둘러 30초간 반숙 유도.\n3. 밥 위에 미끄러지듯 안착."},
    "오징어 덮밥": {"재료": ["밥 200g", "오징어 150g", "양배추 40g", "매운양념 40g"], "조리법": "1. 250도 웍에 파기름 유도 후 오징어, 양배추 투입.\n2. 매운 양념과 함께 1분 30초간 초고속 배출 조리.\n3. 수분 발생을 억제하여 즉시 배출."},
    "스팸 김치볶음밥": {"재료": ["밥 200g", "숙성김치 120g", "스팸 70g", "계란 1개"], "조리법": "1. 1cm 큐브 스팸을 볶아 유분 추출.\n2. 스팸 기름에 김치 2분 볶음 후 고슬한 밥 가미.\n3. 주걱 팔로 3분간 혼합 분쇄 조리 후 계란프라이 안착."},
    "새우 볶음밥": {"재료": ["밥 200g", "칵테일새우 100g", "계란 1.5개", "굴소스 15g"], "조리법": "1. 새우 유분 가열 후 계란 스크램블 병행.\n2. 수분 감축된 밥 투입 후 초당 2회 웍 태싱(Tossing).\n3. 굴소스를 팬 외곽에 둘러 풍미 결합."},
    "마파두부 덮밥": {"재료": ["밥 200g", "연두부 150g", "다진돼지고기 60g", "두반장 30g"], "조리법": "1. 연두부 데침 과정 선행.\n2. 다진 고기와 두반장 소스를 끓여 베이스 구축.\n3. 연두부 가미 후 전분물로 농도 제어하여 완성."},
    "스테이크 덮밥": {"재료": ["밥 200g", "부채살 150g", "와사비 5g", "스테이크소스 25g"], "조리법": "1. 200도 철판에서 부채살 표면 고속 시어링.\n2. 심부 온도 55도 도달 시 3분 레스팅 유도.\n3. 5mm 슬라이스 후 와사비와 소스 가미."},
    "가지 덮밥": {"재료": ["밥 200g", "가지 120g", "다진고기 50g", "굴소스 20g"], "조리법": "1. 가지를 깍둑썰기하여 180도 고온에서 1분간 초고속 튀김.\n2. 다진 고기와 굴소스를 웍에서 졸여 양념 구축.\n3. 튀긴 가지를 양념에 버무려 밥 위에 안착."},
    "연어 덮밥(사케동)": {"재료": ["초대리밥 200g", "생연어 120g", "무순 10g", "와사비 5g"], "조리법": "1. 배합초 혼합된 밥을 체온(36도)으로 정밀 냉각.\n2. 생연어를 8mm 각도로 초정밀 슬라이스.\n3. 밥 위에 방사형 플레이팅 후 와사비 중앙 안착."},
    "강된장 덮밥": {"재료": ["보리밥 200g", "우렁강된장 120g", "부추 10g", "참기름 5g"], "조리법": "1. 보리밥 조리 후 그릇 배치.\n2. 자박하게 끓인 우렁 강된장 정량 투하.\n3. 0.5cm 커팅된 부추를 외곽에 두르고 참기름 분사."},
    "명란 마요 덮밥": {"재료": ["밥 200g", "저염명란젓 40g", "노른자 1개", "마요네즈 25g"], "조리법": "1. 명란 외피 막 제거 후 알맹이 추출.\n2. 어린잎 채소 베이스 위에 명란 배치.\n3. 마요네즈 정밀 드립 후 노른자 파손 없이 안착."},
    "카레 볶음밥": {"재료": ["밥 200g", "카레가루 20g", "감자당근큐브 40g", "버터 10g"], "조리법": "1. 버터 베이스에 감자, 당근 큐브 완숙 조리.\n2. 찬밥 투입 후 고온 파쇄 가공.\n3. 카레가루 투입 후 황색 불변 시점까지 2분간 웍질."},
    "낙지 덮밥": {"재료": ["밥 200g", "통낙지 150g", "데친콩나물 60g", "매운양념 50g"], "조리법": "1. 낙지를 끓는 물에 10초간 토렴하여 식감 보존.\n2. 250도 웍에서 양념과 낙지를 고속 볶음.\n3. 데친 콩나물과 낙지볶음을 이분할 구획 정돈."},
    "베이컨 계란 볶음밥": {"재료": ["밥 200g", "훈제베이컨 50g", "계란 2개", "대파 20g"], "조리법": "1. 베이컨 가열로 자체 동물성 유분 추출.\n2. 추출 유분에 파기름 동시 조성 후 계란 투입.\n3. 밥 가미 후 고슬한 텍스처 도달 시까지 3분 볶음."},
    "양배추 계란 덮밥": {"재료": ["밥 200g", "양배추 100g", "계란 2개", "쯔유 15g"], "조리법": "1. 채 썬 양배추를 팬에서 숨이 죽을 때까지 가열.\n2. 쯔유 소스 주입 후 계란물을 고르게 분사.\n3. 뚜껑 폐쇄 후 잔열로 부드럽게 익혀 밥 위에 슬라이딩."},
    "소고기 버섯 덮밥": {"재료": ["밥 200g", "우삼겹 100g", "느타리버섯 50g", "굴소스 15g"], "조리법": "1. 우삼겹 가열을 통해 불포화 유분 유도.\n2. 해당 유분에 버섯을 투입하여 풍미 극대화.\n3. 굴소스로 피니시 후 밥 위에 도포."},
    "깍두기 볶음밥": {"재료": ["밥 200g", "다진깍두기 100g", "국물 40g", "피자치즈 30g"], "조리법": "1. 다진 깍두기를 소스와 함께 가열 가공.\n2. 밥 투입 후 국물 배합 조리.\n3. 바닥면 누룽지 2분간 인내 조리 후 치즈 융해 투하."},
    "짜계치 덮밥": {"재료": ["밥 200g", "짜장소스 120g", "계란 1개", "체다치즈 1장"], "조리법": "1. 짜장 소스를 85도 온도로 뭉근하게 액상화.\n2. 밥 위에 소스 투하 후 단면 프라이 계란 안착.\n3. 계란 상단에 체다치즈를 배치하여 열 분산 유도."},
    "꼬막 덮밥": {"재료": ["밥 200g", "자숙꼬막 120g", "부추 20g", "간장양념장 30g"], "조리법": "1. 해감 및 자숙된 꼬막살 정량 계량.\n2. 부추와 매콤한 청양간장 양념장에 꼬막 고속 믹싱.\n3. 밥 위에 비빔 원액 그대로 균일 도포."},
    "장어 덮밥(우나동)": {"재료": ["밥 200g", "민물장어 150g", "초생강 10g", "데리야끼 타레 30g"], "조리법": "1. 초벌구이 장어에 타레 소스를 바르며 오븐 200도에서 3분 조리.\n2. 장어를 2cm 간격 크기로 크기 정렬 커팅.\n3. 소스를 뿌린 밥 위에 정렬 후 초생강 배치."},
    "춘천 닭갈비 덮밥": {"재료": ["밥 200g", "닭다리살 160g", "양배추 50g", "닭갈비양념 45g"], "조리법": "1. 닭다리살을 정육면체 커팅 후 웍 가열.\n2. 깻잎, 양배추, 고구마 큐브와 양념 혼합 조리.\n3. 완전히 익은 닭갈비를 철판 감성으로 밥에 토핑."},
    "대패삼겹살 덮밥": {"재료": ["밥 200g", "대패삼겹살 150g", "숙주 60g", "굴소스간장 25g"], "조리법": "1. 대패삼겹살을 고온 팬에서 바삭하게 급속 조리.\n2. 삼겹살 기름에 숙주와 굴소스 소스를 투입하여 30초 믹싱.\n3. 아삭함이 보존된 숙주와 고기를 밥에 배정."},
    "하이라이스 덮밥": {"재료": ["밥 200g", "데미글라스소스 150g", "소고기슬라이스 40g", "양송이 20g"], "조리법": "1. 버터에 소고기와 양파, 양송이버섯을 캐러멜라이징.\n2. 데미글라스 소스와 물 배합 후 90도에서 졸임.\n3. 깊은 풍미의 소스를 밥 우측 영역에 배분."},
    "짜장 볶음밥": {"재료": ["밥 200g", "춘장소스 40g", "다진채소 30g", "계란 1개"], "조리법": "1. 고온 파기름에 다진 야채와 밥을 볶아 볶음밥 선행.\n2. 별도 파트에서 춘장을 볶아 짜장 베이스 가공.\n3. 중화풍 볶음밥 주변에 짜장 소스를 원형으로 스크리닝."},
    "마늘 볶음밥": {"재료": ["밥 200g", "통마늘슬라이스 30g", "마늘쫑 20g", "버터간장 15g"], "조리법": "1. 슬라이스 마늘을 기름에 튀겨 마늘 칩 가공.\n2. 다진 마늘과 마늘쫑을 버터에 볶아 알싸한 유분 추출.\n3. 밥과 소스를 배합 볶음 조리 후 상단에 마늘 칩 토핑."},
    "게살 볶음밥": {"재료": ["밥 200g", "리얼크랩살 80g", "계란흰자 2개", "대파 20g"], "조리법": "1. 대파와 계란 흰자 스크램블을 부드럽게 가공.\n2. 수분 제어된 밥과 굴소스를 결합하여 초고속 웍질.\n3. 결대로 찢은 게살을 마지막에 투입하여 식감 보존 조리."},
    "김치 베이컨 볶음밥": {"재료": ["밥 200g", "신김치 100g", "베이컨 40g", "참기름 5g"], "조리법": "1. 잘게 썬 베이컨의 크리스피 유분 도출.\n2. 김치를 추가하여 160도에서 풍미 융합 조리.\n3. 밥 투입 후 고온 볶음 처리, 참기름으로 마감."},
    "육회 덮밥": {"재료": ["밥 200g", "소고기우둔살 100g", "배슬라이스 30g", "고추장배합양념 20g"], "조리법": "1. 신선 우둔살을 2mm 두께로 균일 컷팅 가공.\n2. 참기름, 다진마늘, 고추장 양념에 육회 고속 믹싱.\n3. 밥 위에 상추, 배 슬라이스 깔고 육회 안착."},
    "새우장 덮밥": {"재료": ["밥 200g", "간장절임새우 5미", "달걀노른자 1개", "무순 5g"], "조리법": "1. 간장에 숙성된 새우의 껍질을 정밀 탈피.\n2. 한입 크기로 슬라이스 가공.\n3. 버터 간장 비빔밥 상단에 새우장을 방사형 정렬 후 노른자 배치."},
    "전복장 덮밥": {"재료": ["밥 200g", "간장절임전복 2미", "게우소스 20g", "김가루 5g"], "조리법": "1. 숙성 전복을 껍질과 분리 후 슬라이스.\n2. 전복 내장(게우) 소스를 버터와 볶아 비빔 베이스 구축.\n3. 게우 소스 밥 위에 전복 슬라이스를 격자 정렬."},
    "규동(소고기 덮밥)": {"재료": ["밥 200g", "우삼겹 130g", "양파 50g", "초생강 5g"], "조리법": "1. 가쓰오부시 육수와 간장 베이스 소스를 비등점까지 가열.\n2. 양파와 우삼겹을 투입하여 소스가 배어들도록 2분 가열.\n3. 소스 배합 고기를 밥 위에 가득 덮고 초생강 배치."},
    "오삼불고기 덮밥": {"재료": ["밥 200g", "오징어 80g", "삼겹살 80g", "매콤양념 40g"], "조리법": "1. 두꺼운 삼겹살을 먼저 볶아 유분 조성.\n2. 오징어와 야채, 매운 고추장 소스 동시 투입.\n3. 240도 초고온에서 1분 20초간 급속 볶음 후 배출."},
    "쭈꾸미 덮밥": {"재료": ["밥 200g", "손질쭈꾸미 150g", "천사채 30g", "초강력매운양념 50g"], "조리법": "1. 세척 주꾸미를 고온 스팀으로 15초간 1차 가열.\n2. 캡사이신 배합 매운 소스로 오븐 불맛 마찰 조리.\n3. 대접 밥 위에 주꾸미 낙하 후 마요 천사채 측면 배치."},
    "매운 족발 덮밥": {"재료": ["밥 200g", "순살족발 140g", "직화불양념 40g", "땅콩분태 2g"], "조리법": "1. 콜라겐 가득한 족발을 1.5cm 크기로 다이스 커팅.\n2. 토치풍 직화 양념과 함께 웍에서 불길 마찰 조리.\n3. 밥 위에 매운 족발을 채우고 땅콩분태 분사 토핑."},
    "닭간장 조림 덮밥": {"재료": ["밥 200g", "닭정육 150g", "꽈리고추 20g", "단짠간장소스 30g"], "조리법": "1. 닭정육 껍질면을 바닥으로 하여 팬 시어링 유도.\n2. 간장 타레 소스와 꽈리고추를 투입하여 링 형태로 조림.\n3. 밥 위에 윤기 나는 조림 닭고기와 고추 정렬."},
    "버섯 굴소스 볶음밥": {"재료": ["밥 200g", "새송이표고버섯 60g", "청경채 30g", "굴소스 20g"], "조리법": "1. 새송이, 표고, 만가닥 버섯을 편 썰어 고온 가열.\n2. 청경채 투입 후 숨이 죽기 직전 고슬한 밥 가미.\n3. 프리미엄 굴소스로 코팅하듯 2분간 고속 볶음 조리."},
    "소시지 야채 볶음밥": {"재료": ["밥 200g", "비엔나소시지 60g", "파프리카 30g", "케찹배합소스 25g"], "조리법": "1. 비엔나소시지에 칼집 조형 후 노릇하게 튀김 조리.\n2. 파프리카, 양파와 함께 케첩&돈가스 소스 믹싱.\n3. 밥과 재료가 한 몸이 되도록 주걱 믹싱 볶음 유도."},
    "계란 간장 버터밥": {"재료": ["밥 200g", "버터 15g", "계란 2개", "비법맛간장 15g"], "조리법": "1. 밥 200g을 75도 최적 비빔 온도로 고온 유지 안착.\n2. 무염 버터를 밥 내부 중심부에 매립 가공.\n3. 서니사이드업 프라이 2개를 올린 후 맛간장 드립 분사."},
    "텐동(튀김 덮밥)": {"재료": ["밥 200g", "모둠튀김(새우/단호박/김)", "텐동타레 25g"], "조리법": "1. 새우, 단호박, 김을 전용 튀김반죽으로 180도 가공.\n2. 밥 위에 텐동 전용 타레 소스를 나선형 드립.\n3. 바삭한 튀김들을 예술적 각도로 세워 플레이팅 마감."},
    "항정살 명란 덮밥": {"재료": ["밥 200g", "항정살 130g", "구운명란 30g", "와사비마요 20g"], "조리법": "1. 아삭한 식감의 항정살을 기름을 빼며 바삭하게 구움.\n2. 명란을 오븐에 구워 잘게 다진 후 준비.\n3. 밥 위에 항정살 배열 후 다진 구운 명란과 와사비마요 분사."},
    "닭가슴살 아보카도 덮밥": {"재료": ["현미밥 200g", "수비드닭가슴살 120g", "아보카도 0.5개", "스리라차마요 20g"], "조리법": "1. 60도에서 수비드 가공된 닭가슴살을 큐브 커팅.\n2. 잘 익은 아보카도를 얇게 슬라이스하여 정렬.\n3. 현미밥 위에 두 재료를 정돈하여 올린 후 다이어트 소스 맵핑."},
    "우삼겹 숙주 덮밥": {"재료": ["밥 200g", "우삼겹 120g", "숙주나물 80g", "데리야끼간장 20g"], "조리법": "1. 우삼겹을 강불에 구워 고기 기름 축적.\n2. 고기 기름에 숙주를 넣고 굴소스와 함께 20초 단기 화력 볶음.\n3. 숨이 죽지 않은 아삭한 숙주와 고기를 밥 위에 푸짐하게 세팅."},
    "대창 덮밥(호르몬동)": {"재료": ["밥 200g", "소대창 140g", "노른자 1개", "꽈리고추 2미"], "조리법": "1. 대창을 특제 대창 양념을 바르며 철판 직화 구이.\n2. 구운 대창을 1.5cm 두께로 커팅하여 정렬.\n3. 밥 위에 대창을 두르고 양파, 구운 꽈리고추, 노른자 마감."},
    "고추잡채 덮밥": {"재료": ["밥 200g", "돼지고기슬라이스 60g", "피망 80g", "고추기름 15g"], "조리법": "1. 고추기름 베이스에 채 썬 돼지고기를 고속 가열.\n2. 얇게 채 썬 피망과 양파를 투입하여 중화풍 불맛 믹싱.\n3. 굴소스와 두반장으로 간을 맞춰 전용 대접 밥에 배분."},
    "유산슬 덮밥": {"재료": ["밥 200g", "해삼류/새우 60g", "죽순팽이 50g", "전분소스 120g"], "조리법": "1. 채 썬 죽순, 표고버섯, 부추, 새우, 고기를 데침 가공.\n2. 간장 베이스 중화 육수에 재료를 넣고 끓임.\n3. 녹말가루 전분물로 걸쭉한 울면 점도를 구현하여 밥에 도포."},
    "마라 볶음밥": {"재료": ["밥 200g", "우삼겹 50g", "청경채버섯 40g", "마라소스 20g"], "조리법": "1. 웍에 마라유와 우삼겹, 채소 분태를 가열 가공.\n2. 밥을 넣고 밥알 사이에 마라 소스가 스며들도록 파쇄 배합.\n3. 마라의 얼얼한 풍미가 극대화되는 시점까지 2분 30초 웍질."},
    "중화풍 잡채밥": {"재료": ["밥 200g", "당면 80g", "잡채고기야채 60g", "중화간장소스 20g"], "조리법": "1. 불린 당면을 중화 간장 소스에 졸여 색과 맛 유도.\n2. 채 썬 고기, 피망, 목이버섯을 강불 파기름에 볶음 조리.\n3. 모든 재료와 당면을 고추기름에 최종 혼합 가열하여 밥 옆에 배정."}
}

@app.get("/", response_class=HTMLResponse)
def home_page():
    menu_list_html = "".join([f'<button onclick="searchRecipe(\'{m}\')" class="menu-item">{m}</button>' for m in RECIPE_DB.keys()])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>ChefOS v4.1 - AI Robot Control Center</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f1f5f9; font-family: 'Inter', sans-serif; }}
            .sidebar {{ width: 300px; background-color: #0f172a; color: white; height: 100vh; position: fixed; overflow-y: auto; z-index: 10; }}
            .menu-item {{ width: 100%; text-align: left; padding: 12px 24px; border-bottom: 1px solid #1e293b; font-size: 13px; font-weight: 500; transition: all 0.2s; color: #cbd5e1; }}
            .menu-item:hover {{ background-color: #1e293b; color: #38bdf8; padding-left: 32px; }}
            .main-content {{ margin-left: 300px; padding: 40px; }}
            .recipe-card {{ background: white; border-radius: 24px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); overflow: hidden; }}
            .status-tag {{ background: #dcfce7; color: #15803d; padding: 6px 14px; border-radius: 99px; font-size: 12px; font-weight: 700; }}
            ::-webkit-scrollbar {{ width: 6px; }}
            ::-webkit-scrollbar-track {{ background: #0f172a; }}
            ::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 10px; }}
            
            /* 🔥 추가된 팝업 이펙트 애니메이션 (에프터이펙트 스타일) */
            @keyframes popIn {{
                0% {{ transform: scale(0.5); opacity: 0; }}
                60% {{ transform: scale(1.1); opacity: 1; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
            .animate-pop-in {{ animation: popIn 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }}
        </style>
    </head>
    <body class="flex">
        <div class="sidebar py-6">
            <div class="px-6 mb-6 text-center">
                <h1 class="text-2xl font-black text-blue-400 tracking-tight">ChefOS v4.1</h1>
                <p class="text-xs text-slate-400 mt-1 font-mono uppercase tracking-widest">Autonomous Kitchen Network</p>
            </div>
            <div class="px-6 mb-3 text-xs font-bold text-slate-500 uppercase tracking-widest">Active Recipe Database ({len(RECIPE_DB)} Menus)</div>
            <div class="border-t border-slate-800">
                {menu_list_html}
            </div>
        </div>

        <div class="main-content w-full relative">
            <div class="max-w-4xl mx-auto">
                <div class="flex justify-between items-center mb-8">
                    <div class="relative flex-1 max-w-lg">
                        <input type="text" id="menuInput" placeholder="메뉴 검색 또는 좌측 선택..." 
                               class="w-full pl-12 pr-4 py-3.5 rounded-2xl border-none shadow-sm focus:ring-2 focus:ring-blue-500 outline-none font-medium">
                        <div class="absolute left-4 top-4 text-gray-400">🔍</div>
                    </div>
                    <div class="flex gap-3 ml-4">
                        <span class="status-tag">Live Server Active</span>
                        <span class="status-tag" style="background:#eff6ff; color:#1d4ed8;">Cloud Engine Connected</span>
                    </div>
                </div>

                <div id="welcomeMessage" class="text-center py-32 bg-white rounded-3xl border border-dashed border-slate-300">
                    <div class="text-6xl mb-4">🤖</div>
                    <h2 class="text-2xl font-bold text-slate-800">로봇 시스템 대기 중</h2>
                    <p class="text-slate-500 mt-2">왼쪽 리스트의 50종 레시피 중 하나를 호출하여 원격 조리 명령을 내리십시오.</p>
                </div>

                <div id="resultArea" class="hidden recipe-card border border-slate-100">
                    <div class="p-8 border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white">
                        <h2 id="resultTitle" class="text-2xl font-black text-slate-900"></h2>
                    </div>
                    <div class="p-8 space-y-8">
                        <div>
                            <h3 class="text-xs font-bold text-blue-500 uppercase tracking-widest mb-3">g-Unit Ingredients Precision (계량 알고리즘)</h3>
                            <div id="ingredientsList" class="flex flex-wrap gap-2.5"></div>
                        </div>
                        <div>
                            <h3 class="text-xs font-bold text-blue-500 uppercase tracking-widest mb-3">Mechanical Process Flow (로봇 공정식)</h3>
                            <div id="recipeText" class="text-base text-slate-700 leading-relaxed font-medium bg-slate-50 p-6 rounded-xl border border-slate-200 whitespace-pre-line"></div>
                        </div>
                        <div class="pt-4">
                            <button id="sendBtn" onclick="sendToRobot()" 
                                    class="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg shadow-lg hover:bg-blue-700 transition-all transform hover:-translate-y-0.5">
                                🚀 로봇 셰프에게 조리 전송하기
                            </button>
                        </div>
                    </div>
                </div>

                <div id="errorArea" class="hidden text-center py-8 bg-red-50 rounded-xl text-red-600 font-bold mt-4">
                    데이터베이스에 식별되지 않는 메뉴명입니다.
                </div>
            </div>
        </div>

        <div id="successOverlay" class="fixed inset-0 bg-slate-900 bg-opacity-60 backdrop-blur-sm z-50 hidden flex justify-center items-center">
            <div id="successModal" class="bg-white p-12 rounded-[2rem] shadow-2xl transform scale-0 text-center border-4 border-green-400">
                <div class="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner">
                    <span class="text-5xl">✨</span>
                </div>
                <h2 class="text-4xl font-black text-slate-800 mb-3 tracking-tight">전송 완료!</h2>
                <p id="overlayMenuName" class="text-lg text-slate-600 font-medium bg-slate-100 py-2 px-4 rounded-lg inline-block"></p>
                <p class="text-sm text-green-600 font-bold mt-6 animate-pulse">로봇 셰프 #SH-01 조리 가동 중...</p>
            </div>
        </div>

        <script>
            document.getElementById("menuInput").addEventListener("keyup", function(e) {{
                if (e.key === "Enter") {{ searchRecipe(this.value); }}
            }});

            function searchRecipe(menuName) {{
                if (!menuName) return;
                fetch('/api/recipe?menu_name=' + encodeURIComponent(menuName))
                    .then(function(res) {{
                        if (!res.ok) throw new Error();
                        return res.json();
                    }})
                    .then(function(data) {{
                        document.getElementById("welcomeMessage").classList.add("hidden");
                        document.getElementById("errorArea").classList.add("hidden");
                        document.getElementById("resultArea").classList.remove("hidden");
                        
                        document.getElementById("resultTitle").innerText = "✨ " + data.menu;
                        
                        var ingList = document.getElementById("ingredientsList");
                        ingList.innerHTML = "";
                        data.ingredients.forEach(function(item) {{
                            var div = document.createElement("div");
                            div.className = "bg-white border border-slate-200 px-3 py-1.5 rounded-lg text-xs font-bold text-slate-700 shadow-sm";
                            div.innerText = item;
                            ingList.appendChild(div);
                        }});
                        
                        document.getElementById("recipeText").innerText = data.recipe;
                    }})
                    .catch(function() {{
                        document.getElementById("welcomeMessage").classList.add("hidden");
                        document.getElementById("resultArea").classList.add("hidden");
                        document.getElementById("errorArea").classList.remove("hidden");
                    }});
            }}

            // 🔥 애니메이션이 적용된 새로운 전송 로직
            function sendToRobot() {{
                var btn = document.getElementById("sendBtn");
                var menuName = document.getElementById("resultTitle").innerText.replace("✨ ", "");
                var overlay = document.getElementById("successOverlay");
                var modal = document.getElementById("successModal");
                
                // 버튼 누른 직후 로딩 연출
                btn.innerText = "⚡ 시스템 무선 전송 중...";
                btn.className = "w-full bg-slate-500 text-white py-4 rounded-xl font-bold text-lg cursor-not-allowed";
                btn.disabled = true;

                // 0.8초 뒤 화면 정중앙에 팝업 이펙트 등장!
                setTimeout(function() {{
                    // 버튼 텍스트 원상복구
                    btn.innerText = "🚀 로봇 셰프에게 조리 전송하기";
                    btn.className = "w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg shadow-lg hover:bg-blue-700 transition-all transform hover:-translate-y-0.5";
                    btn.disabled = false;
                    
                    // 오버레이에 메뉴 이름 넣고 애니메이션 클래스 추가
                    document.getElementById("overlayMenuName").innerText = "[" + menuName + "] 알고리즘 전송";
                    overlay.classList.remove("hidden");
                    modal.classList.add("animate-pop-in");
                    
                    // 2.5초 뒤에 스르륵 사라짐
                    setTimeout(function() {{
                        overlay.classList.add("hidden");
                        modal.classList.remove("animate-pop-in");
                    }}, 2500);
                }}, 800);
            }}
        </script>
    </body>
    </html>
    """

@app.get("/api/recipe")
def get_recipe(menu_name: str):
    if menu_name not in RECIPE_DB:
        raise HTTPException(status_code=404, detail="Not Found")
    return {
        "menu": menu_name,
        "ingredients": RECIPE_DB[menu_name]["재료"],
        "recipe": RECIPE_DB[menu_name]["조리법"]
    }
    