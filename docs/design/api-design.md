# API設計書

## 1. API概要

### 1.1 API仕様
- **フレームワーク**: FastAPI
- **バージョン**: v1
- **ベースURL**: `http://localhost:8000/api/v1`
- **認証**: 不要（ローカル環境のみ）
- **レスポンス形式**: JSON

### 1.2 API構成
```
/api/v1/
├── /analyze          # 分析実行
├── /results          # 結果取得
├── /history          # 履歴取得
├── /companies        # 企業情報
├── /stock-prices     # 株価データ
├── /financial        # 財務データ
├── /news             # ニュースデータ
├── /cache            # キャッシュ管理
└── /system           # システム情報
```

## 2. 共通レスポンス形式

### 2.1 成功レスポンス
```json
{
  "success": true,
  "data": {
    // 実際のデータ
  },
  "message": "処理が正常に完了しました",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 2.2 エラーレスポンス
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ",
    "details": "詳細情報"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 2.3 ページネーション
```json
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 100,
      "total_pages": 5
    }
  }
}
```

## 3. エンドポイント詳細

### 3.1 分析実行 API

#### POST /api/v1/analyze
分析を実行し、結果を返却します。

**リクエスト**:
```json
{
  "force_refresh": false,
  "target_companies": ["7203", "6758"],  // オプション: 特定企業のみ
  "analysis_options": {
    "include_fundamental": true,
    "include_technical": true,
    "include_news": true
  }
}
```

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "analysis_id": "2024-01-01_001",
    "status": "completed",
    "execution_time": 180.5,
    "companies_analyzed": 3800,
    "top_picks": [
      {
        "rank": 1,
        "company_code": "7203",
        "company_name": "トヨタ自動車",
        "overall_score": 85,
        "fundamental_score": 82,
        "technical_score": 88,
        "news_score": 80
      }
    ],
    "summary": {
      "total_companies": 3800,
      "analyzed_companies": 3800,
      "cached_data_used": 1500,
      "new_data_fetched": 2300
    }
  }
}
```

### 3.2 結果取得 API

#### GET /api/v1/results/{analysis_date}
指定日の分析結果を取得します。

**パラメータ**:
- `analysis_date`: 分析日 (YYYY-MM-DD)
- `limit`: 取得件数 (デフォルト: 10)
- `include_details`: 詳細データ含む (デフォルト: false)

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "analysis_date": "2024-01-01",
    "results": [
      {
        "rank": 1,
        "company": {
          "code": "7203",
          "name": "トヨタ自動車",
          "sector": "自動車",
          "market": "プライム"
        },
        "scores": {
          "overall": 85,
          "fundamental": {
            "total": 82,
            "financial_health": 85,
            "profitability": 80,
            "growth": 78,
            "dividend": 85
          },
          "technical": {
            "total": 88,
            "price_trend": 90,
            "momentum": 85,
            "volatility": 82,
            "volume": 92
          },
          "news": {
            "total": 80,
            "disclosure": 85,
            "news_impact": 75,
            "industry_trend": 80
          }
        },
        "current_price": 2500,
        "price_change": 2.5,
        "market_cap": 3500000000000
      }
    ],
    "summary": {
      "total_companies": 3800,
      "average_score": 65.2,
      "score_distribution": {
        "90-100": 15,
        "80-89": 120,
        "70-79": 450,
        "60-69": 1200,
        "50-59": 1500,
        "0-49": 515
      }
    }
  }
}
```

### 3.3 履歴取得 API

#### GET /api/v1/history
分析履歴を取得します。

**パラメータ**:
- `start_date`: 開始日 (YYYY-MM-DD)
- `end_date`: 終了日 (YYYY-MM-DD)
- `company_code`: 企業コード (オプション)
- `limit`: 取得件数 (デフォルト: 50)

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "analysis_date": "2024-01-01",
        "company_code": "7203",
        "company_name": "トヨタ自動車",
        "rank": 1,
        "overall_score": 85,
        "price_at_analysis": 2500,
        "current_price": 2550,
        "price_change_percent": 2.0
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 50,
      "total": 150,
      "total_pages": 3
    }
  }
}
```

### 3.4 企業情報 API

#### GET /api/v1/companies
企業一覧を取得します。

**パラメータ**:
- `sector`: 業種フィルター
- `market`: 市場フィルター
- `search`: 企業名検索
- `page`: ページ番号
- `per_page`: 1ページあたりの件数

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "companies": [
      {
        "id": 1,
        "code": "7203",
        "name": "トヨタ自動車",
        "sector": "自動車",
        "market": "プライム",
        "listing_date": "1949-05-16",
        "current_price": 2500,
        "market_cap": 3500000000000
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 20,
      "total": 3800,
      "total_pages": 190
    }
  }
}
```

#### GET /api/v1/companies/{code}
特定企業の詳細情報を取得します。

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "company": {
      "id": 1,
      "code": "7203",
      "name": "トヨタ自動車",
      "sector": "自動車",
      "market": "プライム",
      "listing_date": "1949-05-16",
      "current_price": 2500,
      "market_cap": 3500000000000,
      "dividend_yield": 2.5,
      "per": 15.2,
      "pbr": 1.8,
      "roe": 12.5
    },
    "recent_analysis": {
      "last_analysis_date": "2024-01-01",
      "rank": 1,
      "overall_score": 85
    }
  }
}
```

### 3.5 株価データ API

#### GET /api/v1/stock-prices/{code}
企業の株価データを取得します。

