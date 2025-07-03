# 🚀 배포 가이드

인스타그램 인플루언서 분석기를 클라우드에 배포하는 방법을 안내합니다.

## 📋 배포 전 준비사항

1. **GitHub 계정** 생성 및 코드 업로드
2. **클라우드 플랫폼** 계정 생성
3. **도메인** (선택사항)

## 🎯 추천 배포 플랫폼 (난이도별)

### 1️⃣ Railway (가장 쉬움) ⭐⭐⭐⭐⭐

**장점:** 무료 체험, GitHub 연동 자동 배포, 간단한 설정
**비용:** 월 $5부터

**배포 단계:**
1. [Railway.app](https://railway.app) 접속
2. "Start a New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. 이 프로젝트 저장소 선택
5. 자동 배포 완료! 🎉

### 2️⃣ Render (무료 시작) ⭐⭐⭐⭐

**장점:** 무료 플랜 제공, 자동 SSL, 쉬운 설정
**단점:** 무료 플랜은 비활성 시 슬립 모드

**배포 단계:**
1. [Render.com](https://render.com) 가입
2. "New Web Service" 클릭
3. GitHub 저장소 연결
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy 클릭!

### 3️⃣ Heroku (클래식) ⭐⭐⭐

**장점:** 안정적, 많은 애드온
**단점:** 무료 플랜 종료됨

**배포 단계:**
```bash
# Heroku CLI 설치 후
heroku login
heroku create your-app-name
git push heroku main
```

### 4️⃣ DigitalOcean App Platform ⭐⭐⭐

**장점:** 성능 좋음, 합리적 가격
**비용:** 월 $5부터

### 5️⃣ AWS/GCP (고급자용) ⭐⭐

**장점:** 최고 성능, 무한 확장성
**단점:** 복잡한 설정, 비용 관리 필요

## 🔧 환경별 설정 파일

이미 준비된 설정 파일들:
- `Dockerfile` - Docker 컨테이너 배포용
- `railway.toml` - Railway 플랫폼 설정
- `render.yaml` - Render 플랫폼 설정
- `.gitignore` - Git 추적 제외 파일

## 🌐 도메인 연결 (선택사항)

1. **무료 도메인:** Freenom, GitHub Pages
2. **유료 도메인:** Namecheap, GoDaddy
3. **클라우드플레어:** 무료 CDN 및 SSL

## ⚡ 빠른 배포 (Railway 기준)

```bash
# 1. GitHub에 코드 업로드
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo-name.git
git push -u origin main

# 2. Railway 연결
# railway.app에서 GitHub 저장소 선택만 하면 끝!
```

## 🔒 보안 고려사항

1. **환경변수 설정**
   - Instagram 로그인이 필요한 경우 민감정보 보호
   - API 키 등 환경변수로 관리

2. **Rate Limiting**
   - 과도한 요청 방지
   - Instagram API 제한 준수

3. **HTTPS 강제**
   - 모든 플랫폼에서 자동 지원

## 📊 성능 최적화

1. **캐싱 구현**
   - Redis 또는 메모리 캐시 활용
   - 동일 사용자 재요청 시 빠른 응답

2. **CDN 활용**
   - 정적 파일 (CSS, JS, 이미지) 최적화

3. **데이터베이스 고려**
   - 분석 결과 저장으로 재처리 방지

## 🚨 주의사항

1. **Instagram 이용약관 준수**
   - 과도한 크롤링 금지
   - 적절한 지연시간 유지

2. **서버 리소스 관리**
   - 동시 요청 수 제한
   - 메모리 사용량 모니터링

3. **백업 계획**
   - 정기적인 코드 백업
   - 서비스 장애 대응 방안

## 🎯 추천 배포 플랜

**개인/소규모:** Railway ($5/월)
**스타트업:** Render Pro ($25/월)
**기업용:** AWS/GCP (사용량 기반)

## 📞 문제 해결

배포 중 문제가 발생하면:
1. 로그 확인 (각 플랫폼의 로그 메뉴)
2. 환경변수 설정 확인
3. 포트 설정 확인 (`PORT` 환경변수)
4. GitHub 저장소 공개 설정 확인

---

**🎉 축하합니다! 이제 전 세계 어디서나 접근 가능한 인스타그램 인플루언서 분석 서비스를 운영할 수 있습니다!** 