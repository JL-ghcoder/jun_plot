# JunPlot: 我的科研绘图Matplotlib增强库

作为Matplotlib的二次封装库，用于简化Matplotlib的繁琐配置和美化图表的默认样式，以实现风格与尺寸的统一。

## 快速开始

### 基础用法

```python
import numpy as np
import matplotlib.pyplot as plt
from junplot import JunPlot

# 创建JunPlot实例
jp = JunPlot()

# 设置中文字体路径（Windows示例）
jp.set_font_paths(
    regular_path="C:/Windows/Fonts/msyh.ttc",  # 微软雅黑常规字体
    bold_path="C:/Windows/Fonts/msyhbd.ttc"    # 微软雅黑粗体
)

# 创建图表
fig, ax = jp.create_figure()

# 绘制数据
x = np.linspace(0, 10, 100)
y = np.sin(x)
ax.plot(x, y)

# 设置中文标题和标签
jp.set_title(ax, "正弦波图表")
jp.set_xlabel(ax, "时间 (秒)")
jp.set_ylabel(ax, "振幅")

# 添加网格线
ax.grid(True, alpha=0.3)

# 移除上边框和右边框
jp.format_spines(ax)

# 显示图表
plt.tight_layout()
plt.show()
```

### 使用预设样式

```python
# 使用预设的"normal"样式
jp = JunPlot(style="normal")

# 或在创建后加载样式
jp = JunPlot()
jp = load_style("presentation")
```

## API参考

### 核心类: `JunPlot`

```python
JunPlot(
    figsize=(7, 5),             # 图表大小
    font_config=None,           # 字体配置
    padding_config=None,        # 内边距配置
    color_palette=None,         # 颜色配置
    font_paths=None,            # 字体路径
    config_file=None,           # 配置文件
    style=None                  # 预设样式
)
```

#### 主要方法

| 方法 | 描述 |
|------|------|
| `set_font_paths(regular_path, bold_path)` | 设置字体文件路径 |
| `create_figure(figsize=None, dpi=100)` | 创建新图表 |
| `set_title(ax, title, **kwargs)` | 设置标题 |
| `set_xlabel(ax, label, **kwargs)` | 设置x轴标签 |
| `set_ylabel(ax, label, **kwargs)` | 设置y轴标签 |
| `set_legend(ax, **kwargs)` | 设置图例 |
| `format_spines(ax, top=False, right=False)` | 格式化坐标轴边框 |
| `set_tick_params(ax, **kwargs)` | 设置刻度参数 |
| `set_grid(ax, visible=True, alpha=0.3)` | 设置网格线 |
| `save_config(filepath)` | 保存当前配置 |
| `save_as_style(style_name)` | 将当前配置保存为预设样式 |

### 辅助函数

| 函数 | 描述 |
|------|------|
| `load_style(style_name)` | 加载预设样式并返回JunPlot实例 |
| `list_fonts()` | 列出系统中可用的字体 |
| `styles.list_styles()` | 列出可用的预设样式 |

## 配置文件格式

JunPlot支持通过YAML配置文件定制样式。配置文件示例：

```yaml
# 图表基本尺寸
figsize: [7, 5]  # 图表大小 [宽, 高]，单位为英寸

# 字体配置（元素细分）
font_config:
  # 标题字体设置
  title:
    size: 14  # 标题字体大小
    weight: bold  # 字体粗细: normal, bold
  
  # X轴标签字体设置
  xlabel:
    size: 12
    weight: normal
  
  # Y轴标签字体设置
  ylabel:
    size: 12
    weight: normal
  
  # 图例字体设置
  legend:
    size: 10
    weight: normal
  
  # 刻度标签字体设置
  ticks:
    size: 10
    weight: normal
  
  # 默认字体设置（用于未特别指定的元素）
  default:
    size: 12
    weight: normal

# 内边距配置（元素细分）
padding_config:
  title: 12  # 标题内边距
  xlabel: 10  # X轴标签内边距
  ylabel: 10  # Y轴标签内边距
  legend: 5  # 图例内边距

# 字体文件路径 - 根据自己的系统调整
font_paths:
  regular: "C:/Windows/Fonts/msyh.ttc"  # 常规字体路径
  bold: "C:/Windows/Fonts/msyhbd.ttc"  # 粗体字体路径

# 颜色配置，用于颜色循环
color_palette:
  - "#1f77b4"  # 蓝色
  - "#ff7f0e"  # 橙色
  - "#2ca02c"  # 绿色
  - "#d62728"  # 红色
  - "#9467bd"  # 紫色
  - "#8c564b"  # 棕色
  - "#e377c2"  # 粉色
  - "#7f7f7f"  # 灰色
```