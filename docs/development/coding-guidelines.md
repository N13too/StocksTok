# コーディング規約

## 1. 基本原則

### 1.1 可読性優先
- コードは書くよりも読まれることが多い
- 明確で理解しやすいコードを書く
- 適切なコメントを記述する
- 一貫した命名規則を使用する

### 1.2 保守性重視
- モジュラー設計を心がける
- 単一責任の原則を守る
- 依存関係を最小限に保つ
- テストしやすいコードを書く

### 1.3 拡張性考慮
- 将来の機能追加を考慮した設計
- 設定による動作変更が可能な構造
- プラグイン形式での拡張を考慮
- 機械学習機能の統合を意識

## 2. Python コーディング規約

### 2.1 PEP 8準拠
- PEP 8スタイルガイドに準拠
- 4スペースインデント
- 79文字行長制限
- 適切な空行の使用

### 2.2 命名規則

#### 2.2.1 変数・関数名
```python
# 良い例
user_name = "John"
calculate_average_score()
get_stock_price()

# 悪い例
userName = "John"
CalculateAverageScore()
get_stock_price()
```

#### 2.2.2 クラス名
```python
# 良い例
class StockAnalyzer:
    pass

class FundamentalAnalysis:
    pass

# 悪い例
class stockAnalyzer:
    pass

class fundamental_analysis:
    pass
```

#### 2.2.3 定数名
```python
# 良い例
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30
API_BASE_URL = "https://api.example.com"

# 悪い例
maxRetryCount = 3
default_timeout = 30
apiBaseUrl = "https://api.example.com"
```

### 2.3 インポート規則
```python
# 標準ライブラリ
import os
import sys
from datetime import datetime, date
from typing import List, Dict, Optional

# サードパーティライブラリ
import pandas as pd
import numpy as np
import requests
from fastapi import FastAPI
import streamlit as st

# ローカルモジュール
from src.core.config import Config
from src.data.models import Company, StockPrice
from src.analysis.fundamental import FundamentalAnalyzer
```

## 3. プロジェクト固有規約

### 3.1 ディレクトリ構造
```
src/
├── api/                    # FastAPI関連
│   ├── __init__.py
│   ├── main.py
│   ├── models.py          # Pydanticモデル
│   ├── routes/            # ルート定義
│   └── middleware.py      # ミドルウェア
├── core/                  # コア機能
│   ├── __init__.py
│   ├── config.py         # 設定管理
│   ├── exceptions.py     # カスタム例外
│   └── logging.py        # ログ設定
├── data/                  # データアクセス
│   ├── __init__.py
│   ├── models.py         # データモデル
│   ├── repositories.py   # Repositoryクラス
│   └── database.py       # DB接続
├── analysis/              # 分析エンジン
│   ├── __init__.py
│   ├── fundamental.py    # ファンダメンタルズ分析
│   ├── technical.py      # テクニカル分析
│   ├── news.py          # ニュース分析
│   └── evaluator.py     # 総合評価
├── ui/                    # Streamlit UI
│   ├── __init__.py
│   ├── main.py          # メインUI
│   ├── components/      # UIコンポーネント
│   └── pages/           # ページ定義
└── utils/                 # ユーティリティ
    ├── __init__.py
    ├── helpers.py       # ヘルパー関数
    └── validators.py    # バリデーション
```

### 3.2 ファイル命名規則
- **Pythonファイル**: スネークケース (`stock_analyzer.py`)
- **クラスファイル**: パスカルケース (`StockAnalyzer`)
- **設定ファイル**: スネークケース (`config.yaml`)
- **テストファイル**: `test_` プレフィックス (`test_stock_analyzer.py`)

### 3.3 モジュール構造
```python
"""
株価分析エンジン

このモジュールは、株価データの分析機能を提供します。
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, date

from src.core.config import Config
from src.data.models import Company, StockPrice
from src.core.exceptions import AnalysisError

logger = logging.getLogger(__name__)

class StockAnalyzer:
    """
    株価分析エンジン
    
    株価データを分析し、投資判断に必要な情報を提供します。
    """
    
    def __init__(self, config: Config):
        """
        初期化
        
        Args:
            config: 設定オブジェクト
        """
        self.config = config
        self.logger = logging.getLogger(__name__)
    
    def analyze_company(self, company: Company) -> Dict:
        """
        企業の分析を実行
        
        Args:
            company: 分析対象企業
            
        Returns:
            分析結果辞書
            
        Raises:
            AnalysisError: 分析中にエラーが発生した場合
        """
        try:
            # 実装
            pass
        except Exception as e:
            self.logger.error(f"分析中にエラーが発生: {e}")
            raise AnalysisError(f"企業 {company.code} の分析に失敗: {e}")
```

## 4. データベース関連規約

