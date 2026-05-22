# ミセサポ365 LP（静的）

GitHub Pages 向けの単一 HTML ランディングページです。

## ローカル確認

```bash
python3 -m http.server 8080
```

ブラウザで `http://127.0.0.1:8080/` を開きます。

## 画像について

`assets/*.png` は `misesapo_mobile_lp_images` 由来の本番スライスを配置しています（リポジトリには同フォルダは含めず `.gitignore` 済み）。差し替え時は `assets/` を直接更新してください。

## GitHub Pages

リポジトリ設定で **Pages → Branch: main / Folder: / (root)** を選ぶと `index.html` が公開されます。

プロジェクトサイトの場合の URL 例: `https://<ユーザー名>.github.io/<リポジトリ名>/`
