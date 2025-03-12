# title: Jojo invendor's
# author: Ali Dicko & Ervin
# desc: Projet NSI - Action-platformer
# site: https://github.com/cyber-neoxis/Platformer-NSI
# license: MIT
# version: Alpha

import pyxel
#from maps import Maps, Scene

#a = Maps(0)
#b = Scene(0)

#ALIIII, CA VAAAA ? les ennemis peuvent donc bouger vers le joueur, le tirer dessus. mais ensuite jsp où les faires spawn du coup ils apparaissent toutes les 4 sec à 10 bloc du joueur. JSP qu'elle autre modif on peut faire. et pour le spawn des ennemis, on utilise la meme texture ?  

class Enemy:
    def __init__(self, player_x, player_y, player_dir,player_health):
        self.x = player_x + (10 * player_dir)  # Spawn à 10 pixels devant le joueur
        self.y = player_y
        self.speed = 2 
        self.dir = -player_dir
        self.is_alive = True
        self.last_shot_time = 0
        self.bullets = []

    def update(self, player_x, player_y):
        if self.x < player_x:
            self.x += self.speed  
        elif self.x > player_x:
            self.x -= self.speed  

        if self.y < player_y:
            self.y += self.speed 
        elif self.y > player_y:
            self.y -= self.speed


        if abs(self.x - player_x) < 8 and abs(self.y - player_y) < 8:
            self.is_alive = False
            player_health -= 1

        if pyxel.frame_count - self.last_shot_time >= 120:
            self.shoot(player_x, player_y)
            self.last_shot_time = pyxel.frame_count
            
        for bullet in self.bullets:
            bullet.update()
            if abs(bullet.x - player.x) < 4 and abs(bullet.y - player.y) < 4:
                player.health -= 1
                bullet.is_alive = False  
                
        self.bullets = [bullet for bullet in self.bullets if bullet.is_alive]
        
    def shoot(self):
        self.bullets.append(Bullet(self.x, self.y + 4, 2, self.dir))  

    def draw(self):
        pyxel.blt(self.x, self.y,0, 24,24,8,1)
        

class Enemysettings:
    def __init__(self):
        self.enemies = []
        self.last_spawn_time = 0

    def update(self, player_x, player_y, player_dir,player_health):
        if pyxel.frame_count - self.last_spawn_time >= 240:  # Spawn toutes les 4 sec
            self.enemies.append(Enemy(player_x, player_y, player_dir))
            self.last_spawn_time = pyxel.frame_count

        for enemy in self.enemies:
            enemy.update(player_x, player_y)

        # Supprime les ennemis morts (qui ont touché le joueur)
        self.enemies = [enemy for enemy in self.enemies if enemy.is_alive]

    def draw(self):
        for enemy in self.enemies:
            enemy.draw()

            
class Bullet:
    def __init__(self, x, y, speed, dir) :
        self.x = x
        self.y = y
        self.dir = dir
        self.speed = speed
        self.is_alive = True

    def update(self): 
        if self.dir == 1 :
            self.x += self.speed
        else :
            self.x -= self.speed
        
        if (self.x > pyxel.width or self.y > pyxel.height
            or self.x < 0 or self.y < 0) :
            self.is_alive = False
        # if .. Contact avec ennemie
        # if .. Contact avec un obstacle


    def draw(self):
        #u = pyxel.frame_count // 4 % 4 * 8 + 16 (au cas ou il y aurait une deuxième texture)
        pyxel.blt(self.x, self.y,0, 24,33,8,1)

class Player:
    def __init__(self, x=16, y=112):
        self.bullet_liste = []
        #Mouvement
        self.x = x
        self.y = y 
        self.speed = 5
        self.moved = False
        self.dir = 1
        #Dash
        self.dash = False
        self.dash_ready = True
        self.dash_speed = 3
        self.cooldown = 0

    def update(self):
        self.moved = False

        #Dash
        if pyxel.frame_count - self.cooldown == 60 :
            self.speed = self.speed//self.dash_speed
            self.dash_ready = True

        if pyxel.btnr(pyxel.KEY_0) and self.dash_ready:
            self.cooldown = pyxel.frame_count
            self.speed = self.speed * self.dash_speed
            self.dash_ready = False
        
        #Deplacements (zqsd)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dir = 1
            self.moved = True
            self.x = min(120, self.x + self.speed)

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dir = -1
            self.moved = True
            self.x = max(0, self.x - self.speed)
        
        if pyxel.btn(pyxel.KEY_UP): #Remplacer par space
            self.moved = True
            self.y = max(0, self.y-self.speed)
        
        if pyxel.btn(pyxel.KEY_DOWN): #se baisser
            self.y = min(pyxel.height-8, self.y + self.speed)
        
        #tir
        if pyxel.btn(pyxel.KEY_K) :
            if self.dir == 1 :
                self.bullet_liste.append(Bullet(self.x+8, self.y+4, 3, self.dir))
            else :
                self.bullet_liste.append(Bullet(self.x, self.y+4, 3, self.dir))
        
        for i in self.bullet_liste :
            i.update()
            if i.is_alive == False :
                del i

        
        

    def draw(self):
        #Animation de mouvement (24,0)
        if self.moved and pyxel.frame_count % 6 < 3 :
            pyxel.blt(self.x, self.y, 0, 16,0, 8*self.dir, 8, colkey=0)
        else :
            pyxel.blt(self.x, self.y, 0, 8,0, 8*self.dir, 8, colkey=0)
        for i in self.bullet_liste :
            i.draw()
        

class App:
    def __init__(self):
        pyxel.init(128,128,title="NSI Platformer", fps=30,quit_key=pyxel.KEY_Q)
        pyxel.load("1.pyxres")
        self.Neoxis = Player()
        pyxel.run(self.update, self.draw)
        self.enemy_manager = Enemysettings()

    def update(self):
        self.Neoxis.update()
        self.enemy_manager.update(self.Neoxis.x, self.Neoxis.y, self.Neoxis.dir)

    def draw(self):
        pyxel.cls(0)
        #Maps
        pyxel.bltm(0,0,0,0,0,128,128)
        self.Neoxis.draw()
        

App()