### 4.1 モデル定義
```python
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

@dataclass
class Company:
    """企業情報モデル"""
    
    id: Optional[int]
    code: str
    name: str
    sector: Optional[str]
    market: Optional[str]
    listing_date: Optional[date]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """バリデーション"""
        if not self.code:
            raise ValueError("証券コードは必須です")
        if not self.name:
            raise ValueError("企業名は必須です")
```

### 4.2 Repository パターン
```python
from abc import ABC, abstractmethod
from typing import List, Optional
from src.data.models import Company

class CompanyRepository(ABC):
    """企業情報リポジトリの抽象クラス"""
    
    @abstractmethod
    def find_by_code(self, code: str) -> Optional[Company]:
        """証券コードで企業を検索"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Company]:
        """全企業を取得"""
        pass
    
    @abstractmethod
    def save(self, company: Company) -> Company:
        """企業情報を保存"""
        pass

class SQLiteCompanyRepository(CompanyRepository):
    """SQLite用企業情報リポジトリ"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def find_by_code(self, code: str) -> Optional[Company]:
        # 実装
        pass
```

## 5. API関連規約

### 5.1 Pydanticモデル
```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class AnalysisRequest(BaseModel):
    """分析リクエストモデル"""
    
    force_refresh: bool = Field(default=False, description="強制更新フラグ")
    target_companies: Optional[List[str]] = Field(
        default=None, 
        description="分析対象企業コードリスト"
    )
    analysis_options: dict = Field(
        default_factory=dict,
        description="分析オプション"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "force_refresh": False,
                "target_companies": ["7203", "6758"],
                "analysis_options": {
                    "include_fundamental": True,
                    "include_technical": True,
                    "include_news": True
                }
            }
        }

class AnalysisResponse(BaseModel):
    """分析レスポンスモデル"""
    
    success: bool
    data: dict
    message: str
    timestamp: str
```

### 5.2 エンドポイント定義
```python
from fastapi import APIRouter, HTTPException, Depends
from src.api.models import AnalysisRequest, AnalysisResponse
from src.core.exceptions import AnalysisError

router = APIRouter(prefix="/api/v1", tags=["analysis"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_stocks(
    request: AnalysisRequest,
    analyzer: StockAnalyzer = Depends(get_analyzer)
) -> AnalysisResponse:
    """
    株価分析を実行
    
    Args:
        request: 分析リクエスト
        analyzer: 分析エンジン
        
    Returns:
        分析結果
        
    Raises:
        HTTPException: 分析に失敗した場合
    """
    try:
        result = await analyzer.analyze(request)
        return AnalysisResponse(
            success=True,
            data=result,
            message="分析が正常に完了しました",
            timestamp=datetime.now().isoformat()
        )
    except AnalysisError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        raise HTTPException(status_code=500, detail="内部サーバーエラー")
```

## 6. エラーハンドリング規約

### 6.1 カスタム例外
```python
class StocksTokError(Exception):
    """StocksTok基本例外クラス"""
    pass

class AnalysisError(StocksTokError):
    """分析関連エラー"""
    pass

class DataFetchError(StocksTokError):
    """データ取得エラー"""
    pass

class ValidationError(StocksTokError):
    """バリデーションエラー"""
    pass
```

### 6.2 エラーハンドリング
```python
import logging
from typing import Optional
from src.core.exceptions import AnalysisError, DataFetchError

logger = logging.getLogger(__name__)

def safe_analyze(company_code: str) -> Optional[dict]:
    """
    安全な分析実行
    
    Args:
        company_code: 企業コード
        
    Returns:
        分析結果（エラーの場合はNone）
    """
    try:
        result = analyzer.analyze(company_code)
        return result
    except DataFetchError as e:
        logger.warning(f"データ取得エラー: {e}")
        return None
    except AnalysisError as e:
        logger.error(f"分析エラー: {e}")
        return None
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        return None
```

## 7. ログ規約

### 7.1 ログレベル使用
```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: 詳細なデバッグ情報
logger.debug(f"データ取得開始: {company_code}")

# INFO: 一般的な情報
logger.info(f"分析完了: {company_code}, スコア: {score}")

# WARNING: 警告（処理は継続）
logger.warning(f"データが古い可能性: {company_code}")

# ERROR: エラー（処理に影響）
logger.error(f"分析に失敗: {company_code}, エラー: {e}")

# CRITICAL: 重大なエラー（システム停止）
logger.critical(f"データベース接続失敗: {e}")
```

### 7.2 構造化ログ
```python
import logging
from datetime import datetime

def log_analysis_result(company_code: str, score: int, duration: float):
    """分析結果のログ記録"""
    logger.info(
        "分析結果",
        extra={
            "company_code": company_code,
            "score": score,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        }
    )
```

## 8. テスト規約

