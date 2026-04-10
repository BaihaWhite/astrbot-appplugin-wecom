#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信平台适配器插件主文件
"""

# 插件主文件，仅用于标识插件入口
# AstrBot会自动加载plugins目录下的插件

__all__ = ['plugin']

# 注意：平台适配器不需要导出插件实例
# 平台适配器会通过 register_platform_adapter 装饰器自动注册