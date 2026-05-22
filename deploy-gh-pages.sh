#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
REPO_NAME="${1:-misesapo365-lp}"
GH=/opt/homebrew/bin/gh

if ! "$GH" auth status &>/dev/null; then
  echo "先に GitHub ログインしてください:"
  echo "  $GH auth login -h github.com -p https -w"
  exit 1
fi

if ! git rev-parse --git-dir &>/dev/null; then
  git init
  git branch -M main 2>/dev/null || true
fi

git add -A
if git diff --staged --quiet; then
  echo "コミットする変更なし"
else
  GIT_AUTHOR_NAME="LP" GIT_AUTHOR_EMAIL="noreply@local" \
  GIT_COMMITTER_NAME="LP" GIT_COMMITTER_EMAIL="noreply@local" \
  git commit -m "chore: sync for GitHub Pages"
fi

if ! git remote get-url origin &>/dev/null; then
  "$GH" repo create "$REPO_NAME" --public --source=. --remote=origin --push
else
  git push -u origin HEAD
fi

ORIGIN_URL=$(git remote get-url origin)
# https://github.com/OWNER/REPO.git または git@github.com:OWNER/REPO.git
if [[ "$ORIGIN_URL" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
  OWNER_REPO="${BASH_REMATCH[1]}/${BASH_REMATCH[2]}"
else
  OWNER_REPO=$("$GH" repo view --json nameWithOwner -q .nameWithOwner)
fi

echo "GitHub Pages を branch=main / path=/ で有効化しています…"
if "$GH" api -X POST "repos/${OWNER_REPO}/pages" \
  --input - <<< '{"build_type":"legacy","source":{"branch":"main","path":"/"}}' >/dev/null 2>&1; then
  echo "Pages API: OK"
else
  echo "Pages API: 既に設定済みか権限のためスキップしました。手動なら Settings → Pages → Deploy from branch → main / (root)"
fi

USER=$("$GH" api user -q .login)
echo ""
echo "公開 URL（反映まで1〜3分かかることがあります）:"
echo "  https://${USER}.github.io/${REPO_NAME}/"
