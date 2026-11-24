# design

プロフィールの画像（`assets/*.png`）と README の元。

- `cards.html` に全部のカードがある。ブラウザでそのまま開くと一覧で見られる
- 見た目は tsuzukit.com のガチャのデザイン（赤桃の水玉、こげ茶の線、RocknRoll One と M PLUS Rounded 1c）に合わせている

## 数字を tsuzukit.com にそろえる

```bash
python3 design/sync.py --site <tsuzukit.com のリポジトリ>
bash design/render.sh
```

- `sync.py` がサイトの `assets/data/apps.json` と `app-ranking.json` を読んで、`design/data.js`（cards.html が読む数字）と `README.md` を作る
- `README.md` は `README.template.md` の `{{key}}` を埋めたもの。文を変えるときはテンプレートを直す
- `render.sh` は全部を 2 倍の PNG に書き出す。1枚だけなら `bash design/render.sh hero`
- サイトの `/update-portfolio-info` の 8章がこれを流す
