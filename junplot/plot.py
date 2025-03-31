"""
junplot.plot 模块
===========================
支持为图表的各个元素（标题、图例、坐标轴标签等）分别设置字体和大小
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from cycler import cycler
import os
import yaml
import platform
from typing import Dict, List, Tuple, Optional, Any

# 定义包路径及样式文件夹
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(PACKAGE_DIR, 'config')

if not os.path.exists(CONFIG_DIR):
    os.makedirs(CONFIG_DIR)

# 常见字体路径映射
COMMON_FONT_PATHS = {
    'Windows': {
        'regular': 'C:\\Windows\\Fonts\\arial.ttf',
        'bold': 'C:\\Windows\\Fonts\\arialbd.ttf',
    },
    'Darwin': {  # macOS
        'regular': '/System/Library/Fonts/Supplemental/Arial.ttf',
        'bold': '/System/Library/Fonts/Supplemental/Arial Bold.ttf',
    },
    'Linux': {
        'regular': '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf',
        'bold': '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf',
    }
}

class JunPlot:
    """可定制各元素的绘图库"""
    
    def __init__(self, 
                 figsize: Tuple[float, float] = (5, 4),
                 font_config: Optional[Dict[str, Any]] = None,
                 padding_config: Optional[Dict[str, int]] = None,
                 color_palette: Optional[List[str]] = None,
                 font_paths: Optional[Dict[str, str]] = None,
                 config_file: Optional[str] = None,
                 style: Optional[str] = None,
                 dpi: int = 100):
        """
        初始化绘图风格
        
        参数:
        -----
        figsize: Tuple[float, float]
            图像默认大小，单位为英寸
        font_config: Optional[Dict[str, Any]]
            字体配置，包含各元素的字体大小
        padding_config: Optional[Dict[str, int]]
            内边距配置，包含各元素的内边距
        color_palette: Optional[List[str]]
            自定义颜色列表
        font_paths: Optional[Dict[str, str]]
            字体路径配置，包含regular和bold字体的路径
        config_file: Optional[str]
            YAML配置文件路径，如果提供则从文件加载配置
        style: Optional[str]
            预设样式名称，如果提供则从内置样式加载配置
        dpi: int
            图像分辨率，默认为100
        """
        # 默认配色
        default_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        # 默认字体配置
        default_font_config = {
            'title': {'size': 12, 'weight': 'bold'},
            'xlabel': {'size': 10, 'weight': 'normal'},
            'ylabel': {'size': 10, 'weight': 'normal'},
            'legend': {'size': 8, 'weight': 'normal'},
            'ticks': {'size': 8, 'weight': 'normal'},
            'default': {'size': 10, 'weight': 'normal'}
        }
        
        # 默认内边距配置
        default_padding_config = {
            'title': 10,
            'xlabel': 8,
            'ylabel': 8,
            'legend': 3
        }
        
        # 先设置默认值
        self.figsize = figsize
        self.dpi = dpi  # 保存DPI作为实例属性
        self.font_config = default_font_config.copy()
        self.padding_config = default_padding_config.copy()
        self.color_palette = color_palette if color_palette else default_colors
        self.font_paths = {}
        
        # 检测当前操作系统
        system = platform.system()
        # 获取系统默认字体路径
        if system in COMMON_FONT_PATHS:
            self.font_paths = COMMON_FONT_PATHS[system].copy()
        
        # 如果提供了字体路径，则更新
        if font_paths:
            self.font_paths.update(font_paths)
        
        # 如果提供了样式名称，则加载内置样式
        if style:
            config = self._load_style(style)
            self._update_from_config(config)
            
        # 如果提供了配置文件，则从文件加载配置
        elif config_file:
            if os.path.exists(config_file):
                print(f"从配置文件加载: {config_file}")
                config = self._load_config(config_file)
                self._update_from_config(config)
            else:
                print(f"警告: 配置文件 {config_file} 不存在!")
        
        # 如果提供了字体配置参数，则更新配置
        if font_config:
            for key, value in font_config.items():
                if key in self.font_config:
                    self.font_config[key].update(value)
        
        # 如果提供了内边距配置参数，则更新配置
        if padding_config:
            self.padding_config.update(padding_config)
        
        # 初始化字体对象
        self.fonts = {}
        self._init_fonts()
        
        # 应用全局设置
        self._setup_style()
    
    def _update_from_config(self, config: Dict):
        """从配置字典更新设置"""
        if not config:
            return
            
        # 更新配置
        if 'figsize' in config:
            self.figsize = tuple(config['figsize'])
        
        # 更新字体配置
        if 'font_config' in config:
            for key, value in config['font_config'].items():
                if key in self.font_config:
                    self.font_config[key].update(value)
        
        # 更新内边距配置
        if 'padding_config' in config:
            self.padding_config.update(config['padding_config'])
        
        # 更新颜色配置
        if 'color_palette' in config:
            self.color_palette = config['color_palette']
        
        # 更新字体路径
        if 'font_paths' in config:
            self.font_paths.update(config['font_paths'])
        
        # 更新DPI值
        if 'dpi' in config:
            self.dpi = config['dpi']
    
    def _load_config(self, config_file: str) -> Dict:
        """从YAML文件加载配置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                return config if config else {}
        except Exception as e:
            print(f"加载配置文件出错: {e}")
            return {}
    
    def _load_style(self, style_name: str) -> Dict:
        """从内置样式加载配置"""
        # 构建样式文件路径
        style_file = os.path.join(CONFIG_DIR, f"{style_name}.yaml")
        
        # 检查样式文件是否存在
        if not os.path.exists(style_file):
            print(f"警告: 样式 '{style_name}' 不存在!")
            return {}
        
        # 加载样式配置
        return self._load_config(style_file)
    
    def _init_fonts(self):
        """初始化字体对象"""
        # 获取字体路径
        regular_path = self.font_paths.get('regular')
        bold_path = self.font_paths.get('bold')
        
        # 为每个元素创建字体对象
        for element, config in self.font_config.items():
            size = config.get('size', 10)
            weight = config.get('weight', 'normal')
            
            # 根据权重选择字体路径
            font_path = bold_path if weight == 'bold' else regular_path
            
            # 创建字体对象
            if font_path and os.path.exists(font_path):
                self.fonts[element] = fm.FontProperties(fname=font_path, size=size, weight=weight)
            else:
                # 如果找不到字体文件，则使用系统默认字体
                self.fonts[element] = fm.FontProperties(family='sans-serif', size=size, weight=weight)
        
    def set_font_paths(self, regular_path: Optional[str] = None, bold_path: Optional[str] = None):
        """手动设置字体路径"""
        if regular_path and os.path.exists(regular_path):
            self.font_paths['regular'] = regular_path
        
        if bold_path and os.path.exists(bold_path):
            self.font_paths['bold'] = bold_path
        
        # 重新初始化字体对象
        self._init_fonts()
        
        # 重新应用样式
        self._setup_style()
        
        return self  # 返回自身以支持链式调用
        
    def _setup_style(self):
        """设置matplotlib全局样式"""
        # 基础设置
        plt.rcParams['figure.figsize'] = self.figsize
        plt.rcParams['figure.dpi'] = self.dpi  # 设置全局DPI
        
        # 字体设置
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
        
        # 使用默认字体配置
        default_size = self.font_config['default']['size']
        plt.rcParams['font.size'] = default_size
        
        # 颜色循环
        plt.rcParams['axes.prop_cycle'] = cycler(color=self.color_palette)
        
        # 负号显示
        plt.rcParams['axes.unicode_minus'] = False
        
    def create_figure(self, figsize=None, dpi=None):
        """
        创建一个新的图表
        
        参数:
        -----
        figsize: Optional[Tuple[float, float]]
            图表大小，如果不指定则使用默认大小
        dpi: Optional[int]
            图表DPI，如果不指定则使用默认DPI
        
        返回:
        ------
        Tuple[Figure, Axes]
            matplotlib图表和坐标轴对象
        """
        # 使用实例默认值，如果未提供参数
        if figsize is None:
            figsize = self.figsize
        if dpi is None:
            dpi = self.dpi
        
        # 保存当前rcParams
        old_rcParams = plt.rcParams.copy()
        
        # 应用DPI设置
        plt.rcParams['figure.dpi'] = dpi
        
        # 创建图表
        fig, ax = plt.subplots(figsize=figsize)
        
        # 确保新创建的图表应用正确的颜色循环
        ax.set_prop_cycle(cycler(color=self.color_palette))
        
        # 应用样式设置到轴
        self._apply_styles_to_axes(ax)
        
        # 恢复原始rcParams
        plt.rcParams.update(old_rcParams)
        
        return fig, ax
    
    def _apply_styles_to_axes(self, ax):
        """将样式设置应用到坐标轴"""
        # 这个方法可以在create_figure中使用，确保样式正确应用
        # 可以添加额外的样式设置，如网格线、刻度等
        pass
    
    def set_title(self, ax, title):
        """设置带有适当字体和内边距的标题"""
        font_props = self.fonts.get('title')
        pad = self.padding_config.get('title', 10)
        
        if font_props:
            ax.set_title(title, fontproperties=font_props, pad=pad)
        else:
            ax.set_title(title, fontsize=self.font_config['title']['size'], 
                        fontweight=self.font_config['title']['weight'], pad=pad)
    
    def set_xlabel(self, ax, label):
        """设置带有适当字体和内边距的x轴标签"""
        font_props = self.fonts.get('xlabel')
        pad = self.padding_config.get('xlabel', 8)
        
        if font_props:
            ax.set_xlabel(label, fontproperties=font_props, labelpad=pad)
        else:
            ax.set_xlabel(label, fontsize=self.font_config['xlabel']['size'], 
                         fontweight=self.font_config['xlabel']['weight'], labelpad=pad)
    
    def set_ylabel(self, ax, label):
        """设置带有适当字体和内边距的y轴标签"""
        font_props = self.fonts.get('ylabel')
        pad = self.padding_config.get('ylabel', 8)
        
        if font_props:
            ax.set_ylabel(label, fontproperties=font_props, labelpad=pad)
        else:
            ax.set_ylabel(label, fontsize=self.font_config['ylabel']['size'], 
                         fontweight=self.font_config['ylabel']['weight'], labelpad=pad)
    
    def set_legend(self, ax, **kwargs):
        """设置带有适当字体的图例"""
        font_props = self.fonts.get('legend')
        
        if 'prop' not in kwargs:
            if font_props:
                kwargs['prop'] = font_props
            else:
                kwargs['fontsize'] = self.font_config['legend']['size']
        
        ax.legend(**kwargs)
    
    def format_spines(self, ax, top=False, right=False):
        """移除上边框和右边框"""
        ax.spines['top'].set_visible(top)
        ax.spines['right'].set_visible(right)
    
    def set_tick_params(self, ax):
        """设置刻度参数"""
        font_props = self.fonts.get('ticks')
        
        if font_props:
            for label in ax.get_xticklabels():
                label.set_fontproperties(font_props)
            for label in ax.get_yticklabels():
                label.set_fontproperties(font_props)
        else:
            ax.tick_params(axis='both', which='major', 
                          labelsize=self.font_config['ticks']['size'])
    
    def export_config(self) -> Dict:
        """导出当前配置为字典"""
        config = {
            'figsize': self.figsize,
            'dpi': self.dpi,
            'font_config': self.font_config,
            'padding_config': self.padding_config,
            'color_palette': self.color_palette,
            'font_paths': self.font_paths
        }
        return config
    
    def save_config(self, filepath):
        """将配置保存为YAML文件"""
        config = self.export_config()
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            print(f"配置已保存到: {filepath}")
        except Exception as e:
            print(f"保存配置出错: {e}")

# 辅助函数，用于直接加载样式
def load_style(style_name: str) -> JunPlot:
    """
    直接加载预设样式并返回JunPlot实例
    
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