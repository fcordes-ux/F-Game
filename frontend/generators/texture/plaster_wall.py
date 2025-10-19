from ursina import Texture
from PIL import Image, ImageDraw, ImageFilter
from frontend.asset_manager import IAssetGeneratorV2, AssetManager


class PlasterWallGenerator(IAssetGeneratorV2):
    id = "texture.plaster_wall"
    category = "texture"
    description = "Plaster or whitewashed wall texture with subtle roughness and stains."
    parameters = {
        "size":      {"type": "int", "default":512, "min":128, "max":2048},
        "roughness": {"type": "float", "default":0.25, "min":0.0, "max":1.0},
        "stains":    {"type": "int", "default":40, "min":0, "max":200},
        "tone":      {"type": "enum", "default":"neutral", "values":["neutral","warm","cold"]},
    }

    def generate(self, cfg):
        cfg = self.validate(cfg)
        rng = self.rng(cfg)
        size = cfg["size"]

        tone_mod = {"neutral": (210,205,200), "warm": (215,210,190), "cold": (190,195,210)}[cfg["tone"]]
        img = Image.new("RGB", (size, size), tone_mod)
        draw = ImageDraw.Draw(img)

        # texture noise
        for _ in range(int(size * size * cfg["roughness"] * 0.3)):
            x, y = rng.randint(0, size - 1), rng.randint(0, size - 1)
            val = rng.randint(180, 230)
            img.putpixel((x, y), (val, val, val))

        # stains
        for _ in range(cfg["stains"]):
            x, y = rng.randint(0, size - 1), rng.randint(0, size - 1)
            r = rng.randint(10, 40)
            c = rng.randint(120, 180)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=(c, c, c))

        img = img.filter(ImageFilter.GaussianBlur(1.2))
        return Texture(img)


AssetManager.register_generator(PlasterWallGenerator)
