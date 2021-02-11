#!/usr/bin/env bash
set -e

# Install curl, jq
# sudo apt-get install curl jq unzip zip -y

# Extract url
URL=$(curl -L -X GET 'http://app.box.com/index.php?folder_id=117401888243&q%5Bshared_item%5D%5Bshared_name%5D=pakte9wz7u0xfoitmktxsspbz01wsijc&rm=box_v2_zip_shared_folder' | jq | grep download_url | awk '{print $2}' | sed "s/\"//g" | sed "s/,//g")

# Download Tiles
OUT="tiles-data-parts"
echo "BOX - Tiles Data"
echo "Downloading from $URL"
wget -L $URL -O $OUT

# Unzip
echo "Unzipping tiles..."
unzip $OUT -qq
zip -s 0 $OUT/tiles-data.zip --out unsplit-foo.zip -q
unzip unsplit-foo.zip -qq

# configure $TILES Env
echo "Setting up env variable $TILES"
export TILES="$(pwd)/tiles-full"

