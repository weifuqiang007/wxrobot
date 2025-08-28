import requests
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging

class NewsItem:
    """
    新闻条目类
    """
    
    def __init__(self, title: str, content: str = None, url: str = None, 
                 publish_time: str = None, source: str = None):
        self.title = title
        self.content = content
        self.url = url
        self.publish_time = publish_time
        self.source = source
        
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'publish_time': self.publish_time,
            'source': self.source
        }
        
class NewsService:
    """
    新闻服务类
    负责获取和格式化新闻内容
    """
    
    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key
        self.api_url = api_url
        self.logger = logging.getLogger(__name__)
        
    def get_daily_news(self, count: int = 5) -> List[NewsItem]:
        """
        获取每日新闻
        
        Args:
            count: 新闻数量
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        try:
            if self.api_key and self.api_url:
                return self._fetch_real_news(count)
            else:
                return self._get_mock_news(count)
        except Exception as e:
            self.logger.error(f"获取新闻失败: {e}")
            return self._get_mock_news(count)
            
    def _fetch_real_news(self, count: int) -> List[NewsItem]:
        """
        从真实API获取新闻
        
        Args:
            count: 新闻数量
            
        Returns:
            List[NewsItem]: 新闻列表
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            params = {
                'count': count,
                'category': 'general',
                'language': 'zh'
            }
            
            response = requests.get(self.api_url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            news_items = []
            
            # 根据实际API响应格式解析数据
            # 这里是示例格式，需要根据实际API调整
            for item in data.get('articles', []):
                news_item = NewsItem(
                    title=item.get('title', ''),
                    content=item.get('description', ''),
                    url=item.get('url', ''),
                    publish_time=item.get('publishedAt', ''),
                    source=item.get('source', {}).get('name', '')
                )
                news_items.append(news_item)
                
            return news_items[:count]
            
        except Exception as e:
            self.logger.error(f"从API获取新闻失败: {e}")
            return self._get_mock_news(count)
            
    def _get_mock_news(self, count: int) -> List[NewsItem]:
        """
        获取模拟新闻数据
        
        Args:
            count: 新闻数量
            
        Returns:
            List[NewsItem]: 模拟新闻列表
        """
        mock_news = [
            NewsItem(
                title="科技创新推动经济发展",
                content="最新研究显示，科技创新正在成为推动经济发展的重要引擎...",
                source="科技日报"
            ),
            NewsItem(
                title="环保政策取得显著成效",
                content="近年来实施的环保政策在改善环境质量方面取得了显著成效...",
                source="环境报"
            ),
            NewsItem(
                title="教育改革持续深化",
                content="教育部门持续推进教育改革，提高教育质量和公平性...",
                source="教育新闻"
            ),
            NewsItem(
                title="医疗健康服务不断完善",
                content="医疗健康服务体系不断完善，为民众提供更好的医疗保障...",
                source="健康报"
            ),
            NewsItem(
                title="文化产业蓬勃发展",
                content="文化产业在数字化转型中展现出强劲的发展势头...",
                source="文化日报"
            ),
            NewsItem(
                title="交通基础设施建设加速",
                content="全国交通基础设施建设进入快车道，便民出行...",
                source="交通报"
            )
        ]
        
        # 添加当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        for news in mock_news:
            news.publish_time = current_time
            
        return mock_news[:count]
        
    def format_news_for_wechat(self, news_list: List[NewsItem]) -> str:
        """
        将新闻格式化为微信消息格式
        
        Args:
            news_list: 新闻列表
            
        Returns:
            str: 格式化后的新闻内容
        """
        if not news_list:
            return "暂无新闻内容"
            
        today = datetime.now().strftime("%Y年%m月%d日")
        formatted_news = f"📰 {today} 每日新闻\n\n"
        
        for i, news in enumerate(news_list, 1):
            formatted_news += f"{i}. {news.title}\n"
            if news.content:
                # 截取内容前50个字符
                content_preview = news.content[:50] + "..." if len(news.content) > 50 else news.content
                formatted_news += f"   {content_preview}\n"
            if news.source:
                formatted_news += f"   来源：{news.source}\n"
            formatted_news += "\n"
            
        formatted_news += "祝大家有美好的一天！ 🌞"
        
        return formatted_news
        
    def get_weather_info(self, city: str = "北京") -> str:
        """
        获取天气信息（模拟）
        
        Args:
            city: 城市名称
            
        Returns:
            str: 天气信息
        """
        # 这里可以接入真实的天气API
        # 目前返回模拟数据
        weather_templates = [
            f"{city}今日天气：晴朗，气温18-25℃，微风，适宜出行",
            f"{city}今日天气：多云，气温15-22℃，东南风，注意保暖",
            f"{city}今日天气：小雨，气温12-18℃，请携带雨具",
            f"{city}今日天气：阴天，气温16-23℃，湿度较高"
        ]
        
        import random
        return random.choice(weather_templates)
        
    def get_daily_tip(self) -> str:
        """
        获取每日小贴士
        
        Returns:
            str: 每日小贴士
        """
        tips = [
            "💡 每日提醒：多喝水，保持身体健康",
            "💡 健康贴士：适量运动，增强免疫力",
            "💡 生活提醒：早睡早起，规律作息",
            "💡 工作建议：劳逸结合，提高效率",
            "💡 饮食提醒：均衡营养，少油少盐",
            "💡 心理健康：保持乐观，积极面对生活"
        ]
        
        import random
        return random.choice(tips)
        
    def create_comprehensive_daily_message(self, city: str = "北京", news_count: int = 3) -> str:
        """
        创建综合的每日消息
        
        Args:
            city: 城市名称
            news_count: 新闻数量
            
        Returns:
            str: 综合每日消息
        """
        try:
            # 获取新闻
            news_list = self.get_daily_news(news_count)
            news_content = self.format_news_for_wechat(news_list)
            
            # 获取天气
            weather_info = self.get_weather_info(city)
            
            # 获取每日贴士
            daily_tip = self.get_daily_tip()
            
            # 组合消息
            comprehensive_message = f"""{news_content}

🌤️ {weather_info}

{daily_tip}

祝大家工作顺利，生活愉快！"""
            
            return comprehensive_message
            
        except Exception as e:
            self.logger.error(f"创建综合消息失败: {e}")
            return self._get_fallback_message()
            
    def _get_fallback_message(self) -> str:
        """
        获取备用消息
        
        Returns:
            str: 备用消息
        """
        today = datetime.now().strftime("%Y年%m月%d日")
        return f"""
📰 {today} 每日问候

🌞 新的一天开始了！
💪 愿大家工作顺利，身体健康！
🎯 保持积极的心态，迎接美好的一天！

温馨提醒：多喝水，适量运动，注意休息。
        """.strip()