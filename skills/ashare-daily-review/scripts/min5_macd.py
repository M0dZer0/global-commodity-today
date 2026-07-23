#!/usr/bin/env python3
"""5分钟级别 MACD 背离/交叉检测（供 ashare-daily-review 技能使用）

用法:
  python3 min5_macd.py <minute_md_file> <名称>

输入: 含 `date`、`price` 列的分钟级 Markdown 表格（先保存到文件）
输出: 今日最低/收盘位置、5分钟 DIF/DEA/BAR、与昨日低点对比的背离判断、今日金死叉
"""
import sys
from collections import defaultdict

def parse_md_table(path):
    rows = []
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip().startswith('|')]
    if len(lines) < 3:
        return []
    header = [c.strip() for c in lines[0].strip('|').split('|')]
    for l in lines[2:]:
        cells = [c.strip() for c in l.strip('|').split('|')]
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows

def ema(series, n):
    k = 2 / (n + 1)
    e = series[0]
    out = [e]
    for v in series[1:]:
        e = v * k + e * (1 - k)
        out.append(e)
    return out

def main(path, name):
    rows = parse_md_table(path)
    byday = defaultdict(list)
    for r in rows:
        byday[r['date']].append(float(r['price']))
    days = sorted(byday)
    if len(days) < 2:
        print(f"{name}: 数据不足（需要至少2日分时）")
        return
    # 1分钟 -> 5分钟 聚合（取每5根的最后一根收盘价）
    all5 = []
    for d in days:
        p = byday[d]
        for i in range(0, len(p), 5):
            all5.append((d, p[min(i + 4, len(p) - 1)]))
    px = [x[1] for x in all5]
    if len(px) < 40:
        print(f"{name}: 5分钟K线数量不足")
        return
    e12, e26 = ema(px, 12), ema(px, 26)
    dif = [a - b for a, b in zip(e12, e26)]
    dea = ema(dif, 9)
    bar = [(d - d2) * 2 for d, d2 in zip(dif, dea)]

    today, yday = days[-1], days[-2]
    t_idx = [i for i, x in enumerate(all5) if x[0] == today]
    y_idx = [i for i, x in enumerate(all5) if x[0] == yday]
    t_px = [px[i] for i in t_idx]
    t_dif = [dif[i] for i in t_idx]
    lo_i = t_px.index(min(t_px))

    print(f"== {name} 5分钟MACD（{today}）==")
    print(f"  今日最低 {min(t_px):.2f}（第{lo_i+1}根5分钟K线），收盘 {t_px[-1]:.2f}")
    print(f"  收盘 DIF {t_dif[-1]:.3f} / DEA {dea[t_idx[-1]]:.3f} / BAR {bar[t_idx[-1]]:.3f}")
    print(f"  今日 DIF 最低 {min(t_dif):.3f}；昨日最低 {min(px[i] for i in y_idx):.2f} 对应 DIF 最低 {min(dif[i] for i in y_idx):.3f}")

    y_lo = min(px[i] for i in y_idx)
    y_dif_lo = min(dif[i] for i in y_idx)
    if min(t_px) < y_lo and min(t_dif) > y_dif_lo:
        print("  >>> 价格创新低而 DIF 未创新低：5分钟底背离迹象")
    elif min(t_px) < y_lo:
        print("  >>> 价格创新低，DIF 同步新低：无背离")
    else:
        print("  >>> 今日低点未破昨日低点（重心未下移）")

    crosses = []
    for j in range(1, len(t_idx)):
        i0, i1 = t_idx[j - 1], t_idx[j]
        if dif[i0] < dea[i0] and dif[i1] > dea[i1]:
            crosses.append(('金叉', j))
        if dif[i0] > dea[i0] and dif[i1] < dea[i1]:
            crosses.append(('死叉', j))
    print(f"  今日交叉: {crosses if crosses else '无'}")
    if bar[t_idx[-1]] > 0:
        print("  尾盘 BAR 翻红，分时做多动能回升")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
