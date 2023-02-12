from typing import List
from pathlib import Path
from PIL import ImageFilter
from pil_utils import BuildImage, Text2Image
from pil_utils.gradient import LinearGradient, ColorStop

from meme_generator import add_meme
from meme_generator.exception import TextOverLength


img_dir = Path(__file__).parent / "images"


def ask(images: List[BuildImage], texts: List[str], args):
    img = images[0].resize_width(640)
    img_w, img_h = img.size
    gradient_h = 150
    gradient = LinearGradient(
        (0, 0, 0, gradient_h),
        [ColorStop(0, (0, 0, 0, 220)), ColorStop(1, (0, 0, 0, 30))],
    )
    gradient_img = gradient.create_image((img_w, gradient_h))
    mask = BuildImage.new("RGBA", img.size)
    mask.paste(gradient_img, (0, img_h - gradient_h), alpha=True)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=3))
    img.paste(mask, alpha=True)

    name = texts[0]
    ta = "他"

    start_w = 20
    start_h = img_h - gradient_h + 5
    text_img1 = Text2Image.from_text(
        f"{name}", 28, fill="orange", weight="bold"
    ).to_image()
    text_img2 = Text2Image.from_text(
        f"{name}不知道哦。", 28, fill="white", weight="bold"
    ).to_image()
    img.paste(
        text_img1,
        (start_w + 40 + (text_img2.width - text_img1.width) // 2, start_h),
        alpha=True,
    )
    img.paste(
        text_img2,
        (start_w + 40, start_h + text_img1.height + 10),
        alpha=True,
    )

    line_h = start_h + text_img1.height + 5
    img.draw_line(
        (start_w, line_h, start_w + text_img2.width + 80, line_h),
        fill="orange",
        width=2,
    )

    sep_w = 30
    sep_h = 80
    frame = BuildImage.new("RGBA", (img_w + sep_w * 2, img_h + sep_h * 2), "white")
    try:
        frame.draw_text(
            (sep_w, 0, img_w + sep_w, sep_h),
            f"让{name}告诉你吧",
            max_fontsize=35,
            halign="left",
        )
        frame.draw_text(
            (sep_w, img_h + sep_h, img_w + sep_w, img_h + sep_h * 2),
            f"啊这，{ta}说不知道",
            max_fontsize=35,
            halign="left",
        )
    except ValueError:
        raise TextOverLength(name)
    frame.paste(img, (sep_w, sep_h))
    return frame.save_jpg()


add_meme("ask", ["问问"], ask, min_images=1, max_images=1, min_texts=1, max_texts=1)