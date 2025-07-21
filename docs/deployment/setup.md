# セットアップ手順書

## 1. 前提条件

### 1.1 システム要件
- **OS**: Windows 11 (64bit)
- **Python**: 3.11以上
- **メモリ**: 4GB以上推奨
- **ディスク**: 2GB以上の空き容量
- **ネットワーク**: インターネット接続

### 1.2 必要なソフトウェア
- Python 3.11+
- Git
- Visual Studio Code（推奨）
- 7-Zip（オプション）

## 2. 開発環境構築

### 2.1 Python環境の確認・インストール

#### 2.1.1 Pythonバージョン確認
```bash
python --version
# Python 3.11.x が表示されることを確認
```

#### 2.1.2 Pythonがインストールされていない場合
1. [Python公式サイト](https://www.python.org/downloads/)からPython 3.11+をダウンロード
2. インストーラーを実行
3. **"Add Python to PATH"**にチェックを入れる
4. **"Install Now"**をクリック
5. インストール完了後、コマンドプロンプトでバージョン確認

### 2.2 Gitのインストール
1. [Git公式サイト](https://git-scm.com/)からGit for Windowsをダウンロード
2. インストーラーを実行（デフォルト設定でOK）
3. インストール完了後、コマンドプロンプトで確認：
```bash
git --version
```

### 2.3 Visual Studio Codeのインストール（推奨）
1. [Visual Studio Code公式サイト](https://code.visualstudio.com/)からダウンロード
2. インストーラーを実行
3. 推奨拡張機能のインストール：
   - Python
   - Python Extension Pack
   - Git Graph
   - SQLite

## 3. プロジェクトセットアップ

### 3.1 リポジトリのクローン
```bash
# 作業ディレクトリに移動
cd C:\Projects

# リポジトリをクローン
git clone https://github.com/your-username/StocksTok.git

# プロジェクトディレクトリに移動
cd StocksTok
```

### 3.2 仮想環境の作成
```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート
venv\Scripts\activate

# プロンプトが (venv) で始まることを確認
```

### 3.3 依存関係のインストール
```bash
# 依存関係をインストール
pip install -r requirements.txt

# インストール確認
pip list
```

### 3.4 必要なディレクトリの作成
```bash
# 必要なディレクトリを作成
mkdir data
mkdir logs
mkdir tests
mkdir src
mkdir src\api
mkdir src\core
mkdir src\data
mkdir src\analysis
mkdir src\ui
mkdir src\utils
```

## 4. 設定ファイルの作成

### 4.1 環境変数ファイルの作成
```bash
# .envファイルを作成
echo # StocksTok Environment Variables > .env
echo DATABASE_URL=sqlite:///data/stocks_tok.db >> .env
echo LOG_LEVEL=INFO >> .env
echo API_TIMEOUT=30 >> .env
echo CACHE_EXPIRY=3600 >> .env
```

### 4.2 設定ファイルの作成
```yaml
# config.yaml を作成
database:
  url: sqlite:///data/stocks_tok.db
  echo: false

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: logs/stocks_tok.log
  max_size: 10MB
  backup_count: 5

api:
  timeout: 30
  retry_count: 3
  rate_limit: 100

cache:
  expiry:
    stock_prices: 86400  # 24時間
    financial_data: 2592000  # 30日
    news_data: 3600  # 1時間

analysis:
  weights:
    fundamental: 0.4
    technical: 0.35
    news: 0.25
  top_picks_count: 10
```

## 5. データベース初期化

### 5.1 データベース作成スクリプト
```python
# scripts/init_db.py を作成
import sqlite3
import os
from pathlib import Path

def create_database():
    """データベースとテーブルを作成"""
    
    # データディレクトリを作成
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # データベースファイルを作成
    db_path = data_dir / "stocks_tok.db"
    
    with sqlite3.connect(db_path) as conn:
        # 企業情報テーブル
        conn.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code VARCHAR(10) UNIQUE NOT NULL,
                name VARCHAR(100) NOT NULL,
                sector VARCHAR(50),
                market VARCHAR(20),
                listing_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 株価データテーブル
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                date DATE NOT NULL,
                open_price DECIMAL(10,2),
                high_price DECIMAL(10,2),
                low_price DECIMAL(10,2),
                close_price DECIMAL(10,2),
                volume BIGINT,
                market_cap BIGINT,
                dividend_yield DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies(id),
                UNIQUE(company_id, date)
            )
        """)
        
        # その他のテーブルも同様に作成...
        
        print("データベースの初期化が完了しました")

if __name__ == "__main__":
    create_database()
```

### 5.2 データベース初期化の実行
```bash
# データベース初期化スクリプトを実行
python scripts/init_db.py
```

## 6. アプリケーションの起動

### 6.1 開発モードでの起動
```bash
# 仮想環境をアクティベート
venv\Scripts\activate

# FastAPIサーバーを起動
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# 別のターミナルでStreamlitを起動
streamlit run src/ui/main.py --server.port 8501
```

### 6.2 本番モードでの起動
```bash
# 仮想環境をアクティベート
venv\Scripts\activate

# アプリケーションを起動
python main.py
```

## 7. 動作確認

### 7.1 APIの動作確認
```bash
# FastAPIサーバーが起動していることを確認
curl http://localhost:8000/health

# 期待されるレスポンス
# {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}
```

### 7.2 UIの動作確認
1. ブラウザで `http://localhost:8501` にアクセス
2. Streamlit UIが表示されることを確認
3. 基本的な操作ができることを確認

### 7.3 データベースの確認
```bash
# SQLiteデータベースの確認
sqlite3 data/stocks_tok.db ".tables"

# 期待される出力
# companies
# stock_prices
# financial_data
# news_data
# analysis_results
# cache_data
# system_logs
```

## 8. トラブルシューティング

### 8.1 よくある問題と解決方法

#### 8.1.1 Pythonが見つからない
```bash
# 環境変数PATHを確認
echo %PATH%

# Pythonのパスが含まれていない場合、手動で追加
# システム環境変数でPATHに以下を追加：
# C:\Users\[ユーザー名]\AppData\Local\Programs\Python\Python311\
# C:\Users\[ユーザー名]\AppData\Local\Programs\Python\Python311\Scripts\
```

#### 8.1.2 仮想環境のアクティベートが失敗
```bash
# PowerShellの場合、実行ポリシーを変更
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# または、コマンドプロンプトを使用
cmd
venv\Scripts\activate.bat
```

#### 8.1.3 依存関係のインストールエラー
```bash
# pipをアップグレード
python -m pip install --upgrade pip

# キャッシュをクリアして再インストール
pip cache purge
pip install -r requirements.txt --no-cache-dir
```

#### 8.1.4 ポートが使用中
```bash
# 使用中のポートを確認
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# プロセスを終了
taskkill /PID [プロセスID] /F

# または、別のポートを使用
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
streamlit run src.ui.main.py --server.port 8502
```

### 8.2 ログの確認
```bash
# ログファイルを確認
type logs\stocks_tok.log

# リアルタイムでログを監視
Get-Content logs\stocks_tok.log -Wait
```

## 9. 開発環境の最適化

### 9.1 VS Code設定
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./venv/Scripts/python.exe",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": false,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### 9.2 開発用スクリプト
```bash
# run_dev.bat を作成
@echo off
echo Starting StocksTok Development Environment...
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo Starting FastAPI server...
start "FastAPI Server" cmd /k "uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting Streamlit UI...
start "Streamlit UI" cmd /k "streamlit run src.ui.main.py --server.port 8501"

echo Development environment started!
echo FastAPI: http://localhost:8000
echo Streamlit: http://localhost:8501
echo.
pause
```

## 10. 本番環境への移行

### 10.1 本番用設定
```bash
# 本番用環境変数
echo DATABASE_URL=sqlite:///data/stocks_tok_prod.db > .env.prod
echo LOG_LEVEL=WARNING >> .env.prod
echo API_TIMEOUT=60 >> .env.prod
echo CACHE_EXPIRY=7200 >> .env.prod
```

### 10.2 サービス化（Windows）
```xml
<!-- stocks_tok_service.xml -->
<service>
    <id>StocksTok</id>
    <name>StocksTok Stock Analysis Service</name>
    <description>StocksTok株価分析サービス</description>
    <executable>C:\Projects\StocksTok\venv\Scripts\python.exe</executable>
    <arguments>C:\Projects\StocksTok\main.py</arguments>
    <logmode>rotate</logmode>
</service>
```

### 10.3 自動起動設定
```bash
# スタートアップフォルダにショートカットを作成
# Win+R → shell:startup
# ショートカットを作成し、以下を設定：
# ターゲット: C:\Projects\StocksTok\run_prod.bat
# 作業フォルダ: C:\Projects\StocksTok
```

## 11. バックアップ・復元

### 11.1 データベースバックアップ
```bash
# バックアップスクリプト
@echo off
set BACKUP_DIR=backups
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set TIME=%time:~0,2%%time:~3,2%%time:~6,2%

if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

echo Creating backup...
copy data\stocks_tok.db %BACKUP_DIR%\stocks_tok_%DATE%_%TIME%.db

echo Backup completed: %BACKUP_DIR%\stocks_tok_%DATE%_%TIME%.db
pause
```

### 11.2 設定ファイルバックアップ
```bash
# 設定ファイルのバックアップ
copy config.yaml backups\config_%DATE%_%TIME%.yaml
copy .env backups\env_%DATE%_%TIME%.txt
```

## 12. パフォーマンスチューニング

### 12.1 データベース最適化
```sql
-- インデックスの作成
CREATE INDEX idx_companies_code ON companies(code);
CREATE INDEX idx_stock_prices_company_date ON stock_prices(company_id, date);
CREATE INDEX idx_analysis_date_company ON analysis_results(analysis_date, company_id);

-- 統計情報の更新
ANALYZE;
```

### 12.2 メモリ使用量最適化
```python
# 設定ファイルでメモリ制限を設定
cache:
  max_memory: 1GB
  cleanup_interval: 3600
```

### 12.3 並列処理設定
```python
# 並列処理の設定
analysis:
  max_workers: 4
  chunk_size: 100
```

## 13. セキュリティ設定

### 13.1 ファイアウォール設定
```bash
# Windowsファイアウォールでポートを制限
netsh advfirewall firewall add rule name="StocksTok API" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="StocksTok UI" dir=in action=allow protocol=TCP localport=8501
```

### 13.2 アクセス制御
```python
# アクセス制御の設定
security:
  allowed_hosts: ["localhost", "127.0.0.1"]
  rate_limit: 100
  max_request_size: 10MB
```

## 14. 監視・ログ管理

### 14.1 ログローテーション設定
```python
# ログ設定
logging:
  rotation: "1 day"
  retention: "30 days"
  compression: true
  max_size: "100MB"
```

### 14.2 ヘルスチェック
```python
# ヘルスチェックエンドポイント
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }
```

## 15. 更新・アップグレード

### 15.1 アプリケーション更新
```bash
# 最新版を取得
git pull origin main

# 依存関係を更新
pip install -r requirements.txt --upgrade

# データベースマイグレーション
python scripts/migrate_db.py

# アプリケーションを再起動
python main.py
```

### 15.2 設定ファイル更新
```bash
# 設定ファイルのバックアップ
copy config.yaml config.yaml.backup

# 新しい設定ファイルを適用
# 手動で設定を更新

# アプリケーションを再起動
python main.py
``` 