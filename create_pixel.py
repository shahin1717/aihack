import base64
import os
from pathlib import Path

# 1x1 transparent PNG in base64
png_base64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='

# Get the directory where this script is located
script_dir = Path(__file__).parent
static_dir = script_dir / 'app' / 'static'

# Create static directory if it doesn't exist
static_dir.mkdir(parents=True, exist_ok=True)

# Decode and write PNG file
png_data = base64.b64decode(png_base64)
pixel_path = static_dir / 'pixel.png'

with open(pixel_path, 'wb') as f:
    f.write(png_data)

print(f"Created {pixel_path}")

