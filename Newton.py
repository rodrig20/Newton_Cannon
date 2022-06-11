from math import hypot, cos, sin, acos, pi, degrees
import pygame
import random

pygame.init()

lar = 1340
alt = 660

planeta = 275
tam = 6

m = 1

rel = pygame.time.Clock()
fundo = pygame.display.set_mode([lar,alt],pygame.RESIZABLE)
pygame.display.set_caption('Screen')
font = pygame.font.SysFont(None,30)
background = pygame.Surface(fundo.get_size())
background = background.convert()

terra_o = pygame.image.load(r'Jogos\Newton\Terra.png').convert_alpha()
terra = pygame.transform.scale(terra_o, (planeta*2,planeta*2))
planeta = terra.get_rect().center[0]

def texto(v,a):
    texto1 = font.render(f'Velocidade Inicial: {v}',True,(245,66,66))
    fundo.blit(texto1,(0+5,30))
    texto1 = font.render(f'Altura Inicial: {a}',True,(245,66,66))
    fundo.blit(texto1,(0+5,0+5))

def gravitação(distancia):
    f = (6.67*(10**-11))*((5.972*(10**14)*m))/(distancia*distancia)
    return f

def acel(total_f,distancia,x1,x2):
    global mx, my, px, py

    x = (x1-x2)

    ang1 = acos(x/distancia)

    if px >= mx and py <= my:
        ang = ang1
    elif px >= mx and py >= my:
        ang = 2*pi - ang1
    elif px <= mx and py <= my:
        ang = ang1
    elif px <= mx and py >= my:
        ang = 2*pi - ang1
    
    fx = -1*total_f*(cos(ang))
    fy = 1*total_f*(sin(ang))

    return fx, fy, degrees(ang)

chao = alt/2 - planeta - tam
vi = 10
ai = 0
shift = False

mx, my = lar/2,alt/2
project_pos = (lar/2,chao)
px,py = project_pos

ns = 300
stars = [[random.randint(0, lar),random.randint(0, alt)]for x in range(ns)]

estrelas = False
line = True

velx = 0
vely = 0
acelx = 0
acely = 0

zoom = 1

vx = 0
vy = 0
vectorx = 0
vectory = 0
vecx = 0
vecy = 0
scroll = 15
z = 0
 
p = 1
sim = 0

angle_1 = 90
angle_2 = 0

pontos = []

start = 0
stop = 0
run = True
restart = False

while run:
    tmp_z = zoom
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEWHEEL:
            zoom += event.y * 0.008
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_RETURN:
                restart = True
            if event.key == pygame.K_LSHIFT:
                shift = True
            if event.key == pygame.K_LEFT:
                vx += scroll
                vectorx = scroll
            if event.key == pygame.K_RIGHT:
                vx += -scroll
                vectorx = -scroll
            if event.key == pygame.K_UP:
                vy += scroll
                vectory = scroll
            if event.key == pygame.K_DOWN:
                vy += -scroll
                vectory = -scroll
            if event.key == pygame.K_w:
                if start == 0:
                    if shift == False:
                        vi += 0.2
                    elif shift == True:
                        ai -= 5
                        py -= 5     
            if event.key == pygame.K_s:
                if start == 0:
                    if shift == False:
                        vi -= 0.2
                    elif shift == True and not -ai <= 0:
                        ai += 5
                        py += 5
            if event.key == pygame.K_l:
                line = not line
            if event.key == pygame.K_m:
                z += -0.01
            if event.key == pygame.K_n:
                z += 0.01
            if event.key == pygame.K_e:
                estrelas = not estrelas   
            if event.key == pygame.K_SPACE:
                if start == 0:
                    start = 1
                    velx = round(vi,2)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                shift = False
            if event.key == pygame.K_LEFT:
                vx -= scroll
                vectorx = 0
            if event.key == pygame.K_RIGHT:
                vx -= -scroll
                vectorx = 0
            if event.key == pygame.K_UP:
                vy -= scroll
                vectory = 0
            if event.key == pygame.K_DOWN:
                vy -= -scroll
                vectory = 0
            if event.key == pygame.K_m:
                z -= -0.01
            if event.key == pygame.K_n:
                z -= 0.01

    background.fill((0,0,0))
    fundo.fill((0,0,0))
    for star in stars:
        pygame.draw.line(background,
            (255, 255, 255), (star[0], star[1]), (star[0], star[1]))
        if estrelas == True:
            star[0] = star[0] - 0.2
            if star[0] < 0:
                star[0] = lar
                star[1] = random.randint(0, alt)
    fundo.blit(background, (0,0))
    vecx += vectorx
    vecy += vectory
    mx += vx
    my += vy   
    zoom += z
    if planeta*2*zoom <= 0:
        zoom = tmp_z
    if tmp_z != zoom:
        terra = pygame.transform.scale(terra_o, (planeta*2*zoom,planeta*2*zoom))

    vi = round(vi,2)

    if start == True:
        if angle_1 > 90 and angle_2 <= 90:
            p = 0
            if sim != 100:
                sim = 99
        if p == 1 and sim != 0:
            sim -= 1
        if p == 1 and sim == 0:
            sim = 3
            pontos.append([px,py])
        if sim == 99:
            sim = 100
            pontos.append([px,py])
     
        t = 0
        for ponto in pontos:
            if t == 0:
                t = 1
                lx = ponto[0] + vx
                ly = ponto[1] + vy
            ponto[0] += vx
            ponto[1] += vy
            if line == True:
                pygame.draw.lines(fundo,(200,0,0),False,[(lx*zoom,ly*zoom),(ponto[0]*zoom,ponto[1]*zoom)])
            lx = ponto[0]
            ly = ponto[1]

    px += vx
    py += vy   

    fundo.blit(terra,((mx*zoom)-(planeta*zoom),(my*zoom)-(planeta*zoom)))
    d = hypot(px-mx,py-my)
    
    if start == 1:
        forca = gravitação(d)

        ax, ay, angl= acel(forca,d,px,mx)

        angle_1, angle_2 = angle_2, angl

        acelx = ax/m
        acely = ay/m
              
        velx += acelx
        vely += acely
            
        if d < planeta + tam: 
            velx = acelx = 0
            vely = acely = 0
            
        px += velx
        py += vely

        d = hypot(px-mx,py-my)
        if d <= planeta + tam:
            px -= velx
            py -= vely
            if stop == 0:
                r = velx / vely
                stop = 1
                while True:
                    d = hypot(px-mx,py-my)
                    px += r
                    py += 1
                    if d <= planeta + tam: 
                        break

        pygame.draw.circle(fundo,(100,100,100), (px*zoom,py*zoom), tam*zoom)
    
    else:
        pygame.draw.circle(fundo,(100,100,100), (px*zoom,(py)*zoom), tam*zoom)
    
    if restart == True:
        px,py = (lar/2+vecx,chao+vecy+ai)
        velx = 0
        vely = 0
        acelx = 0
        acely = 0

        vx = 0
        vy = 0
        scroll = 15
        z = 0
        
        p = 1
        sim = 0

        angle_1 = 90
        angle_2 = 0

        pontos = []

        start = 0
        stop = 0
        restart = False
        continue
    
    texto(vi,-ai)
    pygame.display.update()
    rel.tick(50)