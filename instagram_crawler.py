import instaloader
import asyncio
from typing import Dict, Any, List
import time
from datetime import datetime, timedelta
import os

class InstagramCrawler:
    def __init__(self):
        self.loader = instaloader.Instaloader()
        # 더 안전한 User-Agent 설정과 추가 옵션
        self.loader.context.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        # 요청 간격 설정 (Instagram 제한 회피)
        self.loader.context.request_timeout = 60
        self.loader.context.max_connection_attempts = 3
        
    async def get_influencer_info(self, username: str) -> Dict[str, Any]:
        """인플루언서의 정보를 크롤링합니다."""
        try:
            # 재시도 로직으로 프로필 가져오기
            profile = await self._get_profile_with_retry(username)
            
            # 기본 정보
            basic_info = {
                "id": profile.username,
                "instagram_link": f"https://www.instagram.com/{profile.username}",
                "followers_count": profile.followers,
                "following_count": profile.followees,
                "post_count": profile.mediacount,
                "full_name": profile.full_name,
                "biography": profile.biography,
                "external_url": profile.external_url,
                "is_verified": profile.is_verified,
                "is_business_account": profile.is_business_account,
                "profile_pic_url": profile.profile_pic_url
            }
            
            # 게시물 분석을 위한 최신 게시물 가져오기 (최대 20개)
            posts_data = await self._analyze_posts(profile, limit=20)
            reels_data = await self._analyze_reels(profile, limit=10)
            
            result = {
                **basic_info,
                "posts_analysis": posts_data,
                "reels_analysis": reels_data,
                "crawled_at": datetime.now().isoformat()
            }
            
            return result
            
        except instaloader.exceptions.ProfileNotExistsException:
            raise ValueError(f"사용자 '{username}'을(를) 찾을 수 없습니다.")
        except instaloader.exceptions.LoginRequiredException:
            raise ValueError("이 계정은 비공개 계정이거나 Instagram에서 접근을 제한했습니다.")
        except instaloader.exceptions.ConnectionException as e:
            if "401" in str(e):
                raise ValueError("Instagram에서 접근을 거부했습니다. 잠시 후 다시 시도해주세요.")
            else:
                raise ValueError("Instagram에 연결할 수 없습니다. 네트워크를 확인해주세요.")
        except Exception as e:
            if "401" in str(e):
                raise ValueError("Instagram에서 접근을 거부했습니다. 현재 많은 요청으로 인해 일시적으로 제한되었을 수 있습니다.")
            else:
                raise ValueError(f"프로필 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")
    
    async def _get_profile_with_retry(self, username: str, max_retries: int = 3):
        """재시도 로직이 포함된 프로필 가져오기"""
        for attempt in range(max_retries):
            try:
                await asyncio.sleep(attempt * 2)  # 지연 시간 증가
                profile = instaloader.Profile.from_username(self.loader.context, username)
                return profile
            except Exception as e:
                if attempt == max_retries - 1:  # 마지막 시도
                    raise e
                print(f"프로필 가져오기 시도 {attempt + 1} 실패: {str(e)}")
                await asyncio.sleep(5)  # 재시도 전 5초 대기
    
    async def _analyze_posts(self, profile, limit: int = 20) -> Dict[str, Any]:
        """게시물들을 분석하여 평균 인게이지먼트를 계산합니다."""
        posts = []
        total_likes = 0
        total_comments = 0
        post_count = 0
        
        try:
            for post in profile.get_posts():
                if post_count >= limit:
                    break
                
                # 릴스가 아닌 일반 게시물만 분석
                if not post.is_video or post.typename != 'GraphVideo':
                    likes = post.likes
                    comments = post.comments
                    
                    posts.append({
                        "shortcode": post.shortcode,
                        "url": f"https://www.instagram.com/p/{post.shortcode}/",
                        "likes": likes,
                        "comments": comments,
                        "engagement": likes + comments,
                        "date": post.date.isoformat(),
                        "caption": post.caption[:100] + "..." if post.caption and len(post.caption) > 100 else post.caption
                    })
                    
                    total_likes += likes
                    total_comments += comments
                    post_count += 1
                
                # API 제한을 피하기 위한 지연 (더 긴 시간)
                await asyncio.sleep(2.0)
        
        except Exception as e:
            print(f"게시물 분석 중 오류: {str(e)}")
        
        if post_count > 0:
            avg_likes = total_likes / post_count
            avg_comments = total_comments / post_count
            avg_engagement = avg_likes + avg_comments
            
            # 인게이지먼트율 계산 (팔로워 대비)
            engagement_rate = (avg_engagement / profile.followers * 100) if profile.followers > 0 else 0
        else:
            avg_likes = avg_comments = avg_engagement = engagement_rate = 0
        
        return {
            "analyzed_posts_count": post_count,
            "average_likes": round(avg_likes, 2),
            "average_comments": round(avg_comments, 2),
            "average_engagement": round(avg_engagement, 2),
            "engagement_rate_percent": round(engagement_rate, 2),
            "recent_posts": posts[:5]  # 최신 5개 게시물만 반환
        }
    
    async def _analyze_reels(self, profile, limit: int = 10) -> Dict[str, Any]:
        """릴스들을 분석하여 평균 인게이지먼트를 계산합니다."""
        reels = []
        total_likes = 0
        total_comments = 0
        total_video_views = 0
        reels_count = 0
        
        try:
            for post in profile.get_posts():
                if reels_count >= limit:
                    break
                
                # 릴스(비디오) 게시물만 분석
                if post.is_video and post.typename == 'GraphVideo':
                    likes = post.likes
                    comments = post.comments
                    video_views = getattr(post, 'video_view_count', 0)
                    
                    reels.append({
                        "shortcode": post.shortcode,
                        "url": f"https://www.instagram.com/reel/{post.shortcode}/",
                        "likes": likes,
                        "comments": comments,
                        "video_views": video_views,
                        "engagement": likes + comments,
                        "date": post.date.isoformat(),
                        "caption": post.caption[:100] + "..." if post.caption and len(post.caption) > 100 else post.caption
                    })
                    
                    total_likes += likes
                    total_comments += comments
                    total_video_views += video_views
                    reels_count += 1
                
                # API 제한을 피하기 위한 지연 (더 긴 시간)
                await asyncio.sleep(2.0)
        
        except Exception as e:
            print(f"릴스 분석 중 오류: {str(e)}")
        
        if reels_count > 0:
            avg_likes = total_likes / reels_count
            avg_comments = total_comments / reels_count
            avg_engagement = avg_likes + avg_comments
            avg_video_views = total_video_views / reels_count
            
            # 인게이지먼트율 계산 (팔로워 대비)
            engagement_rate = (avg_engagement / profile.followers * 100) if profile.followers > 0 else 0
        else:
            avg_likes = avg_comments = avg_engagement = avg_video_views = engagement_rate = 0
        
        return {
            "analyzed_reels_count": reels_count,
            "average_likes": round(avg_likes, 2),
            "average_comments": round(avg_comments, 2),
            "average_engagement": round(avg_engagement, 2),
            "average_video_views": round(avg_video_views, 2),
            "engagement_rate_percent": round(engagement_rate, 2),
            "recent_reels": reels[:5]  # 최신 5개 릴스만 반환
        } 