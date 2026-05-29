#!/bin/bash
# Linux packaging script for File Harbor (AppImage)
set -e

# Run PyInstaller
echo "Building with PyInstaller..."
pyinstaller build.spec

# AppDir structure
APPDIR="dist/FileHarbor.AppDir"
mkdir -p "$APPDIR/usr/bin"
cp -r dist/FileHarbor/* "$APPDIR/usr/bin/"

# Desktop file
cat > "$APPDIR/fileharbor.desktop" << EOF
[Desktop Entry]
Type=Application
Name=File Harbor
Exec=FileHarbor
Icon=fileharbor
Categories=Utility;
EOF

# Download linuxdeploy
if [ ! -f "linuxdeploy-x86_64.AppImage" ]; then
    wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
    chmod +x linuxdeploy-x86_64.AppImage
fi

# Build AppImage
./linuxdeploy-x86_64.AppImage --appdir "$APPDIR" --output appimage
mv File_Harbor*.AppImage dist/
echo "Done! AppImage is in dist/"
