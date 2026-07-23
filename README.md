# My Awesome Skills

## 金融行情

| 名称 | 描述 |
|---|---|
| `global-commodity-today` | 查询伦敦金、伦敦银、伦敦铜、纽约铂、布伦特原油的实时价格与当日涨跌幅，支持行情简报和单品种查询。 |
| `ashare-daily-review` | 生成 A 股每日复盘报告，覆盖市场概览、技术形态、板块涨跌、关注板块、外围市场与明日策略，支持输出 HTML 与 PNG 长图。 |

## 学术写作

| 名称 | 描述 |
|---|---|
| `paper-zh-to-en` | 将中文学术论文、摘要、章节或 `.docx` 稿件翻译为符合国际期刊风格的英文，尽量保留原意、结构与格式。 |

## 给 Agent 安装 Skill

1. 克隆本仓库到本地。
2. 将 skill 目录复制到 Agent 的 skills 目录（默认：`${CODEX_HOME:-$HOME/.codex}/skills`）。

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R skills/global-commodity-today "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/ashare-daily-review "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/paper-zh-to-en "${CODEX_HOME:-$HOME/.codex}/skills/"
```

3. 重启 Agent 会话后即可使用对应的 skill。
