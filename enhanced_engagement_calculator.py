# 향상된 인게이지먼트율 계산 방법 예시

class EnhancedEngagementCalculator:
    """더 정교한 인게이지먼트율 계산을 위한 클래스"""
    
    @staticmethod
    def calculate_basic_engagement_rate(likes, comments, followers):
        """기본 인게이지먼트율 계산"""
        engagement = likes + comments
        rate = (engagement / followers * 100) if followers > 0 else 0
        return round(rate, 2)
    
    @staticmethod
    def calculate_weighted_engagement_rate(likes, comments, saves, shares, followers):
        """가중치를 적용한 인게이지먼트율 계산"""
        # 각 액션에 가중치 부여
        weighted_engagement = (
            likes * 1.0 +      # 좋아요: 가중치 1.0
            comments * 3.0 +   # 댓글: 가중치 3.0 (더 높은 참여도)
            saves * 5.0 +      # 저장: 가중치 5.0 (매우 높은 참여도)
            shares * 7.0       # 공유: 가중치 7.0 (최고 참여도)
        )
        rate = (weighted_engagement / followers * 100) if followers > 0 else 0
        return round(rate, 2)
    
    @staticmethod
    def calculate_video_engagement_rate(likes, comments, views, followers):
        """비디오(릴스) 전용 인게이지먼트율 계산"""
        # 방법 1: 팔로워 기준
        follower_based = ((likes + comments) / followers * 100) if followers > 0 else 0
        
        # 방법 2: 조회수 기준 (더 정확함)
        view_based = ((likes + comments) / views * 100) if views > 0 else 0
        
        return {
            "follower_based_rate": round(follower_based, 2),
            "view_based_rate": round(view_based, 2)
        }
    
    @staticmethod
    def get_engagement_grade(engagement_rate):
        """인게이지먼트율에 따른 등급 분류"""
        if engagement_rate >= 6.0:
            return "A+ (매우 우수)"
        elif engagement_rate >= 3.0:
            return "A (우수)"
        elif engagement_rate >= 1.5:
            return "B (양호)"
        elif engagement_rate >= 1.0:
            return "C (보통)"
        else:
            return "D (개선 필요)"

# 사용 예시
if __name__ == "__main__":
    calc = EnhancedEngagementCalculator()
    
    # 예시 데이터
    followers = 10000
    avg_likes = 500
    avg_comments = 50
    avg_saves = 30  # 실제로는 API에서 가져올 수 없음
    avg_shares = 10  # 실제로는 API에서 가져올 수 없음
    avg_views = 5000  # 릴스 조회수
    
    # 기본 인게이지먼트율
    basic_rate = calc.calculate_basic_engagement_rate(avg_likes, avg_comments, followers)
    print(f"기본 인게이지먼트율: {basic_rate}%")
    
    # 가중치 적용 인게이지먼트율
    weighted_rate = calc.calculate_weighted_engagement_rate(
        avg_likes, avg_comments, avg_saves, avg_shares, followers
    )
    print(f"가중치 적용 인게이지먼트율: {weighted_rate}%")
    
    # 비디오 인게이지먼트율
    video_rates = calc.calculate_video_engagement_rate(
        avg_likes, avg_comments, avg_views, followers
    )
    print(f"릴스 인게이지먼트율 (팔로워 기준): {video_rates['follower_based_rate']}%")
    print(f"릴스 인게이지먼트율 (조회수 기준): {video_rates['view_based_rate']}%")
    
    # 등급 분류
    grade = calc.get_engagement_grade(basic_rate)
    print(f"인게이지먼트 등급: {grade}") 