from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI(title="ChefOS - AI 로봇 셰프 대시보드")

# 1. 확장된 레시피 데이터베이스 (덮밥 & 볶음밥 20종)
RECIPE_DB = {
    "치킨 마요 덮밥": {"재료": ["밥 200g", "순살치킨 150g", "마요네즈 30g", "데리야끼소스 20g"], "조리법": "치킨을 바삭하게 튀긴 후 밥 위에 얹고 소스와 마요네즈를 지그재그로 뿌립니다."},
    "참치 마요 덮밥": {"재료": ["밥 200g", "캔참치 100g", "마요네즈 40g", "조미김 5g"], "조리법": "기름기를 뺀 참치와 마요네즈를 버무려 밥 위에 올리고 김가루를 뿌려 마무리합니다."},
    "제육 덮밥": {"재료": ["밥 200g", "돼지고기 전지 180g", "고추장양념 40g", "양파 30g"], "조리법": "강한 불에 고기와 양파를 볶아 불향을 입힌 뒤 밥 옆에 정갈하게 담아냅니다."},
    "불고기 덮밥": {"재료": ["밥 200g", "소불고기 150g", "팽이버섯 30g", "간장소스 30g"], "조리법": "소고기와 버섯을 간장 베이스 소스에 자작하게 졸여 밥 위에 얹어 서빙합니다."},
    "돈까스 덮밥(가츠동)": {"재료": ["밥 200g", "돈까스 1장", "계란 1개", "쯔유소스 40g"], "조리법": "쯔유 소스에 양파와 계란을 풀어 끓인 뒤 튀긴 돈까스 위에 부어 촉촉하게 만듭니다."},
    "오징어 덮밥": {"재료": ["밥 200g", "오징어 150g", "대파 20g", "매운고춧가루 15g"], "조리법": "손질된 오징어를 채소와 함께 매콤하게 볶아 밥 위에 올립니다."},
    "스팸 김치볶음밥": {"재료": ["밥 200g", "잘게 썬 김치 100g", "스팸 60g", "계란 1개"], "조리법": "스팸과 김치를 먼저 충분히 볶은 뒤 밥을 넣어 고슬고슬하게 볶고 계란프라이를 올립니다."},
    "새우 볶음밥": {"재료": ["밥 200g", "칵테일새우 80g", "스크램블에그 50g", "굴소스 10g"], "조리법": "새우를 먼저 익힌 후 밥과 계란, 굴소스를 넣어 고온에서 빠르게 볶아냅니다."},
    "마파두부 덮밥": {"재료": ["밥 200g", "연두부 150g", "다진돼지고기 50g", "두반장 20g"], "조리법": "고기와 두반장을 볶다가 두부와 전분물을 넣어 걸쭉하게 만든 뒤 밥 위에 붓습니다."},
    "스테이크 덮밥": {"재료": ["밥 200g", "부채살 스테이크 150g", "와사비 5g", "스테이크소스 20g"], "조리법": "미디엄으로 익힌 스테이크를 얇게 썰어 밥 위에 두르고 와사비를 곁들입니다."},
    "가지 덮밥": {"재료": ["밥 200g", "가지 1개", "굴소스 15g", "다진마늘 10g"], "조리법": "가지를 깍둑썰기하여 기름에 튀기듯 볶은 후 짭조름한 소스에 버무려 밥과 함께 냅니다."},
    "연어 덮밥(사케동)": {"재료": ["밥 200g", "생연어 120g", "무순 5g", "간장소스 20g"], "조리법": "초대리가 된 밥 위에 신선한 연어를 올리고 간장과 무순으로 장식합니다."},
    "강된장 덮밥": {"재료": ["밥 200g", "강된장소스 100g", "두부 50g", "부추 10g"], "조리법": "진하게 끓인 강된장과 으깬 두부를 밥 위에 올리고 신선한 부추를 곁들입니다."},
    "명란 마요 덮밥": {"재료": ["밥 200g", "명란젓 30g", "마요네즈 20g", "어린잎채소 10g"], "조리법": "명란의 껍질을 제거한 뒤 마요네즈와 섞어 밥 위에 올리고 채소를 얹습니다."},
    "카레 볶음밥": {"재료": ["밥 200g", "카레가루 15g", "감자/당근 30g", "햄 40g"], "조리법": "잘게 썬 채소와 햄을 볶다가 밥과 카레가루를 넣어 노란색이 잘 배도록 볶습니다."},
    "낙지 덮밥": {"재료": ["밥 200g", "낙지 150g", "콩나물 50g", "매운양념 40g"], "조리법": "데친 콩나물과 매콤한 낙지볶음을 밥 위에 푸짐하게 올려 제공합니다."},
    "베이컨 계란 볶음밥": {"재료": ["밥 200g", "베이컨 3줄", "계란 2개", "파기름 10g"], "조리법": "파기름에 베이컨과 계란을 먼저 볶은 후 밥을 넣어 풍미를 살려 볶습니다."},
    "양배추 계란 덮밥": {"재료": ["밥 200g", "양배추 100g", "계란 2개", "쯔유 15g"], "조리법": "채 썬 양배추가 숨이 죽을 때까지 볶은 후 계란물을 부어 부드럽게 익혀 밥 위에 얹습니다."},
    "소고기 버섯 덮밥": {"재료": ["밥 200g", "우삼겹 100g", "느타리버섯 50g", "굴소스 15g"], "조리법": "우삼겹에서 나온 기름에 버섯을 볶아 풍미를 극대화한 뒤 소스로 마무리하여 밥과 냅니다."},
    "깍두기 볶음밥": {"재료": ["밥 200g", "다진 깍두기 80g", "깍두기 국물 30g", "김가루 5g"], "조리법": "잘 익은 깍두기를 밥과 함께 볶아 아삭한 식감을 살린 뒤 김가루를 듬뿍 뿌립니다."}
}

