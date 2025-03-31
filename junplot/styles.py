"""
junplot.styles 模块
=================
用于管理和加载预设样式的模块
"""

import os
import yaml
from typing import Dict, List
from . import JunPlot

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(PACKAGE_DIR, 'config')

# 确保配置目录存在
if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

def load_style(style_name: str) -> JunPlot:
    """
    加载预设样式并返回JunPlot实例
    
    参数:
    -----
    style_name: str
        预设样式名称
        
    返回:
    ------
    JunPlot
        已加载样式的JunPlot实例
    """
    return JunPlot(style=style_name)

def list_styles() -> List[str]:
    """
    列出所有可用的预设样式
    
    返回:
    ------
    List[str]
        可用样式名称列表
    """
    styles = []
    
    # 遍历配置目录中的所有YAML文件
    if os.path.exists(CONFIG_DIR):
        for file in os.listdir(CONFIG_DIR):
            if file.endswith('.yaml'):
                styles.append(os.path.splitext(file)[0])
    
    return sorted(styles)

def save_style(config: Dict, style_name: str) -> str:
    """
    将配置保存为预设样式
    
    参数:
    -----
    config: Dict
        样式配置字典
    style_name: str
        样式名称
        
    返回:
    ------
    str
        样式文件路径
    """
    # 确保配置目录存在
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    # 构建样式文件路径
    style_file = os.path.join(CONFIG_DIR, f"{style_name}.yaml")
    
    # 保存配置
    try:
        with open(style_file, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print(f"样式已保存到: {style_file}")
        return style_file
    except Exception as e:
        print(f"保存样式出错: {e}")
        return ""

def get_style_path(style_name: str) -> str:
    """
    获取样式文件路径
    
    参数:
    -----
    style_name: str
        样式名称
        
    返回:
    ------
    str
        样式文件路径，如果样式不存在则返回空字符串
    """
    style_file = os.path.join(CONFIG_DIR, f"{style_name}.yaml")
    
    if os.path.exists(style_file):
        return style_file
    else:
        print(f"警告: 样式 '{style_name}' 不存在!")
        return ""