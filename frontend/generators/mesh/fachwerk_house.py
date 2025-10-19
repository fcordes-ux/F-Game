# ==========================================
# frontend/generators/mesh/fachwerk_house.py
# ==========================================
from ursina import Mesh, Vec3
from frontend.asset_manager import IAssetGeneratorV2, AssetManager
from math import radians, sin, cos
import random
from pathlib import Path
from PIL import Image

# we reuse beam extrusion from existing module
from fachwerk import fachwerk_wall, add_beam


class FachwerkHouseGenerator(IAssetGeneratorV2):
    id = "mesh.fachwerk_house"
    category = "mesh"
    description = "Procedural German Fachwerk house with plaster infill and wooden beams."
    parameters = {
        "floors":     {"type": "int", "default":2, "min":1, "max":4},
        "width":      {"type": "float", "default":6.0, "min":3.0, "max":12.0},
        "depth":      {"type": "float", "default":4.0, "min":3.0, "max":10.0},
        "beam_thick": {"type": "float", "default":0.2, "min":0.05, "max":0.5},
        "diagonals":  {"type": "bool", "default":True},
        "roof_pitch": {"type": "float", "default":45.0, "min":25.0, "max":60.0},
    }

    def generate(self, cfg):
        cfg = self.validate(cfg)
        rng = self.rng(cfg)

        # Geometry basics
        cols = int(cfg["width"] // 1.5)
        rows = int(cfg["floors"] * 2)  # two vertical sections per floor
        verts, tris = [], []

        # Base frame: 4 fachwerk walls
        fachwerk_wall(cols, rows, 1.5, 1.2, cfg["beam_thick"],
                      cfg["diagonals"], verts, tris)

        # Mirror to make back wall
        fachwerk_wall(cols, rows, 1.5, 1.2, cfg["beam_thick"],
                      cfg["diagonals"], [v + Vec3(0, 0, cfg["depth"]) for v in verts], tris)

        # Side beams
        add_beam(Vec3(0, 0, 0), Vec3(0, rows*1.2, cfg["depth"]), cfg["beam_thick"], verts, tris)
        add_beam(Vec3(cols*1.5, 0, 0), Vec3(cols*1.5, rows*1.2, cfg["depth"]),
                 cfg["beam_thick"], verts, tris)

        mesh = Mesh(vertices=verts, triangles=tris, mode='triangle')
        mesh.generate()

        # -----------------------------------------------------------------
        # Compose textures: wood + plaster
        # -----------------------------------------------------------------
        plaster_cfg = {"size": 512, "tone": rng.choice(["neutral", "warm"])}
        wood_cfg    = {"size": 512, "tint": "dark", "grain_noise": 0.4}

        plaster_tex = AssetManager.generate("texture.plaster_wall", plaster_cfg)
        wood_tex    = AssetManager.generate("texture.wood_planks", wood_cfg)

        # merge both into a composite texture for demonstration
        # (in production you'd assign different materials per submesh)
        img_wall = plaster_tex.image
        img_wood = wood_tex.image.resize(img_wall.size)
        blend = Image.blend(img_wall, img_wood, 0.25)

        from ursina import Texture
        mesh.texture = Texture(blend)

        return mesh


AssetManager.register_generator(FachwerkHouseGenerator)