### 8.1 テストファイル構造
```python
import pytest
from unittest.mock import Mock, patch
from src.analysis.fundamental import FundamentalAnalyzer

class TestFundamentalAnalyzer:
    """ファンダメンタルズ分析のテスト"""
    
    def setup_method(self):
        """テスト前の準備"""
        self.analyzer = FundamentalAnalyzer()
        self.mock_company = Mock()
        self.mock_company.code = "7203"
        self.mock_company.name = "トヨタ自動車"
    
    def test_calculate_financial_health_score(self):
        """財務健全性スコア計算のテスト"""
        # 準備
        financial_data = {
            "current_ratio": 1.5,
            "debt_to_equity": 0.8,
            "total_equity": 25000000000000
        }
        
        # 実行
        score = self.analyzer.calculate_financial_health_score(financial_data)
        
        # 検証
        assert 0 <= score <= 100
        assert isinstance(score, int)
    
    @patch('src.data.repositories.CompanyRepository')
    def test_analyze_company_with_mock(self, mock_repo):
        """モックを使用した企業分析テスト"""
        # 準備
        mock_repo.return_value.find_by_code.return_value = self.mock_company
        
        # 実行
        result = self.analyzer.analyze_company("7203")
        
        # 検証
        assert result is not None
        mock_repo.return_value.find_by_code.assert_called_once_with("7203")
```

### 8.2 テスト命名規則
- テストメソッド: `test_` プレフィックス
- テストクラス: `Test` プレフィックス
- テストファイル: `test_` プレフィックス

## 9. パフォーマンス規約

### 9.1 データベース最適化
```python
# 良い例: バッチ処理
def save_companies_batch(companies: List[Company]):
    """企業情報の一括保存"""
    with get_db_connection() as conn:
        conn.executemany(
            "INSERT INTO companies (code, name) VALUES (?, ?)",
            [(c.code, c.name) for c in companies]
        )

# 悪い例: 個別処理
def save_companies_individual(companies: List[Company]):
    """企業情報の個別保存（非効率）"""
    for company in companies:
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO companies (code, name) VALUES (?, ?)",
                (company.code, company.name)
            )
```

### 9.2 メモリ効率
```python
# 良い例: ジェネレータ使用
def get_companies_generator():
    """企業情報のジェネレータ"""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM companies")
        for row in cursor:
            yield Company.from_row(row)

# 悪い例: 全件取得
def get_all_companies():
    """全企業情報取得（メモリ使用量大）"""
    with get_db_connection() as conn:
        cursor = conn.execute("SELECT * FROM companies")
        return [Company.from_row(row) for row in cursor.fetchall()]
```

## 10. セキュリティ規約

### 10.1 入力値検証
```python
import re
from typing import Optional

def validate_company_code(code: str) -> Optional[str]:
    """企業コードの検証"""
    if not code:
        return "企業コードは必須です"
    
    if not re.match(r'^\d{4}$', code):
        return "企業コードは4桁の数字である必要があります"
    
    return None

def sanitize_input(text: str) -> str:
    """入力値のサニタイズ"""
    # HTMLエスケープ
    import html
    return html.escape(text.strip())
```

### 10.2 機密情報管理
```python
import os
from src.core.config import Config

# 良い例: 環境変数使用
class Config:
    def __init__(self):
        self.api_key = os.getenv("API_KEY")
        self.database_url = os.getenv("DATABASE_URL")

# 悪い例: ハードコーディング
class Config:
    def __init__(self):
        self.api_key = "secret_key_here"  # 危険
        self.database_url = "sqlite:///data.db"
```

## 11. ドキュメント規約

### 11.1 関数ドキュメント
```python
def calculate_roe(net_income: float, total_equity: float) -> float:
    """
    ROE（自己資本利益率）を計算
    
    Args:
        net_income: 純利益
        total_equity: 純資産
        
    Returns:
        ROE（小数点形式、例: 0.15 = 15%）
        
    Raises:
        ValueError: 純資産が0以下の場合
        
    Example:
        >>> calculate_roe(1000000, 10000000)
        0.1
    """
    if total_equity <= 0:
        raise ValueError("純資産は0より大きい必要があります")
    
    return net_income / total_equity
```

### 11.2 クラスドキュメント
```python
class StockAnalyzer:
    """
    株価分析エンジン
    
    株価データを分析し、投資判断に必要な情報を提供します。
    
    Attributes:
        config: 設定オブジェクト
        logger: ロガーインスタンス
        
    Methods:
        analyze_company: 企業の分析を実行
        calculate_score: スコアを計算
        generate_report: レポートを生成
    """
```

## 12. レビュー基準

### 12.1 コードレビューチェックリスト
- [ ] PEP 8準拠
- [ ] 適切な命名規則
- [ ] エラーハンドリング
- [ ] ログ記録
- [ ] ドキュメント
- [ ] テストカバレッジ
- [ ] セキュリティ考慮
- [ ] パフォーマンス考慮
- [ ] 可読性
- [ ] 保守性

### 12.2 自動チェック
```bash
# コードフォーマット
black src/

# リンター
flake8 src/

# 型チェック
mypy src/

# セキュリティチェック
bandit src/

# テスト実行
pytest tests/
``` 