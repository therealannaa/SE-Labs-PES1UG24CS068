"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.
"""

import random
import pygame

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
ROUND_TIME_SEC = 30

BALLOON_TYPES = {
    "normal": {"color": (220, 40, 40), "points": 10, "weight": 70},
    "bonus": {"color": (255, 215, 0), "points": 30, "weight": 15},
    "penalty": {"color": (100, 100, 100), "points": -20, "weight": 15},
}

class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.time_left = ROUND_TIME_SEC

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
        if self.game_over:
            return

        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        if self.game_over:
            return

        elapsed_ms = pygame.time.get_ticks() - self.start_time
        self.time_left = max(0, ROUND_TIME_SEC - (elapsed_ms // 1000))
        
        if self.time_left <= 0:
            self.game_over = True

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for b in self.balloons:
            b.update()

        active_balloons = []
        for b in self.balloons:
            if b.is_past_bottom(HEIGHT):
                if b.kind != "penalty":
                    self.lives -= 1
            else:
                active_balloons.append(b)
        
        self.balloons = active_balloons

        if self.lives <= 0:
            self.lives = 0
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons, font)
        
        # Draw Score (Top-Left)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        
        # Draw Time (Top-Center)
        time_text = f"Time: {self.time_left}"
        time_width = font.size(time_text)[0]
        renderer.draw_text(surface, font, time_text, (WIDTH // 2 - time_width // 2, 10))

        # Draw Lives (Top-Right)
        lives_text = f"Lives: {self.lives}"
        lives_width = font.size(lives_text)[0]
        renderer.draw_text(surface, font, lives_text, (WIDTH - lives_width - 10, 10))

        if self.game_over:
            renderer.draw_banner(surface, font, f"Final Score: {self.score}")
            
            # Draw restart prompt below the banner
            restart_text = "Press R to play again"
            restart_width = font.size(restart_text)[0]
            renderer.draw_text(surface, font, restart_text, (WIDTH // 2 - restart_width // 2, HEIGHT // 2 + 35))