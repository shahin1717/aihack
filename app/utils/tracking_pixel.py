import base64
from fastapi.responses import StreamingResponse
from pathlib import Path


def get_tracking_pixel():
    pixel_path = Path(__file__).parent.parent / "static" / "pixel.png"
    
    # Create pixel.png if it doesn't exist
    if not pixel_path.exists():
        pixel_path.parent.mkdir(parents=True, exist_ok=True)
        # 1x1 transparent PNG in base64
        png_base64 = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
        png_data = base64.b64decode(png_base64)
        with open(pixel_path, 'wb') as f:
            f.write(png_data)
    
    def generate():
        with open(pixel_path, "rb") as f:
            yield f.read()
    
    return StreamingResponse(generate(), media_type="image/png")

