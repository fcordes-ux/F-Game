# ==========================================
# frontend/asset_manager.py
# ==========================================
"""
AssetManager – unified registry and cache for procedural and static assets.

Each procedural generator conforms to IAssetGenerator:
    id: str
    category: str (e.g., 'texture', 'mesh')
    description: str
    parameters: Dict[str, Any]
    generate(**kwargs) -> object (Ursina Texture/Mesh/etc.)
"""
from typing import Dict, Callable, Any, Type
from ursina import Texture
from PIL import Image
import inspect


# ==========================================
# frontend/asset_manager.py (interface base)
# ==========================================
from typing import Dict, Any
import random, hashlib, json


class IAssetGeneratorV2:
    """Unified procedural generator interface (v2)."""

    id: str
    category: str
    description: str
    version: str = "1.0"
    parameters: Dict[str, Dict[str, Any]] = {}

    # ------------------ template & validation ---------------------------
    def get_template(self) -> Dict[str, Any]:
        tmpl = {"_id": self.id, "_version": self.version, "_meta": {}}
        cfg = {}
        for name, spec in self.parameters.items():
            cfg[name] = spec.get("default")
            tmpl["_meta"][name] = {k: v for k, v in spec.items() if k != "default"}
        tmpl["config"] = cfg
        return tmpl

    def validate(self, cfg: Dict[str, Any]) -> Dict[str, Any]:
        fixed = {}
        for name, spec in self.parameters.items():
            v = cfg.get(name, spec.get("default"))
            t = spec.get("type")
            if t == "int":
                v = int(v)
                if "min" in spec: v = max(spec["min"], v)
                if "max" in spec: v = min(spec["max"], v)
            elif t == "float":
                v = float(v)
                if "min" in spec: v = max(spec["min"], v)
                if "max" in spec: v = min(spec["max"], v)
            elif t == "enum":
                if v not in spec.get("values", []):
                    v = spec.get("default")
            elif t == "bool":
                v = bool(v)
            fixed[name] = v
        return fixed

    def rng(self, cfg: Dict[str, Any]) -> random.Random:
        """Return deterministic RNG based on config hash."""
        h = hashlib.sha256(json.dumps(cfg, sort_keys=True).encode()).hexdigest()
        return random.Random(int(h[:8], 16))

    def generate(self, cfg: Dict[str, Any]):
        raise NotImplementedError


class AssetManager:
    _registry: Dict[str, Type[IAssetGenerator]] = {}
    _cache: Dict[str, object] = {}

    # ------------------------------------------------------------------
    # Generator registration & discovery
    # ------------------------------------------------------------------
    @classmethod
    def register_generator(cls, generator_cls: Type[IAssetGenerator]):
        if not hasattr(generator_cls, "id"):
            raise ValueError("Generator class must define an 'id' attribute")
        cls._registry[generator_cls.id] = generator_cls
        print(f"[AssetManager] Registered generator '{generator_cls.id}'")

    @classmethod
    def discover_generators(cls):
        """Auto-import all frontend.generators.* modules."""
        base_pkg = "frontend.generators"
        package = importlib.import_module(base_pkg)
        base_path = pathlib.Path(package.__file__).parent

        for category_pkg in base_path.iterdir():
            if not category_pkg.is_dir():
                continue
            category_name = category_pkg.name
            for _, mod_name, _ in pkgutil.iter_modules([str(category_pkg)]):
                full_name = f"{base_pkg}.{category_name}.{mod_name}"
                importlib.import_module(full_name)

    # ------------------------------------------------------------------
    # Access API
    # ------------------------------------------------------------------
    @classmethod
    def list_generators(cls, category: str = None):
        return {
            gid: g for gid, g in cls._registry.items()
            if category is None or g.category == category
        }

    @classmethod
    def get_generator(cls, id_: str):
        return cls._registry.get(id_)

@classmethod
def generate(cls, id_: str, config: dict = None):
    gen_cls = cls.get_generator(id_)
    if not gen_cls:
        raise KeyError(f"No generator '{id_}' registered")
    gen = gen_cls()
    config = config or {k: v["default"] for k, v in gen.parameters.items()}
    config = gen.validate(config)
    import json, hashlib
    cache_key = f"{id_}:{hashlib.md5(json.dumps(config, sort_keys=True).encode()).hexdigest()}"
    if cache_key in cls._cache:
        return cls._cache[cache_key]
    result = gen.generate(config)
    cls._cache[cache_key] = result
    return result

