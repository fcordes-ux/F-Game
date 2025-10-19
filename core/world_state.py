# ==========================================
# core/world_state.py
# ==========================================
"""
Minimal WorldState for the playable demo.
Manages simple entities with (x, z) positions and optional movement target.
"""
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import math


@dataclass
class EntityState:
    eid: str
    pos: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    target: Optional[Tuple[float, float, float]] = None
    speed: float = 3.0

    def update(self, dt: float):
        """Move linearly toward target if set."""
        if not self.target:
            return
        px, py, pz = self.pos
        tx, ty, tz = self.target
        dx, dy, dz = tx - px, ty - py, tz - pz
        dist = math.sqrt(dx*dx + dy*dy + dz*dz)
        if dist < 0.05:
            self.pos = (tx, ty, tz)
            self.target = None
            return
        step = self.speed * dt
        if step > dist:
            step = dist
        nx, ny, nz = dx / dist, dy / dist, dz / dist
        self.pos = (px + nx * step, py + ny * step, pz + nz * step)


class WorldState:
    def __init__(self):
        self.entities: Dict[str, EntityState] = {}

    def add(self, entity: EntityState):
        self.entities[entity.eid] = entity

    def get(self, eid: str) -> Optional[EntityState]:
        return self.entities.get(eid)

    def all(self) -> Dict[str, EntityState]:
        return dict(self.entities)

    def tick(self, dt: float):
        for ent in self.entities.values():
            ent.update(dt)
