import os
import platform
import subprocess

def check_requirements():
    """检查并安装必要的依赖"""
    try:
        import PyInstaller
    except ImportError:
        print('正在安装 PyInstaller...')
        subprocess.check_call(['pip', 'install', 'pyinstaller'])

def create_icon():
    """创建应用图标"""
    if not os.path.exists('resources/icon.ico'):
        print('警告: 未找到图标文件 icon.ico，将使用默认图标')

def build():
    """执行打包操作"""
    # 检查依赖
    check_requirements()
    create_icon()
    
    # 获取当前操作系统
    system = platform.system().lower()
    
    # 基本打包命令
    cmd = [
        'pyinstaller',
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认覆盖
        'build.spec'  # 使用配置文件
    ]
    
    # 根据操作系统添加特定选项
    if system == 'darwin':  # macOS系统
        cmd.extend([
            '--codesign-identity', '-'  # 使用临时签名
        ])
    
    # 执行打包
    print(f'开始为 {system} 平台打包...')
    try:
        subprocess.check_call(cmd)
        print('打包完成！')
        
        # 输出文件位置
        dist_dir = os.path.join(os.getcwd(), 'dist')
        if system == 'windows':
            exe_path = os.path.join(dist_dir, '小游戏集合.exe')
        elif system == 'darwin':
            exe_path = os.path.join(dist_dir, '小游戏集合.app')
        else:
            exe_path = os.path.join(dist_dir, '小游戏集合')
            
        if os.path.exists(exe_path):
            print(f'可执行文件已生成: {exe_path}')
        else:
            print('警告: 未找到生成的可执行文件')
            
    except subprocess.CalledProcessError as e:
        print(f'打包失败: {str(e)}')
        return

if __name__ == '__main__':
    build()