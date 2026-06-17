from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="ChefOS - AI 로봇 셰프 대시보드 v3.0")

# 1. 20종의 초정밀 하드코어 레시피 데이터베이스 (온도, 시간, 조리 공정 세분화)
RECIPE_DB = {
    "치킨 마요 덮밥": {"재료": ["밥 200g", "순살치킨 150g", "마요네즈 30g", "데리야끼소스 20g", "파슬리 1g"], "조리법": "1. 섭씨 180도로 예열된 튀김기에서 순살 치킨을 정확히 4분 30초간 바삭하게 튀겨냅니다.\n2. 덮밥 전용 볼에 밥 200g을 평평하게 깔아줍니다.\n3. 튀겨진 치킨을 3cm 크기로 컷팅하여 밥 위에 정갈하게 올립니다.\n4. 로봇 팔의 듀얼 노즐을 활용해 데리야끼 소스와 마요네즈를 십자 격자무늬(Crosshatch)로 균일하게 분사한 뒤 파슬리를 뿌려 완성합니다."},
    "PD의 밤샘 제육 덮밥": {"재료": ["밥 200g", "돼지고기 전지 180g", "고추장양념 50g", "양파 30g", "대파 10g"], "조리법": "1. 광고 제작과 영상 편집으로 밤을 지새우는 방송국 사람들을 위한 고단백 스태미나 메뉴입니다.\n2. 섭씨 220도의 웍에서 돼지고기와 썰어둔 양파를 초강불로 2분간 볶아 마이야르 반응을 극대화합니다.\n3. 특제 고추장 양념을 투입하고 1분 30초간 추가로 볶아 묵직한 숯불향을 입힙니다.\n4. 밥 옆에 고기를 산처럼 쌓고 알싸한 파채를 곁들여 즉각적인 에너지 보충이 가능하도록 서빙합니다."},
    "15개월 알바생 짜계치 덮밥": {"재료": ["밥 200g", "짜장소스 100g", "계란 1개", "슬라이스 치즈 1장"], "조리법": "1. 15개월 장기 근무 알바생의 노하우가 듬뿍 담긴 피시방 황금 레시피를 로봇 셰프가 완벽히 재현합니다.\n2. 꾸덕한 짜장 소스를 85도에서 뭉근하게 데워 준비된 밥 위에 고르게 부어줍니다.\n3. 정확히 1분 40초간 기름에 튀기듯 조리한 서니사이드업 반숙 계란 프라이를 올립니다.\n4. 계란의 잔열이 남아있을 때 슬라이스 치즈를 덮어 자연스럽게 녹아내리도록 플레이팅합니다."},
    "물류센터 파이팅 덮밥": {"재료": ["밥 220g", "소시지 100g", "스크램블 에그 80g", "매콤케첩 30g"], "조리법": "1. 쉴 새 없이 돌아가는 물류 현장의 든든함을 책임지는 고단백 스피드 덮밥입니다.\n2. 닭가슴살 소시지에 촘촘하게 칼집을 내고 180도 오븐에서 5분간 구워 육즙을 가둡니다.\n3. 로봇 팔을 고속 회전시켜 몽글몽글한 식감의 스크램블 에그를 30초 만에 신속하게 조리합니다.\n4. 밥 위에 소시지와 에그를 반반씩 올리고 매콤새콤한 케첩을 듬뿍 뿌려 마무리합니다."},
    "참치 마요 덮밥": {"재료": ["밥 200g", "캔참치 120g", "마요네즈 40g", "조미김 5g", "단무지 20g"], "조리법": "1. 참치는 200N의 압력으로 프레스하여 기름기를 95% 이상 완벽하게 제거합니다.\n2. 마요네즈와 참치를 믹싱 로봇 팔을 이용해 30초간 균일하게 버무립니다.\n3. 밥 200g 위에 버무린 참치를 돔 형태로 소복하게 쌓아 올립니다.\n4. 다진 단무지를 주변에 두르고 잘게 부순 조미김을 최상단에 토핑하여 식감과 풍미를 끌어올립니다."},
    "철야 노가다 국밥풍 덮밥": {"재료": ["밥 200g", "돼지국밥 육수 50g", "수육 고기 100g", "부추무침 30g", "다대기 15g"], "조리법": "1. 새벽 이슬을 맞으며 일하는 현장 작업자들의 얼어붙은 몸을 녹여줄 든든한 국밥 스타일의 덮밥입니다.\n2. 섭씨 95도로 가열된 진한 돼지 육수를 밥 위에 자작하게 부어 토렴 과정을 거칩니다.\n3. 얇게 썬 수육 고기를 육수 증기로 30초간 데워 촉촉하게 만든 뒤 밥 위에 둥글게 펼칩니다.\n4. 참기름에 갓 무쳐낸 신선한 부추무침과 매콤한 다대기를 중앙에 올려 마무리합니다."},
    "불고기 덮밥": {"재료": ["밥 200g", "소불고기 150g", "팽이버섯 30g", "간장소스 40g", "당면 20g"], "조리법": "1. 미리 불려둔 당면과 팽이버섯을 섭씨 100도의 끓는 물에서 1분간 데쳐냅니다.\n2. 얇게 슬라이스 된 소고기를 비법 간장 소스와 함께 팬에 넣고 160도에서 3분간 졸이듯 볶아줍니다.\n3. 고기의 단백질이 완전히 익고 소스가 자작하게 배어들면 조리를 멈춥니다.\n4. 넓은 그릇에 밥을 담고 그 위에 불고기와 당면을 흐트러지지 않게 올려 한식의 정갈함을 연출합니다."},
    "돈까스 덮밥(가츠동)": {"재료": ["밥 200g", "수제 돈까스 1장(150g)", "계란 1개", "양파 40g", "가츠동 쯔유 50g"], "조리법": "1. 170도의 깨끗한 기름에서 돈까스를 5분간 튀긴 후 기름을 빼고 2cm 간격으로 일정하게 썰어줍니다.\n2. 전용 팬에 쯔유 소스와 채 썬 양파를 넣고 끓어오를 때까지 가열합니다.\n3. 양파가 투명해지면 썰어둔 돈까스를 얹고 가볍게 푼 계란물을 가장자리부터 둥글게 둘러 붓습니다.\n4. 뚜껑을 덮고 30초간 뜸을 들여 계란을 반숙 상태로 익힌 뒤, 밥 위에 원형 그대로 미끄러지듯 얹어냅니다."},
    "오징어 덮밥": {"재료": ["밥 200g", "손질 오징어 150g", "양배추 40g", "대파 20g", "불맛 매운양념 40g"], "조리법": "1. 몸통과 다리를 분리하여 한 입 크기로 손질된 오징어를 준비합니다.\n2. 섭씨 250도로 달궈진 웍에 기름을 두르고 파를 먼저 볶아 파기름을 냅니다.\n3. 오징어와 양배추, 특제 불맛 양념을 동시에 투입하고 1분 30초 동안 초고속 강불 볶음을 진행하여 물이 생기는 것을 방지합니다.\n4. 매콤한 향이 올라오면 즉시 밥 위에 얹어 쫄깃한 식감을 살려 서빙합니다."},
    "스팸 김치볶음밥": {"재료": ["밥 200g", "숙성 김치 120g", "스팸 70g", "계란 1개", "참기름 5g"], "조리법": "1. 적절히 산미가 도는 숙성 김치를 0.5cm 크기로, 스팸을 1cm 큐브 모양으로 정밀하게 깍둑썰기합니다.\n2. 스팸을 먼저 팬에 넣어 자체 기름을 뽑아내고, 그 기름에 김치를 넣어 2분간 볶아 감칠맛을 냅니다.\n3. 고슬고슬한 밥을 넣고 로봇 셰프의 주걱 팔을 이용해 밥알이 뭉치지 않도록 3분간 고르게 볶습니다.\n4. 마지막에 참기름을 두르고, 별도로 조리된 가장자리가 바삭한 계란프라이를 화룡점정으로 올립니다."},
    "새우 볶음밥": {"재료": ["밥 200g", "칵테일 새우 100g", "대파 30g", "계란 1.5개", "굴소스 15g"], "조리법": "1. 파기름을 낸 후 새우를 넣어 표면이 붉은색으로 변할 때까지 1차 볶음을 진행합니다.\n2. 새우를 팬 한쪽으로 밀어두고 빈 공간에 계란물을 부어 스크램블을 만듭니다.\n3. 수분이 적은 볶음용 밥을 투입하고 모든 재료가 섞이도록 초당 2회의 속도로 팬을 흔들며(Tossing) 볶습니다.\n4. 굴소스를 팬 가장자리에 둘러 불맛을 입힌 뒤, 볼에 눌러 담았다가 접시에 뒤집어 예쁜 돔 모양으로 플레이팅합니다."},
    "마파두부 덮밥": {"재료": ["밥 200g", "연두부 1팩(150g)", "다진 돼지고기 60g", "두반장 30g", "전분물 20g"], "조리법": "1. 부드러운 연두부를 깍둑썰기하여 형태가 부서지지 않게 끓는 물에 살짝 데쳐 준비합니다.\n2. 다진 고기를 마늘, 생강과 함께 볶다가 사천식 두반장 소스와 물을 넣고 끓여 베이스를 만듭니다.\n3. 끓는 소스에 데친 연두부를 조심스럽게 넣고 소스가 스며들도록 2분간 조립니다.\n4. 전분물을 조금씩 나누어 부으며 로봇 팔로 부드럽게 저어 완벽한 농도를 맞춘 뒤 밥 위에 덮습니다."},
    "스테이크 덮밥": {"재료": ["밥 200g", "부채살 150g", "생와사비 5g", "양파 슬라이스 30g", "스테이크 소스 25g"], "조리법": "1. 로봇의 정밀 온도 제어 시스템을 통해 200도 철판에서 부채살의 겉면을 강하게 시어링(Searing)합니다.\n2. 내부 온도가 55도(미디엄 레어)에 도달하면 조리를 멈추고 3분간 레스팅(Resting)하여 육즙을 재분배합니다.\n3. 고기를 5mm 두께로 비스듬히 슬라이스하여 밥 위에 부채꼴 모양으로 펼쳐 올립니다.\n4. 매운맛을 뺀 얇은 양파 슬라이스와 생와사비를 곁들이고 달콤짭짤한 소스를 뿌려 고급스러움을 더합니다."},
    "연어 덮밥(사케동)": {"재료": ["초대리 밥 200g", "생연어 슬라이스 120g", "무순 10g", "생와사비 5g", "특제 간장 20g"], "조리법": "1. 식초, 설탕, 소금을 황금 비율로 배합한 초대리를 밥에 섞어 체온과 비슷한 36도로 식혀 준비합니다.\n2. 신선한 생연어를 로봇의 초정밀 칼날을 이용해 8mm 두께로 일정한 각도로 슬라이스합니다.\n3. 초대리 밥 위에 연어 조각을 장미꽃잎처럼 겹겹이 둥글게 둘러 덮어줍니다.\n4. 중앙에 무순과 와사비를 다소곳이 얹고, 덮밥 전용 달짝지근한 간장을 별도 용기에 담아 제공합니다."},
    "강된장 덮밥": {"재료": ["보리밥 200g", "우렁 강된장 120g", "상추 20g", "부추 10g", "참기름 5g"], "조리법": "1. 백미와 보리를 7:3 비율로 섞어 지은 건강한 보리밥을 그릇에 담습니다.\n2. 뚝배기에서 자박자박하게 끓여낸 짭조름한 밥도둑 우렁 강된장을 듬뿍 퍼서 밥 위에 얹습니다.\n3. 상추와 부추를 0.5cm 간격으로 채 썰어 강된장 주변에 빙 둘러 푸릇한 색감을 살립니다.\n4. 마지막으로 100% 통참깨를 착유한 진한 참기름을 한 바퀴 둘러 고소한 향을 극대화합니다."},
    "명란 마요 덮밥": {"재료": ["밥 200g", "저염 명란젓 40g", "계란 노른자 1개", "마요네즈 25g", "어린잎 채소 15g"], "조리법": "1. 저염 명란젓의 얇은 막을 로봇 핀셋으로 제거하고 부드러운 알맹이만 조심스럽게 추출합니다.\n2. 밥 위에 어린잎 채소를 둥지 모양으로 깔고 그 중앙에 추출한 명란을 소복하게 올립니다.\n3. 명란의 짭짤함을 중화시켜 줄 마요네즈를 지그재그 패턴으로 정교하게 뿌립니다.\n4. 명란 바로 옆에 신선한 계란 노른자 1알을 터지지 않게 착륙시켜 톡 터뜨려 비벼 먹도록 유도합니다."},
    "카레 볶음밥": {"재료": ["밥 200g", "카레 가루 20g", "다진 돼지고기 40g", "감자/당근 큐브 40g", "버터 10g"], "조리법": "1. 1cm 크기로 썬 감자와 당근, 돼지고기를 버터 10g을 두른 팬에서 완전히 익을 때까지 볶아냅니다.\n2. 찬밥 200g을 투입하고 밥알이 흩어지도록 주걱으로 가르며 볶습니다.\n3. 숙성된 특제 카레 가루를 넣고 뭉치는 곳 없이 전체적으로 샛노란 색이 입혀질 때까지 2분간 웍질합니다.\n4. 강불에서 30초간 마지막으로 볶아 카레의 스파이시한 풍미를 끌어올린 후 접시에 세팅합니다."},
    "낙지 덮밥": {"재료": ["밥 200g", "통낙지 1마리(150g)", "아삭 콩나물 60g", "매운 고춧가루 양념 50g", "통깨 2g"], "조리법": "1. 굵은 소금으로 치대 불순물을 제거한 통낙지를 끓는 물에 10초만 데쳐 야들야들한 식감을 잡습니다.\n2. 250도의 초고온 웍에서 양배추, 양파와 함께 특제 매운 양념을 넣고 1분 내로 짧고 굵게 볶아냅니다.\n3. 밥 위에 매운맛을 중화시켜 줄 하얗게 데친 콩나물을 한 쪽에 듬뿍 쌓습니다.\n4. 콩나물 옆에 붉은 낙지볶음을 올리고 통깨를 솔솔 뿌려 침샘을 자극하는 비주얼을 완성합니다."},
    "베이컨 계란 볶음밥": {"재료": ["밥 200g", "훈제 베이컨 50g", "계란 2개", "대파 20g", "후추 1g"], "조리법": "1. 훈제 베이컨을 1cm 너비로 썰어 팬에 올리고 약불에서 은근하게 가열하여 돼지기름을 충분히 뽑아냅니다.\n2. 베이컨 기름에 송송 썬 대파를 튀기듯 볶아 서양과 동양의 풍미가 결합된 베이컨 파기름을 완성합니다.\n3. 계란 2개를 풀어 스크램블을 만든 후 밥을 넣고 고슬고슬하게 볶아줍니다.\n4. 밥알 하나하나에 베이컨의 스모키한 향과 계란의 코팅이 입혀지면 굵은 흑후추를 갈아 넣어 완성합니다."},
    "깍두기 볶음밥": {"재료": ["밥 200g", "잘 익은 깍두기 100g", "깍두기 국물 40g", "김가루 10g", "치즈 30g"], "조리법": "1. 새콤하게 잘 익은 깍두기를 물에 씻지 않고 양념장 그대로 0.5cm 크기로 잘게 다져 팬에 올립니다.\n2. 깍두기와 밥을 볶다가 비법인 깍두기 국물을 부어 전체적으로 붉고 먹음직스러운 색을 냅니다.\n3. 팬의 바닥에 밥을 얇게 펴서 누룽지가 생기도록 중약불에서 2분간 인내심을 갖고 지져냅니다.\n4. 치즈를 솔솔 뿌려 뚜껑을 덮어 녹인 뒤, 치즈가 길게 늘어나는 환상적인 볶음밥을 서빙합니다."}
}

