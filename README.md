# 인스타그램 인플루언서 분석기

Instagram 인플루언서의 정보와 인게이지먼트 데이터를 크롤링하여 분석하는 웹 서비스입니다.

## 기능

- **기본 정보 수집**: 사용자명, 팔로워 수, 게시물 수, 프로필 정보
- **게시물 분석**: 평균 좋아요, 댓글, 인게이지먼트율 계산
- **릴스 분석**: 릴스 게시물의 평균 인게이지먼트와 조회수 분석
- **시각적 대시보드**: 아름다운 웹 인터페이스로 결과 표시

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
python main.py
```

또는

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 웹 브라우저 접속

[http://localhost:8000](http://localhost:8000) 에서 서비스를 이용할 수 있습니다.

## 사용 방법

1. 웹 페이지에서 분석하고 싶은 인스타그램 사용자명을 입력합니다.
2. "분석하기" 버튼을 클릭합니다.
3. 분석 결과를 확인합니다:
   - 기본 프로필 정보
   - 게시물 인게이지먼트 통계
   - 릴스 인게이지먼트 통계

## 기술 스택

- **백엔드**: FastAPI, Python
- **크롤링**: Instaloader
- **프론트엔드**: HTML5, CSS3, JavaScript, Bootstrap 5
- **UI/UX**: Font Awesome, 그라데이션 디자인

## 주의사항

- 공개 계정만 분석 가능합니다.
- Instagram의 이용약관을 준수하여 적절한 지연시간을 두고 크롤링합니다.
- 과도한 요청 시 일시적으로 제한될 수 있습니다.

## API 엔드포인트

### GET /
메인 웹 페이지를 반환합니다.

### POST /analyze
인플루언서 정보를 분석합니다.

**요청 파라미터:**
- `username` (form-data): 인스타그램 사용자명

**응답 예시:**
```json
{
  "id": "example_user",
  "instagram_link": "https://www.instagram.com/example_user",
  "followers_count": 10000,
  "post_count": 150,
  "posts_analysis": {
    "average_likes": 500.5,
    "average_comments": 25.2,
    "average_engagement": 525.7,
    "engagement_rate_percent": 5.26
  },
  "reels_analysis": {
    "average_likes": 800.3,
    "average_comments": 40.1,
    "average_video_views": 2500.0,
    "engagement_rate_percent": 8.40
  }
}
```

### GET /health
서버 상태를 확인합니다.

## 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제작되었습니다. 상업적 사용 시 Instagram의 이용약관을 반드시 확인하세요. 