#!/usr/bin/env bash

# Usage: ./count_loc.sh [REPO_DIR] [-v|--verbose]

REPO_DIR="."
VERBOSE=false

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        *)
            if [[ -d "$1" ]]; then
                REPO_DIR="$1"
            else
                echo "Error: Invalid argument or directory: $1" >&2
                exit 1
            fi
            shift
            ;;
    esac
done

if [[ ! -d "$REPO_DIR/.git" ]]; then
    echo "Error: Not a Git repository (or parent of one): $REPO_DIR" >&2
    exit 1
fi

cd "$REPO_DIR" || exit 1

echo "Lines of code in Git repository: $(pwd)"
echo "----------------------------------------"

# Count LOC for each file type (exclude binaries, ipynb, stl)
FILTERED_FILES=$(git ls-files \
    | grep -vE '\.(bin|png|jpg|jpeg|gif|zip|jar|pdf|ico||xml|svd|xsl)$' \
    | xargs file \
    | grep -E 'ASCII|UTF-8|text' \
    | cut -d ':' -f 1)

# Print per-file counts if verbose mode enabled
if [[ "$VERBOSE" == true ]]; then
    echo "$FILTERED_FILES" \
        | xargs wc -l \
        | grep -v ' total$' \
        | sort -nr
    echo "----------------------------------------"
fi

# Print total LOC
echo "$FILTERED_FILES" \
    | xargs wc -l \
    | grep ' total$'