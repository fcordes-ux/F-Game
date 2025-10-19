# ==========================================
# frontend/neighbourhood_assembler.py
# ==========================================
from ursina import Entity, color
from frontend.asset_manager import AssetManager
from hashlib import md5
import json


class NeighbourhoodInstance:
    """Container for a fully built neighbourhood."""
    def __init__(self, root: Entity, entities: list, cache_key: str):
        self.root = root
        self.entities = entities
        self.cache_key = cache_key

    def unload(self):
        """Destroy all Ursina entities belonging to this neighbourhood."""
        for e in self.entities:
            if hasattr(e, "disable"):
                e.disable()
            if hasattr(e, "destroy"):
                e.destroy()
        if self.root:
            self.root.disable()
            self.root.destroy()
        AssetManager._cache.pop(self.cache_key, None)
        print(f"[NeighbourhoodAssembler] Unloaded {self.root.name}")


class NeighbourhoodAssembler:
    """Builds or reuses cached neighbourhood entity trees."""

    @staticmethod
    def _make_cache_key(neighbourhood_id: str, cfg: dict) -> str:
        key_data = json.dumps(cfg, sort_keys=True)
        return f"{neighbourhood_id}:{md5(key_data.encode()).hexdigest()}"

    @classmethod
    def build(cls, blueprint: dict, neighbourhood_id: str, cfg: dict):
        cache_key = cls._make_cache_key(neighbourhood_id, cfg)
        cached = AssetManager.get_cached(cache_key)
        if cached:
            print(f"[NeighbourhoodAssembler] Using cached assembly for {neighbourhood_id}")
            return cached

        print(f"[NeighbourhoodAssembler] Assembling new neighbourhood {neighbourhood_id}")
        root = Entity(name=f"Neighbourhood_{neighbourhood_id}")
        entities = []

        # --- ground -----------------------------------------------------
        g = blueprint.get("ground")
        if g:
            tex = AssetManager.generate(g["texture"], {"size":512})
            ground = Entity(
                parent=root,
                model=g["model"],
                texture=tex,
                scale=g.get("scale", (1, 1, 1)),
                texture_scale=g.get("texture_scale", (1, 1)),
                collider="box"
            )
            entities.append(ground)

        # --- houses -----------------------------------------------------
        for h in blueprint.get("houses", []):
            if "mesh_obj" in h:
                ent = Entity(
                    parent=root,
                    model=h["mesh_obj"],
                    position=h["pos"],
                    rotation=h["rot"],
                    scale=h.get("scale", 1.0),
                )
            else:
                ent = Entity(
                    parent=root,
                    model=h.get("mesh", "cube"),
                    color=color.brown,
                    position=h["pos"],
                    rotation=h["rot"],
                    scale=h.get("scale", 1.0),
                )
            entities.append(ent)

        # --- fountain ---------------------------------------------------
        f = blueprint.get("fountain")
        if f:
            ent = Entity(
                parent=root,
                model=f.get("mesh", "cylinder"),
                color=color.azure,
                position=f.get("pos", (0, 0, 0)),
                scale=f.get("scale", (2, 1, 2)),
            )
            entities.append(ent)

        # --- trees ------------------------------------------------------
        for t in blueprint.get("trees", []):
            ent = Entity(
                parent=root,
                model=t.get("mesh", "cone"),
                color=color.green,
                position=t["pos"],
                scale=t.get("scale", 1.0),
            )
            entities.append(ent)

        instance = NeighbourhoodInstance(root, entities, cache_key)
        AssetManager.set_cached(cache_key, instance)
        print(f"[NeighbourhoodAssembler] Cached {neighbourhood_id}")
        return instance
