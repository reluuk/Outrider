import pygame
import random
import math
import os  # Für das Erstellen von Verzeichnissen und Dateipfade
import datetime  # Für den Zeitstempel der Highscore-Datei

pygame.init()  # Pygame initialisieren
pygame.mixer.init()  # Mixer initialisieren für Sounds

# Spiel-Fenster-Einstellungen: Passt die Fenstergröße dynamisch an, aber im Fenstermodus
info = pygame.display.Info()  # Ermittelt die Bildschirmauflösung
SCREEN_SCALE = 0.9  # Fenster soll 90% der Bildschirmgröße sein
WIDTH, HEIGHT = int(info.current_w * SCREEN_SCALE), int(info.current_h * SCREEN_SCALE)  # Setze die Breite und Höhe
PLAY_AREA_HEIGHT = int(HEIGHT * 0.9)  # Untere 90% des Bildschirms sind die Spielfläche
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)  # Fenster mit veränderbarer Größe
pygame.display.set_caption("Outrider")

# Farben
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BlueViolet = (138, 43, 226)
DarkRed = (139, 0, 0)
DarkMagenta = (139, 0, 139)
Gold = (255, 215, 0)
Magenta = (255, 0, 255)
Purple = (160, 32, 240)
Turquoise = (0, 245, 255)
GroundPause = (19, 19, 76)  # (64, 64, 151)
GroundStar = (179, 179, 0)  # (205, 205, 0)
GroundStart = (0, 0, 37)
Backgroundspace = (19, 19, 39)

# Spieler Einstellungen
PLAYER_WIDTH, PLAYER_HEIGHT = 85, 75
PLAYER_SPEED = 10
MAX_HP = 10
START_HP = 10
IMMUNE_TIME = 1000  # 1 Sekunden in Millisekunden

# Spieler-Schuss Einstellungen
BULLET_SPEED = 10
MAX_BULLETS = 5
SHOOT_COOLDOWN = 200  # Millisekunden zwischen Schüssen

# Hindernisse Einstellungen (Asteroid)
ASTEROID_WIDTH, ASTEROID_HEIGHT = 70, 85
OBSTACLE_SPEED = 6
OBSTACLE_FREQUENCY = (1500 + random.randint(0, 1000))  # Millisekunden zwischen Hindernissen

# Gegner1 Einstellungen
ENEMYSHIP1_WIDTH, ENEMYSHIP1_HEIGHT = 60, 75
ENEMYSHIP1_SPEED = 3
ENEMYSHIP1_BULLET_SPEED = 8
ENEMYSHIP1_FREQUENCY = 1500  # Millisekunden zwischen Gegnern
ENEMYSHIP1_HP = 1
ENEMYSHIP1_SHOOT_COOLDOWN = 1500  # Gegner1 kann einmal pro 1,5 Sekunde schießen
ENEMYSHIP1_SPAWN_MAX_HEIGHT = int(PLAY_AREA_HEIGHT * 0.1)
ENEMYSHIP1_SPAWN_MIN_HEIGHT = PLAY_AREA_HEIGHT

# Gegner2
ENEMYSHIP2_WIDTH, ENEMYSHIP2_HEIGHT = 80, 100
ENEMYSHIP2_SPEED = 2
ENEMYSHIP2_BULLET_SPEED = 10
ENEMYSHIP2_FREQUENCY = 2500  # Gegner2 erscheint alle 2,5 Sekunden
ENEMYSHIP2_HP = 2
ENEMYSHIP2_SHOOT_COOLDOWN = 2500
ENEMYSHIP2_SPAWN_MAX_HEIGHT = int(PLAY_AREA_HEIGHT * 0.86)
ENEMYSHIP2_SPAWN_MIN_HEIGHT = int(PLAY_AREA_HEIGHT * 0.3)

# Gegner3
ENEMYSHIP3_WIDTH, ENEMYSHIP3_HEIGHT = 100, 125
ENEMYSHIP3_SPEED = 1
ENEMYSHIP3_BULLET_SPEED = 12
ENEMYSHIP3_FREQUENCY = 3000  # Gegner3 erscheint alle 3 Sekunden
ENEMYSHIP3_HP = 3
ENEMYSHIP3_SHOOT_COOLDOWN = 3000
ENEMYSHIP3_SPAWN_MAX_HEIGHT = int(PLAY_AREA_HEIGHT * 0.86)
ENEMYSHIP3_SPAWN_MIN_HEIGHT = int(PLAY_AREA_HEIGHT * 0.3)

# Boss allgemeine Einstellungen
BOSSSHIP_FREQUENCY = 20000

# Boss1
BOSSSHIP1_WIDTH, BOSSSHIP1_HEIGHT = 110, 125
BOSSSHIP1_YAXIS_SPEED = 2
BOSSSHIP1_HP = 10
BOSSSHIP1_SPAWNPOINT = PLAY_AREA_HEIGHT // 8
BOSS1_SHOOT_COOLDOWN = 3000  # Boss kann einmal pro 3 Sekunden schießen
BOSS1_BULLET_COLOR = ORANGE
BOSS1_BULLET_SPEED = 8
BOSS1_BULLET_WIDTH, BOSS1_BULLET_HEIGHT = 12, 6

