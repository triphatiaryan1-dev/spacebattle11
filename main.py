# SPACE BATTLE v2 - TEXTURED COLLECTABLE ITEMS + MOBILE CONTROLS
# Run: python space_battle_collect.py
import pygame, random, math, os, sys
pygame.init()
pygame.mixer.init()

W, H = 900, 540
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("SPACE BATTLE v2 - Collectables")
clock = pygame.time.Clock()

WHITE=(255,255,255); YELLOW=(255,210,0); CYAN=(0,229,255)
PINK=(255,0,85); GREEN=(0,255,136); ORANGE=(255,170,0)
RED=(255,60,60); BLUE=(0,150,255); PURPLE=(180,0,255)

HS_FILE="highscore.txt"
high = 0
if os.path.exists(HS_FILE):
    try: high = int(open(HS_FILE).read())
    except: high = 0

def beep(freq=800, dur=80):
    try:
        import numpy as np
        sr=22050
        t=np.linspace(0,dur/1000,int(sr*dur/1000),False)
        wave=(np.sin(2*np.pi*freq*t)*8000).astype(np.int16)
        snd=pygame.sndarray.make_sound(np.column_stack((wave,wave)))
        snd.play()
    except: pass

# ============ SHIP TEXTURES ============
def make_player_ship(color_main, color_wing):
    s = pygame.Surface((60,60), pygame.SRCALPHA)
    pygame.draw.polygon(s, color_wing, [(5,45),(30,25),(55,45),(30,35)])
    pygame.draw.polygon(s, color_wing, [(2,50),(30,30),(58,50),(30,42)])
    pygame.draw.polygon(s, color_main, [(30,2),(38,25),(35,50),(25,50),(22,25)])
    pygame.draw.polygon(s, (255,255,255), [(30,2),(34,18),(26,18)])
    pygame.draw.ellipse(s, CYAN, (25,20,10,16))
    pygame.draw.ellipse(s, WHITE, (27,22,4,5))
    pygame.draw.circle(s, ORANGE, (24,52), 3)
    pygame.draw.circle(s, ORANGE, (36,52), 3)
    return s

def make_enemy_ship(kind):
    s = pygame.Surface((60,60), pygame.SRCALPHA)
    if kind == "normal":
        pygame.draw.ellipse(s, (150,0,200), (10,15,40,35))
        pygame.draw.polygon(s, (100,0,150), [(5,30),(30,5),(55,30)])
        pygame.draw.circle(s, RED, (22,30), 6)
        pygame.draw.circle(s, RED, (38,30), 6)
    elif kind == "fast":
        pygame.draw.polygon(s, YELLOW, [(30,2),(45,40),(30,32),(15,40)])
        pygame.draw.polygon(s, ORANGE, [(30,10),(38,38),(30,32),(22,38)])
        pygame.draw.circle(s, WHITE, (30,25), 5)
    elif kind == "zig":
        pygame.draw.ellipse(s, GREEN, (5,22,50,18))
        pygame.draw.ellipse(s, (0,180,100), (5,28,50,12))
        pygame.draw.ellipse(s, (200,255,200), (20,8,20,20))
        pygame.draw.circle(s, (0,0,0), (26,15), 3)
        pygame.draw.circle(s, (0,0,0), (34,15), 3)
    elif kind == "tank":
        pygame.draw.rect(s, (120,120,120), (15,10,30,40))
        pygame.draw.polygon(s, (180,180,180), [(10,20),(30,5),(50,20)])
        pygame.draw.rect(s, RED, (20,15,20,10))
        pygame.draw.circle(s, YELLOW, (25,35), 4)
        pygame.draw.circle(s, YELLOW, (35,35), 4)
    elif kind == "boss":
        pygame.draw.polygon(s, (200,0,50), [(10,10),(50,10),(55,40),(30,55),(5,40)])
        pygame.draw.circle(s, YELLOW, (22,25), 7)
        pygame.draw.circle(s, YELLOW, (38,25), 7)
        pygame.draw.circle(s, (0,0,0), (22,25), 3)
        pygame.draw.circle(s, (0,0,0), (38,25), 3)
        pygame.draw.rect(s, WHITE, (20,40,20,5))
    return s

