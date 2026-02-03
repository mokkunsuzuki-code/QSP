Stage177｜CI/CD Attack Matrix Auto-Execution

Continuous Security Evidence

目的

QSP プロジェクトにおいて、安全性の主張を継続的に自動検証し、
「いつ見ても再現可能」な状態を CI/CD により保証する。

ゴール

GitHub への push / pull request ごとに
Attack-01〜Attack-06 および demo を自動実行する

各攻撃シナリオの PASS / FAIL を記録する

集約結果を summary.md として artifact に保存する

いずれかが FAIL した場合、CI 全体を FAIL とし fail-closed を強制する

構成

GitHub Actions workflow

matrix 実行（attack-01..06, demo）

Docker Compose による再現可能な実行環境

集約スクリプト summarize_results.sh

セキュリティ主張（Stage177で保証されること）

攻撃検知ロジックは 常に自動検証されている

人手による「安全宣言」は存在しない

安全でない状態は CI段階で排除される

非ゴール

攻撃の網羅性の完全性を主張するものではない

新規攻撃モデルの自動生成は対象外