@app.get("/", response_class=HTMLResponse)
def home_page():
    # 메뉴 목록 생성을 위한 코드
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
            .menu-item {{ width: 100%; text-align: left; padding: 12px 20px; border-bottom: 1px solid #334155; font-size: 14px; transition: 0.2s; }}
            .menu-item:hover {{ background-color: #334155; color: #38bdf8; }}
            .main-content {{ margin-left: 280px; padding: 40px; }}
            .recipe-card {{ background: white; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); overflow: hidden; }}
            .status-tag {{ background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 99px; font-size: 12px; font-weight: bold; }}
        </style>
    </head>
    <body class="flex">
        <div class="sidebar py-6">
            <div class="px-6 mb-8 text-center">
                <h1 class="text-xl font-black text-blue-400">ChefOS v2.0</h1>
                <p class="text-xs text-gray-400 mt-1">AI Kitchen Intelligence</p>
            </div>
            <div class="px-4 mb-4 text-xs font-bold text-gray-500 uppercase tracking-widest">Recipe List</div>
            {menu_list_html}
        </div>

        <div class="main-content w-full">
            <div class="max-w-4xl mx-auto">
                <div class="flex justify-between items-center mb-8">
                    <div class="relative flex-1 max-w-lg">
                        <input type="text" id="menuInput" placeholder="메뉴 이름을 검색하거나 왼쪽에서 선택하세요..." 
                               class="w-full pl-12 pr-4 py-3 rounded-2xl border-none shadow-sm focus:ring-2 focus:ring-blue-500 outline-none">
                        <div class="absolute left-4 top-3.5 text-gray-400">🔍</div>
                    </div>
                    <div class="flex gap-4 ml-6">
                        <span class="status-tag">Echo Gate Active</span>
                        <span class="status-tag" style="background:#fef3c7; color:#92400e;">Robot ID: #SH-01</span>
                    </div>
                </div>

                <div id="welcomeMessage" class="text-center py-20">
                    <div class="text-6xl mb-6">👨‍🍳</div>
                    <h2 class="text-2xl font-bold text-gray-800">레시피를 선택해 주세요</h2>
                    <p class="text-gray-500 mt-2">왼쪽 목록에서 메뉴를 클릭하거나 검색창을 이용하세요.</p>
                </div>

                <div id="resultArea" class="hidden recipe-card">
                    <div class="p-8 border-b border-gray-100 bg-blue-50">
                        <h2 id="resultTitle" class="text-2xl font-black text-gray-800"></h2>
                    </div>
                    <div class="p-8 space-y-8">
                        <div>
                            <h3 class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">Precision Ingredients (정밀 계량)</h3>
                            <div id="ingredientsList" class="flex flex-wrap gap-3"></div>
                        </div>
                        <div>
                            <h3 class="text-sm font-bold text-gray-400 uppercase tracking-widest mb-4">Cooking Process (조리 공정)</h3>
                            <div id="recipeText" class="text-lg text-gray-700 leading-relaxed font-medium"></div>
                        </div>
                        <div class="pt-6">
                            <button class="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg shadow-lg hover:bg-blue-700 transition">
                                로봇 셰프에게 조리 전송하기
                            </button>
                        </div>
                    </div>
                </div>

                <div id="errorArea" class="hidden text-center py-10 bg-red-50 rounded-2xl text-red-600 font-bold border border-red-100">
                    등록되지 않은 메뉴입니다. 메뉴명을 다시 확인해 주세요.
                </div>
            </div>
        </div>

        <script>
            document.getElementById("menuInput").addEventListener("keyup", function(e) {{
                if (e.key === "Enter") {{ searchRecipe(this.value); }}
            }});

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
                        
                        const ingList = document.getElementById("ingredientsList");
                        ingList.innerHTML = "";
                        data.ingredients.forEach(item => {{
                            const div = document.createElement("div");
                            div.className = "bg-white border-2 border-blue-100 px-4 py-2 rounded-xl text-sm font-bold text-blue-600";
                            div.innerText = item;
                            ingList.appendChild(div);
                        }});
                        
                        document.getElementById("recipeText").innerText = data.recipe;
                    }})
                    .catch(() => {{
                        document.getElementById("welcomeMessage").classList.add("hidden");
                        document.getElementById("resultArea").classList.add("hidden");
                        document.getElementById("errorArea").classList.remove("hidden");
                    }});
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
    