PLAYER_TEXTURES = [make_player_ship(CYAN,(0,100,255)), make_player_ship(PINK,(150,0,100)), make_player_ship(YELLOW,ORANGE)]
ENEMY_TEXTURES = {k: make_enemy_ship(k) for k in ["normal","fast","zig","tank"]}
BOSS_TEXTURE = pygame.transform.scale(make_enemy_ship("boss"), (100,100))

# ============ NEW: COLLECTABLE ITEMS TEXTURE ============
def make_collectable(kind):
    s = pygame.Surface((44,44), pygame.SRCALPHA)
    # Outer glow circle
    if kind == "double": # Double Gun - Golden Gun Box
        pygame.draw.circle(s, (255,210,0), (22,22), 20)
        pygame.draw.circle(s, (120,80,0), (22,22), 20, 2)
        pygame.draw.circle(s, (255,255,180), (22,22), 15)
        # 2 guns
        pygame.draw.rect(s, (50,50,50), (10,18,10,8))
        pygame.draw.rect(s, (50,50,50), (24,18,10,8))
        pygame.draw.rect(s, (0,0,0), (12,14,3,4))
        pygame.draw.rect(s, (0,0,0), (26,14,3,4))
        pygame.draw.circle(s, YELLOW, (22,8), 3)

    elif kind == "shield": # Shield - Blue Shield
        pygame.draw.circle(s, (0,200,255), (22,22), 20)
        pygame.draw.circle(s, (0,80,180), (22,22), 20, 2)
        pygame.draw.polygon(s, (0,120,255), [(22,6),(34,12),(34,24),(22,38),(10,24),(10,12)])
        pygame.draw.polygon(s, (180,240,255), [(22,10),(30,14),(30,24),(22,34),(14,24),(14,14)])
        pygame.draw.circle(s, WHITE, (22,22), 3)

    elif kind == "bomb": # Bomb - Black Bomb with Spark
        pygame.draw.circle(s, (255,140,0), (22,22), 20)
        pygame.draw.circle(s, (150,70,0), (22,22), 20, 2)
        pygame.draw.circle(s, (30,30,30), (22,24), 13)
        pygame.draw.circle(s, (80,80,80), (18,20), 4) # shine
        pygame.draw.rect(s, (60,60,60), (19,8,6,6))
        # spark
        pygame.draw.line(s, YELLOW, (22,8), (22,2), 2)
        pygame.draw.line(s, YELLOW, (18,9), (15,5), 2)
        pygame.draw.line(s, YELLOW, (26,9), (29,5), 2)
        pygame.draw.circle(s, YELLOW, (22,2), 2)

    elif kind == "life": # Life - Red Heart with Cross
        pygame.draw.circle(s, (255,0,85), (22,22), 20)
        pygame.draw.circle(s, (150,0,50), (22,22), 20, 2)
        # Heart shape
        pygame.draw.circle(s, WHITE, (16,18), 7)
        pygame.draw.circle(s, WHITE, (28,18), 7)
        pygame.draw.polygon(s, WHITE, [(10,22),(34,22),(22,38)])
        pygame.draw.circle(s, RED, (22,22), 4)
        pygame.draw.rect(s, RED, (20,18,4,8))
        pygame.draw.rect(s, (255,255,255), (20,20,4,1))

    elif kind == "coin": # Coin / Star - Score +50
        pygame.draw.circle(s, (255,220,0), (22,22), 20)
        pygame.draw.circle(s, (200,150,0), (22,22), 20, 2)
        pygame.draw.circle(s, (255,255,150), (22,22), 14)
        pygame.draw.circle(s, (255,200,0), (22,22), 14, 2)
        f = pygame.font.SysFont("Arial", 22, bold=True)
        txt = f.render("$", True, (150,100,0))
        s.blit(txt, (15,10))

    elif kind == "star": # Star Power - Invincible / Magnet
        pygame.draw.circle(s, PURPLE, (22,22), 20)
        pygame.draw.circle(s, (100,0,180), (22,22), 20, 2)
        # Star
        pts = []
        for i in range(10):
            ang = -math.pi/2 + i*math.pi/5
            r = 14 if i%2==0 else 6
            pts.append((22+math.cos(ang)*r, 22+math.sin(ang)*r))
        pygame.draw.polygon(s, YELLOW, pts)
        pygame.draw.polygon(s, WHITE, pts, 1)
        pygame.draw.circle(s, WHITE, (22,22), 3)
    return s

