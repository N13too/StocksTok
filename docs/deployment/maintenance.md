# 運用・保守手順書

## 1. 日常運用

### 1.1 アプリケーション監視

#### 1.1.1 プロセス監視
```bash
# プロセス状態確認
tasklist | findstr python
tasklist | findstr uvicorn
tasklist | findstr streamlit

# 期待される出力例
# python.exe                   1234 Console                    1     45,632 K
# uvicorn.exe                  5678 Console                    1     23,456 K
# streamlit.exe                9012 Console                    1     34,567 K
```

#### 1.1.2 ポート監視
```bash
# 使用中ポートの確認
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# 期待される出力例
# TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING       5678
# TCP    0.0.0.0:8501           0.0.0.0:0              LISTENING       9012
```

#### 1.1.3 リソース使用量監視
```bash
# メモリ使用量確認
wmic process where name="python.exe" get ProcessId,WorkingSetSize

# CPU使用量確認
wmic process where name="python.exe" get ProcessId,PercentProcessorTime

# ディスク使用量確認
dir data\stocks_tok.db
dir logs\
```

### 1.2 ログ監視

#### 1.2.1 ログファイル確認
```bash
# 最新ログの確認
type logs\stocks_tok.log | findstr /C:"ERROR" /C:"WARNING"

# ログファイルサイズ確認
dir logs\stocks_tok.log

# ログローテーション確認
dir logs\stocks_tok.log.*
```

#### 1.2.2 リアルタイムログ監視
```bash
# リアルタイムログ監視
Get-Content logs\stocks_tok.log -Wait

# エラーログの監視
Get-Content logs\stocks_tok.log -Wait | Select-String "ERROR"
```

### 1.3 パフォーマンス監視

#### 1.3.1 レスポンス時間監視
```bash
# API応答時間確認
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8000/health"

# curl-format.txt の内容
#      time_namelookup:  %{time_namelookup}\n
#         time_connect:  %{time_connect}\n
#      time_appconnect:  %{time_appconnect}\n
#     time_pretransfer:  %{time_pretransfer}\n
#        time_redirect:  %{time_redirect}\n
#   time_starttransfer:  %{time_starttransfer}\n
#                      ----------\n
#           time_total:  %{time_total}\n
```

#### 1.3.2 データベースパフォーマンス監視
```sql
-- データベースサイズ確認
SELECT 
    name,
    page_count * page_size as size_bytes,
    page_count * page_size / 1024 / 1024 as size_mb
FROM pragma_page_count(), pragma_page_size()
WHERE name = 'stocks_tok.db';

-- テーブルサイズ確認
SELECT 
    name,
    sqlite_total_compressed_pages(name) * 4096 as size_bytes,
    sqlite_total_compressed_pages(name) * 4096 / 1024 / 1024 as size_mb
FROM sqlite_master 
WHERE type = 'table';

-- インデックス使用状況確認
SELECT 
    name,
    sqlite_total_compressed_pages(name) * 4096 as size_bytes
FROM sqlite_master 
WHERE type = 'index';
```

## 2. 定期メンテナンス

### 2.1 日次メンテナンス

#### 2.1.1 ログファイル管理
```bash
# 日次ログローテーション
@echo off
set LOG_DIR=logs
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%

echo Rotating log files...
if exist %LOG_DIR%\stocks_tok.log (
    move %LOG_DIR%\stocks_tok.log %LOG_DIR%\stocks_tok_%DATE%.log
)

echo Compressing old log files...
for %%f in (%LOG_DIR%\stocks_tok_*.log) do (
    if not exist "%%f.gz" (
        gzip "%%f"
    )
)

echo Cleaning up old log files (older than 30 days)...
forfiles /p %LOG_DIR% /s /m *.log.gz /d -30 /c "cmd /c del @path" 2>nul

echo Daily log maintenance completed.
```

