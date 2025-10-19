# ==========================================
# frontend/player_controller.py
# ==========================================
"""
Handles user input for controlling the player.
Right-click: move player to world position.
Middle mouse drag: pan camera.
"""
from ursina import mouse, camera, Vec3
from core.world_state import WorldState


class PlayerController:
    def __init__(self, world: WorldState, player_id: str):
        self.world = world
        self.player_id = player_id

    def update(self):
        # --- click-to-move ---
        if mouse.right and mouse.world_point:
            target = mouse.world_point
            player = self.world.get(self.player_id)
            if player:
                # clamp Y=0 to keep it on ground plane
                player.target = (target.x, 0, target.z)

        # --- camera pan ---
        if mouse.middle:
            camera.position += Vec3(-mouse.velocity[0]*20, 0, -mouse.velocity[1]*20)
