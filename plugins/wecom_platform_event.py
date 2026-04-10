from astrbot.api.event import AstrMessageEvent, MessageChain
from astrbot.api.platform import AstrBotMessage, PlatformMe

class WecomPlatformEvent(AstrMessageEvent):
    """
    企业微信平台事件类
    """
    def __init__(self, message_str: str, message_obj: AstrBotMessage, platform_meta, session_id: str, client):
        super().__init__(
            message_str=message_str,
            message_obj=message_obj,
            platform_meta=platform_meta,
            session_id=session_id
        )
        self.client = client  # 企业微信客户端实例
    
    async def reply(self, message_chain: MessageChain):
        """
        回复消息
        """
        # 实现回复逻辑
        pass
    
    async def reply_text(self, text: str):
        """
        回复文本消息
        """
        try:
            result = await self.client.send_text(self.session_id, text)
            return result
        except Exception as e:
            self.logger.error(f"回复文本消息异常: {e}")
            return None
    
    async def reply_image(self, media_id: str):
        """
        回复图片消息
        """
        try:
            result = await self.client.send_image(self.session_id, media_id)
            return result
        except Exception as e:
            self.logger.error(f"回复图片消息异常: {e}")
            return None
    
    async def reply_voice(self, media_id: str):
        """
        回复语音消息
        """
        try:
            result = await self.client.send_voice(self.session_id, media_id)
            return result
        except Exception as e:
            self.logger.error(f"回复语音消息异常: {e}")
            return None
    
    async def reply_message(self, message_data: dict):
        """
        回复消息的通用方法
        """
        try:
            result = await self.client.send_message(self.session_id, message_data)
            return result
        except Exception as e:
            self.logger.error(f"回复消息异常: {e}")
            return None