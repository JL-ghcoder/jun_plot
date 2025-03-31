import matplotlib.font_manager as fm

def list_fonts():
    # 列出所有字体文件
    print("Available fonts:")
    font_files = fm.findSystemFonts()
    for font in font_files:
        print(font)

    # 或者获取字体名称
    print("\nAvailable font names:")
    font_names = [fm.FontProperties(fname=fname).get_name() for fname in font_files]
    unique_names = sorted(set(font_names))
    for name in unique_names:
        print(name)