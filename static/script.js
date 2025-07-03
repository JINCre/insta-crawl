// 폼 제출 이벤트 처리
document.getElementById('analyzeForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    if (!username) {
        showError('사용자명을 입력해주세요.');
        return;
    }
    
    // UI 상태 변경
    showLoading();
    hideError();
    hideResults();
    
    try {
        const formData = new FormData();
        formData.append('username', username);
        
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || '분석 중 오류가 발생했습니다.');
        }
        
        // 결과 표시
        displayResults(data);
        showResults();
        
    } catch (error) {
        showError(error.message);
    } finally {
        hideLoading();
    }
});

// 로딩 표시
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('analyzeBtn').disabled = true;
    document.getElementById('analyzeBtn').innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>분석중...';
}

// 로딩 숨기기
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('analyzeBtn').disabled = false;
    document.getElementById('analyzeBtn').innerHTML = '<i class="fas fa-chart-line me-2"></i>분석하기';
}

// 에러 표시
function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorAlert').style.display = 'block';
}

// 에러 숨기기
function hideError() {
    document.getElementById('errorAlert').style.display = 'none';
}

// 결과 표시
function showResults() {
    document.getElementById('results').style.display = 'block';
    
    // 부드러운 스크롤 효과
    document.getElementById('results').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// 결과 숨기기
function hideResults() {
    document.getElementById('results').style.display = 'none';
}

// 결과 데이터 표시
function displayResults(data) {
    // 기본 정보
    document.getElementById('profilePic').src = data.profile_pic_url || '/static/default-avatar.png';
    document.getElementById('fullName').textContent = data.full_name || data.id;
    document.getElementById('username_result').textContent = data.id;
    
    // 인증 배지
    if (data.is_verified) {
        document.getElementById('verifiedBadge').style.display = 'inline-block';
    } else {
        document.getElementById('verifiedBadge').style.display = 'none';
    }
    
    // 통계
    document.getElementById('followersCount').textContent = formatNumber(data.followers_count);
    document.getElementById('postCount').textContent = formatNumber(data.post_count);
    document.getElementById('followingCount').textContent = formatNumber(data.following_count);
    
    // 바이오그래피
    document.getElementById('biography').textContent = data.biography || '바이오그래피가 없습니다.';
    
    // 외부 링크
    if (data.external_url) {
        document.getElementById('externalUrl').href = data.external_url;
        document.getElementById('externalUrl').style.display = 'inline-block';
    } else {
        document.getElementById('externalUrl').style.display = 'none';
    }
    
    // 인스타그램 링크
    document.getElementById('instagramLink').href = data.instagram_link;
    
    // 게시물 분석 결과
    const postsAnalysis = data.posts_analysis;
    document.getElementById('avgPostLikes').textContent = formatNumber(postsAnalysis.average_likes);
    document.getElementById('avgPostComments').textContent = formatNumber(postsAnalysis.average_comments);
    document.getElementById('avgPostEngagement').textContent = formatNumber(postsAnalysis.average_engagement);
    document.getElementById('postEngagementRate').textContent = postsAnalysis.engagement_rate_percent + '%';
    
    // 릴스 분석 결과
    const reelsAnalysis = data.reels_analysis;
    document.getElementById('avgReelsLikes').textContent = formatNumber(reelsAnalysis.average_likes);
    document.getElementById('avgReelsComments').textContent = formatNumber(reelsAnalysis.average_comments);
    
    // 조회수 표시 개선
    const avgViews = reelsAnalysis.average_video_views;
    if (avgViews === 0) {
        document.getElementById('avgReelsViews').innerHTML = '<small class="text-muted">제한됨</small>';
        document.getElementById('avgReelsViews').title = 'Instagram 정책으로 인해 조회수 정보에 접근할 수 없습니다';
    } else {
        document.getElementById('avgReelsViews').textContent = formatNumber(avgViews);
    }
    
    document.getElementById('avgReelsEngagement').textContent = formatNumber(reelsAnalysis.average_engagement);
    document.getElementById('reelsEngagementRate').textContent = reelsAnalysis.engagement_rate_percent + '%';
}

// 숫자 포맷팅 함수
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    } else {
        return num.toLocaleString();
    }
}

// 페이지 로드 시 사용자명 입력 필드에 포커스
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('username').focus();
    
    // 엔터 키로 폼 제출
    document.getElementById('username').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('analyzeForm').dispatchEvent(new Event('submit'));
        }
    });
});

// 입력 필드 실시간 검증
document.getElementById('username').addEventListener('input', function(e) {
    const value = e.target.value.trim();
    const submitBtn = document.getElementById('analyzeBtn');
    
    if (value) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('disabled');
    } else {
        submitBtn.disabled = true;
        submitBtn.classList.add('disabled');
    }
});

// 결과 카드 애니메이션
function animateNumbers() {
    const numbers = document.querySelectorAll('.stat-number');
    numbers.forEach(number => {
        const value = number.textContent;
        number.textContent = '0';
        
        const increment = parseInt(value.replace(/[^\d]/g, '')) / 100;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= parseInt(value.replace(/[^\d]/g, ''))) {
                number.textContent = value;
                clearInterval(timer);
            } else {
                number.textContent = Math.floor(current).toLocaleString();
            }
        }, 20);
    });
} 