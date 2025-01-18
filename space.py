import pygame as pg
from pygame.math import Vector2 as vec2, Vector3 as vec3
from random import uniform, randrange, choice
from math import pi, sin, cos


RES = WIDTH, HEIGHT = 1920, 1080 # put your screen res here
CENTER = vec2(WIDTH // 2, HEIGHT // 2)
FPS = 120
STAR_NUM = 1000
Z_DISTANCE = 60
ALPHA = 45
SCALE_POS = 2 # increase to remove the wormhole and make it like space
ROTATION = 0.25 # speed of rotation
COLORS = 'cyan pink lightblue snow lightpink skyblue'.split()


class Star:
	def __init__(self, app):
		self.screen = app.screen
		self.old_vel = 0
		self.vel = uniform(0.02, 0.3) # speed of stars
		self.color = choice(COLORS)
		self.screen_pos = vec2(0, 0)
		self.rotation = ROTATION # uniform(-1, 1) could be used to make the rotation random like a solar system
		self.backwards = False
		self.pos3d = self.get_pos3d()

	def get_pos3d(self):
		angle = uniform(0, 2 * pi)
		radius = randrange(HEIGHT, HEIGHT*SCALE_POS)
		x = radius * sin(angle)
		y = radius * cos(angle)
		return vec3(x, y, (1 if self.backwards else Z_DISTANCE))

	def reverse(self):
		self.vel, self.old_vel = -self.vel, -self.old_vel
		self.backwards = not(self.backwards)

	def spin(self):
		self.old_vel, self.vel = self.vel, self.old_vel # freezes velocity and only the speed remains

	def update(self):
		self.pos3d.z -= self.vel
		if self.pos3d.z < 0 or self.pos3d.z > Z_DISTANCE:
			self.pos3d = self.get_pos3d() # reset star position when it get off screen

		self.screen_pos = CENTER + vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z # move star
		self.size = (Z_DISTANCE - self.pos3d.z) / (self.pos3d.z * 0.2) # change size with distance
		self.pos3d.xy = self.pos3d.xy.rotate(self.rotation) # rotate stars

		self.screen_pos += CENTER - vec2(pg.mouse.get_pos()) # move pov with mouse

	def draw(self):
		pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))


class App:
	def __init__(self):
		self.screen = pg.display.set_mode(RES, pg.NOFRAME)
		self.alpha_surface = pg.Surface(RES)
		self.alpha_surface.set_alpha(ALPHA)
		self.clock = pg.time.Clock()
		self.stars = [Star(self) for i in range(STAR_NUM)]
		self.frozen = False
		self.spin = True

		pg.mouse.set_visible(False)
		pg.mouse.set_pos(CENTER)


	def run(self):
		while True:
			self.screen.blit(self.alpha_surface, (0, 0))
			self.move_stars()
			pg.draw.circle(self.screen, 'white', CENTER, 3)  # CENTER point

			pg.display.flip()

			for event in pg.event.get():
				if event.type == pg.QUIT:
					exit()
				if event.type == pg.MOUSEBUTTONDOWN:
					[star.reverse() for star in self.stars]

				if event.type == pg.KEYDOWN:
					if event.key == pg.K_s:
						[star.spin() for star in self.stars]

			self.clock.tick(FPS)


	def move_stars(self):
		[star.update() for star in self.stars]
		self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
		[star.draw() for star in self.stars]


if __name__ == '__main__':
	App().run()