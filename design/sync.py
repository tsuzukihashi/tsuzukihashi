#!/usr/bin/env python3
"""tsuzukit.com のデータから、プロフィールの数字をそろえる。

読むもの（サイトのリポジトリ）
- assets/data/apps.json         … 公開中のアプリ数（total_apps）、各アプリの download_count・評価・アイコン
- assets/data/app-ranking.json  … 総ダウンロード（grand_total。App Store＋Google Play）

書くもの（このリポジトリ）
- design/data.js  … cards.html が読む数字（window.P）
- README.md       … design/README.template.md の {{key}} を埋めたもの

数は切り捨てて「+」を付ける（サイトの scripts/apply_download_totals.py と同じ。実測より大きく見せない）。
レア度はサイトのガチャと同じしきい値（SSR 10万・SR 1万・R 1000）。

使い方: python3 design/sync.py --site <tsuzukit.com のリポジトリ>
このあと bash design/render.sh で画像を作り直す。
"""
import argparse
import datetime
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
START_YEAR = 2016  # 個人開発を始めた年

# 大当たりのカード（cards.html の PICKS の id と App Store の ID）
PICKS = {
    "pick-unchikun": "6758856276",
    "pick-notepad": "1598380826",
    "pick-travel": "6478291625",
    "pick-oshi": "6751716346",
}
TIERS = [("SSR", 100_000), ("SR", 10_000), ("R", 1_000), ("N", 0)]


def rarity(n):
    return next(t for t, low in TIERS if n >= low)


def work(n):  # 290,000+
    step = 10_000 if n >= 100_000 else 1_000
    return f"{n // step * step:,}+"


def en_short(n):  # 820K
    if n >= 1_000_000:
        return f"{n // 100_000 / 10:g}M"
    return f"{n // 10_000 * 10}K"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", required=True, help="tsuzukit.com のリポジトリのパス")
    site = ap.parse_args().site

    apps_doc = json.load(open(os.path.join(site, "assets/data/apps.json"), encoding="utf-8"))
    rank = json.load(open(os.path.join(site, "assets/data/app-ranking.json"), encoding="utf-8"))
    apps = apps_doc["apps"]
    grand = int(rank["grand_total"])

    dl = lambda a: int(a.get("download_count") or 0)
    by_id = {str(a["id"]): a for a in apps}
    ordered = sorted(apps, key=lambda a: -dl(a))
    tiers = {t: [] for t, _ in TIERS}
    for a in ordered:
        tiers[rarity(dl(a))].append(a["icon_url"].replace("512x512bb", "256x256bb"))

    picks = {}
    for key, aid in PICKS.items():
        a = by_id.get(aid)
        if not a:
            print(f"⚠️  {key} のアプリ（{aid}）が apps.json に無い。cards.html の PICKS を見直す")
            continue
        r = float(a.get("rating") or 0)
        picks[key] = {
            "dl": work(dl(a)),
            "rare": rarity(dl(a)),
            "star": f"★{r:.1f}" if r >= 4.0 else "",  # 4 未満は出さない
            "star_sp": f" ★{r:.1f}" if r >= 4.0 else "",  # README の alt 用（前に空白つき）
        }

    years = datetime.date.today().year - START_YEAR
    P = {
        "apps": int(apps_doc["total_apps"]),
        "years": years,
        "years_ja": f"{years}年",
        "dl_man": grand // 10_000,
        "dl_ja": f"{grand // 10_000}万+",
        "dl_en_label": f"{en_short(grand)}+ downloads",
        "dl_en_full": f"{grand // 10_000 * 10_000:,}",
        "n_SSR": len(tiers["SSR"]), "n_SR": len(tiers["SR"]), "n_R": len(tiers["R"]), "n_N": len(tiers["N"]),
        "tiers": tiers,
        "picks": picks,
    }
    open(os.path.join(HERE, "data.js"), "w", encoding="utf-8").write(
        "// design/sync.py が作る。手で直さない\nwindow.P = " + json.dumps(P, ensure_ascii=False, indent=1) + ";\n")

    flat = {k: v for k, v in P.items() if not isinstance(v, (dict, list))}
    for key, v in picks.items():
        for f, x in v.items():
            flat[f"{key}.{f}"] = x
    tpl = open(os.path.join(HERE, "README.template.md"), encoding="utf-8").read()
    missing = sorted(set(re.findall(r"\{\{([\w.-]+)\}\}", tpl)) - set(flat))
    if missing:
        raise SystemExit(f"README.template.md に埋められない {{{{key}}}} がある: {missing}")
    out = re.sub(r"\{\{([\w.-]+)\}\}", lambda m: str(flat[m.group(1)]), tpl)
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(out)

    print(f"公開 {P['apps']}本・合計 {grand:,}（{P['dl_ja']}）・個人開発 {years}年")
    print(f"レア度 SSR {P['n_SSR']} / SR {P['n_SR']} / R {P['n_R']} / N {P['n_N']}")
    for key, v in picks.items():
        print(f"  {key}: {v['rare']} {v['dl']} {v['star']}")


if __name__ == "__main__":
    main()
