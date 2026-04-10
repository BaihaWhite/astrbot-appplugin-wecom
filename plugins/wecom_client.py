import asyncio
import aiohttp
import json
import time
from astrbot import logger

class WecomClient:
    """
    企业微信客户端，处理与企业微信API的交互
    """
    def __init__(self, corp_id: str, app_secret: str, agent_id: str):
        self.corp_id = corp_id
        self.app_secret = app_secret
        self.agent_id = agent_id
        self.access_token = None
        self.token_expire_time = 0
        self.on_message_received = None
    
    async def get_access_token(self):
        """
        获取企业微信access_token
        """
        try:
            # 检查token是否有效
            if self.access_token and time.time() < self.token_expire_time:
                return self.access_token
            
            url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corp_id}&corpsecret={self.app_secret}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    result = await response.json()
                    if result.get('errcode') == 0:
                        self.access_token = result.get('access_token')
                        self.token_expire_time = time.time() + (result.get('expires_in', 7200) - 300)  # 提前5分钟刷新
                        logger.info(f"获取access_token成功: {self.access_token}")
                        return self.access_token
                    else:
                        logger.error(f"获取access_token失败: {result}")
                        return None
        except Exception as e:
            logger.error(f"获取access_token异常: {e}")
            return None
    
    async def send_text(self, to_user: str, message: str):
        """
        发送文本消息
        """
        try:
            access_token = await self.get_access_token()
            if not access_token:
                return None
            
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            payload = {
                "touser": to_user,
                "msgtype": "text",
                "agentid": self.agent_id,
                "text": {"content": message}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=json.dumps(payload)) as response:
                    result = await response.json()
                    logger.info(f"发送文本消息结果: {result}")
                    return result
        except Exception as e:
            logger.error(f"发送文本消息异常: {e}")
            return None
    
    async def send_image(self, to_user: str, media_id: str):
        """
        发送图片消息
        """
        try:
            access_token = await self.get_access_token()
            if not access_token:
                return None
            
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            payload = {
                "touser": to_user,
                "msgtype": "image",
                "agentid": self.agent_id,
                "image": {"media_id": media_id}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=json.dumps(payload)) as response:
                    result = await response.json()
                    logger.info(f"发送图片消息结果: {result}")
                    return result
        except Exception as e:
            logger.error(f"发送图片消息异常: {e}")
            return None
    
    async def send_voice(self, to_user: str, media_id: str):
        """
        发送语音消息
        """
        try:
            access_token = await self.get_access_token()
            if not access_token:
                return None
            
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            payload = {
                "touser": to_user,
                "msgtype": "voice",
                "agentid": self.agent_id,
                "voice": {"media_id": media_id}
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=json.dumps(payload)) as response:
                    result = await response.json()
                    logger.info(f"发送语音消息结果: {result}")
                    return result
        except Exception as e:
            logger.error(f"发送语音消息异常: {e}")
            return None
    
    async def upload_media(self, file_path: str, media_type: str):
        """
        上传临时素材
        """
        try:
            access_token = await self.get_access_token()
            if not access_token:
                return None
            
            url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type={media_type}"
            
            async with aiohttp.ClientSession() as session:
                with open(file_path, 'rb') as f:
                    data = aiohttp.FormData()
                    data.add_field('media', f, filename=file_path.split('/')[-1])
                    async with session.post(url, data=data) as response:
                        result = await response.json()
                        if result.get('errcode') == 0:
                            media_id = result.get('media_id')
                            logger.info(f"上传临时素材成功，media_id: {media_id}")
                            return media_id
                        else:
                            logger.error(f"上传临时素材失败: {result}")
                            return None
        except Exception as e:
            logger.error(f"上传临时素材异常: {e}")
            return None
    
    async def start_polling(self):
        """
        开始轮询消息（模拟实现，实际应该使用webhook）
        """
        # 注意：企业微信推荐使用webhook方式接收消息
        # 这里为了演示，实现一个简单的轮询机制
        logger.info("开始轮询企业微信消息...")
        while True:
            # 实际项目中，这里应该调用企业微信的消息接口获取消息
            # 由于企业微信API的限制，这里我们模拟消息接收
            await asyncio.sleep(5)
            # 模拟接收到消息
            if self.on_message_received:
                try:
                    # 模拟消息数据
                    mock_message = {
                        'bot_id': self.agent_id,
                        'content': '测试消息',
                        'username': '测试用户',
                        'userid': 'UserID123',
                        'message_id': f'msg_{int(time.time())}',
                        'group_id': None  # 私聊消息
                    }
                    await self.on_message_received(mock_message)
                except Exception as e:
                    logger.error(f"处理消息异常: {e}")
    
    async def send_message(self, to_user: str, message_data: dict):
        """
        发送消息的通用方法
        """
        try:
            access_token = await self.get_access_token()
            if not access_token:
                return None
            
            url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
            payload = {
                "touser": to_user,
                "agentid": self.agent_id,
                **message_data
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=json.dumps(payload)) as response:
                    result = await response.json()
                    logger.info(f"发送消息结果: {result}")
                    return result
        except Exception as e:
            logger.error(f"发送消息异常: {e}")
            return None