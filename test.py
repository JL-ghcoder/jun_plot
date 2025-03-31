import numpy as np
import matplotlib.pyplot as plt
from junplot import JunPlot, load_style, list_fonts

# list_fonts()

# jp = JunPlot(config_file="normal.yaml")
jp = JunPlot(style="normal")  

jp.set_font_paths(
    regular_path="C:/Windows/Fonts/msyh.ttc",
    bold_path="C:/Windows/Fonts/msyhbd.ttc"
)

# 生成数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.exp(-0.2*x) * np.sin(x)

# 创建图表
fig, ax = jp.create_figure()

# 绘制线条
ax.plot(x, y1, label=r'$\sin(x)$')
ax.plot(x, y2, label=r'$\cos(x)$')
ax.plot(x, y3, label=r'$e^{-0.2x}\sin(x)$')

# 设置标题和标签
#jp.set_title(ax, 'Simple Line Plot')
jp.set_title(ax, '中文线图测试')

#jp.set_xlabel(ax, 'x')
jp.set_xlabel(ax, 'x坐标')
#jp.set_ylabel(ax, 'y')
jp.set_ylabel(ax, 'y坐标')

# 设置刻度参数
jp.set_tick_params(ax)

# 添加图例
jp.set_legend(ax, loc='best')

# 添加网格线
ax.grid(True, alpha=0.3)

# 移除上边框和右边框
jp.format_spines(ax)

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()