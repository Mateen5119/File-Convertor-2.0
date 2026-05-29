import os
import sys
from PIL import Image, ImageDraw

def bootstrap_assets():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    fonts_dir = os.path.join(assets_dir, "fonts")
    
    # 1. Create directory structures
    os.makedirs(fonts_dir, exist_ok=True)
    print(f"Created assets folder structure in: {assets_dir}")
    
    # 2. Generate a high-quality 256x256 logo (Electric Blue & Indigo palette)
    img = Image.new("RGBA", (256, 256), color="#131315")
    draw = ImageDraw.Draw(img)
    
    # Rounded glass card shape
    draw.rounded_rectangle([20, 20, 236, 236], radius=48, fill="#1c1c1e", outline="#adc6ff", width=4)
    # Interactive premium blue geometric icon in center
    draw.regular_polygon((128, 128, 60), 6, rotation=30, fill="#adc6ff", outline="#c2c1ff", width=2)
    
    # Save standard PNG icon
    png_path = os.path.join(assets_dir, "icon.png")
    img.save(png_path, "PNG")
    print(f"Generated PNG icon: {png_path}")
    
    # Save standard Windows ICO icon
    ico_path = os.path.join(assets_dir, "icon.ico")
    img.save(ico_path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
    print(f"Generated ICO icon: {ico_path}")

if __name__ == "__main__":
    bootstrap_assets()
