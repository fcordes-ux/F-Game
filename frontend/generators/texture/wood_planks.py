from ursina import Texture
from PIL import Image, ImageDraw, ImageFilter
from frontend.asset_manager import IAssetGeneratorV2, AssetManager


class WoodPlankGenerator(IAssetGeneratorV2):
    id = "texture.wood_planks"
    category = "texture"
    description = "Procedural wooden plank texture, weathered medieval style."
    parameters = {
        "size":         {"type": "int", "default":512, "min":128, "max":2048},
        "plank_count":  {"type": "int", "default":8,   "min":2,   "max":32},
        "grain_noise":  {"type": "float", "default":0.3, "min":0.0, "max":1.0},
        "tint":         {"type": "enum", "default":"oak", "values":["oak","dark","grey"]},
    }

    def generate(self, cfg):
        cfg = self.validate(cfg)
        rng = self.rng(cfg)
        size, plank_count = cfg["size"], cfg["plank_count"]

        img = Image.new("RGB", (size, size), (90, 70, 50))
        draw = ImageDraw.Draw(img)
        plank_w = size // plank_count

        for i in range(plank_count):
            x0 = i * plank_w
            base = rng.randint(70, 100)
            tint_mod = {"oak": (1.0, 0.9, 0.8),
                        "dark": (0.7, 0.6, 0.5),
                        "grey": (0.6, 0.6, 0.6)}[cfg["tint"]]
            col = tuple(int(base * t) for t in tint_mod)
            draw.rectangle([x0, 0, x0 + plank_w, size], fill=col)

            # grain lines
            for _ in range(int(100 + 200 * cfg["grain_noise"])):
                y = rng.randint(0, size - 1)
                offset = rng.randint(-3, 3)
                draw.line([x0 + offset, y, x0 + plank_w - offset, y], fill=(60, 45, 30))

            # seams
            draw.line([x0, 0, x0, size], fill=(40, 25, 15), width=2)

        img = img.filter(ImageFilter.GaussianBlur(0.6))
        return Texture(img)


AssetManager.register_generator(WoodPlankGenerator)
