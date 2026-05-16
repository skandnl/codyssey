#!/usr/bin/env bash
set -e
# Change to the directory containing this script
cd "$(dirname "$0")"
# Initialize git repository if not already initialized
if [ ! -d .git ]; then
  git init
fi
# Add all files
git add .
# Commit (skip if there are no changes)
if ! git diff-index --quiet HEAD --; then
  git commit -m "Initial commit – premium portfolio website"
fi
# Set main branch
git branch -M main
# Add remote if not already present
if ! git remote | grep -q origin; then
  git remote add origin https://github.com/skandnl/codyssey.git
fi
# Push to remote
git push -u origin main