#### 2.1.2 データベース最適化
```sql
-- 日次データベース最適化
VACUUM;
ANALYZE;
REINDEX;

-- 統計情報の更新
ANALYZE companies;
ANALYZE stock_prices;
ANALYZE financial_data;
ANALYZE news_data;
ANALYZE analysis_results;
```

#### 2.1.3 キャッシュクリーンアップ
```python
# 日次キャッシュクリーンアップスクリプト
import sqlite3
from datetime import datetime, timedelta

def cleanup_cache():
    """期限切れキャッシュの削除"""
    
    with sqlite3.connect('data/stocks_tok.db') as conn:
        # 期限切れキャッシュを削除
        conn.execute("""
            DELETE FROM cache_data 
            WHERE expires_at < ?
        """, (datetime.now(),))
        
        # 削除件数を確認
        deleted_count = conn.total_changes
        print(f"Cleaned up {deleted_count} expired cache entries")

if __name__ == "__main__":
    cleanup_cache()
```

### 2.2 週次メンテナンス

#### 2.2.1 データベースバックアップ
```bash
# 週次バックアップスクリプト
@echo off
set BACKUP_DIR=backups
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set TIME=%time:~0,2%%time:~3,2%%time:~6,2%

if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

echo Creating weekly backup...
copy data\stocks_tok.db %BACKUP_DIR%\stocks_tok_weekly_%DATE%_%TIME%.db

echo Compressing backup...
gzip %BACKUP_DIR%\stocks_tok_weekly_%DATE%_%TIME%.db

echo Cleaning up old backups (older than 4 weeks)...
forfiles /p %BACKUP_DIR% /s /m stocks_tok_weekly_*.db.gz /d -28 /c "cmd /c del @path" 2>nul

echo Weekly backup completed: %BACKUP_DIR%\stocks_tok_weekly_%DATE%_%TIME%.db.gz
```

#### 2.2.2 パフォーマンス分析
```python
# 週次パフォーマンス分析スクリプト
import sqlite3
import json
from datetime import datetime, timedelta

def analyze_performance():
    """週次パフォーマンス分析"""
    
    with sqlite3.connect('data/stocks_tok.db') as conn:
        # 分析実行時間の統計
        conn.execute("""
            SELECT 
                AVG(execution_time) as avg_time,
                MAX(execution_time) as max_time,
                MIN(execution_time) as min_time,
                COUNT(*) as total_runs
            FROM analysis_results 
            WHERE analysis_date >= ?
        """, (datetime.now() - timedelta(days=7),))
        
        # データ取得統計
        conn.execute("""
            SELECT 
                COUNT(*) as total_companies,
                COUNT(DISTINCT company_id) as analyzed_companies
            FROM analysis_results 
            WHERE analysis_date >= ?
        """, (datetime.now() - timedelta(days=7),))
        
        # 結果をJSONファイルに保存
        with open('logs/performance_analysis.json', 'w') as f:
            json.dump({
                'analysis_date': datetime.now().isoformat(),
                'period': 'weekly',
                'metrics': {
                    'avg_execution_time': avg_time,
                    'max_execution_time': max_time,
                    'min_execution_time': min_time,
                    'total_runs': total_runs,
                    'total_companies': total_companies,
                    'analyzed_companies': analyzed_companies
                }
            }, f, indent=2)

if __name__ == "__main__":
    analyze_performance()
```

### 2.3 月次メンテナンス

#### 2.3.1 完全バックアップ
```bash
# 月次完全バックアップスクリプト
@echo off
set BACKUP_DIR=backups
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set TIME=%time:~0,2%%time:~3,2%%time:~6,2%

if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

echo Creating monthly full backup...
xcopy /E /I /Y data %BACKUP_DIR%\full_backup_%DATE%_%TIME%

echo Creating archive...
cd %BACKUP_DIR%
tar -czf full_backup_%DATE%_%TIME%.tar.gz full_backup_%DATE%_%TIME%
rmdir /S /Q full_backup_%DATE%_%TIME%

echo Cleaning up old monthly backups (older than 6 months)...
forfiles /p %BACKUP_DIR% /s /m full_backup_*.tar.gz /d -180 /c "cmd /c del @path" 2>nul

echo Monthly full backup completed: %BACKUP_DIR%\full_backup_%DATE%_%TIME%.tar.gz
```

