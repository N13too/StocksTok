"""
設定モジュールのテスト
"""

import pytest
from src.core.config import Config

def test_config_default_values():
    """設定のデフォルト値テスト"""
    config = Config()
    
    assert config.database_url == "sqlite:///data/stocks_tok.db"
    assert config.log_level == "INFO"
    assert config.api_timeout == 30
    assert config.fundamental_weight == 0.4
    assert config.technical_weight == 0.35
    assert config.news_weight == 0.25
    assert config.top_picks_count == 10

def test_config_weight_sum():
    """重みの合計が1.0になることを確認"""
    config = Config()
    
    total_weight = (
        config.fundamental_weight + 
        config.technical_weight + 
        config.news_weight
    )
    
    assert abs(total_weight - 1.0) < 0.001

def test_config_validation():
    """設定値の妥当性テスト"""
    config = Config()
    
    # 重みが0以上1以下であることを確認
    assert 0.0 <= config.fundamental_weight <= 1.0
    assert 0.0 <= config.technical_weight <= 1.0
    assert 0.0 <= config.news_weight <= 1.0
    
    # タイムアウトが正の値であることを確認
    assert config.api_timeout > 0
    
    # ピック数が正の値であることを確認
    assert config.top_picks_count > 0 