**パラメータ**:
- `start_date`: 開始日 (YYYY-MM-DD)
- `end_date`: 終了日 (YYYY-MM-DD)
- `period`: 期間 (1d, 5d, 1m, 3m, 6m, 1y)

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "company_code": "7203",
    "company_name": "トヨタ自動車",
    "prices": [
      {
        "date": "2024-01-01",
        "open": 2480,
        "high": 2520,
        "low": 2470,
        "close": 2500,
        "volume": 15000000,
        "market_cap": 3500000000000
      }
    ],
    "summary": {
      "current_price": 2500,
      "price_change": 20,
      "price_change_percent": 0.8,
      "volume_avg": 12000000
    }
  }
}
```

### 3.6 財務データ API

#### GET /api/v1/financial/{code}
企業の財務データを取得します。

**パラメータ**:
- `fiscal_year`: 会計年度
- `quarter`: 四半期 (1-4)

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "company_code": "7203",
    "company_name": "トヨタ自動車",
    "financial_data": [
      {
        "fiscal_year": 2023,
        "quarter": 4,
        "revenue": 45000000000000,
        "operating_income": 4500000000000,
        "net_income": 3500000000000,
        "total_assets": 75000000000000,
        "total_equity": 25000000000000,
        "current_ratio": 1.2,
        "debt_to_equity": 0.8,
        "roe": 14.0,
        "per": 15.2,
        "pbr": 1.8
      }
    ]
  }
}
```

### 3.7 ニュースデータ API

#### GET /api/v1/news/{code}
企業のニュースデータを取得します。

**パラメータ**:
- `start_date`: 開始日 (YYYY-MM-DD)
- `end_date`: 終了日 (YYYY-MM-DD)
- `limit`: 取得件数 (デフォルト: 20)

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "company_code": "7203",
    "company_name": "トヨタ自動車",
    "news": [
      {
        "id": 1,
        "title": "トヨタ、EV戦略を強化",
        "content": "トヨタ自動車は電気自動車戦略を強化することを発表...",
        "url": "https://example.com/news/1",
        "source": "日本経済新聞",
        "published_at": "2024-01-01T10:00:00Z",
        "sentiment_score": 0.8,
        "importance_score": 85
      }
    ],
    "summary": {
      "total_news": 25,
      "positive_news": 15,
      "negative_news": 5,
      "neutral_news": 5,
      "average_sentiment": 0.6
    }
  }
}
```

### 3.8 キャッシュ管理 API

#### GET /api/v1/cache/status
キャッシュの状態を取得します。

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "cache_status": {
      "stock_prices": {
        "total_cached": 1500,
        "expires_in": "6 hours",
        "last_updated": "2024-01-01T10:00:00Z"
      },
      "financial_data": {
        "total_cached": 800,
        "expires_in": "30 days",
        "last_updated": "2024-01-01T10:00:00Z"
      },
      "news_data": {
        "total_cached": 2000,
        "expires_in": "1 hour",
        "last_updated": "2024-01-01T10:00:00Z"
      }
    }
  }
}
```

#### POST /api/v1/cache/clear
キャッシュをクリアします。

**リクエスト**:
```json
{
  "cache_type": "all",  // all, stock_prices, financial_data, news_data
  "force": false
}
```

### 3.9 システム情報 API

#### GET /api/v1/system/status
システムの状態を取得します。

**レスポンス**:
```json
{
  "success": true,
  "data": {
    "system_status": {
      "version": "1.0.0",
      "uptime": "24 hours",
      "database_size": "500MB",
      "memory_usage": "1.2GB",
      "cpu_usage": "15%",
      "last_analysis": "2024-01-01T10:00:00Z"
    },
    "api_status": {
      "yahoo_finance": "healthy",
      "edinet": "healthy",
      "news_api": "healthy"
    }
  }
}
```

#### GET /api/v1/system/logs
システムログを取得します。

**パラメータ**:
- `level`: ログレベル (INFO, WARNING, ERROR)
- `component`: コンポーネント名
- `start_date`: 開始日
- `end_date`: 終了日
- `limit`: 取得件数

## 4. エラーハンドリング

### 4.1 HTTPステータスコード
- `200`: 成功
- `400`: バドリクエスト
- `404`: リソースが見つからない
- `422`: バリデーションエラー
- `500`: サーバーエラー

### 4.2 エラーコード
```json
{
  "COMPANY_NOT_FOUND": "企業が見つかりません",
  "INVALID_DATE_FORMAT": "日付形式が無効です",
  "ANALYSIS_IN_PROGRESS": "分析が実行中です",
  "CACHE_EXPIRED": "キャッシュが期限切れです",
  "API_RATE_LIMIT": "API制限に達しました",
  "DATABASE_ERROR": "データベースエラーが発生しました"
}
```

## 5. レート制限

### 5.1 制限設定
- **分析実行**: 1回/分
- **データ取得**: 100回/分
- **履歴取得**: 1000回/分

### 5.2 レート制限ヘッダー
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## 6. バージョニング

### 6.1 バージョン管理
- URLパスでのバージョニング (`/api/v1/`)
- 後方互換性の維持
- 非推奨APIの段階的廃止

### 6.2 バージョン移行
```json
{
  "deprecated_endpoints": [
    {
      "endpoint": "/api/v1/old-endpoint",
      "replacement": "/api/v1/new-endpoint",
      "deprecated_since": "2024-01-01",
      "removal_date": "2024-07-01"
    }
  ]
}
``` 