#### 2.3.2 データベース最適化
```sql
-- 月次データベース最適化
-- 完全なVACUUM実行
VACUUM;

-- 全テーブルの統計情報更新
ANALYZE;

-- 全インデックスの再構築
REINDEX;

-- データベース整合性チェック
PRAGMA integrity_check;
```

#### 2.3.3 設定ファイルレビュー
```bash
# 設定ファイルのバックアップとレビュー
@echo off
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%

echo Backing up configuration files...
copy config.yaml backups\config_%DATE%.yaml
copy .env backups\env_%DATE%.txt

echo Reviewing configuration...
echo Current configuration:
type config.yaml
echo.
echo Current environment variables:
type .env
```

## 3. 障害対応

### 3.1 障害検知

#### 3.1.1 自動監視スクリプト
```python
# 自動監視スクリプト
import requests
import sqlite3
import logging
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

def check_application_health():
    """アプリケーション健全性チェック"""
    
    try:
        # API健全性チェック
        response = requests.get('http://localhost:8000/health', timeout=10)
        if response.status_code != 200:
            raise Exception(f"API health check failed: {response.status_code}")
        
        # データベース接続チェック
        with sqlite3.connect('data/stocks_tok.db') as conn:
            conn.execute("SELECT 1")
        
        # ログファイルサイズチェック
        import os
        log_size = os.path.getsize('logs/stocks_tok.log')
        if log_size > 100 * 1024 * 1024:  # 100MB
            raise Exception("Log file size exceeded limit")
        
        return True
        
    except Exception as e:
        # 障害通知
        send_alert(f"Application health check failed: {e}")
        return False

def send_alert(message):
    """障害通知送信"""
    # メール通知の実装
    # Slack通知の実装
    # ログ記録
    logging.error(f"ALERT: {message}")

if __name__ == "__main__":
    check_application_health()
```

#### 3.1.2 障害検知ルール
```yaml
# 監視ルール設定
monitoring:
  health_check:
    interval: 5 minutes
    timeout: 30 seconds
    retry_count: 3
  
  alerts:
    api_unavailable:
      threshold: 1 failure
      action: restart_service
    database_error:
      threshold: 1 failure
      action: check_database
    high_memory_usage:
      threshold: 80%
      action: optimize_memory
    disk_space_low:
      threshold: 90%
      action: cleanup_disk
```

### 3.2 障害復旧手順

#### 3.2.1 サービス停止
```bash
# サービス停止手順
@echo off
echo Stopping StocksTok services...

echo Stopping FastAPI server...
taskkill /F /IM uvicorn.exe 2>nul

echo Stopping Streamlit UI...
taskkill /F /IM streamlit.exe 2>nul

echo Stopping Python processes...
taskkill /F /IM python.exe 2>nul

echo All services stopped.
pause
```

#### 3.2.2 データベース復旧
```sql
-- データベース復旧手順
-- 1. データベース整合性チェック
PRAGMA integrity_check;

-- 2. 破損した場合の復旧
-- バックアップから復元
-- または、破損部分の修復

-- 3. インデックスの再構築
REINDEX;

-- 4. 統計情報の更新
ANALYZE;
```

