# ==========================================
# main.py — camera + lighting diagnostic
# ==========================================
from ursina import (
    Ursina, Entity, camera, color, DirectionalLight,
    AmbientLight, Vec3, window
)
from frontend.asset_manager import AssetManager
from frontend.neighbourhood_assembler import NeighbourhoodAssembler

def main():
    app = Ursina(development_mode=False, fullscreen=False, borderless=False)
    window.color = color.rgb(95, 130, 155)       # light blue background

    # Auto-discover all procedural generators
    AssetManager.discover_generators()

    for gid, gen in AssetManager.list_generators('texture').items():
        instance = gen()
        tmpl = instance.get_template()
        print(f"\n{gid} template:")
        print(tmpl)


    # --- lighting -----------------------------------------------------
    sun = DirectionalLight()
    sun.look_at(Vec3(1, -1, 1))
    AmbientLight(color=color.rgb(140, 140, 140))

    # --- reference geometry ------------------------------------------
    # ground plane
    Entity(model='plane', color=color.rgb(80, 160, 80), scale=(25, 1, 25))
    ground_tex = AssetManager.generate_cobblestone(size=512, cell=20)
    Entity(model='plane', texture=ground_tex, scale=(25, 1, 25))
    # center marker (player placeholder)
    Entity(model='cube', color=color.azure, position=(0, 0.5, 0))
    # north/east axis markers
    Entity(model='cube', color=color.red, scale=(0.1, 0.1, 5), position=(0, 0.05, 2.5))
    Entity(model='cube', color=color.green, scale=(5, 0.1, 0.1), position=(2.5, 0.05, 0))

    # --- camera setup -------------------------------------------------
    camera.parent = None           # detach from UI
    camera.rotation_x = 60         # look down at 60°
    camera.position = (0, 20, -20) # above and behind origin
    camera.look_at(Vec3(0, 0, 0))  # point at player
    camera.fov = 60                # narrower FOV = more zoom-out

    print("[Camera] position:", camera.position, "rotation:", camera.rotation)

    app.run()

if __name__ == "__main__":
    main()