# Boss2
BOSSSHIP2_WIDTH, BOSSSHIP2_HEIGHT = 125, 140
BOSSSHIP2_YAXIS_SPEED = 4
BOSSSHIP2_HP = 15
BOSSSHIP2_SPAWNPOINT = (PLAY_AREA_HEIGHT // 8) * 7
BOSS2_SHOOT_COOLDOWN = 2500  # Boss kann einmal pro 2,5 Sekunden schießen
BOSS2_BULLET_COLOR = RED
BOSS2_BULLET_SPEED = 9
BOSS2_BULLET_WIDTH, BOSS2_BULLET_HEIGHT = 18, 9

# Boss3
BOSSSHIP3_WIDTH, BOSSSHIP3_HEIGHT = 140, 155
BOSSSHIP3_YAXIS_SPEED = 6
BOSSSHIP3_HP = 20
BOSSSHIP3_SPAWNPOINT = (PLAY_AREA_HEIGHT // 8) * 4
BOSS3_SHOOT_COOLDOWN = 2000  # Boss kann einmal pro 2 Sekunden schießen
BOSS3_BULLET_COLOR = DarkRed
BOSS3_BULLET_SPEED = 10
BOSS3_BULLET_WIDTH, BOSS3_BULLET_HEIGHT = 24, 12

# Background settings
star_field = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(333)]

# Initialisieren des Fonts
FONT = pygame.font.SysFont('Arial', 28)
FONT1 = pygame.font.SysFont('Comic Sans', 148)
FONT2 = pygame.font.SysFont('Times New Roman', 36)
FONT3 = pygame.font.SysFont('Comic Sans', 72)
FONT4 = pygame.font.SysFont('Comic Sans', 48)
FONT5 = pygame.font.SysFont('Comic Sans', 96)
FONT6 = pygame.font.SysFont('Times New Roman', 22)

# Highscore-Liste
highscore = []
level_score = []

# Bilder laden und skalieren
player_image = pygame.image.load('assets/images/player.png')
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
enemyship1_image = pygame.image.load('assets/images/enemy1.png')
enemyship1_image = pygame.transform.scale(enemyship1_image, (ENEMYSHIP1_WIDTH, ENEMYSHIP1_HEIGHT))
enemyship2_image = pygame.image.load('assets/images/enemy2.png')
enemyship2_image = pygame.transform.scale(enemyship2_image, (ENEMYSHIP2_WIDTH, ENEMYSHIP2_HEIGHT))
enemyship3_image = pygame.image.load('assets/images/enemy3.png')
enemyship3_image = pygame.transform.scale(enemyship3_image, (ENEMYSHIP3_WIDTH, ENEMYSHIP3_HEIGHT))
asteroid_image = pygame.image.load('assets/images/asteroid.png')
asteroid_image = pygame.transform.scale(asteroid_image, (ASTEROID_WIDTH, ASTEROID_HEIGHT))
bossship1_image = pygame.image.load('assets/images/boss1.png')
bossship1_image = pygame.transform.scale(bossship1_image, (BOSSSHIP1_WIDTH, BOSSSHIP1_HEIGHT))
bossship2_image = pygame.image.load('assets/images/boss2.png')
bossship2_image = pygame.transform.scale(bossship2_image, (BOSSSHIP2_WIDTH, BOSSSHIP2_HEIGHT))
bossship3_image = pygame.image.load('assets/images/boss3.png')
bossship3_image = pygame.transform.scale(bossship3_image, (BOSSSHIP3_WIDTH, BOSSSHIP3_HEIGHT))

# Lade Sounddateien
player_shoot_sound = pygame.mixer.Sound('assets/sounds/player_shoot.mp3')
player_shoot_sound.set_volume(0.03)
player_explosion_sound = pygame.mixer.Sound('assets/sounds/player_explosion.mp3')
player_explosion_sound.set_volume(0.2)
player_hit_sound = pygame.mixer.Sound('assets/sounds/player_hit.mp3')
player_hit_sound.set_volume(0.07)

enemy_hit_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.mp3')
enemy_hit_sound.set_volume(0.1)
asteroid_explosion_sound = pygame.mixer.Sound('assets/sounds/obstacle_explosion.mp3')
asteroid_explosion_sound.set_volume(0.02)

boss_shoot_sound = pygame.mixer.Sound('assets/sounds/boss_shoot.mp3')
boss_shoot_sound.set_volume(0.02)
boss_explosion_sound = pygame.mixer.Sound('assets/sounds/boss_explosion.mp3')
boss_explosion_sound.set_volume(0.25)
boss_hit_sound = pygame.mixer.Sound('assets/sounds/boss_hit.mp3')
boss_hit_sound.set_volume(0.05)

level_transition_sound = pygame.mixer.Sound('assets/sounds/level_transition.mp3')
level_transition_sound.set_volume(0.1)
pause_menu_sound = pygame.mixer.Sound('assets/sounds/pause.mp3')
pause_menu_sound.set_volume(0.2)
gameover_sound = pygame.mixer.Sound('assets/sounds/game_over.mp3')
gameover_sound.set_volume(0.2)
win_sound = pygame.mixer.Sound('assets/sounds/win.mp3')
win_sound.set_volume(0.2)

# Lade und spiele Hintergrundmusik
Gameplay_backgroundmusic = 'assets/sounds/background_music.mp3'
Gameplay_backgroundmusic_volume = 0.25
Startmenu_backgroundmusik = 'assets/sounds/start.mp3'
Startmenu_backgroundmusik_volume = 0.25

# Spielobjekte
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Erstelle Maske basierend auf Bild
        self.rect.center = (50, PLAY_AREA_HEIGHT // 2)  # Startposition des Spielers
        self.hp = START_HP
        self.last_hit = 0
        self.last_shot = 0
        self.score = 0

    def update(self, keys_pressed):  # Bewegt den Spieler basierend auf gedrückten Tasten
        if keys_pressed[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys_pressed[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys_pressed[pygame.K_w] and self.rect.top > 0 and self.rect.top > HEIGHT - PLAY_AREA_HEIGHT:
            self.rect.y -= PLAYER_SPEED
        if keys_pressed[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += PLAYER_SPEED

    def shoot(self):  # Feuert einen Schuss, wenn die Abklingzeit vorbei ist
        now = pygame.time.get_ticks()
        if now - self.last_shot > SHOOT_COOLDOWN:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery)  # Schuss kommt aus der rechten Seite des Spielers
            all_sprites.add(bullet)
            bullets.add(bullet)
            player_shoot_sound.play()

    def get_hit(self):  # Reduziert HP des Spielers und aktiviert Immunität für eine kurze Zeit
        now = pygame.time.get_ticks()
        if now - self.last_hit > IMMUNE_TIME:
            self.last_hit = now
            self.hp -= 1
            player_hit_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 8))  # Horizontale Kugel
        self.image.fill(Turquoise)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):  # Bewegt den Schuss nach rechts
        self.rect.x += BULLET_SPEED
        if self.rect.left > WIDTH:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_speed, width=5, height=8, color=Magenta):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.bullet_speed = bullet_speed

    def update(self):  # Bewegt den Schuss nach links
        self.rect.x -= self.bullet_speed
        if self.rect.right < 0:
            self.kill()

