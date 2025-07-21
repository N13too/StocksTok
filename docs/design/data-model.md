# データモデル設計書

## 1. データベース概要

### 1.1 データベース選択
- **データベース**: SQLite
- **理由**: 
  - 軽量で単一ファイル
  - Python標準ライブラリで対応
  - ローカル環境に最適
  - バックアップ・移行が容易

### 1.2 データベース構成
```
stocks_tok.db
├── companies (企業情報)
├── stock_prices (株価データ)
├── financial_data (財務データ)
├── news_data (ニュースデータ)
├── analysis_results (分析結果)
├── cache_data (キャッシュデータ)
└── system_logs (システムログ)
```

## 2. テーブル設計

### 2.1 companies (企業情報テーブル)

```sql
CREATE TABLE companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(10) UNIQUE NOT NULL,           -- 証券コード
    name VARCHAR(100) NOT NULL,                 -- 企業名
    sector VARCHAR(50),                         -- 業種
    market VARCHAR(20),                         -- 市場区分
    listing_date DATE,                          -- 上場日
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**インデックス**:
- `idx_companies_code` ON companies(code)
- `idx_companies_sector` ON companies(sector)

### 2.2 stock_prices (株価データテーブル)

```sql
CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,                -- 企業ID
    date DATE NOT NULL,                         -- 日付
    open_price DECIMAL(10,2),                   -- 始値
    high_price DECIMAL(10,2),                   -- 高値
    low_price DECIMAL(10,2),                    -- 安値
    close_price DECIMAL(10,2),                  -- 終値
    volume BIGINT,                              -- 出来高
    market_cap BIGINT,                          -- 時価総額
    dividend_yield DECIMAL(5,2),                -- 配当利回り
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, date)
);
```

**インデックス**:
- `idx_stock_prices_company_date` ON stock_prices(company_id, date)
- `idx_stock_prices_date` ON stock_prices(date)

### 2.3 financial_data (財務データテーブル)

```sql
CREATE TABLE financial_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,                -- 企業ID
    fiscal_year INTEGER NOT NULL,               -- 会計年度
    quarter INTEGER DEFAULT 4,                  -- 四半期 (1-4)
    revenue BIGINT,                             -- 売上高
    operating_income BIGINT,                    -- 営業利益
    net_income BIGINT,                          -- 純利益
    total_assets BIGINT,                        -- 総資産
    total_equity BIGINT,                        -- 純資産
    current_ratio DECIMAL(5,2),                 -- 流動比率
    debt_to_equity DECIMAL(5,2),                -- 負債比率
    roe DECIMAL(5,2),                           -- ROE
    per DECIMAL(5,2),                           -- PER
    pbr DECIMAL(5,2),                           -- PBR
    dividend_payout_ratio DECIMAL(5,2),         -- 配当性向
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(company_id, fiscal_year, quarter)
);
```

**インデックス**:
- `idx_financial_company_year` ON financial_data(company_id, fiscal_year)
- `idx_financial_year` ON financial_data(fiscal_year)

### 2.4 news_data (ニュースデータテーブル)

```sql
CREATE TABLE news_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id INTEGER NOT NULL,                -- 企業ID
    title VARCHAR(200) NOT NULL,                -- ニュースタイトル
    content TEXT,                               -- ニュース内容
    url VARCHAR(500),                           -- ニュースURL
    source VARCHAR(100),                        -- ニュースソース
    published_at TIMESTAMP,                     -- 公開日時
    sentiment_score DECIMAL(3,2),               -- 感情スコア (-1.0 to 1.0)
    importance_score INTEGER DEFAULT 0,         -- 重要度スコア (0-100)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
