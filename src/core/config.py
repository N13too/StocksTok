"""
設定管理モジュール
"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseSettings

class Config(BaseSettings):
    """アプリケーション設定"""
    
    # データベース設定
    database_url: str = "sqlite:///data/stocks_tok.db"
    
    # ログ設定
    log_level: str = "INFO"
    log_file: str = "logs/stocks_tok.log"
    
    # API設定
    api_timeout: int = 30
    api_retry_count: int = 3
    
    # キャッシュ設定
    cache_expiry: int = 3600  # 1時間
    
    # 分析設定
    fundamental_weight: float = 0.4
    technical_weight: float = 0.35
    news_weight: float = 0.25
    top_picks_count: int = 10
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# グローバル設定インスタンス
config = Config() 