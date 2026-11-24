# design

プロフィールの画像（`assets/*.png`）の元。

- `cards.html` に全部のカードがある。ブラウザでそのまま開くと一覧で見られる
- `bash design/render.sh` で全部を 2 倍の PNG に書き出す。1枚だけなら `bash design/render.sh hero`
- 見た目は tsuzukit.com のガチャのデザイン（赤桃の水玉、こげ茶の線、RocknRoll One と M PLUS Rounded 1c）に合わせている
- `data.js` はラインナップのカプセルに入れるアイコン。tsuzukit.com の `assets/data/app-ranking.json` から作った
- 数字（105本・82万DL など）は `cards.html` と `README.md` に直接書いているので、サイトを更新したらここもそろえる
