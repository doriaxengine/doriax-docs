#!/usr/bin/env bash
#
# Builds every published version of the documentation into one output tree:
#
#   site/            latest stable release (mirror, the canonical URLs)
#   site/0.7/        the 0.7 release series
#   site/unstable/   the current main branch
#   site/versions.json   drives the version picker in the header
#
# One version is published per minor series, built from the highest patch tag
# in it (v0.7.0, v0.7.1 -> series "0.7" built from v0.7.1). Pre-release tags
# (v0.8.0-rc1) are ignored.
#
# Every version is built with main's theme/, so a layout fix reaches published
# versions on the next build; only docs/ and mkdocs.yml come from the tag
# itself. Set DOCS_SHARED_THEME=0 to build each version with its own theme.
#
# Set DOCS_PDF=1 to also give each of those directories a doriax-docs.pdf, which
# turns on the download link in the theme. That takes requirements-pdf.txt and the
# Pango and font packages .github/workflows/docs.yml installs.
#
# Usage: scripts/build-versions.sh [output-dir]
set -euo pipefail

REPO_ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$REPO_ROOT"

OUT="$(realpath -m "${1:-site}")"
SITE_URL="${DOCS_SITE_URL_BASE:-https://docs.doriax.org}"
SITE_URL="${SITE_URL%/}"
SHARED_THEME="${DOCS_SHARED_THEME:-1}"
BUILD_PDF="$([ "${DOCS_PDF:-0}" = 1 ] && echo true || echo false)"

WORKTREES=()
cleanup() {
  rm -f "$REPO_ROOT/.mkdocs.version.yml"
  for w in "${WORKTREES[@]:-}"; do
    [ -n "$w" ] && git worktree remove --force "$w" 2>/dev/null || true
  done
}
trap cleanup EXIT

# checkout <ref> -> sets CHECKOUT_PATH to a throwaway worktree holding that ref.
# Sets a global rather than printing: called in a command substitution it would
# register its worktree in a subshell, and cleanup would never remove it.
CHECKOUT_PATH=""
checkout() {
  local ref="$1" path
  path="$(mktemp -d)/src"
  git worktree add --detach "$path" "$ref" >/dev/null
  WORKTREES+=("$path")
  if [ "$SHARED_THEME" = 1 ]; then
    rm -rf "$path/theme"
    cp -a "$REPO_ROOT/theme" "$path/theme"
  fi
  CHECKOUT_PATH="$path"
}

# build <config-dir> <version-id> <dest-subdir|""> <noindex>
#
# Each build gets a generated child config that INHERITs the version's own
# mkdocs.yml and overrides the version metadata. (A child config rather than
# env vars: mkdocs resolves !ENV values through YAML's implicit types, which
# would read a version like 0.10 as the float 0.1.) It also means a version
# predating the picker still builds with one, since the keys the theme needs
# come from here rather than from that version's mkdocs.yml.
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
  version_pdf: $BUILD_PDF
YAML

  echo "==> building '$id' -> ${sub:-<root>}"
  mkdocs build --strict -f "$cfg" -d "$dest"
  rm -f "$cfg"
}

declare -A SERIES_REF=() SERIES_TITLE=()

# Release tags, highest patch first; the first tag seen in a series wins.
while read -r ref; do
  [ -n "$ref" ] || continue
  version="${ref##*/v}"
  case "$version" in *-*) continue ;; esac          # skip pre-releases
  minor="$(echo "$version" | cut -d. -f1,2)"
  if [ -z "${SERIES_REF[$minor]:-}" ]; then
    SERIES_REF[$minor]="$ref"
    SERIES_TITLE[$minor]="$version"
  fi
done < <(git for-each-ref --sort=-v:refname --format='%(refname)' 'refs/tags/v[0-9]*')

SERIES=()
while read -r s; do
  [ -n "$s" ] && SERIES+=("$s")
done < <(printf '%s\n' "${!SERIES_REF[@]}" | sort -Vr)

LATEST="${SERIES[0]:-}"

rm -rf "$OUT"
mkdir -p "$OUT"

# The root build must come first: mkdocs wipes its own site_dir, and here that
# is the directory the per-version subdirectories live in.
if [ -n "$LATEST" ]; then
  echo "==> latest series '$LATEST' from ${SERIES_REF[$LATEST]#refs/tags/}"
  checkout "${SERIES_REF[$LATEST]}"
  build "$CHECKOUT_PATH" "$LATEST" "" false
else
  echo "==> no release tags found; publishing 'unstable' at the root"
  build "$REPO_ROOT" unstable "" false
fi

for minor in "${SERIES[@]:-}"; do
  [ -n "$minor" ] || continue
  echo "==> series '$minor' from ${SERIES_REF[$minor]#refs/tags/}"
  checkout "${SERIES_REF[$minor]}"
  build "$CHECKOUT_PATH" "$minor" "$minor" true
done

build "$REPO_ROOT" unstable unstable true

# After the sites, since mkdocs wipes its site_dir. The PDFs build side by side,
# with their output held back so that the logs do not interleave.
if [ "$BUILD_PDF" = true ]; then
  PDF_LOGS="$(mktemp -d)"
  declare -A PDF_JOBS=()

  # pdf <version-id> <ref>
  pdf() {
    "$REPO_ROOT/scripts/build-pdf.py" --ref "$2" --out "$OUT/$1/doriax-docs.pdf" > "$PDF_LOGS/$1.log" 2>&1 &
    PDF_JOBS[$1]=$!
  }

  for minor in "${SERIES[@]:-}"; do
    [ -n "$minor" ] || continue
    pdf "$minor" "${SERIES_REF[$minor]#refs/tags/}"
  done
  pdf unstable main

  PDF_FAILED=0
  for id in "${!PDF_JOBS[@]}"; do
    wait "${PDF_JOBS[$id]}" || PDF_FAILED=1
    echo "==> PDF of '$id'"
    cat "$PDF_LOGS/$id.log"
  done
  rm -rf "$PDF_LOGS"
  [ "$PDF_FAILED" = 0 ] || exit 1

  # The root mirrors the newest version, its PDF included.
  cp "$OUT/${LATEST:-unstable}/doriax-docs.pdf" "$OUT/doriax-docs.pdf"
fi

SERIES_TITLES="{"
for minor in "${SERIES[@]:-}"; do
  [ -n "$minor" ] || continue
  SERIES_TITLES="$SERIES_TITLES\"$minor\":\"${SERIES_TITLE[$minor]}\","
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
