import os
import datetime

# 基础配置
class Config:
    TODAY = datetime.datetime.today().strftime('%Y-%m-%d')+' auto'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # 文件存储路径
    DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads', TODAY)
    LINK_FOLDER = os.path.join(BASE_DIR, 'links', TODAY)
    COPYDST_FOLDER = r'\\Synology\home\sync od\dy-fastnas\\'+TODAY
    DATA_FILE = os.path.join(BASE_DIR, 'data.json')
    
    # Flask配置
    DEBUG = True
    PORT = 9090
    HOST = '0.0.0.0'
    
    @staticmethod
    def init_app():
        """初始化应用配置"""
        os.makedirs(Config.DOWNLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.LINK_FOLDER, exist_ok=True)