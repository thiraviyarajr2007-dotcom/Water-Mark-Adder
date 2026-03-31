from PIL import Image, ImageDraw, ImageFont
import math


def add_watermark(input_path, output_path, text,
                  angle=45, opacity=80):

    # Open original image
    base = Image.open(input_path).convert("RGBA")
    width, height = base.size

    # 🔥 Create BIG canvas (avoid cutting after rotation)
    diagonal = int(math.sqrt(width**2 + height**2))
    canvas_size = (diagonal, diagonal)

    txt_layer = Image.new("RGBA", canvas_size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    # 🔥 Dynamic font size (fits diagonal perfectly)
    font_size = int(diagonal / 12)
    font = ImageFont.truetype("arial.ttf", font_size)

    # Measure text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    # 🔥 Center text on BIG canvas
    x = (canvas_size[0] - text_width) / 2
    y = (canvas_size[1] - text_height) / 2

    # Draw text with opacity
    draw.text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255, opacity)
    )

    # 🔥 Rotate (perfect diagonal)
    txt_layer = txt_layer.rotate(angle, resample=Image.BICUBIC, expand=True)

    # 🔥 Crop CENTER area equal to original image size
    cx, cy = txt_layer.size[0] // 2, txt_layer.size[1] // 2
    left = cx - width // 2
    top = cy - height // 2
    right = left + width
    bottom = top + height

    txt_layer = txt_layer.crop((left, top, right, bottom))

    # 🔥 Blend with original
    result = Image.alpha_composite(base, txt_layer)

    # Save with same format & name
    result = result.convert("RGB")
    result.save(output_path)