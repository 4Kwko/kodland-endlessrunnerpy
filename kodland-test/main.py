WIDTH = 720
HEIGHT = 360
TITLE = "Kodland - Endless Runner"

from pgzero.actor import Actor
from pygame import Rect
import random

BG_SPEED = 180.0
GROUND_SPEED = 260.0
GRAVITY = 2600.0
JUMP_V = -1000.0

bg1 = Actor("bg_layer1", (WIDTH // 2, HEIGHT // 2))
bg2 = Actor("bg_layer1", (WIDTH + WIDTH // 2, HEIGHT // 2))

hero_run = ["run000","run001","run002","run003","run004","run005","run006","run007","run008","run009"]
hero_slide = ["slide000","slide001"]
hero_jump = ["jump000","jump001","jump002"]
fireball_frames = ["fireball000","fireball001","fireball002","fireball003"]

hero = Actor(hero_run[0])
hero.pos = (220, HEIGHT - 120)
hero_rect = Rect(hero.x - 12, hero.y - 36, 24, 36)

state = "run"
vy = 0.0
frame = 0
timer = 0.0
FRAME_RUN = 0.08
FRAME_JUMP = 0.10
FRAME_SLIDE = 0.14

ground_y = HEIGHT - 80
ground_h = 24
ground1 = Rect(0, ground_y, WIDTH, ground_h)
ground2 = Rect(WIDTH, ground_y, WIDTH, ground_h)

SPIKE_IMG = "spikes000"
spikes = []
spawn_timer = 0.0
spawn_interval = 2.0

FIREBALL_SPEED = 320.0
fireballs = []
fb_spawn_timer = 0.0
fb_spawn_interval = 1.8
fb_anim_timer = 0.0
FB_FRAME_DELAY = 0.08
fb_frame_index = 0

SAFE_GAP_X = 120
score = 0

game_state = "menu"
music_on = True
hover_btn = None

def draw_round_rect(r: Rect, color, radius=16):
    screen.draw.filled_rect(Rect(r.left+radius, r.top, r.width-2*radius, r.height), color)
    screen.draw.filled_rect(Rect(r.left, r.top+radius, radius, r.height-2*radius), color)
    screen.draw.filled_rect(Rect(r.right-radius, r.top+radius, radius, r.height-2*radius), color)
    screen.draw.filled_circle((r.left+radius, r.top+radius), radius, color)
    screen.draw.filled_circle((r.right-radius, r.top+radius), radius, color)
    screen.draw.filled_circle((r.left+radius, r.bottom-radius), radius, color)
    screen.draw.filled_circle((r.right-radius, r.bottom-radius), radius, color)

class Button:
    def __init__(self, x, y, w, h, label, on_click):
        self.rect = Rect(x, y, w, h)
        self.label = label
        self.on_click = on_click
        self.hover = False
    def draw(self):
        base = (52, 52, 84) if not self.hover else (76, 76, 132)
        shadow = Rect(self.rect.x, self.rect.y+3, self.rect.w, self.rect.h)
        draw_round_rect(shadow, (12, 12, 20), 14)
        draw_round_rect(self.rect, base, 14)
        screen.draw.text(self.label, center=self.rect.center, fontsize=26, color="white")

def reset_game():
    global spikes, fireballs, spawn_timer, fb_spawn_timer, score, vy, state, frame, timer
    spikes = []
    fireballs = []
    spawn_timer = 0.0
    fb_spawn_timer = 0.0
    score = 0
    vy = 0.0
    state = "run"
    frame = 0
    timer = 0.0
    hero_rect.width, hero_rect.height = 24, 36
    hero_rect.centerx = 220
    hero_rect.bottom = ground_y
    hero.pos = (hero_rect.centerx, hero_rect.bottom - hero.height // 2)
    bg1.x, bg2.x = WIDTH // 2, WIDTH + WIDTH // 2
    ground1.x, ground2.x = 0, WIDTH

def start_game():
    global game_state
    reset_game()
    if music_on:
        try:
            music.play("game_theme")
            music.set_volume(0.6)
        except Exception:
            pass
    game_state = "game"

def toggle_music():
    global music_on
    music_on = not music_on
    btn_music.label = "Music: ON" if music_on else "Music: OFF"
    if music_on:
        try:
            music.play("menu_theme" if game_state == "menu" else "game_theme")
            music.set_volume(0.6)
        except Exception:
            pass
    else:
        music.stop()

def do_exit():
    exit()

btn_w, btn_h = 200, 44
cx = WIDTH // 2
start_y = HEIGHT // 2 - 72
btn_start = Button(cx - btn_w // 2, start_y,          btn_w, btn_h, "Start Game", start_game)
btn_music = Button(cx - btn_w // 2, start_y + 56,     btn_w, btn_h, "Music: ON", toggle_music)
btn_exit  = Button(cx - btn_w // 2, start_y + 112,    btn_w, btn_h, "Exit", do_exit)
menu_buttons = [btn_start, btn_music, btn_exit]

def make_spike_group(x):
    group = []
    s0 = Actor(SPIKE_IMG)
    tile_w = s0.width - 2
    for i in range(5):
        s = Actor(SPIKE_IMG)
        s.pos = (x + i * tile_w, ground_y - s.height / 2)
        group.append(s)
    return group

def make_fireball(x):
    fb = Actor(fireball_frames[0])
    fb.pos = (x, ground_y - 120)
    return fb

def can_spawn_fireball_at(x):
    for s in spikes:
        if abs(s.x - x) < (s.width + SAFE_GAP_X):
            return False
    return True

def draw_game():
    screen.clear()
    bg1.draw()
    bg2.draw()
    screen.draw.filled_rect(ground1, (70, 70, 90))
    screen.draw.filled_rect(ground2, (70, 70, 90))
    for s in spikes:
        s.draw()
    for fb in fireballs:
        fb.draw()
    hero.draw()
    screen.draw.text(f"SCORE {int(score)}", (12, 10), fontsize=24, color="white")

def draw_menu():
    draw_game()
    screen.draw.text("KODLAND - ENDLESS RUNNER", center=(WIDTH//2, HEIGHT//2 - 140), fontsize=44, color="white")
    for b in menu_buttons:
        b.draw()

def update_menu(dt):
    pass

def draw():
    if game_state == "menu":
        draw_menu()
        return
    draw_game()

def update(dt):
    if game_state == "menu":
        update_menu(dt)
        return
    global vy, state, frame, timer, spawn_timer, spawn_interval, score
    global fb_spawn_timer, fb_spawn_interval, fb_anim_timer, fb_frame_index

    bg1.x -= BG_SPEED * dt
    bg2.x -= BG_SPEED * dt
    if bg1.right < 0:
        bg1.x = bg2.x + WIDTH
    if bg2.right < 0:
        bg2.x = bg1.x + WIDTH

    ground1.x -= GROUND_SPEED * dt
    ground2.x -= GROUND_SPEED * dt
    if ground1.right < 0:
        ground1.x = ground2.x + WIDTH
    if ground2.right < 0:
        ground2.x = ground1.x + WIDTH

    spawn_timer += dt
    if spawn_timer >= spawn_interval:
        spawn_timer = 0.0
        spawn_interval = random.uniform(2.0, 3.0)
        spikes.extend(make_spike_group(WIDTH + 60))

    for s in spikes:
        s.x -= GROUND_SPEED * dt
    spikes[:] = [s for s in spikes if s.right > 0]

    fb_spawn_timer += dt
    if fb_spawn_timer >= fb_spawn_interval:
        fb_spawn_timer = 0.0
        fb_spawn_interval = random.uniform(1.6, 2.6)
        x_try = WIDTH + 40
        attempts = 0
        while attempts < 6 and not can_spawn_fireball_at(x_try):
            x_try += 60
            attempts += 1
        if can_spawn_fireball_at(x_try):
            fireballs.append(make_fireball(x_try))

    for fb in fireballs:
        fb.x -= FIREBALL_SPEED * dt
    fireballs[:] = [fb for fb in fireballs if fb.right > 0]

    fb_anim_timer += dt
    if fb_anim_timer >= FB_FRAME_DELAY:
        fb_anim_timer = 0.0
        fb_frame_index = (fb_frame_index + 1) % len(fireball_frames)
        for fb in fireballs:
            fb.image = fireball_frames[fb_frame_index]

    on_ground = hero_rect.bottom >= ground_y
    if (keyboard.space or keyboard.up or keyboard.w) and on_ground:
        vy = JUMP_V
        state = "jump"
        frame = 0
        timer = 0.0
    if (keyboard.down or keyboard.s) and on_ground:
        state = "slide"
    elif on_ground and state != "jump":
        state = "run"

    vy += GRAVITY * dt
    hero_rect.y += int(vy * dt)
    if hero_rect.bottom > ground_y:
        hero_rect.bottom = ground_y
        vy = 0.0
        if state == "jump":
            state = "run"

    if state == "slide":
        hero_rect.height = 34
    else:
        hero_rect.height = 48
    hero_rect.width = 24
    hero_rect.centerx = 220
    hero.pos = (hero_rect.centerx, hero_rect.bottom - hero.height // 2)

    hit = False
    for s in spikes:
        srect = Rect(int(s.left), int(s.top), int(s.width), int(s.height))
        if hero_rect.colliderect(srect):
            hit = True
            break
    if not hit:
        for fb in fireballs:
            fbrect = Rect(int(fb.left + fb.width * 0.25),
                          int(fb.top + fb.height * 0.25),
                          int(fb.width * 0.5),
                          int(fb.height * 0.5))
            if hero_rect.colliderect(fbrect) and state != "slide":
                hit = True
                break

    if hit:
        score = 0
        spikes.clear()
        fireballs.clear()
        spawn_timer = 0.0
        fb_spawn_timer = 0.0
        hero_rect.bottom = ground_y
        state = "run"
        vy = 0.0
        if frame != 0:
            frame = 0
        hero.image = hero_run[0]

    timer += dt
    if state == "run":
        if timer >= FRAME_RUN:
            timer = 0.0
            frame = (frame + 1) % len(hero_run)
            hero.image = hero_run[frame]
    elif state == "slide":
        if timer >= FRAME_SLIDE:
            timer = 0.0
            frame = (frame + 1) % len(hero_slide)
            hero.image = hero_slide[frame]
    else:
        if timer >= FRAME_JUMP and frame < len(hero_jump) - 1:
            timer = 0.0
            frame += 1
        hero.image = hero_jump[frame]

    score += dt * 10

def on_mouse_move(pos):
    global hover_btn
    if game_state != "menu":
        return
    hover_btn = None
    for b in menu_buttons:
        b.hover = b.rect.collidepoint(pos)
        if b.hover:
            hover_btn = b

def on_mouse_down(pos, button):
    if game_state != "menu":
        return
    for b in menu_buttons:
        if b.rect.collidepoint(pos):
            b.on_click()

if music_on:
    try:
        music.play("menu_theme")
        music.set_volume(0.6)
    except Exception:
        pass