#### 3.2.3 サービス再起動
```bash
# サービス再起動手順
@echo off
echo Restarting StocksTok services...

echo Starting FastAPI server...
start "FastAPI Server" cmd /k "cd /d C:\Projects\StocksTok && venv\Scripts\activate && uvicorn src.api.main:app --host 0.0.0.0 --port 8000"

echo Starting Streamlit UI...
start "Streamlit UI" cmd /k "cd /d C:\Projects\StocksTok && venv\Scripts\activate && streamlit run src.ui.main.py --server.port 8501"

echo Waiting for services to start...
timeout /t 10 /nobreak

echo Checking service health...
curl -f http://localhost:8000/health
if %errorlevel% neq 0 (
    echo ERROR: FastAPI service failed to start
    exit /b 1
)

echo All services restarted successfully.
```

### 3.3 障害報告

#### 3.3.1 障害報告テンプレート
```markdown
# 障害報告書

## 基本情報
- **障害発生日時**: YYYY-MM-DD HH:MM:SS
- **障害検知日時**: YYYY-MM-DD HH:MM:SS
- **障害復旧日時**: YYYY-MM-DD HH:MM:SS
- **障害レベル**: Critical/High/Medium/Low
- **報告者**: [担当者名]

## 障害内容
### 現象
- 具体的な障害現象

### 影響範囲
- 影響を受けた機能
- 影響を受けたユーザー数
- 業務への影響

### 原因
- 根本原因
- 直接原因

## 対応内容
### 緊急対応
- 実施した緊急対応

### 復旧作業
- 実施した復旧作業

### 再発防止策
- 実施した再発防止策

## 今後の対応
- 追加で実施予定の対策
- スケジュール
```

## 4. パフォーマンスチューニング

### 4.1 データベース最適化

#### 4.1.1 クエリ最適化
```sql
-- 遅いクエリの特定
SELECT 
    sql,
    COUNT(*) as execution_count,
    AVG(duration) as avg_duration,
    MAX(duration) as max_duration
FROM query_log
WHERE duration > 1000  -- 1秒以上
GROUP BY sql
ORDER BY avg_duration DESC;

-- インデックス使用状況確認
EXPLAIN QUERY PLAN SELECT * FROM companies WHERE code = '7203';

-- インデックス追加
CREATE INDEX IF NOT EXISTS idx_companies_code ON companies(code);
CREATE INDEX IF NOT EXISTS idx_stock_prices_date ON stock_prices(date);
```

#### 4.1.2 データベース設定最適化
```sql
-- SQLite設定最適化
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 10000;
PRAGMA temp_store = MEMORY;
PRAGMA mmap_size = 268435456;  -- 256MB
```

### 4.2 メモリ最適化

#### 4.2.1 メモリ使用量監視
```python
# メモリ使用量監視スクリプト
import psutil
import logging
from datetime import datetime

def monitor_memory_usage():
    """メモリ使用量監視"""
    
    process = psutil.Process()
    memory_info = process.memory_info()
    
    # メモリ使用量をログに記録
    logging.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    
    # メモリ使用量が閾値を超えた場合の警告
    if memory_info.rss > 2 * 1024 * 1024 * 1024:  # 2GB
        logging.warning("Memory usage exceeded 2GB threshold")
        
        # ガベージコレクション実行
        import gc
        gc.collect()

if __name__ == "__main__":
    monitor_memory_usage()
```

#### 4.2.2 キャッシュ最適化
```python
# キャッシュ最適化
import functools
import time
from collections import OrderedDict

class LRUCache:
    """LRUキャッシュ実装"""
    
    def __init__(self, max_size=1000):
        self.max_size = max_size
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            # 使用されたアイテムを最後に移動
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.max_size:
                # 最も古いアイテムを削除
                self.cache.popitem(last=False)
        self.cache[key] = value

# グローバルキャッシュインスタンス
stock_cache = LRUCache(max_size=1000)
```

### 4.3 並列処理最適化

