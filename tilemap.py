#Imports
import pygame as pg
from settings import *

#Map (level) class
class Map:
	def __init__(self,fileName):
		#Retrieving data
		self.data = []
		with open(fileName, 'rt') as f:
			for line in f:
				line.replace("\r", "")
				self.data.append(line)

		#Initializing variables
		self.tileWidth = len(self.data[0])
		self.tileHeight = len(self.data)
		self.width = self.tileWidth * TILE_SIZE
		self.height = self.tileHeight * TILE_SIZE

#Camera (screen) class
class Camera:
	def __init__(self, width, height):
		self.camera = pg.Rect(0, 0, WIDTH, HEIGHT)
		self.width = width
		self.height = height

	#Camera offset function
	def apply(self, entity):
		#Applying camera offset to input sprite
		return entity.rect.move(self.camera.topleft)

	#Updating camera position
	def update(self,target):
		#Moving camera
		x = -target.rect.x + int(WIDTH/2)
		y = -target.rect.y + int(HEIGHT/2)

		#Limit scrolling
		x = min(0, x) #left
		y = min(0, y) #top
		x = max(-(self.width - WIDTH), x) #right
		y = max(-(self.height - HEIGHT), y) #bottom

		#Updating camera rectangle
		self.camera = pg.Rect(x, y, self.width, self.height)

class ShellObject:
	def __init__(self, game, x, y):
		self.x = x
		self.y = y
		self.rect = pg.Rect(x, y, 20, 20)

	def update(self):
		keys = pg.key.get_pressed()
		if keys[pg.K_a]:
			self.x -= 5
		if keys[pg.K_d]:
			self.x += 5
		if keys[pg.K_w]:
			self.y -= 5
		if keys[pg.K_s]:
			self.y += 5
			
		self.rect.left = self.x
		self.rect.top = self.y



def generateMap(game):
	#Creating empty 2D list
	mapList = [["." for i in range(game.map.tileWidth)] for j in range(game.map.tileHeight)]
	returnString = ""

	#Filling mapList
	for tile in game.tiles:
		mapList[tile.rect.top//TILE_SIZE][tile.rect.left//TILE_SIZE] = "s"
	for enemy in game.enemy_sprites:
		mapList[enemy.rect.top//TILE_SIZE][enemy.rect.left//TILE_SIZE] = str(enemy.vel)
	mapList[game.player.rect.top//TILE_SIZE][game.player.rect.left//TILE_SIZE] = "p"
	for end in game.endpoint_sprites:
		mapList[end.rect.top//TILE_SIZE][end.rect.left//TILE_SIZE] = "e"
	for spike in game.spike_sprites:
		mapList[(spike.rect.top - 10)//TILE_SIZE][spike.rect.left//TILE_SIZE] = "i"
	for ghost in game.ghost_sprites:
		mapList[ghost.rect.top//TILE_SIZE][ghost.rect.left//TILE_SIZE] = "n"
	for turret in game.turret_sprites:
		if turret.direction == 1:
			mapList[turret.rect.top//TILE_SIZE][turret.rect.left//TILE_SIZE] = "r"
		else:
			mapList[turret.rect.top//TILE_SIZE][turret.rect.left//TILE_SIZE] = "l"
	#Converting mapList to a string
	for row in mapList:
		returnString += "".join(row) + "\n"

	#Returning the map in string form
	return returnString