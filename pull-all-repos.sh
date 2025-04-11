#!/bin/bash

BASE_DIR="/home/eva/Documents/vw/gitea"

find "$BASE_DIR" -type d -name ".git" | while read gitdir; do
  repo_dir=$(dirname "$gitdir")
  echo "Pulling in $repo_dir"
  (cd "$repo_dir" && git pull)
done