#### 4.3.1 並列処理設定
```python
# 並列処理最適化
import concurrent.futures
import multiprocessing

def optimize_parallel_processing():
    """並列処理の最適化"""
    
    # CPUコア数に基づくワーカー数設定
    max_workers = min(multiprocessing.cpu_count(), 8)
    
    # ThreadPoolExecutorの設定
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers,
        thread_name_prefix="StocksTok"
    )
    
    return executor

# 並列処理でのデータ取得
def fetch_data_parallel(company_codes):
    """並列データ取得"""
    
    with optimize_parallel_processing() as executor:
        futures = {
            executor.submit(fetch_company_data, code): code 
            for code in company_codes
        }
        
        results = {}
        for future in concurrent.futures.as_completed(futures):
            company_code = futures[future]
            try:
                results[company_code] = future.result()
            except Exception as e:
                logging.error(f"Error fetching data for {company_code}: {e}")
        
        return results
```

## 5. セキュリティ管理

### 5.1 セキュリティ監査

#### 5.1.1 定期的なセキュリティチェック
```bash
# セキュリティチェックスクリプト
@echo off
echo Running security checks...

echo Checking file permissions...
icacls data\stocks_tok.db
icacls config.yaml
icacls .env

echo Checking for sensitive data in logs...
findstr /i "password\|api_key\|secret" logs\*.log

echo Checking for unauthorized access...
findstr /i "unauthorized\|forbidden\|error 403" logs\*.log

echo Security checks completed.
```

#### 5.1.2 脆弱性スキャン
```bash
# 依存関係の脆弱性チェック
pip install safety
safety check

# セキュリティスキャン
pip install bandit
bandit -r src/ -f json -o security_report.json
```

### 5.2 アクセス制御

#### 5.2.1 ログアクセス監視
```python
# アクセス監視スクリプト
import re
from datetime import datetime, timedelta

def monitor_access_logs():
    """アクセスログの監視"""
    
    suspicious_patterns = [
        r'error 404',
        r'error 403',
        r'error 500',
        r'failed login',
        r'sql injection',
        r'xss'
    ]
    
    with open('logs/stocks_tok.log', 'r') as f:
        for line in f:
            for pattern in suspicious_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    logging.warning(f"Suspicious activity detected: {line.strip()}")
                    # 管理者に通知
                    send_security_alert(line.strip())

def send_security_alert(message):
    """セキュリティアラート送信"""
    # セキュリティチームへの通知実装
    pass
```

## 6. バックアップ・復元

### 6.1 バックアップ戦略

#### 6.1.1 自動バックアップスクリプト
```bash
# 自動バックアップスクリプト
@echo off
set BACKUP_DIR=backups
set DATE=%date:~0,4%%date:~5,2%%date:~8,2%
set TIME=%time:~0,2%%time:~3,2%%time:~6,2%

if not exist %BACKUP_DIR% mkdir %BACKUP_DIR%

echo Creating backup...
copy data\stocks_tok.db %BACKUP_DIR%\stocks_tok_%DATE%_%TIME%.db

echo Creating incremental backup...
sqlite3 data\stocks_tok.db ".backup %BACKUP_DIR%\stocks_tok_incremental_%DATE%_%TIME%.db"

echo Compressing backups...
gzip %BACKUP_DIR%\stocks_tok_%DATE%_%TIME%.db
gzip %BACKUP_DIR%\stocks_tok_incremental_%DATE%_%TIME%.db

echo Cleaning up old backups...
forfiles /p %BACKUP_DIR% /s /m *.db.gz /d -7 /c "cmd /c del @path" 2>nul

echo Backup completed successfully.
```