```

**インデックス**:
- `idx_news_company_date` ON news_data(company_id, published_at)
- `idx_news_published_at` ON news_data(published_at)

### 2.5 analysis_results (分析結果テーブル)

```sql
CREATE TABLE analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_date DATE NOT NULL,                -- 分析実行日
    company_id INTEGER NOT NULL,                -- 企業ID
    rank INTEGER,                               -- ランキング順位
    
    -- ファンダメンタルズ分析スコア
    financial_health_score INTEGER,             -- 財務健全性 (0-100)
    profitability_score INTEGER,                -- 収益性 (0-100)
    growth_score INTEGER,                       -- 成長性 (0-100)
    dividend_score INTEGER,                     -- 配当政策 (0-100)
    fundamental_total INTEGER,                  -- ファンダメンタルズ総合 (0-100)
    
    -- テクニカル分析スコア
    price_trend_score INTEGER,                  -- 価格トレンド (0-100)
    momentum_score INTEGER,                     -- モメンタム (0-100)
    volatility_score INTEGER,                   -- ボラティリティ (0-100)
    volume_score INTEGER,                       -- 出来高 (0-100)
    technical_total INTEGER,                    -- テクニカル総合 (0-100)
    
    -- ニュース分析スコア
    disclosure_score INTEGER,                   -- 開示情報 (0-100)
    news_impact_score INTEGER,                  -- ニュース影響度 (0-100)
    industry_trend_score INTEGER,               -- 業界動向 (0-100)
    news_total INTEGER,                         -- ニュース総合 (0-100)
    
    -- 総合評価
    overall_score INTEGER,                      -- 総合評価 (0-100)
    
    -- 詳細データ (JSON形式)
    detailed_data TEXT,                         -- 詳細データ
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_id) REFERENCES companies(id),
    UNIQUE(analysis_date, company_id)
);
```

**インデックス**:
- `idx_analysis_date_company` ON analysis_results(analysis_date, company_id)
- `idx_analysis_overall_score` ON analysis_results(overall_score)

### 2.6 cache_data (キャッシュデータテーブル)

```sql
CREATE TABLE cache_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key VARCHAR(100) UNIQUE NOT NULL,     -- キャッシュキー
    cache_type VARCHAR(50) NOT NULL,            -- キャッシュタイプ
    data TEXT NOT NULL,                         -- キャッシュデータ (JSON)
    expires_at TIMESTAMP NOT NULL,              -- 有効期限
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**インデックス**:
- `idx_cache_key` ON cache_data(cache_key)
- `idx_cache_expires` ON cache_data(expires_at)

### 2.7 system_logs (システムログテーブル)

```sql
CREATE TABLE system_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_level VARCHAR(10) NOT NULL,             -- ログレベル
    component VARCHAR(50) NOT NULL,             -- コンポーネント名
    message TEXT NOT NULL,                      -- ログメッセージ
    error_details TEXT,                         -- エラー詳細
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**インデックス**:
- `idx_logs_level_date` ON system_logs(log_level, created_at)
- `idx_logs_component` ON system_logs(component)

## 3. データフロー設計

### 3.1 データ取得フロー

```
1. 企業リスト取得
   ↓
2. 各企業の株価データ取得
   ↓
3. 各企業の財務データ取得
   ↓
4. 各企業のニュースデータ取得
   ↓
5. データ検証・クリーニング
   ↓
6. データベース保存
```

### 3.2 分析実行フロー

```
1. キャッシュチェック
   ↓
2. 必要データ取得
   ↓
3. ファンダメンタルズ分析
   ↓
4. テクニカル分析
   ↓
5. ニュース分析
   ↓
6. 総合評価計算
   ↓
7. 結果保存
```

## 4. データモデルクラス

### 4.1 Company (企業クラス)

```python
@dataclass
class Company:
    id: Optional[int]
    code: str
    name: str
    sector: Optional[str]
    market: Optional[str]
    listing_date: Optional[date]
    created_at: datetime
    updated_at: datetime
