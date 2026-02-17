import pygame
import random
import time
from collections import deque
import heapq

pygame.init()

WIDTH = 600
ROWS = 20
CELL = WIDTH // ROWS
TOP = 80

WIN = pygame.display.set_mode((WIDTH, WIDTH+TOP))
pygame.display.set_caption("GOOD PERFORMANCE TIME APP")

FONT = pygame.font.SysFont("arial",20)

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (128,0,128)
GRAY = (200,200,200)

grid = [[0 for _ in range(ROWS)] for _ in range(ROWS)]

start = (0,0)
end = (ROWS-1,ROWS-1)

for i in range(ROWS):
    for j in range(ROWS):
        if random.random() < 0.2:
            grid[i][j] = 1

grid[start[0]][start[1]] = 0
grid[end[0]][end[1]] = 0

dirs = [(-1,0),(0,1),(1,0),(1,1),(0,-1),(-1,-1),(1,-1),(-1,1)]

current_algo = "BFS"
final_path = []

def draw(open_set, closed_set, path):
    WIN.fill(WHITE)

    pygame.draw.rect(WIN, GRAY, (0,0,WIDTH,TOP))
    menu = [
        "1 = BFS    2 = DFS    3 = UCS",
        "4 = DLS    5 = IDDFS  6 = BIDIRECTIONAL",
        "SPACE = RUN   |   Current: "+current_algo
    ]
    for i,t in enumerate(menu):
        txt = FONT.render(t, True, BLACK)
        WIN.blit(txt,(10,10+i*20))

    pygame.draw.rect(WIN, BLACK, (0,TOP,WIDTH,WIDTH),2)

    for i in range(ROWS):
        for j in range(ROWS):
            x = j*CELL
            y = i*CELL + TOP
            r = pygame.Rect(x,y,CELL,CELL)
            if grid[i][j] == 1:
                pygame.draw.rect(WIN, BLACK, r)
            else:
                pygame.draw.rect(WIN, GRAY, r,1)

    for x,y in open_set:
        pygame.draw.rect(WIN, YELLOW,(y*CELL, x*CELL+TOP, CELL, CELL))
    for x,y in closed_set:
        pygame.draw.rect(WIN, BLUE,(y*CELL, x*CELL+TOP, CELL, CELL))
    for x,y in path:
        pygame.draw.rect(WIN, PURPLE,(y*CELL, x*CELL+TOP, CELL, CELL))

    pygame.draw.rect(WIN, GREEN,(start[1]*CELL,start[0]*CELL+TOP,CELL,CELL))
    pygame.draw.rect(WIN, RED,(end[1]*CELL,end[0]*CELL+TOP,CELL,CELL))

    pygame.display.update()
    time.sleep(0.05)

def spawn_obstacle():
    if random.random() < 0.05:
        x = random.randint(0,ROWS-1)
        y = random.randint(0,ROWS-1)
        if grid[x][y] == 0 and (x,y)!=start and (x,y)!=end:
            grid[x][y] = 1

def reconstruct(p,parent):
    path=[]
    while p in parent:
        path.append(p)
        p=parent[p]
    return path

def bfs():
    q=deque([start])
    parent={}
    open_set=[start]
    closed=[]
    while q:
        spawn_obstacle()
        n=q.popleft()
        open_set.remove(n)
        closed.append(n)
        if n==end:
            return reconstruct(n,parent)
        for dx,dy in dirs:
            x=n[0]+dx
            y=n[1]+dy
            if 0<=x<ROWS and 0<=y<ROWS and grid[x][y]==0:
                if (x,y) not in parent and (x,y)!=start:
                    parent[(x,y)]=n
                    q.append((x,y))
                    open_set.append((x,y))
        draw(open_set,closed,final_path)
    return []

