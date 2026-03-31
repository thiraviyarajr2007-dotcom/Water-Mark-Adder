from PIL import Image, ImageDraw, ImageFont

def add_watermark(input_path, output_path, text, angle=45, opacity=100):
    base = Image.open(input_path).convert("RGBA")

    txt_layer = Image.new("RGBA", base.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)

    font = ImageFont.truetype("arial.ttf", 80)

    width, height = base.size
    draw.text((width//4, height//2), text, font=font, fill=(255,255,255,opacity))

    txt_layer = txt_layer.rotate(angle, expand=1)

    watermarked = Image.alpha_composite(base, txt_layer)

    watermarked.convert("RGB").save(output_path)