#### 6.1.2 バックアップ検証
```python
# バックアップ検証スクリプト
import sqlite3
import os
from datetime import datetime

def verify_backup(backup_path):
    """バックアップの検証"""
    
    try:
        # バックアップファイルの存在確認
        if not os.path.exists(backup_path):
            return False, "Backup file not found"
        
        # データベース整合性チェック
        with sqlite3.connect(backup_path) as conn:
            result = conn.execute("PRAGMA integrity_check").fetchone()
            if result[0] != "ok":
                return False, f"Integrity check failed: {result[0]}"
        
        # テーブル存在確認
        with sqlite3.connect(backup_path) as conn:
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            expected_tables = ['companies', 'stock_prices', 'financial_data', 'news_data', 'analysis_results']
            
            for table in expected_tables:
                if (table,) not in tables:
                    return False, f"Missing table: {table}"
        
        return True, "Backup verification successful"
        
    except Exception as e:
        return False, f"Verification error: {e}"

if __name__ == "__main__":
    backup_path = "backups/stocks_tok_latest.db"
    success, message = verify_backup(backup_path)
    print(f"Verification result: {message}")
```

### 6.2 復元手順

#### 6.2.1 データベース復元
```bash
# データベース復元スクリプト
@echo off
set BACKUP_FILE=%1

if "%BACKUP_FILE%"=="" (
    echo Usage: restore_db.bat backup_file.db
    exit /b 1
)

if not exist %BACKUP_FILE% (
    echo Backup file not found: %BACKUP_FILE%
    exit /b 1
)

echo Stopping application...
taskkill /F /IM python.exe 2>nul

echo Creating backup of current database...
copy data\stocks_tok.db data\stocks_tok_before_restore.db

echo Restoring database...
copy %BACKUP_FILE% data\stocks_tok.db

echo Verifying restored database...
python scripts\verify_backup.py data\stocks_tok.db

echo Restarting application...
start "StocksTok" cmd /k "python main.py"

echo Database restore completed.
```

#### 6.2.2 設定ファイル復元
```bash
# 設定ファイル復元スクリプト
@echo off
set BACKUP_DATE=%1

if "%BACKUP_DATE%"=="" (
    echo Usage: restore_config.bat YYYYMMDD
    exit /b 1
)

echo Restoring configuration files...

if exist backups\config_%BACKUP_DATE%.yaml (
    copy backups\config_%BACKUP_DATE%.yaml config.yaml
    echo Configuration file restored.
) else (
    echo Configuration backup not found for date: %BACKUP_DATE%
)

if exist backups\env_%BACKUP_DATE%.txt (
    copy backups\env_%BACKUP_DATE%.txt .env
    echo Environment file restored.
) else (
    echo Environment backup not found for date: %BACKUP_DATE%
)

echo Configuration restore completed.
```

## 7. 更新・アップグレード

### 7.1 アプリケーション更新

#### 7.1.1 更新手順
```bash
# アプリケーション更新スクリプト
@echo off
echo Starting application update...

echo Stopping current application...
taskkill /F /IM python.exe 2>nul

echo Creating backup before update...
copy data\stocks_tok.db backups\stocks_tok_before_update.db
copy config.yaml backups\config_before_update.yaml

echo Updating application code...
git pull origin main

echo Updating dependencies...
venv\Scripts\activate
pip install -r requirements.txt --upgrade

echo Running database migrations...
python scripts\migrate_db.py

echo Starting updated application...
start "StocksTok Updated" cmd /k "python main.py"

echo Update completed successfully.
```

#### 7.1.2 ロールバック手順
```bash
# ロールバックスクリプト
@echo off
echo Starting rollback...

echo Stopping current application...
taskkill /F /IM python.exe 2>nul

echo Restoring previous version...
git reset --hard HEAD~1

echo Restoring previous database...
copy backups\stocks_tok_before_update.db data\stocks_tok.db

echo Restoring previous configuration...
copy backups\config_before_update.yaml config.yaml

echo Starting previous version...
start "StocksTok Previous" cmd /k "python main.py"

echo Rollback completed.
```

### 7.2 依存関係更新

#### 7.2.1 依存関係更新チェック
```bash
# 依存関係更新チェックスクリプト
@echo off
echo Checking for dependency updates...

venv\Scripts\activate

echo Checking pip packages...
pip list --outdated

echo Checking security vulnerabilities...
safety check

echo Checking for new versions...
pip install pip-review
pip-review --local --interactive

echo Dependency check completed.
```

