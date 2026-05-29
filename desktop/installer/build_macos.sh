#!/bin/bash
# MacOS packaging script for File Harbor
set -e

# Run PyInstaller
echo "Building with PyInstaller..."
pyinstaller build.spec

# Create DMG
echo "Creating DMG..."
npm install -g create-dmg
create-dmg \
  --volname "File Harbor Installer" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "FileHarbor.app" 200 190 \
  --hide-extension "FileHarbor.app" \
  --app-drop-link 600 185 \
  "dist/FileHarbor.dmg" \
  "dist/FileHarbor.app"

echo "Done! DMG is at dist/FileHarbor.dmg"
