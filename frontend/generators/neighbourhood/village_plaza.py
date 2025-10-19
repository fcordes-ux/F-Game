# ==========================================
# frontend/generators/neighbourhood/village_plaza.py
# ==========================================
from frontend.asset_manager import IAssetGeneratorV2, AssetManager
from ursina import Mesh
import random


class VillagePlazaNeighbourhood(IAssetGeneratorV2):
    id = "neighbourhood.village_plaza"
    category = "neighbourhood"
    description = "Generates a compact medieval plaza with cobblestone floor and Fachwerk houses."
    parameters = {
        "seed":        {"type": "int", "default": 42, "min": 0, "max": 999999},
        "houses":      {"type": "int", "default": 4, "min": 1, "max": 12},
        "radius":      {"type": "float", "default": 10.0, "min": 5.0, "max": 20.0},
        "tree_count":  {"type": "int", "default": 6, "min": 0, "max": 20},
        "house_style": {"type": "enum", "default": "classic", "values": ["classic", "diagonal", "plain"]},
    }

    def generate(self, cfg):
        cfg = self.validate(cfg)
        rng = self.rng(cfg)

        # main blueprint dict
        blueprint = {
            "ground": {
                "texture": "texture.cobblestone",
                "model": "plane",
                "scale": (30, 1, 30),
                "texture_scale": (10, 10)
            },
            "houses": [],
            "trees": [],
            "fountain": {
                "mesh": "mesh.fountain",  # placeholder
                "pos": (0, 0, 0)
            }
        }

        # --- Procedural Houses ----------------------------------------
        for i in range(cfg["houses"]):
            angle = (i / cfg["houses"]) * 360
            x = cfg["radius"] * rng.uniform(0.9, 1.1) * (1 if rng.random() < 0.5 else -1)
            z = cfg["radius"] * rng.uniform(0.9, 1.1) * (1 if rng.random() < 0.5 else -1)

            house_cfg = {
                "floors": rng.choice([1, 2, 3]),
                "width":  rng.uniform(5, 8),
                "depth":  rng.uniform(3, 5),
                "beam_thick": rng.uniform(0.15, 0.25),
                "diagonals": (cfg["house_style"] != "plain"),
                "roof_pitch": rng.uniform(40, 50),
            }

            # generate mesh using AssetManager
            house_mesh = AssetManager.generate("mesh.fachwerk_house", house_cfg)

            blueprint["houses"].append({
                "mesh_obj": house_mesh,
                "pos": (x, 0, z),
                "rot": (0, rng.uniform(0, 360), 0),
                "scale": 1.0,
            })

        # --- Trees (placeholders) -------------------------------------
        for _ in range(cfg["tree_count"]):
            x, z = rng.uniform(-12, 12), rng.uniform(-12, 12)
            blueprint["trees"].append({
                "mesh": "mesh.tree",  # placeholder mesh type
                "pos": (x, 0, z),
                "scale": rng.uniform(0.8, 1.4)
            })

        return blueprint


AssetManager.register_generator(VillagePlazaNeighbourhood)