def dfs():
    stack=[start]
    parent={}
    open_set=[start]
    closed=[]
    while stack:
        spawn_obstacle()
        n=stack.pop()
        open_set.remove(n)
        closed.append(n)
        if n==end:
            return reconstruct(n,parent)
        for dx,dy in dirs:
            x=n[0]+dx
            y=n[1]+dy
            if 0<=x<ROWS and 0<=y<ROWS and grid[x][y]==0:
                if (x,y) not in parent and (x,y)!=start:
                    parent[(x,y)]=n
                    stack.append((x,y))
                    open_set.append((x,y))
        draw(open_set,closed,final_path)
    return []

def ucs():
    pq=[]
    heapq.heappush(pq,(0,start))
    parent={}
    cost={start:0}
    open_set=[start]
    closed=[]
    while pq:
        spawn_obstacle()
        c,n=heapq.heappop(pq)
        if n in open_set:
            open_set.remove(n)
        closed.append(n)
        if n==end:
            return reconstruct(n,parent)
        for dx,dy in dirs:
            x=n[0]+dx
            y=n[1]+dy
            if 0<=x<ROWS and 0<=y<ROWS and grid[x][y]==0:
                new=c+1
                if (x,y) not in cost or new<cost[(x,y)]:
                    cost[(x,y)]=new
                    parent[(x,y)]=n
                    heapq.heappush(pq,(new,(x,y)))
                    open_set.append((x,y))
        draw(open_set,closed,final_path)
    return []

def dls(limit):
    stack=[(start,0)]
    parent={}
    open_set=[start]
    closed=[]
    while stack:
        spawn_obstacle()
        n,d=stack.pop()
        open_set.remove(n)
        closed.append(n)
        if n==end:
            return reconstruct(n,parent)
        if d<limit:
            for dx,dy in dirs:
                x=n[0]+dx
                y=n[1]+dy
                if 0<=x<ROWS and 0<=y<ROWS and grid[x][y]==0:
                    if (x,y) not in parent and (x,y)!=start:
                        parent[(x,y)]=n
                        stack.append(((x,y),d+1))
                        open_set.append((x,y))
        draw(open_set,closed,final_path)
    return []

def iddfs():
    for i in range(1,ROWS*ROWS):
        p=dls(i)
        if p:
            return p
    return []

def bidirectional():
    q1=deque([start])
    q2=deque([end])
    p1={}
    p2={}
    v1={start}
    v2={end}
    while q1 and q2:
        spawn_obstacle()
        a=q1.popleft()
        b=q2.popleft()
        for dx,dy in dirs:
            x=a[0]+dx
            y=a[1]+dy
            if 0<=x<ROWS and 0<=y<ROWS and grid[x][y]==0:
                if (x,y) not in v1:
                    p1[(x,y)]=a
                    v1.add((x,y))
                    q1.append((x,y))
                    if (x,y) in v2:
                        return reconstruct((x,y),p1)+reconstruct((x,y),p2)
        for dx,dy in dirs:
            x=b[0]+dx
            y=b[1]+dy
            if 0<=x<ROWS and 0<=y<ROWS and grid[x][y]==0:
                if (x,y) not in v2:
                    p2[(x,y)]=b
                    v2.add((x,y))
                    q2.append((x,y))
                    if (x,y) in v1:
                        return reconstruct((x,y),p1)+reconstruct((x,y),p2)
        draw(list(v1),list(v2),final_path)
    return []

algo = bfs

run=True
while run:
    draw([],[],final_path)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_1:
                algo=bfs; current_algo="BFS"
            if event.key==pygame.K_2:
                algo=dfs; current_algo="DFS"
            if event.key==pygame.K_3:
                algo=ucs; current_algo="UCS"
            if event.key==pygame.K_4:
                algo=lambda:dls(30); current_algo="DLS"
            if event.key==pygame.K_5:
                algo=iddfs; current_algo="IDDFS"
            if event.key==pygame.K_6:
                algo=bidirectional; current_algo="BIDIRECTIONAL"
            if event.key==pygame.K_SPACE:
                final_path=[]
                final_path = algo()

pygame.quit()