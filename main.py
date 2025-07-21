"""
StocksTok - 株価スイングトレード分析ツール
メインエントリーポイント
"""

import sys
import logging
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.config import Config
from src.ui.main import run_streamlit_app

def main():
    """メイン関数"""
    try:
        # 設定読み込み
        config = Config()
        
        # ログ設定
        logging.basicConfig(
            level=config.log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/stocks_tok.log'),
                logging.StreamHandler()
            ]
        )
        
        # Streamlitアプリケーション起動
        run_streamlit_app()
        
    except Exception as e:
        logging.error(f"アプリケーション起動エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 