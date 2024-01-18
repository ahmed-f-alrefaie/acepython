#!/usr/bin/env bash

echo "Publishing wheels..."
ls -l
echo "CIRRUS_RELEASE: $CIRRUS_RELEASE"
echo "CIRRUS_REPO_FULL_NAME: $CIRRUS_REPO_FULL_NAME"
echo "Current wheels"
ls -l wheelhouse/*

if [[ "$CIRRUS_RELEASE" == "" ]]; then
  echo "Not a release. No need to deploy!"
  exit 0
fi

if [[ "$GITHUB_TOKEN" == "" ]]; then
  echo "Please provide GitHub access token via GITHUB_TOKEN environment variable!"
  exit 1
fi

mkdir dist
cp wheelhouse/* dist/

python -m twine upload dist/


file_content_type="application/octet-stream"


for fpath in dist/*;
do
  echo "Uploading $fpath..."
  name=$(basename "$fpath")
  url_to_upload="https://uploads.github.com/repos/$CIRRUS_REPO_FULL_NAME/releases/$CIRRUS_RELEASE/assets?name=$name"
  curl -X POST \
    --data-binary @$fpath \
    --header "Authorization: token $GITHUB_TOKEN" \
    --header "Content-Type: $file_content_type" \
    $url_to_upload
done

# Publish wheels to PyPI