class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed

    def update(self):  # Bewegt den Schuss nach links
        self.rect.x -= self.speed
        if self.rect.right < 0:  # Entferne das Geschoss, wenn es aus dem Bildschirm fliegt
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = asteroid_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Maske basierend auf Bild
        self.rect.y = random.randint(HEIGHT - PLAY_AREA_HEIGHT, HEIGHT - self.rect.height)
        self.rect.x = WIDTH  # Hindernis kommt von der rechten Seite
        self.speed = OBSTACLE_SPEED + random.randint(-2, 2)  # Zufällige Geschwindigkeit

    def update(self):
        self.rect.x -= self.speed  # Verwende die zufällige Geschwindigkeit
        if self.rect.right < 0:
            self.kill()

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
        super().__init__()
        if enemy_type == 1:
            self.image = enemyship1_image
            self.rect = self.image.get_rect()  # Initialize rect based on the image
            self.hp = ENEMYSHIP1_HP
            self.speed = ENEMYSHIP1_SPEED
            self.shoot_cooldown = ENEMYSHIP1_SHOOT_COOLDOWN
            self.rect.y = random.randint(int( self.rect.height * 1.5), PLAY_AREA_HEIGHT  - int(self.rect.height * 1.5))  # Zufällige Y-Position über Playarea
            self.bullet_speed = ENEMYSHIP1_BULLET_SPEED  # Schussgeschwindigkeit für Gegner1
        elif enemy_type == 2:
            self.image = enemyship2_image
            self.rect = self.image.get_rect()
            self.hp = ENEMYSHIP2_HP
            self.speed = ENEMYSHIP2_SPEED
            self.shoot_cooldown = ENEMYSHIP2_SHOOT_COOLDOWN
            self.rect.y = random.randint(int(self.rect.height * 1.5), PLAY_AREA_HEIGHT - int(self.rect.height * 1.5))
            self.bullet_speed = ENEMYSHIP2_BULLET_SPEED
        elif enemy_type == 3:
            self.image = enemyship3_image
            self.rect = self.image.get_rect()
            self.hp = ENEMYSHIP3_HP
            self.speed = ENEMYSHIP3_SPEED
            self.shoot_cooldown = ENEMYSHIP3_SHOOT_COOLDOWN
            self.rect.y = random.randint(int(self.rect.height * 1.5), PLAY_AREA_HEIGHT - int(self.rect.height * 1.5))
            self.bullet_speed = ENEMYSHIP3_BULLET_SPEED
        self.mask = pygame.mask.from_surface(self.image)  # Maske basierend auf Bild
        self.rect.x = WIDTH
        self.last_shot = 0
        self.angle = random.uniform(0, 2 * math.pi)
        # Füge hier einen zufälligen Versatz für den ersten Schuss hinzu
        self.shoot_offset = random.randint(0, 1000)  # Zufälliger Versatz bis zu 1 Sekunde

    def update(self):
        self.rect.x -= self.speed
        self.rect.y += int(4 * math.sin(self.angle))
        self.angle += 0.03
        # Begrenzt die Bewegung innerhalb des Bildschirms
        if self.rect.top <= int(HEIGHT * 0.1):
            self.rect.top = int(HEIGHT * 0.1)
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right < 0:
            self.kill()
        # Gegner schießt basierend auf individuellem Timer
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_cooldown + self.shoot_offset:
            self.last_shot = now
            self.shoot_offset = random.randint(0, 1000)  # Neuen zufälligen Offset für den nächsten Schuss setzen
            enemy_bullet = EnemyBullet(self.rect.left, self.rect.centery, self.bullet_speed)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)

