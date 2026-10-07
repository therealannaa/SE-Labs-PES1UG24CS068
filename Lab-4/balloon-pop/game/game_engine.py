"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.
"""

import random

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45

BALLOON_TYPES = {
    "normal": {"color": (220, 40, 40), "points": 10, "weight": 70},
    "bonus": {"color": (255, 215, 0), "points": 30, "weight": 15},
    "penalty": {"color": (100, 100, 100), "points": -20, "weight": 15},
}

class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0

    def _spawn_balloon(self):
        kinds = list(BALLOON_TYPES.keys())
        weights = [v["weight"] for v in BALLOON_TYPES.values()]
        kind = random.choices(kinds, weights=weights)[0]
        config = BALLOON_TYPES[kind]

        if kind == "bonus":
            radius = random.randint(12, 30)
            speed = random.uniform(2.5, 4.5)
        else:
            radius = random.randint(16, 44)
            speed = random.uniform(1.5, 3.0)

        x = random.randint(radius + 10, WIDTH - radius - 10)
        
        self.balloons.append(Balloon(
            x=x, y=-radius, radius=radius, speed=speed,
            color=config["color"], kind=kind, points=config["points"]
        ))

    def handle_click(self, pos):
        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        self.balloons = [b for b in self.balloons if not b.is_past_bottom(HEIGHT)]

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons, font)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))