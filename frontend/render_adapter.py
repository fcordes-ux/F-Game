# ==========================================
# frontend/render_adapter.py
# ==========================================
"""
Simple adapter that mirrors WorldState into Ursina Entities.
"""
from ursina import Entity, Vec3, color
from core.world_state import WorldState


class RenderAdapter:
    def __init__(self, world: WorldState):
        self.world = world
        self.entities = {}

    def sync(self):
        snapshot = self.world.all()

        # spawn new
        for eid, state in snapshot.items():
            if eid not in self.entities:
                e = Entity(
                    model='cube',
                    color=color.azure if eid == "player" else color.orange,
                    position=Vec3(*state.pos),
                    scale=1
                )
                self.entities[eid] = e

        # update transforms
        for eid, e in list(self.entities.items()):
            state = snapshot.get(eid)
            if not state:
                e.disable()
                self.entities.pop(eid)
                continue
            e.position = Vec3(*state.pos)
