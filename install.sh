#!/usr/bin/env bash
# 把三个 skill 链接进 DSH 的 skills 目录。
# 用法: ./install.sh [目标目录，默认 $HOME/.dsh/skills]
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/skills"
DEST="${1:-${DSH_SKILLS_DIR:-$HOME/.dsh/skills}}"

[ -d "$SRC" ] || { echo "找不到 $SRC"; exit 1; }
mkdir -p "$DEST"

linked=0
for s in image-brief knowledge-intake review-workflow; do
  if [ -e "$DEST/$s" ] || [ -L "$DEST/$s" ]; then
    echo "skip  $s（已存在）"
    continue
  fi
  ln -s "$SRC/$s" "$DEST/$s"
  echo "link  $s -> $DEST/$s"
  linked=$((linked + 1))
done

if [ "$linked" -gt 0 ] && [ ! -d "$HOME/.dsh" ]; then
  echo "提示: 没找到 ~/.dsh，确认已安装 DeepSeek Harness"
fi
echo "done: $linked 个 skill"
