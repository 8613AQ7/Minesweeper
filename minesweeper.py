import pygame
import random
import myMap
import sys
from pygame.locals import *

M = 15
N = 10
K = 25

bgColor = (191,206,227)
fontColor = (253, 3, 27)
fontColor2 = (255, 0,255)

pygame.init()

loseSound = pygame.mixer.Sound('sound/lose.wav')
loseSound.set_volume(0.4)
winSound = pygame.mixer.Sound('sound/win.wav')
winSound.set_volume(0.4)
expandSound = pygame.mixer.Sound('sound/expand.wav')
expandSound.set_volume(0.2)

def printMessage(message,color,size,location):
    font = pygame.font.Font(None, size) 
    message = font.render(message,True, color)
    screen.blit(message, location)
    
def createMap(m,n,k):
    #暂定为10x10 自定义大小时用变量代替
    mine = random.sample(range(m*n),k)
    num = []
    mp = []
    
    count = 0
    for i in range(m):
        num.append([])
        mp.append([])
        for j in range(n):
            num[i].append(-1 if count in mine else 0)
            mp[i].append([])
            count += 1
    
    for i in range(m):
        for j in range(n):
            mine = 0
            if num[i][j] == -1:
                mp[i][j] = myMap.Square(-1,i,j)
            else:
                for x in range(-1,2):
                    for y in range(-1,2):
                        if -1<i+x<m and -1<j+y<n:
                            if num[i+x][j+y] == -1:
                                mine += 1
                mp[i][j] = myMap.Square(mine,i,j)
    return mp

def createMapPlus(m,n,k):
    mine = [1 if i < k else 0 for i in range(m*n)]
    for i in range(m*n):
        loc = random.randint(0,i)
        mine[loc],mine[i] = mine[i],mine[loc]
    #print(mine)
    
def drawMap(mp,m,n):
    global screen
    for i in range(m):
            for j in range(n):
                s = mp[i][j]
                if s.flag:
                    s.image = s.iflag
                elif not s.cover:
                    s.image = s.istatus
                else:
                    s.image = s.icover
                screen.blit(s.image, s.rect)
                
def bfs(mp,x,y,m,n):
    global startcounting1 
    q = []
    q.append([x,y])
    while q:
        s = q[0] #pop
        q = q[1:]#push
        x,y = s
        mp[x][y].cover = False
        if mp[x][y].status == -1 and not mp[x][y].flag:
            startcounting1 = True
        elif mp[x][y].status == 0 :
            expandSound.play()
            for i in range(-1,2):
                for j in range(-1,2):
                    sx,sy = x+i,y+j
                    if -1<sx<m and -1<sy<n and mp[sx][sy].cover == True:
                        q.append([sx,sy])
    return mp

def expand(mp,x,y,m,n):
    global startcounting1
    mine = 0
    for i in range(-1,2):
        for j in range(-1,2):
            sx,sy = x+i,y+j
            if -1<sx<m and -1<sy<n :
                if mp[sx][sy].flag == True:
                    mine += 1
    if mine == mp[x][y].status:
        for i in range(-1,2):
            for j in range(-1,2):
                sx,sy = x+i,y+j
                if -1<sx<m and -1<sy<n and mp[sx][sy].cover:
                    bfs(mp,sx,sy,m,n)
    
def main(m,n,k):
    mp = createMap(m,n,k)
    pic = [ myMap.Clock(m,n),myMap.Mine(m,n)]
    bgSize = width,height = myMap.Square.width * m,myMap.Square.height * n + 80
    tick = 0
    second = 0
    mine = k
    
    global screen
    
    screen = pygame.display.set_mode(bgSize)
    pygame.display.set_caption('扫雷')
    
    clock = pygame.time.Clock()
    gameOver = False
    global startcounting1
    startcounting1 = False
    startcounting2 = False
    count1 = 0
    count2 = 0
    lastt = 0
    lastl = (-1,-1)
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN: 
                if event.key == K_ESCAPE:  #Esc键退出
                    sys.exit()
                    pygame.quit()
                    
                #简单重启
                if event.key == K_RETURN and gameOver:
                    mp = createMap(m,n,k)
                    tick = 0
                    second = 0
                    mine = k
                    gameOver = False
                    
            if event.type ==pygame.MOUSEBUTTONUP:
                x,y = event.pos
                x,y = x // myMap.Square.width,y // myMap.Square.height
                if event.button == 1:
                    mp = bfs(mp,x,y,m,n)
                    if second - lastt<=1 and (x,y) == lastl :
                        expand(mp,x,y,m,n)
                    lastt = second
                    lastl = (x,y)
                    
                elif event.button == 3 and mp[x][y].cover == True:
                    if mp[x][y].flag:
                        mine +=1
                    else:
                        mine -= 1
                    mp[x][y].flag = not mp[x][y].flag
                    
        tick += 1
        if tick == 40:
            tick = 0
            second += 1

        #延时结束(其实很短) 防止gameover不出现或是被再次出现的方块覆盖
        if startcounting1:   
            count1 += 1
        if count1 == 5:
            count1 = 0
            gameOver = True
            startcounting1 = False
            printMessage('You Lose!',fontColor,60,(width * 0.3, height * 0.3))
            loseSound.play()
            
        if startcounting2:   
            count2 += 1
        if count2 == 5:
            count2 = 0
            gameOver = True
            startcounting2 = False
            printMessage('You Win!',fontColor,60,(width * 0.3, height * 0.3))
            winSound.play()

        if not gameOver:
            #判定胜利
            mines = 0
            for i in range(m):
                for j in range(n):
                    if mp[i][j].status == -1 and mp[i][j].flag == True:
                        mines += 1
            if mines == k:
                startcounting2 = True

            #打印地图元素
            screen.fill(bgColor)
            drawMap(mp,m,n)
            printMessage(str(second),fontColor2,50,(m * myMap.Square.width / 10 + myMap.Clock.width+10, n * myMap.Square.height + 20))
            printMessage(str(mine),fontColor2,50,(m * myMap.Square.width * 0.9- myMap.Mine.width - 50, n * myMap.Square.height + 20))

            for i in pic:
                screen.blit(i.image, i.rect)

        else:
            printMessage('Press ENTER to play again',fontColor,40,(width * 0.2, height * 0.5))
            
        pygame.display.flip()
        clock.tick(40)

if __name__ == '__main__':
    main(M,N,K)
    #createMapPlus(M,N,K)