@app.get("/", response_class=HTMLResponse)
def home_page():
    # 메뉴 목록 동적 생성
    menu_list_html = "".join([f'<button onclick="searchRecipe(\'{m}\')" class="menu-item">{m}</button>' for m in RECIPE_DB.keys()])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>ChefOS - AI Robot Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style>
            body {{ background-color: #f8fafc; font-family: 'Inter', sans-serif; }}
            .sidebar {{ width: 280px; background-color: #1e293b; color: white; height: 100vh; position: fixed; overflow-y: auto; }}
            .menu-item {{ width: 100%; text-align: left; padding: 14px 24px; border-bottom: 1px solid #334155; font-size: 14px; font-weight: 500; transition: 0.2s; }}
            .menu-item:hover {{ background-color: #334155; color: #38bdf8; padding-left: 30px; }}
            .main-content {{ margin-left: 280px; padding: 40px; padding-bottom: 100px; }}
            .recipe-card {{ background: white; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); overflow: hidden; }}
            .status-tag {{ background: #dcfce7; color: #166534; padding: 6px 14px; border-radius: 99px; font-size: 12px; font-weight: bold; letter-spacing: 0.5px; }}
            
            /* 스크롤바 꾸미기 */
            ::-webkit-scrollbar {{ width: 8px; }}
            ::-webkit-scrollbar-track {{ background: #1e293b; }}
            ::-webkit-scrollbar-thumb {{ background: #475569; border-radius: 10px; }}
            ::-webkit-scrollbar-thumb:hover {{ background: #64748b; }}
        </style>
    </head>
    <body class="flex">
        <div class="sidebar py-6">
            <div class="px-6 mb-8 text-center">
                <h1 class="text-2xl font-black text-blue-400 tracking-tight">ChefOS v3.0</h1>
                <p class="text-xs text-gray-400 mt-2 font-medium tracking-widest uppercase">AI Kitchen System</p>
            </div>
            <div class="px-6 mb-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Available Menus ({len(RECIPE_DB)})</div>
            <div class="border-t border-gray-700">
                {menu_list_html}
            </div>
        </div>

        <div class="main-content w-full relative">
            <div class="max-w-4xl mx-auto">
                <div class="flex justify-between items-center mb-10">
                    <div class="relative flex-1 max-w-xl">
                        <input type="text" id="menuInput" placeholder="메뉴 이름을 검색하거나 왼쪽에서 메뉴를 클릭하세요..." 
                               class="w-full pl-14 pr-6 py-4 rounded-2xl border border-gray-200 shadow-sm focus:ring-4 focus:ring-blue-100 outline-none text-gray-700 font-medium transition-all">
                        <div class="absolute left-5 top-4 text-xl opacity-50">🔍</div>
                    </div>
                    <div class="flex gap-4 ml-6">
                        <span class="status-tag flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> Network Active</span>
                        <span class="status-tag flex items-center gap-2" style="background:#fef3c7; color:#92400e;">🤖 Robot ID: #SH-01</span>
                    </div>
                </div>

                <div id="welcomeMessage" class="text-center py-32 bg-white rounded-3xl border border-dashed border-gray-300">
                    <div class="text-7xl mb-6">👨‍🍳</div>
                    <h2 class="text-3xl font-black text-gray-800 tracking-tight">레시피 데이터를 호출하세요</h2>
                    <p class="text-gray-500 mt-4 font-medium">좌측의 메뉴판에서 조리할 덮밥을 선택해 주십시오.</p>
                </div>

                <div id="resultArea" class="hidden recipe-card border border-gray-100">
                    <div class="p-10 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-white">
                        <h2 id="resultTitle" class="text-3xl font-black text-gray-900 tracking-tight"></h2>
                    </div>
                    <div class="p-10 space-y-10">
                        <div>
                            <h3 class="text-xs font-black text-blue-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                                ⚖️ Precision Ingredients (로봇 정밀 계량)
                            </h3>
                            <div id="ingredientsList" class="flex flex-wrap gap-3"></div>
                        </div>
                        <div>
                            <h3 class="text-xs font-black text-blue-500 uppercase tracking-widest mb-4 flex items-center gap-2">
                                ⚙️ Cooking Process (조리 세부 알고리즘)
                            </h3>
                            <div id="recipeText" class="text-base text-gray-700 leading-loose font-medium bg-gray-50 p-6 rounded-2xl border border-gray-100"></div>
                        </div>
                        <div class="pt-6">
                            <button id="sendBtn" onclick="sendToRobot()" 
                                    class="w-full bg-blue-600 text-white py-5 rounded-2xl font-black text-lg shadow-lg hover:bg-blue-700 hover:shadow-xl hover:-translate-y-1 transition-all duration-200 flex justify-center items-center gap-3">
                                <span>⚡ 로봇 셰프에게 조리 전송하기</span>
                            </button>
                        </div>
                    </div>
                </div>

                <div id="errorArea" class="hidden text-center py-10 bg-red-50 rounded-2xl text-red-600 font-bold border border-red-100 shadow-inner mt-4">
                    ❌ 데이터베이스에 등록되지 않은 메뉴입니다. 메뉴명을 다시 확인해 주세요.
                </div>
            </div>
        </div>

        <div id="toastNotification" class="fixed bottom-10 right-10 transform translate-y-32 opacity-0 transition-all duration-500 ease-out bg-gray-900 text-white px-8 py-5 rounded-2xl shadow-2xl flex items-center gap-5 z-50 border border-gray-700">
            <div class="text-4xl">✅</div>
            <div>
                <h4 class="font-black text-lg tracking-tight text-green-400">전송 성공!</h4>
                <p id="toastMessage" class="text-sm text-gray-300 font-medium mt-1">로봇 셰프에게 조리 명령이 하달되었습니다.</p>
            </div>
        </div>

        <script>
            // 엔터키 검색
            document.getElementById("menuInput").addEventListener("keyup", function(e) {{
                if (e.key === "Enter") {{ searchRecipe(this.value); }}
            }});

            // 메뉴 검색 기능
            function searchRecipe(menuName) {{
                if (!menuName) return;
                
                fetch(`/api/recipe?menu_name=${{encodeURIComponent(menuName)}}`)
                    .then(res => {{
                        if (!res.ok) throw new Error();
                        return res.json();
                    }})
                    .then(data => {{
                        document.getElementById("welcomeMessage").classList.add("hidden");
                        document.getElementById("errorArea").classList.add("hidden");
                        const resultArea = document.getElementById("resultArea");
                        resultArea.classList.remove("hidden");
                        
                        document.getElementById("resultTitle").innerText = `✨ ${{data.menu}}`;
                        
                        // 재료 렌더링
                        const ingList = document.getElementById("ingredientsList");
                        ingList.innerHTML = "";
                        data.ingredients.forEach(item => {{
                            const div = document.createElement("div");
                            div.className = "bg-white border border-gray-200 px-4 py-2.5 rounded-xl text-sm font-bold text-gray-700 shadow-sm";
                            div.innerText = item;
                            ingList.appendChild(div);
                        }});
                        
                        // 레시피 렌더링 (줄바꿈 인식)
                        const formattedRecipe = data.recipe.replace(/\\n/g, '<br><br>');
                        document.getElementById("recipeText").innerHTML = formattedRecipe;
                    }})
                    .catch(() => {{
                        document.getElementById("welcomeMessage").classList.add("hidden");
                        document.getElementById("resultArea").classList.add("hidden");
                        document.getElementById("errorArea").classList.remove("hidden");
                    }});
            }}

            // 🚀 전송 버튼 애니메이션 기능
            function sendToRobot() {{
                const btn = document.getElementById("sendBtn");
                const toast = document.getElementById("toastNotification");
                const menuName = document.getElementById("resultTitle").innerText.replace('✨ ', '');
                
                // 버튼 누른 효과 (버튼 텍스트 변경)
                const originalText = btn.innerHTML;
                btn.innerHTML = `<span class="animate-spin">⏳</span> 데이터 전송 중...`;
                btn.classList.replace("bg-blue-600", "bg-gray-500");
                btn.disabled = true;

                // 1초 뒤에 알림창 띄우기
                setTimeout(() => {{
                    // 버튼 원상복구
                    btn.innerHTML = originalText;
                    btn.classList.replace("bg-gray-500", "bg-blue-600");
                    btn.disabled = false;
                    
                    // 토스트 메시지 띄우기
                    document.getElementById("toastMessage").innerText = `'${{menuName}}' 조리 명령이 #SH-01 로봇으로 하달되었습니다.`;
                    toast.classList.remove("translate-y-32", "opacity-0");
                    
                    // 3.5초 뒤에 토스트 메시지 숨기기
                    setTimeout(() => {{
                        toast.classList.add("translate-y-32", "opacity-0");
                    }}, 3500);
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
    