```

### 4.2 StockPrice (株価クラス)

```python
@dataclass
class StockPrice:
    id: Optional[int]
    company_id: int
    date: date
    open_price: Optional[Decimal]
    high_price: Optional[Decimal]
    low_price: Optional[Decimal]
    close_price: Optional[Decimal]
    volume: Optional[int]
    market_cap: Optional[int]
    dividend_yield: Optional[Decimal]
    created_at: datetime
```

### 4.3 FinancialData (財務データクラス)

```python
@dataclass
class FinancialData:
    id: Optional[int]
    company_id: int
    fiscal_year: int
    quarter: int
    revenue: Optional[int]
    operating_income: Optional[int]
    net_income: Optional[int]
    total_assets: Optional[int]
    total_equity: Optional[int]
    current_ratio: Optional[Decimal]
    debt_to_equity: Optional[Decimal]
    roe: Optional[Decimal]
    per: Optional[Decimal]
    pbr: Optional[Decimal]
    dividend_payout_ratio: Optional[Decimal]
    created_at: datetime
```

### 4.4 AnalysisResult (分析結果クラス)

```python
@dataclass
class AnalysisResult:
    id: Optional[int]
    analysis_date: date
    company_id: int
    rank: Optional[int]
    
    # ファンダメンタルズ分析
    financial_health_score: int
    profitability_score: int
    growth_score: int
    dividend_score: int
    fundamental_total: int
    
    # テクニカル分析
    price_trend_score: int
    momentum_score: int
    volatility_score: int
    volume_score: int
    technical_total: int
    
    # ニュース分析
    disclosure_score: int
    news_impact_score: int
    industry_trend_score: int
    news_total: int
    
    # 総合評価
    overall_score: int
    detailed_data: Dict[str, Any]
    created_at: datetime
```

## 5. データアクセス層設計

### 5.1 Repository パターン

```python
class CompanyRepository:
    def find_by_code(self, code: str) -> Optional[Company]
    def find_all(self) -> List[Company]
    def save(self, company: Company) -> Company
    def update(self, company: Company) -> Company
    def delete(self, company_id: int) -> bool

class StockPriceRepository:
    def find_by_company_and_date(self, company_id: int, date: date) -> Optional[StockPrice]
    def find_by_company_and_period(self, company_id: int, start_date: date, end_date: date) -> List[StockPrice]
    def save(self, stock_price: StockPrice) -> StockPrice
    def save_bulk(self, stock_prices: List[StockPrice]) -> List[StockPrice]

class AnalysisResultRepository:
    def find_by_date(self, analysis_date: date) -> List[AnalysisResult]
    def find_top_ranked(self, analysis_date: date, limit: int = 10) -> List[AnalysisResult]
    def save(self, result: AnalysisResult) -> AnalysisResult
    def save_bulk(self, results: List[AnalysisResult]) -> List[AnalysisResult]
```

## 6. キャッシュ戦略

### 6.1 キャッシュレベル

1. **アプリケーションレベルキャッシュ**
   - 分析結果のメモリキャッシュ
   - 設定情報のキャッシュ

2. **データベースレベルキャッシュ**
   - 頻繁にアクセスされるデータ
   - 計算結果のキャッシュ

3. **ファイルレベルキャッシュ**
   - 履歴データ
   - 大量データのキャッシュ

### 6.2 キャッシュ有効期限

- **株価データ**: 1日間
- **財務データ**: 決算日まで
- **ニュースデータ**: 1時間
- **分析結果**: 1日間
- **企業情報**: 1週間

## 7. データ移行・バックアップ

### 7.1 データ移行

```python
class DatabaseMigration:
    def create_tables(self) -> None
    def add_indexes(self) -> None
    def migrate_data(self, from_version: str, to_version: str) -> None
```

### 7.2 バックアップ戦略

- **自動バックアップ**: 日次バックアップ
- **手動バックアップ**: 重要な変更前
- **バックアップ形式**: SQLiteファイルのコピー
- **バックアップ保存**: 別ディレクトリに保存 