COLLECT_TEXTURES = {
    "double": make_collectable("double"),
    "shield": make_collectable("shield"),
    "bomb": make_collectable("bomb"),
    "life": make_collectable("life"),
    "coin": make_collectable("coin"),
    "star": make_collectable("star"),
}

COLLECT_INFO = {
    "double": "DOUBLE GUN!",
    "shield": "SHIELD ON!",
    "bomb": "+1 BOMB!",
    "life": "+1 LIFE!",
    "coin": "+50 SCORE!",
    "star": "STAR POWER!",
}

# ============ MOBILE CONTROLS ============
JOY_CENTER = (110, H-110)
JOY_RADIUS = 60
JOY_KNOB = 25
FIRE_BTN = pygame.Rect(W-130, H-150, 100, 100)
BOMB_BTN = pygame.Rect(W-240, H-90, 70, 70)

joy_active_id = None
joy_dx, joy_dy = 0, 0
fire_held = False
fire_touch_id = None

player = {"x":W//2, "y":H-120, "lives":3, "bombs":2}
skin_idx = 0
score=0; level=1; frame=0
bullets=[]; ebullets=[]; enemies=[]; particles=[]; powerups=[]
stars=[{"x":random.randint(0,W),"y":random.randint(0,H),"s":random.randint(1,3),"sp":random.randint(1,3)} for _ in range(90)]
boss=None; shield=False; double_until=0
game_state="menu"
flame_anim=0
collect_msg = ""
collect_msg_time = 0

def explosion(x,y,color=YELLOW,n=20):
    for _ in range(n):
        a=random.uniform(0,math.pi*2); sp=random.uniform(1,5)
        particles.append({"x":x,"y":y,"vx":math.cos(a)*sp,"vy":math.sin(a)*sp,"life":30,"color":color})
    beep(120,150)

def spawn_enemy():
    t=random.random()
    e={"x":random.randint(30,W-30),"y":-30,"hp":1,"speed":1.5+level*0.2,"type":"normal","score":10,"t":0}
    if t<0.22: e.update({"type":"fast","speed":e["speed"]+2.5,"score":20})
    elif t<0.38: e.update({"type":"zig","hp":2,"score":15})
    elif t<0.48: e.update({"type":"tank","hp":4,"speed":e["speed"]*0.6,"score":30})
    enemies.append(e)

def spawn_boss():
    global boss
    boss={"x":W//2,"y":90,"hp":30+level*8,"max":30+level*8,"dir":1,"fire":0}

def spawn_power(x,y):
    # Ab 6 tarah ke items - coin aur star bhi
    typ=random.choice(["double","shield","bomb","life","coin","coin","star"])
    powerups.append({"x":x,"y":y,"type":typ, "spin":0})

def draw_text(txt,x,y,color=WHITE,size=22):
    f=pygame.font.SysFont("Arial",size,bold=True)
    s=f.render(txt,True,color)
    screen.blit(s,(x,y))

def use_bomb():
    global boss
    if player["bombs"]<=0: return
    player["bombs"]-=1
    enemies.clear(); ebullets.clear()
    if boss: boss["hp"]-=12
    explosion(player["x"],player["y"],YELLOW,40)

def draw_mobile_controls():
    if game_state != "playing": return
    pygame.draw.circle(screen, (255,255,255), JOY_CENTER, JOY_RADIUS, 2)
    pygame.draw.circle(screen, (255,255,255), (JOY_CENTER[0]+joy_dx, JOY_CENTER[1]+joy_dy), JOY_KNOB)
    pygame.draw.circle(screen, CYAN, (JOY_CENTER[0]+joy_dx, JOY_CENTER[1]+joy_dy), JOY_KNOB-5)
    fire_color = PINK if fire_held else (180,0,60)
    pygame.draw.circle(screen, fire_color, FIRE_BTN.center, 50)
    pygame.draw.circle(screen, WHITE, FIRE_BTN.center, 50, 3)
    draw_text("FIRE", FIRE_BTN.centerx-22, FIRE_BTN.centery-10, WHITE, 20)
    pygame.draw.circle(screen, ORANGE, BOMB_BTN.center, 35)
    pygame.draw.circle(screen, WHITE, BOMB_BTN.center, 35, 2)
    draw_text("💣", BOMB_BTN.centerx-12, BOMB_BTN.centery-12, WHITE, 24)
    draw_text(f"{player['bombs']}", BOMB_BTN.centerx-5, BOMB_BTN.centery+18, WHITE, 14)

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.FINGERDOWN or event.type==pygame.MOUSEBUTTONDOWN:
            if event.type==pygame.FINGERDOWN:
                tx, ty = event.x * W, event.y * H; fid = event.finger_id
            else:
                tx, ty = event.pos; fid = -1
            if game_state=="menu":
                for i in range(3):
                    sx = W//2-110 + i*80
                    if sx <= tx <= sx+60 and 230 <= ty <= 290:
                        skin_idx=i
                if ty > 350:
                    game_state="playing"; score=0; level=1; player["lives"]=3; player["bombs"]=2
                    enemies.clear(); bullets.clear(); boss=None; powerups.clear()
            elif game_state=="over":
                if ty>250: game_state="menu"
            elif game_state=="playing":
                dist = math.hypot(tx-JOY_CENTER[0], ty-JOY_CENTER[1])
                if dist < JOY_RADIUS+20 and joy_active_id is None:
                    joy_active_id = fid
                elif math.hypot(tx-FIRE_BTN.centerx, ty-FIRE_BTN.centery) < 55:
                    fire_held=True; fire_touch_id=fid
                elif math.hypot(tx-BOMB_BTN.centerx, ty-BOMB_BTN.centery) < 40:
                    use_bomb()
        if event.type==pygame.FINGERMOTION or event.type==pygame.MOUSEMOTION:
            if event.type==pygame.FINGERMOTION:
                tx, ty = event.x * W, event.y * H; fid = event.finger_id
            else:
                if pygame.mouse.get_pressed()[0]:
                    tx, ty = event.pos; fid = -1
                else: continue
            if fid == joy_active_id:
                dx = tx - JOY_CENTER[0]; dy = ty - JOY_CENTER[1]
                d = math.hypot(dx,dy)
                if d > JOY_RADIUS:
                    dx = dx/d*JOY_RADIUS; dy = dy/d*JOY_RADIUS
                joy_dx, joy_dy = dx, dy
        if event.type==pygame.FINGERUP or event.type==pygame.MOUSEBUTTONUP:
            fid = event.finger_id if event.type==pygame.FINGERUP else -1
            if fid == joy_active_id:
                joy_active_id=None; joy_dx, joy_dy=0,0
            if fid == fire_touch_id:
                fire_held=False; fire_touch_id=None
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_1: skin_idx=0
            if event.key==pygame.K_2: skin_idx=1
            if event.key==pygame.K_3: skin_idx=2
            if event.key==pygame.K_b: use_bomb()
            if event.key==pygame.K_SPACE and game_state=="menu":
                game_state="playing"; score=0; level=1; player["lives"]=3; player["bombs"]=2
                enemies.clear(); bullets.clear(); boss=None
            if event.key==pygame.K_r and game_state=="over":
                game_state="menu"

    screen.fill((5,1,15))
    for s in stars:
        s["y"]+=s["sp"]
        if s["y"]>H: s["y"]=0; s["x"]=random.randint(0,W)
        pygame.draw.circle(screen,(180,180,255),(s["x"],s["y"]),s["s"])

    if game_state=="menu":
        draw_text("SPACE BATTLE v2",W//2-180,80,CYAN,48)
        draw_text("Collect Items - Win Game!",W//2-150,140,YELLOW,20)
        draw_text(f"HIGH SCORE: {high}",W//2-90,175,YELLOW,22)
        for i, tex in enumerate(PLAYER_TEXTURES):
            screen.blit(tex, (W//2-110 + i*80, 230))
            draw_text(f"{i+1}", W//2-90 + i*80, 295, WHITE, 20)
        # Collectables preview in menu
        draw_text("COLLECTABLES:", W//2-80, 330, WHITE, 16)
        for i, k in enumerate(["double","shield","bomb","life","coin","star"]):
            screen.blit(pygame.transform.scale(COLLECT_TEXTURES[k], (32,32)), (W//2-160 + i*55, 355))
        draw_text("TAP BELOW TO PLAY  ▶",W//2-130,410,PINK,28)
        draw_text("Left Joystick = Move | Right FIRE = Shoot",W//2-200,460,WHITE,16)

    elif game_state=="playing":
        frame+=1; flame_anim+=1
        keys=pygame.key.get_pressed()
        sp=6
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: player["x"]-=sp
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: player["x"]+=sp
        if keys[pygame.K_w] or keys[pygame.K_UP]: player["y"]-=sp
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: player["y"]+=sp
        if joy_dx!=0 or joy_dy!=0:
            player["x"] += joy_dx / JOY_RADIUS * sp
            player["y"] += joy_dy / JOY_RADIUS * sp
        player["x"]=max(24,min(W-24,player["x"])); player["y"]=max(60,min(H-60,player["y"]))

        if (keys[pygame.K_SPACE] or fire_held) and frame%8==0:
            bullets.append({"x":player["x"],"y":player["y"]-24,"vx":0})
            if pygame.time.get_ticks()<double_until:
                bullets.append({"x":player["x"]-14,"y":player["y"]-10,"vx":-1})
                bullets.append({"x":player["x"]+14,"y":player["y"]-10,"vx":1})
            beep(880,40)

        if frame%max(22,55-level*4)==0: spawn_enemy()
        if frame%900==0 and frame>0 and not boss:
            level+=1
            if level%5==0: spawn_boss()

        for e in enemies[:]:
            if e["type"]=="zig":
                e["t"]+=1; e["x"]+=math.sin(e["t"]/12)*3
            e["y"]+=e["speed"]
            screen.blit(ENEMY_TEXTURES[e["type"]], (e["x"]-30, e["y"]-30))
            if random.random()<0.004: ebullets.append({"x":e["x"],"y":e["y"]+20,"vx":0})
            if abs(e["x"]-player["x"])<32 and abs(e["y"]-player["y"])<32:
                enemies.remove(e)
                if shield: shield=False
                else: player["lives"]-=1; explosion(player["x"],player["y"],PINK)
            if e["y"]>H+50 and e in enemies: enemies.remove(e)

        if boss:
            boss["x"]+=boss["dir"]*2
            if boss["x"]<80 or boss["x"]>W-80: boss["dir"]*=-1
            boss["fire"]+=1
            if boss["fire"]%40==0:
                for a in [-1,0,1]: ebullets.append({"x":boss["x"]+a*20,"y":boss["y"]+30,"vx":a*1.2})
            screen.blit(BOSS_TEXTURE, (boss["x"]-50, boss["y"]-50))
            pygame.draw.rect(screen,(50,50,50),(20,10,W-40,12))
            pygame.draw.rect(screen,PINK,(20,10,(W-40)*boss["hp"]/boss["max"],12))
            draw_text("BOSS FIGHT!",W//2-60,28,PINK,16)
            if abs(boss["x"]-player["x"])<70 and abs(boss["y"]-player["y"])<60:
                if shield: shield=False
                else: player["lives"]-=1

        for b in bullets[:]:
            b["y"]-=9; b["x"]+=b["vx"]
            pygame.draw.circle(screen,CYAN,(int(b["x"]),int(b["y"])),5)
            for e in enemies[:]:
                if abs(b["x"]-e["x"])<22 and abs(b["y"]-e["y"])<22:
                    if b in bullets: bullets.remove(b)
                    e["hp"]-=1
                    if e["hp"]<=0:
                        enemies.remove(e); score+=e["score"]; explosion(e["x"],e["y"])
                        if random.random()<0.25: spawn_power(e["x"],e["y"])
                    break
            if boss and abs(b["x"]-boss["x"])<55 and abs(b["y"]-boss["y"])<40:
                if b in bullets: bullets.remove(b)
                boss["hp"]-=1
                if boss["hp"]<=0:
                    score+=200; explosion(boss["x"],boss["y"],PINK,50); boss=None; level+=1
            if b["y"]<0 and b in bullets: bullets.remove(b)

        for b in ebullets[:]:
            b["y"]+=4; b["x"]+=b.get("vx",0)
            pygame.draw.circle(screen,PINK,(int(b["x"]),int(b["y"])),5)
            if abs(b["x"]-player["x"])<22 and abs(b["y"]-player["y"])<22:
                ebullets.remove(b)
                if shield: shield=False
                else: player["lives"]-=1; explosion(player["x"],player["y"],PINK)
            if b["y"]>H and b in ebullets: ebullets.remove(b)

        # ============ COLLECTABLES - TEXTURE + ANIMATION ============
        for p in powerups[:]:
            p["y"]+=1.8
            p["spin"]+=0.08
            # Floating + Glow effect
            bob = math.sin(p["spin"]*3)*4
            scale = 1 + math.sin(p["spin"]*2)*0.1
            tex = COLLECT_TEXTURES[p["type"]]
            # Glow circle
            pygame.draw.circle(screen, (255,255,255), (int(p["x"]), int(p["y"]+bob)), 26, 1)
            scaled = pygame.transform.scale(tex, (int(44*scale), int(44*scale)))
            screen.blit(scaled, (p["x"]-22*scale, p["y"]+bob-22*scale))

            if abs(p["x"]-player["x"])<32 and abs(p["y"]-player["y"])<32:
                powerups.remove(p); beep(990,100)
                collect_msg = COLLECT_INFO[p["type"]]
                collect_msg_time = frame
                explosion(p["x"], p["y"], GREEN, 10)
                if p["type"]=="double": double_until=pygame.time.get_ticks()+12000
                elif p["type"]=="shield": shield=True
                elif p["type"]=="bomb": player["bombs"]+=1
                elif p["type"]=="life": player["lives"]=min(5,player["lives"]+1)
                elif p["type"]=="coin": score+=50
                elif p["type"]=="star": score+=100; player["lives"]=min(5,player["lives"]+1)
            if p["y"]>H and p in powerups: powerups.remove(p)

        for pt in particles[:]:
            pt["x"]+=pt["vx"]; pt["y"]+=pt["vy"]; pt["life"]-=1
            pygame.draw.circle(screen,pt["color"],(int(pt["x"]),int(pt["y"])),3)
            if pt["life"]<=0: particles.remove(pt)

        if shield: pygame.draw.circle(screen,GREEN,(player["x"],player["y"]),38,3)
        flame_len = 12 + math.sin(flame_anim/3)*6
        pygame.draw.polygon(screen, ORANGE, [(player["x"]-8, player["y"]+28),(player["x"]+8, player["y"]+28),(player["x"], player["y"]+28+flame_len)])
        pygame.draw.polygon(screen, YELLOW, [(player["x"]-4, player["y"]+28),(player["x"]+4, player["y"]+28),(player["x"], player["y"]+28+flame_len-6)])
        screen.blit(PLAYER_TEXTURES[skin_idx], (player["x"]-30, player["y"]-30))

        draw_text(f"SCORE: {score}",10,10,YELLOW)
        draw_text(f"LIVES: {player['lives']}  LVL: {level}",W//2-80,10,WHITE)
        draw_text(f"HIGH: {max(high,score)}",W-120,10,YELLOW)

        # Collect hone pe message dikhao
        if frame - collect_msg_time < 60 and collect_msg:
            draw_text(collect_msg, W//2-70, H//2-80, GREEN, 26)

        draw_mobile_controls()

        if player["lives"]<=0:
            if score>high:
                high=score; open(HS_FILE,"w").write(str(high))
            game_state="over"

    elif game_state=="over":
        draw_text("GAME OVER",W//2-140,180,PINK,48)
        draw_text(f"Score: {score}",W//2-60,250,YELLOW,28)
        draw_text(f"High Score: {high}",W//2-80,290,YELLOW,22)
        draw_text("TAP TO GO TO MENU",W//2-110,350,WHITE,20)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
