from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from instagram_crawler import InstagramCrawler
import os

app = FastAPI(title="Instagram Influencer Crawler", version="1.0.0")

# 디렉토리 생성 확인
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# 정적 파일과 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Instagram 크롤러 인스턴스
crawler = InstagramCrawler()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """메인 페이지를 렌더링합니다."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_influencer(username: str = Form(...)):
    """인스타그램 사용자명을 받아서 인플루언서 정보를 분석합니다."""
    try:
        # @ 기호 제거
        username = username.replace("@", "").strip()
        
        if not username:
            raise HTTPException(status_code=400, detail="사용자명을 입력해주세요.")
        
        # 인플루언서 정보 크롤링
        result = await crawler.get_influencer_info(username)
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"크롤링 중 오류가 발생했습니다: {str(e)}")

@app.get("/health")
async def health_check():
    """서비스 상태를 확인합니다."""
    return {"status": "healthy", "message": "Instagram Influencer Crawler is running"}

if __name__ == "__main__":
    # 디렉토리가 없으면 생성
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    
    # 환경변수에서 포트 가져오기 (배포 환경 고려)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False) 