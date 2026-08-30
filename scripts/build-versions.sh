#!/usr/bin/env bash
#
# Builds every published version of the documentation into one output tree:
#
#   site/            latest stable release (mirror, the canonical URLs)
#   site/0.7/        newest tag of the 0.7 series
#   site/unstable/   the current main branch
#   site/versions.json   drives the version picker in the header
#
# One version is published per minor series, built from the highest patch tag
# in it (v0.7.0, v0.7.1 -> series "0.7" built from v0.7.1). Pre-release tags
# (v0.8.0-rc1) are ignored.
#
# Usage: scripts/build-versions.sh [output-dir]
set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$REPO_ROOT"

OUT="$(realpath -m "${1:-site}")"
SITE_URL="${DOCS_SITE_URL_BASE:-https://docs.doriax.org}"
SITE_URL="${SITE_URL%/}"

WORKTREES=()
cleanup() {
  rm -f "$REPO_ROOT/.mkdocs.version.yml"
  for w in "${WORKTREES[@]:-}"; do
    [ -n "$w" ] && git worktree remove --force "$w" 2>/dev/null || true
  done
}
trap cleanup EXIT

# build <config-dir> <version-id> <dest-subdir|""> <noindex>
#
# Each build gets a generated child config that INHERITs the version's own
# mkdocs.yml and overrides the version metadata. (A child config rather than
# env vars: mkdocs resolves !ENV values through YAML's implicit types, which
# would read a version like 0.10 as the float 0.1.)
build() {
  local src="$1" id="$2" sub="$3" noindex="$4"
  local dest="$OUT" url="$SITE_URL/" root=""
  if [ -n "$sub" ]; then
    dest="$OUT/$sub"
    url="$SITE_URL/$sub/"
    root="/.."
  fi

  local cfg="$src/.mkdocs.version.yml"
  cat > "$cfg" <<YAML
INHERIT: mkdocs.yml
site_url: '$url'
extra:
  version: '$id'
  version_root: '$root'
  version_noindex: $noindex
YAML

  echo "==> building '$id' -> ${sub:-<root>}"
  mkdocs build --strict -f "$cfg" -d "$dest"
  rm -f "$cfg"
}

# Highest patch tag per minor series, newest series first.
declare -A SERIES_TAG=()
SERIES=()
while read -r tag; do
  [ -n "$tag" ] || continue
  version="${tag#v}"
  case "$version" in *-*) continue ;; esac          # skip pre-releases
  minor="$(echo "$version" | cut -d. -f1,2)"
  if [ -z "${SERIES_TAG[$minor]:-}" ]; then
    SERIES_TAG[$minor]="$version"
    SERIES+=("$minor")
  fi
done < <(git tag -l 'v[0-9]*' --sort=-v:refname)

LATEST="${SERIES[0]:-}"

rm -rf "$OUT"
mkdir -p "$OUT"

# The root build must come first: mkdocs wipes its own site_dir, and here that
# is the directory the per-version subdirectories live in.
if [ -n "$LATEST" ]; then
  root_src="$(mktemp -d)/src"
  git worktree add --detach "$root_src" "v${SERIES_TAG[$LATEST]}" >/dev/null
  WORKTREES+=("$root_src")
  build "$root_src" "$LATEST" "" false
else
  echo "==> no release tags found; publishing 'unstable' at the root"
  build "$REPO_ROOT" unstable "" false
fi

for minor in "${SERIES[@]:-}"; do
  [ -n "$minor" ] || continue
  src="$(mktemp -d)/src"
  git worktree add --detach "$src" "v${SERIES_TAG[$minor]}" >/dev/null
  WORKTREES+=("$src")
  build "$src" "$minor" "$minor" true
done

build "$REPO_ROOT" unstable unstable true

SERIES_TITLES="{"
for minor in "${SERIES[@]:-}"; do
  [ -n "$minor" ] || continue
  SERIES_TITLES="$SERIES_TITLES\"$minor\":\"${SERIES_TAG[$minor]}\","
done
SERIES_TITLES="${SERIES_TITLES%,}}"
export SERIES_TITLES

python3 - "$OUT/versions.json" "$LATEST" "${SERIES[@]:-}" <<'PY'
import json, os, sys

out, latest = sys.argv[1], sys.argv[2]
series = [s for s in sys.argv[3:] if s]
titles = json.loads(os.environ["SERIES_TITLES"])

versions = [{"id": "unstable", "title": "unstable", "note": "in development"}]
for s in series:
    versions.append({
        "id": s,
        "title": titles[s],
        "note": "latest" if s == latest else "",
    })

with open(out, "w") as f:
    json.dump({"latest": latest or "unstable", "versions": versions}, f, indent=2)
    f.write("\n")
PY

echo "==> versions.json"
cat "$OUT/versions.json"
