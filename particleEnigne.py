import pygame, sys
import random
from abc import ABC, abstractmethod
from typing import List, Tuple

pygame.init()

WINDOW_SIZEX, WINDOW_SIZEY = 1200, 700
RENDX, RENDY = 390, 240
DISPLAY_SIZE = (RENDX, RENDY)
VORTEX_VELOCITY = 0.4
BOUNCE = 0.1

screen = pygame.display.set_mode((WINDOW_SIZEX, WINDOW_SIZEY), pygame.RESIZABLE)
display = pygame.Surface(DISPLAY_SIZE)
clock = pygame.time.Clock()


class Particle(ABC):
    def __init__(self, position: List[float], velocity: List[float], size: float):
        self.position = position
        self.velocity = velocity
        self.size = size

    @abstractmethod
    def update(self, vortex: bool, mouse_pos: Tuple[int, int], multiplier_v: float):
        pass

    @abstractmethod
    def render(self, surface: pygame.Surface, color_shift: bool, color_hue: List[int]):
        pass

    def apply_gravity(self, multiplier_v: float) -> None:
        self.velocity[1] += 0.15 * multiplier_v

    def apply_collision(self, bounce: float) -> None:
        if self.position[0] <= 0.0 or self.position[0] >= RENDX:
            self.velocity[0] *= -1 + bounce
        if self.position[1] <= 0.0 or self.position[1] >= RENDY:
            self.velocity[1] *= -1 + bounce

    def is_off_screen(self) -> bool:
        return self.size <= 0


class CircleParticle(Particle):
    def update(self, vortex: bool, mouse_pos: Tuple[int, int], multiplier_v: float) -> None:
        if vortex:
            if self.position[0] < mouse_pos[0]:
                self.velocity[0] += VORTEX_VELOCITY
            else:
                self.velocity[0] -= VORTEX_VELOCITY

            if self.position[1] < mouse_pos[1]:
                self.velocity[1] += VORTEX_VELOCITY
            else:
                self.velocity[1] -= VORTEX_VELOCITY

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.size -= 0.1 if vortex else 0.08
        self.apply_gravity(multiplier_v)

    def render(self, surface: pygame.Surface, color_shift: bool, color_hue: List[int]) -> None:
        color = (color_hue[0], color_hue[1], color_hue[2]) if color_shift else (220, 100, 100)
        pygame.draw.circle(surface, color, (int(self.position[0]), int(self.position[1])), int(self.size))
        radius = self.size * 1.3
        circle_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surf, color, (int(radius), int(radius)), int(radius))
        surface.blit(circle_surf, (int(self.position[0] - radius), int(self.position[1] - radius)),
                     special_flags=pygame.BLEND_RGB_ADD)


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []

    def add_particle(self, particle: Particle) -> None:
        self.particles.append(particle)

    def update_and_render(self, display: pygame.Surface, vortex: bool, mouse_pos: Tuple[int, int], 
                          multiplier_v: float, collisons: bool, color_shift: bool, color_hue: List[int]) -> None:
        for particle in self.particles[:]:
            particle.update(vortex, mouse_pos, multiplier_v)
            if collisons:
                particle.apply_collision(BOUNCE)
            particle.render(display, color_shift, color_hue)
            if particle.is_off_screen():
                self.particles.remove(particle)


class ColorShifter:
    def __init__(self):
        self.color_hue = [0, 5, 180]
        self.shift_flags = {'r': True, 'g': True, 'b': True}

    def update(self) -> None:
        for color, up in self.shift_flags.items():
            index = 'rgb'.index(color)
            if up:
                self.color_hue[index] = min(self.color_hue[index] + [0.5, 1, 1.5][index], 255)
                if self.color_hue[index] >= 255:
                    self.shift_flags[color] = False
            else:
                self.color_hue[index] = max(self.color_hue[index] - [5, 3, 17][index], 0)
                if self.color_hue[index] <= 0:
                    self.shift_flags[color] = True

    def get_color(self) -> List[int]:
        return self.color_hue


def handle_input(vortex: bool, generate: bool, collisons: bool, color_shift: bool, 
                 multiplier_h: float, multiplier_v: float):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        vortex = not vortex
    if keys[pygame.K_2]:
        color_shift = not color_shift
    if keys[pygame.K_SPACE]:
        generate = not generate
    if keys[pygame.K_c]:
        collisons = not collisons

    if keys[pygame.K_LEFT]:
        multiplier_h += 0.05
    if keys[pygame.K_RIGHT]:
        multiplier_h -= 0.05
    if keys[pygame.K_UP]:
        multiplier_v -= 0.05
    if keys[pygame.K_DOWN]:
        multiplier_v += 0.05

    return vortex, generate, collisons, color_shift, multiplier_h, multiplier_v


def redraw_game_window():
    screen.blit(pygame.transform.scale(display, (WINDOW_SIZEX, WINDOW_SIZEY)), (0, 0))
    pygame.display.update()
    clock.tick(60)


def main():
    vortex, generate, collisons, color_shift = False, False, False, False
    multiplier_h, multiplier_v = 1, 1
    particle_system = ParticleSystem()
    color_shifter = ColorShifter()

    while True:
        display.fill((60, 25, 60))
        mouse_pos = pygame.mouse.get_pos()

        vortex, generate, collisons, color_shift, multiplier_h, multiplier_v = handle_input(
            vortex, generate, collisons, color_shift, multiplier_h, multiplier_v)

        if generate:
            particle_system.add_particle(
                CircleParticle([mouse_pos[0], mouse_pos[1]], [random.uniform(-1, 1) * multiplier_h, -1], random.randint(4, 10)))

        color_shifter.update()
        particle_system.update_and_render(display, vortex, mouse_pos, multiplier_v, collisons, color_shift, color_shifter.get_color())

        pygame.draw.line(display, (255, 255, 255), mouse_pos, (mouse_pos[0] - 2, mouse_pos[1] - 2), 1)
        pygame.draw.line(display, (255, 255, 255), mouse_pos, (mouse_pos[0] - 2, mouse_pos[1]), 1)
        pygame.draw.line(display, (255, 255, 255), (mouse_pos[0] - 2, mouse_pos[1] - 2), (mouse_pos[0] - 2, mouse_pos[1]), 1)

        redraw_game_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                global screen
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)

if __name__ == "__main__":
    main()
