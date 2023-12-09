import os
x, y = 0, -200
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

import math
import random

import pgzrun
import pygame
from pgzero.constants import mouse
from pgzero.rect import Rect
from pygame.math import Vector2

WIDTH = 1310
HEIGHT = 700

X0 = WIDTH // 2
Y0 = HEIGHT // 2

# settings
G = 0.4 # gravitational constant 
circle_mass = 4 # particle mass
circle_quantity = 17 # number of particles
min_distance = 23 # minimum distance between particles 
bottom = 5 # lower limit of the distance
top = 25 # upper limit of the distance
top_velocity_limit = 10 # upper velosity limit


class Particle:
    def __init__(self, pos, velocity, acc, top_velocity_limit, mass):
        self.pos = pos
        self.velocity = velocity
        self.acc = acc
        self.top_velocity_limit = top_velocity_limit
        self.mass = mass

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self):
        self.velocity += self.acc
        if self.velocity.length() > self.top_velocity_limit:
            self.velocity.scale_to_length(self.top_velocity_limit)

        self.pos += self.velocity

        # # repulsion from the walls
        # if self.pos.x <= 0:
        #     self.velocity.x = self.velocity.x * -1

        # if self.pos.x >= WIDTH:
        #     self.velocity.x = self.velocity.x * -1

        # if self.pos.y <= 0:
        #     self.velocity.y = self.velocity.y * -1

        # if self.pos.y >= HEIGHT:
        #     self.velocity.y = self.velocity.y * -1

        self.acc = Vector2(0, 0)

    def attract(self, particle):
        # 1. calculate the force of attraction
        force_vec : Vector2 = self.pos - particle.pos
        distance = force_vec.magnitude()
        distance = constraint(distance, bottom, top)
        force_vec.normalize_ip()
        strenght = (G * self.mass * particle.mass) / (distance * distance)
        force_vec = force_vec * strenght
        # 2. apply force to particle
        if distance <= min_distance:
            particle.apply_force(force_vec * -5)
            self.velocity /= 2
        else:
            particle.apply_force(force_vec)

    def draw(self):
        screen.draw.text(f'количество частиц = {circle_quantity}', (0, 0))
        screen.draw.text(f'для обновления нажмите R', (0, 20))
        screen.draw.text(f'для отображения векторов нажмите V', (0, 40))
        screen.draw.circle(pos=self.pos, radius=self.mass * 2, color=(0, 255, 0))
        if keyboard.v:
            screen.draw.line(self.pos, self.pos + self.velocity * 20, color=(0, 255, 0)) # rendering the velocity of each particle
            screen.draw.line(self.pos, self.pos + self.acc * 100, color=(255, 255, 0)) # drawing the direction of each particle
            # screen.draw.text(f"p:{self.pos}, v: {self.velocity}, a:{self.acc}", self.pos) # data output for each particle

def constraint(distance, bottom, top):
    if distance < bottom:
        distance = bottom
    elif distance > top:
        distance = top
    return distance

particles = [
    Particle(
        pos=Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT)),
        velocity=Vector2(0, 0),
        acc=Vector2(0, 0),
        top_velocity_limit=top_velocity_limit,
        mass=circle_mass
    ) for _ in range(circle_quantity)
]

def update():
    for p in particles:
        for p1 in particles:
            if p != p1:
                p1.attract(p)
        p.update()
    if keyboard.r:
        exit()

def draw():
    screen.fill((0, 0, 0))
    for p in particles:
        p.draw()

pgzrun.go()