## 8. 監視・レポート

### 8.1 運用レポート

#### 8.1.1 日次レポート生成
```python
# 日次レポート生成スクリプト
import sqlite3
import json
from datetime import datetime, timedelta

def generate_daily_report():
    """日次レポート生成"""
    
    with sqlite3.connect('data/stocks_tok.db') as conn:
        # 分析実行統計
        analysis_stats = conn.execute("""
            SELECT 
                COUNT(*) as total_analyses,
                AVG(execution_time) as avg_execution_time,
                COUNT(DISTINCT company_id) as companies_analyzed
            FROM analysis_results 
            WHERE analysis_date = ?
        """, (datetime.now().date(),)).fetchone()
        
        # エラーログ統計
        error_stats = conn.execute("""
            SELECT 
                COUNT(*) as total_errors,
                COUNT(CASE WHEN log_level = 'ERROR' THEN 1 END) as errors,
                COUNT(CASE WHEN log_level = 'WARNING' THEN 1 END) as warnings
            FROM system_logs 
            WHERE DATE(created_at) = ?
        """, (datetime.now().date(),)).fetchone()
        
        # レポート生成
        report = {
            'date': datetime.now().isoformat(),
            'analysis_stats': {
                'total_analyses': analysis_stats[0],
                'avg_execution_time': analysis_stats[1],
                'companies_analyzed': analysis_stats[2]
            },
            'error_stats': {
                'total_errors': error_stats[0],
                'errors': error_stats[1],
                'warnings': error_stats[2]
            }
        }
        
        # レポート保存
        with open(f'reports/daily_report_{datetime.now().strftime("%Y%m%d")}.json', 'w') as f:
            json.dump(report, f, indent=2)

if __name__ == "__main__":
    generate_daily_report()
```

#### 8.1.2 月次レポート生成
```python
# 月次レポート生成スクリプト
def generate_monthly_report():
    """月次レポート生成"""
    
    # 月次統計の集計
    # パフォーマンス分析
    # 障害統計
    # 改善提案
    
    pass
```

### 8.2 アラート設定

#### 8.2.1 アラート条件設定
```yaml
# アラート設定
alerts:
  critical:
    - service_down
    - database_corruption
    - disk_space_full
  
  high:
    - high_memory_usage
    - slow_response_time
    - high_error_rate
  
  medium:
    - log_file_large
    - cache_miss_rate_high
    - backup_failed
  
  low:
    - disk_space_warning
    - old_log_files
    - unused_cache_entries
```

#### 8.2.2 アラート通知設定
```python
# アラート通知設定
def send_alert(level, message):
    """アラート通知送信"""
    
    if level == 'critical':
        # 即座に通知
        send_email_alert(message)
        send_slack_alert(message)
        send_sms_alert(message)
    
    elif level == 'high':
        # 30分以内に通知
        send_email_alert(message)
        send_slack_alert(message)
    
    elif level == 'medium':
        # 2時間以内に通知
        send_email_alert(message)
    
    elif level == 'low':
        # 日次レポートに含める
        log_alert(message)
``` 

## 9. 開発時のIssue運用

- 想定外の事象や障害が発生した場合、エージェントは自力で解決策を検討しつつ、**必ずGitHub Issueを立てて記録**する。
- Issueには「問題内容」「原因」「解決策」「対応状況」などを記載する。
- 必要に応じてテンプレートを活用する。

### Issueテンプレート例

---
**タイトル**: [カテゴリ] 問題の要約（例: [バグ] 株価APIが応答しない）

#### 問題内容
- 発生した現象・エラー内容

#### 原因
- 原因の推定や調査内容

#### 解決策
- 実施した/予定の対応策

#### 対応状況
- [ ] 未対応
- [ ] 対応中
- [ ] 解決済み

--- 