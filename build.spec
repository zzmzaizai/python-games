# -*- mode: python ; coding: utf-8 -*-

# PyInstaller打包配置文件
# 用于将Python项目打包成可执行文件

# 定义加密密钥，这里不使用加密
block_cipher = None

# Analysis类用于分析项目依赖
# 收集所有需要打包的Python模块和数据文件
a = Analysis(
    ['main.py'],              # 主脚本文件
    pathex=[],                # 额外的导入路径
    binaries=[],              # 需要包含的二进制文件
    datas=[("resources/icon.ico", "resources")],  # 需要包含的数据文件
    hiddenimports=['pygame'], # 隐式导入的模块
    hookspath=[],             # 自定义钩子脚本路径
    hooksconfig={},           # 钩子配置
    runtime_hooks=[],         # 运行时钩子
    excludes=[],              # 排除的模块
    win_no_prefer_redirects=False,    # Windows特定选项
    win_private_assemblies=False,     # Windows特定选项
    cipher=block_cipher,             # 加密设置
    noarchive=False,                 # 是否不打包成zip文件
    target_arch='universal2'         # macOS通用二进制支持
)

# 创建PYZ归档文件，包含所有Python模块
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 创建可执行文件
exe = EXE(
    pyz,                            # PYZ归档
    a.scripts,                       # 脚本
    a.binaries,                      # 二进制文件
    a.zipfiles,                      # zip文件
    a.datas,                         # 数据文件
    [],                              # 额外选项
    name='Python Game Collection',   # 输出文件名
    debug=False,                     # 是否开启调试
    bootloader_ignore_signals=False,  # 是否忽略引导加载器信号
    strip=False,                     # 是否剥离符号表
    upx=True,                        # 是否使用UPX压缩
    upx_exclude=[],                  # UPX排除项
    runtime_tmpdir=None,             # 运行时临时目录
    console=False,                   # 是否显示控制台窗口
    disable_windowed_traceback=False, # 是否禁用窗口化追踪
    argv_emulation=False,            # 是否模拟命令行参数
    target_arch=None,                # 目标架构，让PyInstaller自动检测
    codesign_identity=None,          # 代码签名身份
    entitlements_file=None,          # 授权文件
    icon='resources/icon.ico',        # 应用程序图标
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleIdentifier': 'com.minigames.collection',
        'CFBundleName': 'Python Game Collection',
        'CFBundleDisplayName': 'Python Game Collection',
        'CFBundlePackageType': 'APPL',
        'LSMinimumSystemVersion': '10.13'
    }                               # macOS应用信息
)
