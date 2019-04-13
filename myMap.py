import pygame

class Square():
    width = 38
    height = 38

    
    def __init__(self,status,x,y):
        self.status = status #-1表示雷 其他表示雷的数量
        self.cover = True #被点开
        self.flag = False #被标记

        self.image = pygame.image.load('image/cover.png')
        self.icover = pygame.image.load('image/cover.png')
        path = 'image/' + str(status) + '.png'
        self.istatus = pygame.image.load(path)
        self.iflag = pygame.image.load('image/flag.png')

        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = x * Square.width,y * Square.height 

class Clock():
    width = 50
    height = 50

    def __init__(self,m,n):
        self.image = pygame.image.load('image/clock.png')
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = m * Square.width / 10, n * Square.height + 10


class Mine():
    width = 50
    height = 50

    def __init__(self,m,n):
        self.image = pygame.image.load('image/mine.png')
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = m * Square.width * 0.9 - Mine.width , n * Square.height + 10
