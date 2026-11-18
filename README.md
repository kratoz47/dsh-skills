# dsh-skills

三个自用工作流 skill，写给 DeepSeek Harness（DSH）用：生图简报、视频入库、内容评审。

不是通用模板。它们来自一套真实在跑的流程，带着踩过的坑和硬约束；装上之前先读各自 SKILL.md 顶部的「配置」段，把路径改成你自己的。

## 内容

| skill | 作用 | 依赖 |
|---|---|---|
| [`skills/image-brief`](skills/image-brief/SKILL.md) | 用户给「场景/物体/状态」，agent 跨方向展开 2–3 个变体供勾选，确认后调 Seedream 出图 | 一个生图管线仓库（本文以 [mythos-pipeline](../mythos-pipeline) 为例），`MYTHOS_ROOT` 环境变量 |
| [`skills/knowledge-intake`](skills/knowledge-intake/SKILL.md) | 视频 → 转录/OCR → 校对 → 抽出带出处的知识点 → 重建索引 | `ffmpeg`、`whisper.cpp`、macOS Vision（见 [mac-ocr-kit](../mac-ocr-kit)） |
| [`skills/review-workflow`](skills/review-workflow/SKILL.md) | 3 名独立评委 + Chair 聚合 + Critic 复核，带 checkpoint 闸门 | `rubric.md`、`review-protocol.md`（同目录自带） |

## 安装

DSH 从 `~/.dsh/skills/` 读 skill。把需要的目录链过去，或直接复制：

```bash
git clone <this-repo> ~/dev/dsh-skills
ln -s ~/dev/dsh-skills/skills/image-brief   ~/.dsh/skills/image-brief
ln -s ~/dev/dsh-skills/skills/knowledge-intake ~/.dsh/skills/knowledge-intake
ln -s ~/dev/dsh-skills/skills/review-workflow  ~/.dsh/skills/review-workflow
```

如果 `~/.dsh/skills` 本身是指向别处的软链，链进那个目录即可。

也可以直接跑仓库里的脚本（已存在的 skill 会跳过）：

```bash
./install.sh                      # 默认链到 ~/.dsh/skills
./install.sh /path/to/skills      # 或指定目录
```

## image-brief 的路径

image-brief 假定生图管线在 `$MYTHOS_ROOT`：

```bash
export MYTHOS_ROOT="$HOME/dev/mythos-pipeline"
```

它引用的文件（`prompts/template.md`、`style/bible.md`、`style/board/INDEX.md`、`prompts/layers.md`、`tools/gen.py`、`taste/cli.py`、`promptforge/*.py`）在 [mythos-pipeline](../mythos-pipeline) 里有最小可用版本；`style/board` 与案例库要你自己建。

## review-workflow 的评审材料

`skills/review-workflow/rubric.md` 是评分卡 v3（16 分制 + 前置三闸 + 冷启动豁免）。它引用 `账号结构.md` 和 `benchmarks.md`，这两个是每个账号自己的东西，仓库不带。

跑之前至少准备：

- `rubric.md` 当前版本
- 对应平台的 3 个 benchmark（带 `review_after`）
- 盲包（含去标识历史摘要）

## 许可

MIT，见 [LICENSE](LICENSE)。三份 rubric / protocol 的文字是原创；image-brief 引用的模板与案例库不在本仓库内。
