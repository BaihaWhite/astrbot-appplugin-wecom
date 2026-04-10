import asyncio
from astrbot.api.platform import Platform, AstrBotMessage, MessageMember, PlatformMetadata, MessageType
from astrbot.api.event import MessageChain
from astrbot.api.message_components import Plain, Image, Record
from astrbot.core.platform.astr_message_event import MessageSesion
from astrbot.api.platform import register_platform_adapter
from astrbot import logger
from .wecom_client import WecomClient
from .wecom_platform_event import WecomPlatformEvent

# 注册平台适配器
@register_platform_adapter("wecom", "企业微信适配器", default_config_tmpl={
    "corp_id": "your_corp_id",
    "app_secret": "your_app_secret",
    "agent_id": "your_agent_id"
})
class WecomPlatformAdapter(Platform):
    
    def __init__(self, platform_config: dict, platform_settings: dict, event_queue: asyncio.Queue) -> None:
        super().__init__(event_queue)
        self.config = platform_config
        self.settings = platform_settings
        self.client = None
        self.access_token = None
    
    async def send_by_session(self, session: MessageSesion, message_chain: MessageChain):
        """
        通过会话发送消息
        """
        await super().send_by_session(session, message_chain)
        # 实现发送逻辑
        pass
    
    def meta(self) -> PlatformMetadata:
        """
        返回平台元数据
        """
        return PlatformMetadata(
            "wecom",
            "企业微信适配器",
        )
    
    async def run(self):
        """
        运行平台适配器
        """
        # 初始化企业微信客户端
        self.client = WecomClient(
            corp_id=self.config['corp_id'],
            app_secret=self.config['app_secret'],
            agent_id=self.config['agent_id']
        )
        
        # 设置消息接收回调
        async def on_received(data):
            logger.info(f"收到企业微信消息: {data}")
            abm = await self.convert_message(data=data)
            await self.handle_msg(abm)
        
        self.client.on_message_received = on_received
        
        # 保存 access_token 引用
        self.access_token = lambda: self.client.get_access_token()
        
        # 开始轮询消息
        await self.client.start_polling()
    
    async def convert_message(self, data: dict) -> AstrBotMessage:
        """
        将企业微信消息转换为 AstrBotMessage
        """
        abm = AstrBotMessage()
        
        # 消息类型
        if data.get('group_id'):
            abm.type = MessageType.GROUP_MESSAGE
            abm.group_id = data['group_id']
        else:
            abm.type = MessageType.FRIEND_MESSAGE
        
        # 消息内容
        abm.message_str = data.get('content', '')
        
        # 发送者信息
        abm.sender = MessageMember(
            user_id=data.get('userid', ''),
            nickname=data.get('username', '')
        )
        
        # 消息链
        abm.message = [Plain(text=abm.message_str)]
        
        # 原始消息
        abm.raw_message = data
        
        # 机器人 ID
        abm.self_id = data.get('bot_id', self.config.get('agent_id', ''))
        
        # 会话 ID
        abm.session_id = data.get('userid', '')
        
        # 消息 ID
        abm.message_id = data.get('message_id', '')
        
        return abm
    
    async def handle_msg(self, message: AstrBotMessage):
        """
        处理消息
        """
        message_event = WecomPlatformEvent(
            message_str=message.message_str,
            message_obj=message,
            platform_meta=self.meta(),
            session_id=message.session_id,
            client=self.client
        )
        self.commit_event(message_event)
    
    async def send_message(self, event, message_data):
        """
        发送消息的辅助方法
        """
        if hasattr(event, 'client') and event.client:
            return await event.client.send_message(event.session_id, message_data)
        elif self.client:
            return await self.client.send_message(event.session_id, message_data)
        return None