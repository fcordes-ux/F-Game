from ursina import Texture
from PIL import Image, ImageDraw, ImageFilter
from frontend.asset_manager import IAssetGeneratorV2, AssetManager


class CobblestoneGenerator(IAssetGeneratorV2):
    id = "texture.cobblestone"
    category = "texture"
    description = "Procedural seamless cobblestone pattern."
    parameters = {
        "size":  {"type": "int", "default":512, "min":128, "max":2048},
        "cell":  {"type": "int", "default":20,  "min":4,   "max":128},
        "style": {"type": "enum", "default":"regular", "values":["regular","cracked","dark"]},
    }

    def generate(self, cfg):
        cfg = self.validate(cfg)
        rng = self.rng(cfg)
        size, cell = cfg["size"], cfg["cell"]

        img = Image.new("RGB", (size, size), (130, 130, 130))
        draw = ImageDraw.Draw(img)

        # stones
        for y in range(0, size, cell):
            for x in range(0, size, cell):
                dx = (x + rng.randint(-2, 2)) % size
                dy = (y + rng.randint(-2, 2)) % size
                w = cell + rng.randint(-2, 2)
                h = cell + rng.randint(-2, 2)
                g = rng.randint(110, 170)
                draw.rectangle([dx, dy, dx + w, dy + h], fill=(g, g, g))

        # cracks or tone variant
        if cfg["style"] == "cracked":
            for _ in range(800):
                x1 = rng.randint(0, size - 1)
                y1 = rng.randint(0, size - 1)
                x2 = (x1 + rng.randint(-3, 3)) % size
                y2 = (y1 + rng.randint(-3, 3)) % size
                draw.line((x1, y1, x2, y2), fill=(60, 60, 60))
        if cfg["style"] == "dark":
            img = img.point(lambda v: int(v * 0.8))

        img = img.filter(ImageFilter.GaussianBlur(0.8))
        return Texture(img)


AssetManager.register_generator(CobblestoneGenerator)