class BossShip(pygame.sprite.Sprite):
    def __init__(self, image, hp, y_speed, shoot_cooldown, boss_movement, bullet_color, bullet_speed, bullet_width, bullet_height):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)  # Maske basierend auf Bild
        self.rect.y = random.randint(HEIGHT // 4, HEIGHT - self.rect.height)
        self.rect.x = WIDTH  # Startet außerhalb des Bildschirms rechts
        self.hp = hp
        self.speed_y = y_speed
        self.shoot_cooldown = shoot_cooldown
        self.bullet_color = bullet_color
        self.bullet_speed = bullet_speed
        self.bullet_width = bullet_width
        self.bullet_height = bullet_height
        self.last_shot = 0
        self.movement = boss_movement
        self.has_entered_screen = False  # Neue Variable, um zu prüfen, ob der Boss vollständig im Bildschirm ist

    def update(self):
        if not self.has_entered_screen:  # Boss fliegt nach links, bis er vollständig sichtbar ist
            if self.rect.right > WIDTH - 10:  # Fliegt nur bis 1cm in den Bildschirm
                self.rect.x -= 2  # Geschwindigkeit beim Einfliegen
            else:
                self.has_entered_screen = True  # Boss ist nun vollständig im Bildschirm
        else:  # Sobald der Boss vollständig im Bildschirm ist, bewegt er sich nur noch hoch und runter
            if self.movement:  # Y-Achsen-Bewegung
                self.rect.y += self.speed_y
                # Begrenze Bewegung innerhalb des Bildschirms
                if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
                    self.speed_y *= -1  # Umkehren, wenn die Ränder erreicht sind

        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_cooldown:
            self.last_shot = now
            positions = [self.rect.top, self.rect.centery, self.rect.bottom]  # Schießt an drei Positionen (oben, mitte, unten)
            for pos in positions:
                boss_bullet = BossBullet(self.rect.left, pos, self.bullet_color, self.bullet_speed, self.bullet_width, self.bullet_height)
                boss_shoot_sound.play()
                all_sprites.add(boss_bullet)
                boss_bullets.add(boss_bullet)

        if self.rect.right < 0:
            self.kill()

def play_music(track, volume):
    pygame.mixer.music.load(track)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)  # Musik wird in Endlosschleife gespielt

def draw_health_bar(surf, x, y, hp, max_hp):  # Zeichnet die Lebensanzeige des Spielers
    BAR_WIDTH, BAR_HEIGHT = 200, 20
    fill = (hp / max_hp) * BAR_WIDTH
    border_rect = pygame.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, border_rect, 2)

def draw_health_text(surf, x, y, hp):  # Zeichnet die Lebenspunkt-Anzeige als Text
    hp_text = FONT.render(f'HP: {hp}', True, WHITE)
    surf.blit(hp_text, (x, y + 25))

def draw_score(surf, x, y, score):  # Zeichnet die Punkte-Anzeige als Text
    score_text = FONT.render(f'Score: {score}', True, WHITE)
    surf.blit(score_text, (x, y))

def update_star_field():
    global star_field
    for star in star_field:
        star[0] -= 3  # Bewegt Sterne nach links

        if star[0] < 0:  # Wenn ein Stern das Ende erreicht, wird er neu positioniert
            star[0] = WIDTH
            star[1] = random.randint(0, HEIGHT)  # Neue Y-Position zufällig setzen

