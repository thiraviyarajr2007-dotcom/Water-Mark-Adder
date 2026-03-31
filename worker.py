import os
from multiprocessing import Pool, cpu_count
from process import add_watermark


def process_single(args):
    input_path, output_path, text, angle, opacity = args

    try:
        add_watermark(input_path, output_path, text, angle, opacity)
    except Exception as e:
        print("Error processing:", input_path, e)


def process_images(input_folder, output_folder, text, angle=45, opacity=80):

    files = [
        f for f in os.listdir(input_folder)
        if f.lower().endswith((".jpg", ".png", ".jpeg"))
    ]

    tasks = []

    for file in files:
        tasks.append((
            os.path.join(input_folder, file),
            os.path.join(output_folder, file),
            text,
            angle,
            opacity
        ))

    print(f"Processing {len(tasks)} images using {cpu_count()} cores...")

    with Pool(cpu_count()) as p:
        p.map(process_single, tasks)