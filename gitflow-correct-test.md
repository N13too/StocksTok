# Gitflow Correct Test

このファイルは正しいgitflow運用のテスト用です。

## 正しい流れ
1. developブランチからfeatureブランチ作成
2. featureブランチで変更・コミット
3. feature → develop のプルリクエスト作成・マージ
4. develop → main のプルリクエスト作成・マージ

## 確認事項
- developブランチを経由した正しい流れ
- ブランチ保護設定の動作
- プルリクエスト経由でのマージ 