def start_menu():
    running = True
    play_music(Startmenu_backgroundmusik, Startmenu_backgroundmusik_volume)
    while running:
        WINDOW.fill(GroundStart)
        for star in star_field:  # Draw Stars
            pygame.draw.circle(WINDOW, GroundStar, star, 1)
        title_text = FONT1.render('Outrider', True, DarkRed)
        start_text = FONT.render('Press ENTER to Start', True, BlueViolet)
        quit_text = FONT.render('Press ESCAPE to Quit', True, WHITE)
        control_text = FONT6.render('CONTROLS', True, ORANGE)
        control_rect = control_text.get_rect(center=(WIDTH // 6.56, HEIGHT // 7 + 442))
        underline_start = (control_rect.left, control_rect.bottom + 1)
        underline_end = (control_rect.right, control_rect.bottom + 1)
        underline_thickness = 2
        pygame.draw.line(WINDOW, ORANGE, underline_start, underline_end, underline_thickness)
        pause_text = FONT6.render('P-Pause', True, ORANGE)
        control1_text = FONT6.render('W-Up  S-Down  D-Right  A-Left', True, ORANGE) # Unicode Pfeile "\u2191" "\u2193" "\u2192" "\u2190"
        control2_text = FONT6.render('␣ SPACEBAR-Shoot \u2423', True, ORANGE)  # Leertaste "\u2423" Enter "\u23CE" Escape "\u238B"
        WINDOW.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - title_text.get_height() // 2 - 150))
        WINDOW.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 - start_text.get_height() // 2))
        WINDOW.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 - quit_text.get_height() // 2 + 60))
        WINDOW.blit(control_text, (WIDTH // 8.15 - control_text.get_width() // 8.15, HEIGHT // 8 - control_text.get_height() // 8 + 450))
        WINDOW.blit(pause_text, (WIDTH // 7.4 - pause_text.get_width() // 7.4, HEIGHT // 8 - pause_text.get_height() // 8 + 500))
        WINDOW.blit(control1_text, (WIDTH // 15.5 - control1_text.get_width() // 15.5, HEIGHT // 12 - control1_text.get_height() // 12 + 580))
        WINDOW.blit(control2_text, (WIDTH // 11 - control2_text.get_width() // 11, HEIGHT // 8 - control2_text.get_height() // 8 + 600))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    return "Quit"
    pygame.mixer.music.stop()

def pause_menu():
    paused = True
    pygame.mixer.music.pause()
    pause_menu_sound.play(loops=5)
    while paused:
        WINDOW.fill(GroundPause)
        for star in star_field:  # Sterne zeichnen
            pygame.draw.circle(WINDOW, GroundStar, star, 1)
        pause_text = FONT3.render('Paused !?!', True, DarkRed)
        resume_text = FONT.render('Press R to Resume', True, BlueViolet)
        quit_text = FONT.render('Press Q to Quit', True, WHITE)
        highscore_text = FONT.render('Press S to View Highscores', True, Gold)
        control_text = FONT6.render('CONTROLS', True, ORANGE)
        control_rect = control_text.get_rect(center=(WIDTH // 6.56, HEIGHT // 7 + 492))
        underline_start = (control_rect.left, control_rect.bottom + 1)
        underline_end = (control_rect.right, control_rect.bottom + 1)
        underline_thickness = 2
        pygame.draw.line(WINDOW, ORANGE, underline_start, underline_end, underline_thickness)
        control1_text = FONT6.render('W-Up  S-Down  D-Right  A-Left', True, ORANGE)  # Unicode Pfeile "\u2191" "\u2193" "\u2192" "\u2190"
        control2_text = FONT6.render('␣ SPACEBAR-Shoot\u2423', True, ORANGE)  # Leertaste "\u2423"
        WINDOW.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2 - 125))
        WINDOW.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2 - resume_text.get_height() // 2 - 20))
        WINDOW.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2 - highscore_text.get_height() // 2 + 100))
        WINDOW.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 - quit_text.get_height() // 2 + 40))
        WINDOW.blit(control_text, (WIDTH // 8.15 - control_text.get_width() // 8.15, HEIGHT // 8 - control_text.get_height() // 8 + 500))
        WINDOW.blit(control1_text, (WIDTH // 15.5 - control1_text.get_width() // 15.5, HEIGHT // 12 - control1_text.get_height() // 12 + 580))
        WINDOW.blit(control2_text, (WIDTH // 11 - control2_text.get_width() // 11, HEIGHT // 8 - control2_text.get_height() // 8 + 600))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
                if event.key == pygame.K_q:
                    paused = False
                    return "Quit"
                if event.key == pygame.K_s:
                    show_highscores()
    pause_menu_sound.stop()
    pygame.mixer.music.unpause()

def level_transition(level):
    global level_score
    delay = 0
    WINDOW.fill(BLACK)
    if (level >= 1) and (level <= 3):
        level_text = FONT5.render(f'Level {level}', True, WHITE)
        level_transition_sound.play()
        delay = 3200
    if level == 4:
        win_sound.play()
        end_text = FONT5.render(f'The End ?', True, RED)
        total_score_text = FONT4.render(f'Score: {sum(level_score)}', True, WHITE)
        creator_text = FONT4.render('Creators :', True, DarkRed)
        c1_text = FONT4.render('Kulb Tobias', True, WHITE)
        c2_text = FONT4.render('Reif Lukas', True, WHITE)
        c3_text = FONT4.render('Wolf David', True, WHITE)
        WINDOW.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 2 - end_text.get_height() // 2 - 250))
        WINDOW.blit(total_score_text, (WIDTH // 2 - total_score_text.get_width() // 2, (HEIGHT // 2 - total_score_text.get_height() // 2) - 150))
        WINDOW.blit(creator_text, (WIDTH // 2 - creator_text.get_width() // 2, HEIGHT // 2 - creator_text.get_height() // 2 - 50))
        WINDOW.blit(c1_text, (WIDTH // 2 - c1_text.get_width() // 2, HEIGHT // 2 - c1_text.get_height() // 2 + 50))
        WINDOW.blit(c2_text, (WIDTH // 2 - c2_text.get_width() // 2, HEIGHT // 2 - c2_text.get_height() // 2 + 150))
        WINDOW.blit(c3_text, (WIDTH // 2 - c3_text.get_width() // 2, HEIGHT // 2 - c2_text.get_height() // 2 + 250))
        delay = 8000
    if level <= 3:
        WINDOW.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - level_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(delay)
    win_sound.stop()
    level_transition_sound.stop()

def game_over_screen():
    global highscore
    gameover_sound.play()
    WINDOW.fill(BLACK)
    game_over_text = FONT5.render('GAME OVER', True, RED)
    retry_text = FONT.render('Press R to Retry', True, BlueViolet)
    quit_text = FONT.render('Press Q to Quit', True, WHITE)
    enter_name_text = FONT.render('Press H to Enter Highscore', True, Gold)
    WINDOW.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2 - 135))
    WINDOW.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 - retry_text.get_height() // 2 - 20))
    WINDOW.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 - quit_text.get_height() // 2 + 40))
    WINDOW.blit(enter_name_text, (WIDTH // 2 - enter_name_text.get_width() // 2, HEIGHT // 2 - enter_name_text.get_height() // 2 + 100))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "Retry"
                if event.key == pygame.K_q:
                    return "Quit"
                if event.key == pygame.K_h:
                    quit_retry = enter_highscore()
                    return quit_retry

def enter_highscore():
    global highscore, level_score
    name = ""
    entering_name = True
    while entering_name:
        WINDOW.fill(GroundStart)
        enter_name_text = FONT2.render('Enter your name: ', True, Gold)
        WINDOW.blit(enter_name_text, (WIDTH // 2 - enter_name_text.get_width() // 2, HEIGHT // 2 - enter_name_text.get_height() // 2 - 60))
        name_text = FONT.render(name, True, WHITE)
        WINDOW.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 2 - name_text.get_height() // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:
                    highscore.append((name, sum(level_score)))
                    highscore = sorted(highscore, key=lambda x: x[1], reverse=True)[:10]  # Nur die Top 10 Highscores
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 8:
                    name += event.unicode

    quit_retry = show_highscores()
    return quit_retry

def show_highscores():
    showing = True
    while showing:
        WINDOW.fill(GroundStart)
        highscore_text = FONT4.render('Highscores:', True, Gold)
        WINDOW.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2 - highscore_text.get_height() // 2 - 120))
        for idx, (name, score) in enumerate(highscore):
            score_text = FONT.render(f'{idx + 1}. {name} : {score}', True, WHITE)
            WINDOW.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - highscore_text.get_height() // 2 - 50 + (idx + 1) * 30))

        retry_text = FONT.render('Press R to Retry or Q to Quit', True, WHITE)
        WINDOW.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT - (HEIGHT // 10)))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "Retry"
                if event.key == pygame.K_q:
                    return "Quit"


def save_highscores(highscores):
    # Stelle sicher, dass der 'highscores'-Ordner existiert
    folder = 'highscores'
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Erzeuge einen Dateinamen basierend auf dem aktuellen Datum und Uhrzeit
    filename = f'highscores_{datetime.datetime.now().strftime("%d%m%Y_%H%M%S")}.txt'
    filepath = os.path.join(folder, filename)

    # Schreibe die Highscores in die Datei
    with open(filepath, 'w') as f:
        f.write("Highscores:\n")
        for idx, (name, score) in enumerate(highscores, start=1):
            f.write(f'{idx}. {name}: {score}\n')

    print(f"Highscores saved to {filepath}")

def limit_highscore_files(folder, limit=20):
    highscore_files = [f for f in os.listdir(folder) if f.startswith('highscores_') and f.endswith('.txt')]

    # Sortiere die Dateien nach Erstellungsdatum (älteste zuerst)
    highscore_files.sort()

    # Wenn die Anzahl der Dateien das Limit überschreitet, lösche die ältesten
    if len(highscore_files) > limit:
        files_to_delete = highscore_files[:len(highscore_files) - limit]
        for file in files_to_delete:
            os.remove(os.path.join(folder, file))
            print(f"Deleted old highscore file: {file}")

def load_highscores():
    folder = 'highscores'
    if not os.path.exists(folder):
        return []  # Kein Highscore verfügbar, also gib eine leere Liste zurück

    # Finde die zuletzt gespeicherte Highscore-Datei
    highscore_files = [f for f in os.listdir(folder) if f.startswith('highscores_') and f.endswith('.txt')]
    if not highscore_files:
        return []  # Keine Highscore-Dateien vorhanden

    # Sortiere die Dateien nach Datum (die neueste Datei zuerst)
    highscore_files.sort(reverse=True)
    latest_file = os.path.join(folder, highscore_files[0])

    # Lese die Datei und lade die Highscores
    highscore_list = []
    with open(latest_file, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:  # Erste Zeile überspringen (Highscores:)
            parts = line.strip().split('. ', 1)  # Trenne nach ". " um Platzierung zu ignorieren
            if len(parts) == 2:
                name, score = parts[1].split(': ')
                highscore_list.append((name, int(score)))

    print(f"Highscores loaded from {latest_file}")
    limit_highscore_files(folder, limit=20)
    return highscore_list

def run_level(level, player):
    clock = pygame.time.Clock()
    pygame.mixer.music.unpause()
    global all_sprites, bullets, enemy_bullets, boss_bullets, obstacles, enemyships, bossships
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    boss_bullets = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    enemyships = pygame.sprite.Group()
    bossships = pygame.sprite.Group()

    all_sprites.add(player)  # Fügt den existierenden Spieler zu all_sprites hinzu

    boss_killed = False

    # Hindernisse Timer
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, OBSTACLE_FREQUENCY)

    # Gegner Timer
    if level >= 1:
        enemyship1_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(enemyship1_timer, ENEMYSHIP1_FREQUENCY)
    if level == 2:
        enemyship2_timer = pygame.USEREVENT + 3
        pygame.time.set_timer(enemyship2_timer, ENEMYSHIP2_FREQUENCY)
    if level == 3:
        enemyship3_timer = pygame.USEREVENT + 4
        pygame.time.set_timer(enemyship3_timer, ENEMYSHIP3_FREQUENCY)

    # Boss Timer
    boss_spawned = False
    boss_timer_start = pygame.time.get_ticks()  # Zeitpunkt des Levelstarts
    pause_duration = 0  # Dauer der Pausenzeit

    run = True
    while run:
        clock.tick(60)
        keys_pressed = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "Quit"
            # Pause Menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pause_start_time = pygame.time.get_ticks()  # Zeitstempel, wann die Pause beginnt
                quit_pause_menu = pause_menu()
                pause_duration += pygame.time.get_ticks() - pause_start_time  # Pausendauer hinzufügen
                if quit_pause_menu == "Quit":
                    return "Quit"

            #if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_1:
                    #return 1
                #if event.key == pygame.K_2:
                    #return 2
                #if event.key == pygame.K_3:
                    #return 3

            # Hinderniss spawn
            if event.type == obstacle_timer:
                obstacle = Obstacle()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            # Gegner spawn in verschiedenen lvl
            if (level == 1 and event.type == enemyship1_timer) or (level == 2 and event.type == enemyship1_timer) or (level == 3 and event.type == enemyship1_timer):
                enemy = EnemyShip(1)  # `enemy_type` 1 in lvl 1, lvl 2, lvl 3
                all_sprites.add(enemy)
                enemyships.add(enemy)
            if level == 2 and event.type == enemyship2_timer:
                enemy = EnemyShip(2)  # `enemy_type` 2 in lvl 2
                all_sprites.add(enemy)
                enemyships.add(enemy)
            if level == 3 and event.type == enemyship3_timer:
                enemy = EnemyShip(3)  # `enemy_type` 3 in lvl 3
                all_sprites.add(enemy)
                enemyships.add(enemy)

        # Boss Spawn nach 20 Sekunden reiner Spielzeit
        now = pygame.time.get_ticks() - pause_duration  # Aktuelle Zeit abzüglich Pausenzeit
        if not boss_spawned and now - boss_timer_start >= BOSSSHIP_FREQUENCY:
            if level == 1:
                boss = BossShip(bossship1_image, BOSSSHIP1_HP, BOSSSHIP1_YAXIS_SPEED, BOSS1_SHOOT_COOLDOWN, True,
                                BOSS1_BULLET_COLOR, BOSS1_BULLET_SPEED, BOSS1_BULLET_WIDTH, BOSS1_BULLET_HEIGHT)
            elif level == 2:
                boss = BossShip(bossship2_image, BOSSSHIP2_HP, BOSSSHIP2_YAXIS_SPEED, BOSS2_SHOOT_COOLDOWN, True,
                                BOSS2_BULLET_COLOR, BOSS2_BULLET_SPEED, BOSS2_BULLET_WIDTH, BOSS2_BULLET_HEIGHT)
            elif level == 3:
                boss = BossShip(bossship3_image, BOSSSHIP3_HP, BOSSSHIP3_YAXIS_SPEED, BOSS3_SHOOT_COOLDOWN, True,
                                BOSS3_BULLET_COLOR, BOSS3_BULLET_SPEED, BOSS3_BULLET_WIDTH, BOSS3_BULLET_HEIGHT)
            all_sprites.add(boss)
            bossships.add(boss)
            boss_spawned = True

        if keys_pressed[pygame.K_SPACE]:
            player.shoot()

        # Update Spiel Objekte
        player.update(keys_pressed)  # Spieler
        bullets.update()  # Geschosse
        enemy_bullets.update()  # Gegnerische Geschosse
        boss_bullets.update()  # Boss Geschosse
        obstacles.update()  # Hindernisse
        enemyships.update()  # Gegner
        bossships.update()  # Bosse
        update_star_field()  # Sternenhimmel

        # Kollision zwischen Hindernissen und Schüssen
        obstacle_hits = pygame.sprite.groupcollide(obstacles, bullets, True, True, pygame.sprite.collide_mask)
        for hit in obstacle_hits:
            asteroid_explosion_sound.play()
            player.score += 100
        # Kollision zwischen Spieler und Hindernissen
        player_hits = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_mask)
        for hit in player_hits:
            player.get_hit()
            hit.kill()
        # Kollision zwischen Gegner und Schüssen
        enemy_hits = pygame.sprite.groupcollide(enemyships, bullets, False, True, pygame.sprite.collide_mask)
        for enemy, bullet_list in enemy_hits.items():
            for bullet in bullet_list:
                enemy.hp -= 1
                if enemy.hp <= 0:
                    enemy.kill()
                    enemy_hit_sound.play()
                    player.score += 250
        # Kollision zwischen Spieler und Gegner
        player_enemy_hits = pygame.sprite.spritecollide(player, enemyships, False, pygame.sprite.collide_mask)
        for hit in player_enemy_hits:
            player.get_hit()
            hit.kill()
        # Kollision zwischen Spieler-Schüssen und feindlichen Schüssen
        player_bullet_enemy_bullet_hits = pygame.sprite.groupcollide(bullets, enemy_bullets, True, True, pygame.sprite.collide_mask)
        # Kollision zwischen Spieler und feindlichen Schüssen
        enemy_bullet_hits = pygame.sprite.spritecollide(player, enemy_bullets, True, pygame.sprite.collide_mask)
        for hit in enemy_bullet_hits:
            player.get_hit()
        # Kollision zwischen Boss und Schüssen
        boss_hits = pygame.sprite.groupcollide(bossships, bullets, False, True, pygame.sprite.collide_mask)
        for boss, bullet_list in boss_hits.items():
            for bullet in bullet_list:
                boss.hp -= 1
                boss_hit_sound.play()  # Spiele den Schuss-Sound ab
                if boss.hp <= 0:
                    boss.kill()
                    boss_explosion_sound.play()
                    player.score += 1000
                    boss_killed = True
                    run = False
        # Kollision zwischen Spieler und Boss
        player_boss_hits = pygame.sprite.spritecollide(player, bossships, False, pygame.sprite.collide_mask)
        for hit in player_boss_hits:
            player.get_hit()  # Spieler erhält Schaden, wenn er vom Boss getroffen wird
        # Kollision zwischen Boss-Schüssen und dem Spieler
        boss_bullet_hits = pygame.sprite.spritecollide(player, boss_bullets, True, pygame.sprite.collide_mask)
        for hit in boss_bullet_hits:
            player.get_hit()
        # Kollision zwischen Spieler-Schüssen und Boss-Schüssen
        player_bullet_boss_bullet_hits = pygame.sprite.groupcollide(bullets, boss_bullets, True, False, pygame.sprite.collide_mask)

        # Alles zeichnen
        WINDOW.fill(Backgroundspace)  # Zeichnen des Bildschirms
        update_star_field()
        for star in star_field:  # Sterne zeichnen
            pygame.draw.circle(WINDOW, YELLOW, star, 1)
        all_sprites.draw(WINDOW)
        draw_health_bar(WINDOW, 10, 10, player.hp, MAX_HP)
        draw_health_text(WINDOW, 10, 10, player.hp)
        draw_score(WINDOW, WIDTH - 150, 10, player.score)
        pygame.display.flip()

        level_score[0] = player.score
        # Wenn Spieler stirbt
        if player.hp <= 0:
            player_explosion_sound.play()
            return "GameOver"

    pygame.mixer.music.pause()

    if boss_killed:  # Wenn Boss stirbt
        pygame.time.delay(100)
        return "Bosskill"

def main():
    retry = True
    global level_score
    clock = pygame.time.Clock()  # Initialisiere die Uhr einmal

    while retry:
        level_choice = 1
        level_score = [0, 0, 0]
        GameOver = True
        quit_game = start_menu()
        if quit_game == "Quit":
            break

        player = Player()  # Initialisiere den Spieler einmal
        play_music(Gameplay_backgroundmusic,
                   Gameplay_backgroundmusic_volume)
        for level in range(1, 5):
            level = level_choice
            pygame.mixer.music.pause()
            level_transition(level)
            pygame.mixer.music.unpause()
            if level >= 4:
                break
            action = run_level(level, player)  # Übergib den Spieler
            if action == "Bosskill":
                level_choice += 1
                GameOver = True
                continue
            if action == "GameOver":
                GameOver = True
                break
            if action == "Quit":
                quit_game = "Quit"
                break
            if action == 1:
                level_choice = 1
                GameOver = False
                continue
            if action == 2:
                level_choice = 2
                GameOver = False
                continue
            if action == 3:
                level_choice = 3
                GameOver = False
                continue

        if quit_game == "Quit":
            break
        pygame.mixer.music.stop()
        if GameOver:
            quit_game = game_over_screen()
            if quit_game == "Quit":
                break

    save_highscores(highscore)  # Speichere die geordnete Highscore-Liste
    pygame.quit()

highscore = load_highscores()  # Highscores beim Spielstart laden

if __name__ == "__main__":
    main()