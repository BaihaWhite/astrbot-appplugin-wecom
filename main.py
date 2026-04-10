#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信平台适配器插件主文件
"""

from astrbot.core import Plugin

# 插件主文件，用于标识插件入口
# AstrBot会自动加载plugins目录下的插件

class WecomPlatformPlugin(Plugin):
    """
    企业微信平台适配器插件
    """
    def __init__(self):
        super().__init__(name="wecom-platform", description="企业微信平台适配器")

# 导出插件实例
plugin = WecomPlatformPlugin()

__all__ = ['plugin']