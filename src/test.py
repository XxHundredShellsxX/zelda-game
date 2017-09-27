__author__ = 'Fahim and Sajid'
from pygame import *
from math import *
from random import*
size = width, height = 1200, 800
screen = display.set_mode(size)
myClock = time.Clock()
font.init()


def splitter(pic, row, col):
    x, y = pic.get_size()
    xsplit = int(x / col)
    ysplit = int(y / row)
    images = []
    for j in range(0, y, ysplit):
        for i in range(0, x, xsplit):
            surf = pic.subsurface(i, j, xsplit, ysplit)
            surf = transform.scale2x(surf)
            images.append(surf)
    return images

"""
'##:::::::'####:'##::: ##:'##:::'##:
 ##:::::::. ##:: ###:: ##: ##::'##::
 ##:::::::: ##:: ####: ##: ##:'##:::
 ##:::::::: ##:: ## ## ##: #####::::
 ##:::::::: ##:: ##. ####: ##. ##:::
 ##:::::::: ##:: ##:. ###: ##:. ##::
 ########:'####: ##::. ##: ##::. ##:
........::....::..::::..::..::::..::"""
class Link:
    def __init__(self, sprite, x, y, bow):
        #intitializing all of Link's stats and states
        self.state = "stand"
        self.hp = 10
        self.hitx = 0
        self.hity = 0
        self.frame = 0
        self.up = []
        self.down = []
        self.left = []
        self.right = []
        self.bow = bow
        self.arrows = []
        #loading all of his sprites
        self.arrowImage = image.load("bow and arrow/arrow.png")
        for i in range(0, 11):
            self.up.append(sprite[i])
            self.down.append(sprite[i + 24])
            self.left.append(sprite[i + 36])
            self.right.append(sprite[i + 12])
        for i in range(48, 59):
            self.up.append(sprite[i])
            self.down.append(sprite[i + 24])
            self.left.append(sprite[i + 36])
            self.right.append(sprite[i + 12])

        for i in range(0, 8):
            self.up.append(sprite[58 - i])
            self.down.append(sprite[82 - i])
            self.left.append(sprite[94 - i])
            self.right.append(sprite[70 - i])

        #initializing more of his properties

        self.dir = "up"
        self.x = x
        self.y = y
        self.centerx = self.x + 24
        self.centery = self.y + 32
        self.rect = Rect(self.x, self.y + 10, 48, 54)
        self.interval = 150
        self.interval2 = 120
        self.go = True
        self.arrownum=20



    def update(self, slash, enemrects,NPCrects, projectiles):
        
        self.NPCrects=NPCrects
        #when not slashing his sword, the hitbox for it is out of the map
        self.hitx = -3
        self.hity = -3
        #draw.rect(screen,(255,0,0),self.rect,1)

        #adding all of the rectangles he is going to take dmg from in a list
        self.dmgrects = []
        for i in range(len(enemrects)):
            self.dmgrects.append(enemrects[i])
        keys = key.get_pressed()

        #if he gets hit from one of these rectangles, he takes damage
        #the interval is so he has an invincibility frame between each heart he loses
        #between interval 30 and 90 he will not take damage
        for rects in self.dmgrects:
            draw.rect(screen,(255,255,0),rects,1)
            if self.rect.colliderect(rects):
                if self.interval2 >= 90:
                    self.hp -= 1
                    self.interval2 = 30

        #when pressing Z, and he is not using arrow, he swings sword
        if self.interval >= 23 and keys[K_z] and self.go:
            self.state = "swing"
            self.interval = 20
            self.frame = 0
            self.go = False

        #when pressing X and he has more than 0 arrows and he is not doing anything else
        #he goes to shooting arrow state

        if keys[K_x] and self.go and self.arrownum>0:
            self.state = "bow"
            self.interval = 20
            self.frame = 0
            self.go = False

        #all the moving, which gets interrupted if he is either swinging his sword
        #or using his bow and arrow
        if keys[K_UP] or keys[K_DOWN] or keys[K_LEFT] or keys[K_RIGHT]:
            if self.interval >= 35:
                if keys[K_z] == False and keys[K_x] == False and self.state != "bow":
                    self.state = "walking"

                elif keys[K_z] and self.go:
                    self.state = "swing"
                    self.interval = 20
                    self.frame = 0
                    self.go = False

                elif keys[K_x] and self.arrownum>0:
                    self.state == "bow"
                    self.interval = 20

                    self.go = False


        #if he is doing no action at all, he is standing
        elif self.state != "swing" and self.state != "bow" and self.interval >= 20:
            self.state = "standing"

        #reset all of the damage rectangles
        self.dmgrects = []

        
        #all the if statements to perform each of Link's functions depending on his state
        if self.state == "swing" and self.interval < 30:
            self.swordslash(slash)
        elif self.state == "bow":
            self.shoot()
        elif self.state == "walking":
            self.move(keys)
        elif self.state == "standing":
            self.stand()
        else:
            self.stand()

        #self.go is used to verify whether he is using bow or sword
        if keys[K_z] == False and keys[K_x] == False:
            self.go = True
            
        #initializing all of the arrows he will use
        self.arrow()

    def shoot(self):
        #this is all the shooting arrow animation
        keys = key.get_pressed()
        if self.dir == "right":
            #redefining his rectangle since it can move when using bow
            self.rect = Rect(self.x + 2, self.y + 13, 44, 48)
            #pulling bow string animation
            if self.frame <= 3:
                self.frame += 0.2
                screen.blit(self.bow[int(self.frame)], (self.x, self.y+20))
            #if the player is not moving, link standing while bringing back arrow frame is blitted
            elif self.frame > 3 and self.go == False and keys[K_RIGHT] == False and keys[K_LEFT] == False and keys[
                K_UP] == False and keys[K_DOWN] == False:
                screen.blit(self.bow[3], (self.x, self.y+20))

            #if moving with the arrow, cycles through the moving with bow animation
            elif self.frame >= 3 and self.go == False:
                if keys[K_RIGHT] or keys[K_UP] or keys[K_LEFT] or keys[K_DOWN]:
                    if self.frame > 12:
                        self.frame = 4
                    self.frame += 0.4
                    screen.blit(self.bow[int(self.frame)], (self.x, self.y+20))
                    #checks for collision whilst moving
                    self.collisioncheck()
                    
            #when self.go is true (x is let go), and the pulling bow string animation is done
            #the letting go of arrow animation is played
            if self.frame > 3 and self.frame <= 15 and self.go:
                if self.frame < 12:
                    self.frame = 12
                self.frame += 0.3
                screen.blit(self.bow[int(self.frame)], (self.x, self.y+20))
            #when let go, an arrow is shot via adding to the arrow list
            #the number of arrows link has decreases by 1
            elif self.frame > 15 and self.go:
                if self.arrownum>0:
                    self.arrownum-=1
                    self.arrows.append(Arrow(self.arrowImage, self.x + 24, self.y + 30, "right"))
                #links state is automatically standing after using arrow
                self.state = "standing"

        #same bow startup applies for all the rest of the directions, just with the appropriate frame images

        if self.dir == "up":
            self.rect = Rect(self.x + 2, self.y + 13, 44, 48)
            if self.frame < 16:
                self.frame = 16
            if self.frame <= 19:
                self.frame += 0.2
                screen.blit(self.bow[int(self.frame)], (self.x, self.y+10))
            elif self.frame > 19 and self.go == False and keys[K_RIGHT] == False and keys[K_LEFT] == False and keys[
                K_UP] == False and keys[K_DOWN] == False:
                screen.blit(self.bow[19], (self.x, self.y+10))
            elif self.frame >= 19 and self.go == False:
                if keys[K_RIGHT] or keys[K_UP] or keys[K_LEFT] or keys[K_DOWN]:
                    if self.frame > 28:
                        self.frame = 20
                    self.frame += 0.4
                    screen.blit(self.bow[int(self.frame)], (self.x, self.y+10))
                    self.collisioncheck()

            if self.frame > 19 and self.frame <= 31 and self.go:
                if self.frame < 28:
                    self.frame = 28
                self.frame += 0.2
                screen.blit(self.bow[int(self.frame)], (self.x, self.y+10))
            elif self.frame > 31 and self.go:
                # insert arrow class
                if self.arrownum>0:
                    self.arrownum-=1
                    self.arrows.append(Arrow(self.arrowImage, self.x + 24, self.y + 30, "up"))
                self.state = "standing"

        if self.dir == "down":
            self.rect = Rect(self.x + 2, self.y + 13, 44, 48)
            if self.frame < 32:
                self.frame = 32
            if self.frame <= 35:
                self.frame += 0.2
                screen.blit(self.bow[int(self.frame)], (self.x+5, self.y+10))
            elif self.frame > 35 and self.go == False and keys[K_RIGHT] == False and keys[K_LEFT] == False and keys[
                K_UP] == False and keys[K_DOWN] == False:
                screen.blit(self.bow[35], (self.x+5, self.y+10))
            elif self.frame >= 35 and self.go == False:
                if keys[K_RIGHT] or keys[K_UP] or keys[K_LEFT] or keys[K_DOWN]:
                    if self.frame > 44:
                        self.frame = 36
                    self.frame += 0.4
                    screen.blit(self.bow[int(self.frame)], (self.x+5, self.y+10))
                    self.collisioncheck()

            if self.frame > 35 and self.frame <= 47 and self.go:
                if self.frame < 44:
                    self.frame = 44
                self.frame += 0.3
                screen.blit(self.bow[int(self.frame)], (self.x+5, self.y+10))
            elif self.frame > 47 and self.go:
                # insert arrow class
                if self.arrownum>0:
                    self.arrownum-=1
                    self.arrows.append(Arrow(self.arrowImage, self.x + 24, self.y + 30, "down"))
                self.state = "standing"

        if self.dir == "left":
            self.rect = Rect(self.x + 2, self.y + 13, 44, 48)
            if self.frame < 48:
                self.frame = 48
            if self.frame <= 51:
                self.frame += 0.2
                screen.blit(self.bow[int(self.frame)], (self.x, self.y+20))
            elif self.frame > 51 and self.go == False and keys[K_RIGHT] == False and keys[K_LEFT] == False and keys[
                K_UP] == False and keys[K_DOWN] == False:
                screen.blit(self.bow[51], (self.x, self.y+20))
            elif self.frame >= 51 and self.go == False:
                if keys[K_RIGHT] or keys[K_UP] or keys[K_LEFT] or keys[K_DOWN]:
                    if self.frame > 60:
                        self.frame = 52
                    self.frame += 0.4
                    screen.blit(self.bow[int(self.frame)], (self.x, self.y+20))
                    self.collisioncheck()

            if self.frame > 51 and self.frame <= 63 and self.go:
                if self.frame < 60:
                    self.frame = 60
                self.frame += 0.2
                screen.blit(self.bow[int(self.frame)], (self.x, self.y+20))
            elif self.frame > 63 and self.go:
                # insert arrow class
                if self.arrownum>0:
                    self.arrows.append(Arrow(self.arrowImage, self.x + 24, self.y + 30, "left"))
                    self.arrownum-=1
                self.state = "standing"


    def arrow(self):
        global mask, currentMask
        #shoots all of the arrows in the arrow list
        #when colliding with the mask of the map it stops
        #when the arrow has been stuck for a couple seconds, it is removed from the list
        #and disappears
        for arw in self.arrows:
            arw.shoot()
            
            if arw.dir == "up" and arw.interval<30:
                if currentMask.get_at((arw.x , arw.y)) == (0, 0, 0) or arw.y<=10:
                    arw.state="stop"
              
             
            elif arw.dir == "down" and arw.interval<30:
                if currentMask.get_at((arw.x , arw.y+35)) == (0, 0, 0) or arw.y+30>=780:
                    arw.state="stop"
          
            elif arw.dir == "left" and arw.interval<30:
                if currentMask.get_at((arw.x -10, arw.y)) == (0, 0, 0)  or arw.x-10<=10:
                    arw.state="stop"
            
            elif self.dir == "right" and arw.interval<30:
                if currentMask.get_at((arw.x + 35, arw.y)) == (0, 0, 0) or arw.x+25>=1180:
                    arw.state="stop"

            if arw.state=="done":
                self.arrows.remove(arw)

    def swordslash(self, slash):
        #defining the center of link
        self.centerx = self.x + 24
        self.centery = self.y + 32

        if self.dir == "up":
            self.frame += 0.5
            # hitbox of sword when slashing
            self.hitx = int(self.centerx + 40 * cos(radians(0 - self.frame * 30)))
            self.hity = int(self.centery - 25 * sin(radians(0 + self.frame * 30)))
            #blitting the correct frame of sword
            screen.blit(slash[int(self.frame)], (self.x - 27, self.y + 5))
            if self.frame > 6:
                #when slashing is done the frame is 0 and his state is standing
                self.frame = 0
                self.stand()

        #same slash animation and hitboxes apply just for different directions
        if self.dir == "right":
            self.frame += 0.5
            self.hitx = int(self.centerx + 40 * cos(radians(90 - self.frame * 30)))
            self.hity = int((self.centery + 5) - 40 * sin(radians(90 - self.frame * 30)))
            draw.circle(screen, (255, 0, 0), (self.hitx, self.hity), 4)
            screen.blit(slash[int(14 + self.frame)], (self.x, self.y))
            if self.frame + 14 > 19:
                self.frame = 0
                self.stand()

        if self.dir == "left":
            self.frame += 0.5
            self.hitx = int(self.centerx - 40 * cos(radians(90 - self.frame * 30)))
            self.hity = int((self.centery + 5) - 40 * sin(radians(90 - self.frame * 30)))
            draw.circle(screen, (255, 0, 0), (self.hitx, self.hity), 4)
            screen.blit(slash[int(20 + self.frame)], (self.x - 20, self.y))
            if self.frame + 20 > 25:
                self.frame = 0
                self.stand()

        if self.dir == "down":
            self.frame += 0.5
            self.hitx = int((self.centerx + 15) + 40 * cos(radians(180 - self.frame * 30)))
            self.hity = int((self.centery + 20) - 40 * sin(radians(180 + self.frame * 30)))
            draw.circle(screen, (255, 0, 0), (self.hitx, self.hity), 4)
            screen.blit(slash[int(8 + self.frame)], (self.x - 10, self.y + 20))
            if self.frame + 8 > 13:
                self.frame = 0
                self.stand()

    def collisioncheck(self):

        keys=key.get_pressed()
        global mask, currentMask

        #checks collision with the maasks of the map

        if keys[K_UP] and currentMask.get_at((self.x + 6, self.y)) != (0, 0, 0) and currentMask.get_at(
                (self.x + 43, self.y)) != (0, 0, 0):
            

                self.y -= 5

        elif keys[K_LEFT] and currentMask.get_at((self.x, self.y + 7)) != (0, 0, 0) and currentMask.get_at(
                (self.x, self.y + 58)) != (0, 0, 0):

                self.x -= 5

        elif keys[K_RIGHT] and currentMask.get_at((self.x + 48, self.y + 7)) != (0, 0, 0) and currentMask.get_at(
                (self.x + 48, self.y + 58)) != (0, 0, 0):
            
            
                self.x += 5

        elif keys[K_DOWN] and currentMask.get_at((self.x + 6, self.y + 64)) != (0, 0, 0) and currentMask.get_at(
                (self.x + 43, self.y + 64)) != (0, 0, 0):
         
          
                self.y += 5


        #checks collision with NPCs
                
        if keys[K_UP]:
            for rects in self.NPCrects:
                if rects.rect.collidepoint(self.x+6, self.y+17) or rects.rect.collidepoint(
                    (self.x + 40, self.y+17)):
                    self.y+=5
            #draw.circle(screen,(255,0,0),(self.x+6, self.y+17),1)
            #draw.circle(screen,(255,0,0),(self.x + 43, self.y+17),1)

        

        elif keys[K_LEFT]:
            for rects in self.NPCrects:
                if rects.rect.collidepoint(self.x+9, self.y + 18) or rects.rect.collidepoint(
                    (self.x+9, self.y + 56)) or rects.rect.collidepoint(self.x+9, self.y + 32):
                    self.x+=5
            
            #draw.circle(screen,(255,255,0),(self.x+9, self.y + 58),1)
            #draw.circle(screen,(255,255,0),(self.x+9, self.y + 18),1)
            #draw.circle(screen,(255,255,0),(self.x+9, self.y + 32),1)

        

        elif keys[K_RIGHT]:
            for rects in self.NPCrects:
                if rects.rect.collidepoint(self.x + 41, self.y + 18) or rects.rect.collidepoint(
                    (self.x+41, self.y + 56)) or rects.rect.collidepoint(self.x + 41, self.y + 32):
                    self.x-=5
            #draw.circle(screen,(255,0,255),(self.x + 41, self.y + 18),1)
            #draw.circle(screen,(255,0,255),(self.x+41, self.y + 58),1)
            #draw.circle(screen,(255,0,255),(self.x + 41, self.y + 32),1)

        

        elif keys[K_DOWN]:
            for rects in self.NPCrects:
                if rects.rect.collidepoint(self.x + 6, self.y + 57) or rects.rect.collidepoint(
                    (self.x + 40, self.y + 57)):
                    self.y-=5

            #draw.circle(screen,(0,255,0),(self.x + 43, self.y + 57),1)
            #draw.circle(screen,(0,255,0),(self.x + 6, self.y + 57),1)




    def move(self, keys):
        self.hitx = -500
        self.hity = -500
        self.centerx = self.x + 24
        self.centery = self.y + 32

        #draw.rect(screen,(255,0,0),self.rect,1)

        self.collisioncheck()
        
        #animates the correct walking animations and redifines Link's rect accordingly
        if keys[K_UP]:
            self.dir="up"
            self.rect = Rect(self.x + 2, self.y + 13, 44, 48)
            self.anim(self.up)

        elif keys[K_LEFT]:
            self.dir="left"
            self.anim(self.left)
            self.rect = Rect(self.x + 3, self.y + 13, 44, 48)

        elif keys[K_RIGHT]:
            self.dir="right"
            self.anim(self.right)
            self.rect = Rect(self.x, self.y + 13, 44, 48)

        elif keys[K_DOWN]:
            self.dir="down"
            self.anim(self.down)
            self.rect = Rect(self.x + 2, self.y + 14, 44, 48)

        

    #function for animating list of images
    def anim(self, sprites):
        self.frame += 0.8
        if self.frame > (len(sprites) - 1):
            self.frame = 0
        screen.blit(sprites[int(self.frame)], (self.x, self.y))

    #blits the correct image for standing
    def stand(self):
        self.frame = 0
        if self.dir == "up":
            self.rect = Rect(self.x , self.y + 13, 44, 50)
            screen.blit(self.up[0], (self.x, self.y))
        if self.dir == "right":
            self.rect = Rect(self.x, self.y + 13, 46, 48)
            screen.blit(self.right[0], (self.x, self.y))
        if self.dir == "left":
            self.rect = Rect(self.x + 3, self.y + 13, 46, 48)
            screen.blit(self.left[0], (self.x, self.y))
        if self.dir == "down":
            self.rect = Rect(self.x + 2, self.y + 14, 44, 56)
            screen.blit(self.down[0], (self.x, self.y))
        draw.rect(screen,(255,0,0),self.rect,1)






"""
:::'###::::'########::'########:::'#######::'##:::::'##:
::'## ##::: ##.... ##: ##.... ##:'##.... ##: ##:'##: ##:
:'##:. ##:: ##:::: ##: ##:::: ##: ##:::: ##: ##: ##: ##:
'##:::. ##: ########:: ########:: ##:::: ##: ##: ##: ##:
 #########: ##.. ##::: ##.. ##::: ##:::: ##: ##: ##: ##:
 ##.... ##: ##::. ##:: ##::. ##:: ##:::: ##: ##: ##: ##:
 ##:::: ##: ##:::. ##: ##:::. ##:. #######::. ###. ###::
..:::::..::..:::::..::..:::::..:::.......::::...::...:::"""


class Arrow:

    def __init__(self, image, x, y, dir):
        self.interval = 0
        self.x = x
        self.xorg = x
        self.y = y
        self.yorg = y
        self.dir = dir
        self.state = "shot"
        if self.dir == "up":
            self.image = transform.rotate(image, 90)
            #self.x += 22
        elif self.dir == "down":
            self.image = transform.rotate(image, 270)
            #self.x += 23
            #self.y += 44
        elif self.dir == "left":
            self.image = transform.rotate(image, 180)
            #self.y += 20
        elif self.dir == "right":
            self.image = image

    def shoot(self):
        global mask, currentMask
        if self.dir == "up" and currentMask.get_at((self.x, self.y)) != (0, 0, 0) and self.y >= 10:
            self.y -= 10
            draw.circle(screen, (255, 0, 0), (self.x, self.y), 4)
        elif self.dir == "down" and currentMask.get_at((self.x, self.y + 35)) != (0, 0, 0) and self.y + 30 <= 780:
            self.y += 10
            draw.circle(screen, (255, 0, 0), (self.x, self.y + 30), 4)
        elif self.dir == "left" and currentMask.get_at((self.x - 10, self.y)) != (0, 0, 0) and self.x - 10 >= 10:
            self.x -= 10
            draw.circle(screen, (255, 0, 0), (self.x - 10, self.y), 4)
        elif self.dir == "right" and currentMask.get_at((self.x + 35, self.y)) != (0, 0, 0) and self.x + 25 <= 1180:
            self.x += 10
            draw.circle(screen, (255, 0, 0), (self.x + 35, self.y), 4)
        screen.blit(self.image, (self.x, self.y))

        if self.state == "stop" and self.interval < 30:
            self.interval += 1
        if self.interval >= 30:
            self.state = "done"

"""
'########::'########:::'#######::::::::'##:'########::'######::'########:'####:'##:::::::'########:
 ##.... ##: ##.... ##:'##.... ##::::::: ##: ##.....::'##... ##:... ##..::. ##:: ##::::::: ##.....::
 ##:::: ##: ##:::: ##: ##:::: ##::::::: ##: ##::::::: ##:::..::::: ##::::: ##:: ##::::::: ##:::::::
 ########:: ########:: ##:::: ##::::::: ##: ######::: ##:::::::::: ##::::: ##:: ##::::::: ######:::
 ##.....::: ##.. ##::: ##:::: ##:'##::: ##: ##...:::: ##:::::::::: ##::::: ##:: ##::::::: ##...::::
 ##:::::::: ##::. ##:: ##:::: ##: ##::: ##: ##::::::: ##::: ##:::: ##::::: ##:: ##::::::: ##:::::::
 ##:::::::: ##:::. ##:. #######::. ######:: ########:. ######::::: ##::::'####: ########: ########:
..:::::::::..:::::..:::.......::::......:::........:::......::::::..:::::....::........::........::"""

class projectile:
    def __init__(self, xorg, yorg, x, y, sprite, speed):
        self.x = xorg
        self.y = yorg
        self.gotox = x
        self.gotoy = y
        self.sprite = sprite
        self.xsize = self.sprite.get_width()
        self.ysize = self.sprite.get_height()
        self.rect = Rect(self.x, self.y, self.xsize, self.ysize)
        self.gotox -= self.xsize/2
        self.gotoy -= self.ysize/2
        self.speed = speed
        self.dx = self.gotox - self.x
        self.dy = self.gotoy - self.y
        self.slope = (self.dy/max(1,self.dx))
        self.gotox += self.gotox*self.slope
        self.gotoy += self.gotoy*self.slope
        self.dist = max(1, hypot(self.dx, self.dy))
        self.state = "alive"
        self.rect = Rect(self.x, self.y, self.xsize, self.ysize)

    def move(self):
        global currentMask
        dist = max(1, hypot(self.dx, self.dy))
        self.vx = self.speed * self.dx / self.dist
        self.vy = self.speed * self.dy / self.dist
        if currentMask.get_at((int(self.x+ self.vx),int(self.y + self.vy))) != (0, 0, 0) and currentMask.get_at(
                            (int(self.x + self.vx + self.xsize), int(self.y + self.vy + self.ysize))) != (0, 0, 0) and int(self.y + self.vy + self.ysize) <= 800-self.ysize and int(self.y + self.vy) >= 0+self.ysize and int(self.x+ self.vx) >= self.xsize and int(self.x+ self.vx+self.xsize) <= 1200-self.xsize:
            draw.circle(screen, (255,0,0), (int(self.x + self.vx + self.xsize),int(self.y + self.vy + self.ysize)), 3)
            draw.circle(screen, (0,255,0), (int(self.x+ self.vx),int(self.y + self.vy)), 3)
            self.x += self.vx
            self.y += self.vy
        else:
            self.state = "dead"
        self.rect = Rect(self.x, self.y, self.xsize, self.ysize)
        draw.rect(screen, (255,0,0), self.rect, 1)
        screen.blit(self.sprite, (self.x, self.y))

"""
'##:::::'##:'####:'########::::'###::::'########::'########::
 ##:'##: ##:. ##::..... ##::::'## ##::: ##.... ##: ##.... ##:
 ##: ##: ##:: ##:::::: ##::::'##:. ##:: ##:::: ##: ##:::: ##:
 ##: ##: ##:: ##::::: ##::::'##:::. ##: ########:: ##:::: ##:
 ##: ##: ##:: ##:::: ##::::: #########: ##.. ##::: ##:::: ##:
 ##: ##: ##:: ##::: ##:::::: ##.... ##: ##::. ##:: ##:::: ##:
. ###. ###::'####: ########: ##:::: ##: ##:::. ##: ########::
:...::...:::....::........::..:::::..::..:::::..::........:::"""

class wizard:
    """teleports to random places, and shoots fireballs towards you"""
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.upAnim = []
        self.downAnim = []
        self.rightAnim = []
        self.leftAnim = []
        self.telePOS = []
        self.health = 4
        self.interval = 0
        self.hit = 0 
        self.hitDir = True
        self.bullets = []
        self.state = "alive"
        self.rect = Rect(self.x+20, self.y, 50, 60)
        for i in range(4):
            self.upAnim.append(image.load("Wizrobe/Wizrobe%i.png"%(i)))
        for i in range(4):
            self.downAnim.append(image.load("Wizrobe/wizzrobe3%i.png"%(i)))
        for i in range(4):
            self.rightAnim.append(image.load("Wizrobe/Wizzrobe2%i.png"%(i)))
        for i in range(4):
            self.leftAnim.append(transform.flip(self.rightAnim[i], True, False))
        for x in range (100, 1100, 200):
            for y in range(100, 700, 200):
                self.telePOS.append((x,y))

    def collide(self, hitx, hity, targetx, targety, targetrect, enemrects, arrowlist):
        #gets bullets to move, and makkes link take damage. Also gets rid of bullet when it hits something
        for p in self.bullets:
            p.move()
            if p.state == "dead":
                self.bullets.remove(p)
            if targetrect.colliderect(p.rect):
                if Main.char.interval2 >= 90:
                    Main.char.hp -= 1
                    Main.char.interval2 = 30
                    p.state = "dead"
        #taking damage
        if self.state == "alive":
            if self.rect.collidepoint(hitx, hity) and self.health > 0 :
                self.health -= 1
                self.state = "hurt"
            for arrows in arrowlist:
                if self.rect.collidepoint(arrows.x, arrows.y) and self.health > 0:
                    self.health -= 1
                    self.state = "hurt"
                    arrows.state = "done"
        if self.state == "hurt":
            self.hit+=1
            if self.hitDir:
                self.x += 5
                self.rect = Rect(self.x+20, self.y, 50, 60)
                self.hitDir = not self.hitDir
            elif not self.hitDir:
                self.x -= 5
                self.rect = Rect(self.x+20, self.y, 50, 60)
                self.hitDir = not self.hitDir
            if self.hit == 10:
                self.hit = 0
                self.state = "alive"
        #kills itself if health is 0
        if self.health == 0:
            Main.wizardKilled += 1
            self.state = "dead"
        #teleports itself every 410 counts
        elif self.interval %400 == 0:
            self.teleport(targetrect, enemrects)

        self.anim(targetx, targety)
    def anim(self, targetx, targety):    
        #detirmins which way he will face
        self.difx = self.x - targetx
        self.dify = self.y - targety
        if abs(self.difx) > abs(self.dify) :
            if self.difx > 0:
                self.dir = "left"
            else:
                self.dir = "right"
        elif abs(self.difx) < abs(self.dify):
            if self.dify > 0:
                self.dir = "up"
            else:
                self.dir = "down"

        #blits frame based on when he is gonna attack
        frame = 0
        if (self.interval)%75 > 45:
            frame = 1
        if self.interval%75 > 55:
            frame = 2
        if self.interval%75 > 65:
            frame = 3
        if self.dir == "up":
            screen.blit(self.upAnim[frame], (self.x, self.y))
        elif self.dir == "down":
            screen.blit(self.downAnim[frame], (self.x, self.y))
        elif self.dir == "left":
            screen.blit(self.leftAnim[frame], (self.x, self.y))
        elif self.dir == "right":
            screen.blit(self.rightAnim[frame], (self.x, self.y)) 
        #shoots bullet every 50 counts        
        if self.interval%75 == 0:
            self.bullets.append(projectile(self.x+30, self.y+15, targetx, targety, image.load("Wizrobe/a.png"), 10))

    def teleport(self, targetrect, enemrects):
        go = True
        while go :
            x = self.telePOS[randint(0,14)][0]
            y = self.telePOS[randint(0,14)][1]
            if len(enemrects) == 0:
                go = False
            for r in enemrects:
                if r.x != x:
                    go = False
                 
        self.x, self.y = x, y
        self.rect = Rect(self.x+20, self.y, 50, 60)



"""
'########:'##::: ##:'########:'##::::'##:'##:::'##:
 ##.....:: ###:: ##: ##.....:: ###::'###:. ##:'##::
 ##::::::: ####: ##: ##::::::: ####'####::. ####:::
 ######::: ## ## ##: ######::: ## ### ##:::. ##::::
 ##...:::: ##. ####: ##...:::: ##. #: ##:::: ##::::
 ##::::::: ##:. ###: ##::::::: ##:.:: ##:::: ##::::
 ########: ##::. ##: ########: ##:::: ##:::: ##::::
........::..::::..::........::..:::::..:::::..:::::"""


class enemy:

    def __init__(self, x, y):
        #initializes all of the moblins properties
        self.nmrects = []

        self.x = x
        self.y = y
        self.rect = Rect(self.x, self.y, 40, 100)
        self.health = 4
        self.counter = 0
        self.frame = 0
        self.over = True
        self.attup = []
        self.attleft = []
        self.attright = []
        self.attdown = []
        self.dying = []

        self.enemiesAnim = []

        #initializes all of his images
        for num in range(31):
            e = image.load(("enemies/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.enemiesAnim.append(e)

        for i in range(8):
            s = image.load(("smoke/%s.png" % (str(i))))
            s = transform.scale2x(s)
            self.enemiesAnim.append(s)

        for i in range(16, 20):
            self.attup.append(self.enemiesAnim[i])
        for i in range(20, 24):
            self.attleft.append(self.enemiesAnim[i])
        for i in range(24, 28):
            self.attright.append(self.enemiesAnim[i])
        for i in range(28, 31):
            self.attdown.append(self.enemiesAnim[i])
        for i in range(31, 38):
            self.dying.append(self.enemiesAnim[i])

        #more of his stats
        self.interval = 30
        self.state = "alive"
        self.dir = "down"
        self.index = 0

    #function for animating
    def anim(self, sprites):
        self.frame += 0.1
        if self.frame > len(sprites):
            self.frame = 0
        screen.blit(sprites[int(self.frame)], (self.x, self.y))

    def collide(self, hitx, hity, targetx, targety, colrect, enemrects, arrowlist):

        #gets all of the other moblin rectangles
        for i in range(len(enemrects)):
            self.nmrects.append(enemrects[i].rect)

        #when hit by sword and also uses interval for invincibility frame
        if self.rect.collidepoint(hitx, hity) and self.interval > 30 and self.health > 0:
            self.interval = 0
            self.health -= 1

        #when hit by arrow
        for arrows in arrowlist:
            if self.rect.collidepoint(arrows.x, arrows.y) and self.interval > 30 and self.health > 0:
                self.interval = 0
                self.health -= 1
                arrows.state = "done"
                
        global mask, currentMask

        #gets knocked back unless touching map mask
        if self.interval < 10:
            if self.dir == "right" and currentMask.get_at(self.rect.topleft) != (0,0,0) and currentMask.get_at(self.rect.bottomleft) != (0,0,0):
                self.x -= 15
                screen.blit(self.attright[0], (self.x, self.y))
                self.rect = Rect(self.x, self.y, 110, 55)
                
            if self.dir == "left"  and currentMask.get_at(self.rect.topright) != (0,0,0) and currentMask.get_at(self.rect.bottomright) != (0,0,0):
                self.x += 15
                screen.blit(self.attleft[0], (self.x, self.y))
                self.rect = Rect(self.x, self.y, 110, 55)
                
            if self.dir == "up"  and currentMask.get_at(self.rect.bottomright) != (0,0,0) and currentMask.get_at(self.rect.bottomleft) != (0,0,0):
                self.y += 15
                screen.blit(self.attup[0], (self.x, self.y))
                self.rect = Rect(self.x, self.y, 55, 76)
                
            if self.dir == "down"  and currentMask.get_at(self.rect.topleft) != (0,0,0) and currentMask.get_at(self.rect.topright) != (0,0,0):
                self.y -= 15
                screen.blit(self.attdown[0], (self.x, self.y))
                self.rect = Rect(self.x, self.y, 55, 76)
                
        #when dead, exploding animation occurs
        if self.interval > 10 and self.health == 0 and self.interval < 40:
            self.index += 0.2
            screen.blit(self.dying[int(self.index)], (self.x, self.y))

        #after exploding animation it is considered dead
        if self.interval > 40 and self.health == 0:
            Main.moblinKilled += 1
            self.state = "dead"
            
        #when it is alive with more than 0 hp it moves towards the player
        if self.health > 0:
            self.move(targetx, targety, colrect)

    def move(self, targetx, targety, colrect):
        global currentMask

        # makes sure the enemies dont hit eachother
        for rects in self.nmrects:
            for rects2 in self.nmrects:
                dx = self.x - rects2.centerx
                dy = self.y - rects2.centery

                dist = max(1, hypot(dx, dy))
                d2 = dist ** 2
                self.x += 10 * dx / d2
                self.y += 10 * dy / d2

        # finds the distance between the enemy and player and enemy runs towards player
        self.dx = targetx - self.rect.centerx
        self.dy = targety - self.rect.centery

 
        dist = max(1, hypot(self.dx, self.dy))

        self.vx = 2.5 * self.dx / dist
        self.vy = 2.5 * self.dy / dist

        d2 = dist ** 2

        # the enemy does not hit the player
        if colrect.colliderect(self.rect) == False:
            self.x += self.vx
            self.y += self.vy

        self.nmrects = []

        # draw.rect(screen,(0,255,0),self.rect,1)

        #correct animation depending on which side it is to the player
        if self.y <= targety:
            if self.x < targetx:
                if abs(self.x - targetx) > abs(targety - self.y):
                    self.dir = "right"
                    self.anim(self.attright)
                    self.rect = Rect(self.x, self.y, 110, 55)

                elif abs(self.x - targetx) < abs(targety - self.y):
                    self.dir = "down"
                    self.anim(self.attdown)
                    self.rect = Rect(self.x, self.y, 55, 76)

            if self.x > targetx:
                if abs(self.x - targetx) > abs(targety - self.y):
                    self.dir = "left"
                    self.anim(self.attleft)
                    self.rect = Rect(self.x, self.y, 105, 55)

                elif abs(self.x - targetx) < abs(targety - self.y):
                    self.dir = "down"
                    self.anim(self.attdown)
                    self.rect = Rect(self.x, self.y, 55, 76)

        if self.y > targety:
            if self.x < targetx:
                if abs(self.x - targetx) > abs(targety - self.y):
                    self.dir = "right"
                    self.anim(self.attright)
                    self.rect = Rect(self.x, self.y, 110, 55)

                elif abs(self.x - targetx) < abs(targety - self.y):
                    self.dir = "up"
                    self.anim(self.attup)
                    self.rect = Rect(self.x, self.y, 55, 76)

            if self.x > targetx:
                if abs(self.x - targetx) > abs(targety - self.y):
                    self.dir = "left"
                    self.anim(self.attleft)
                    self.rect = Rect(self.x, self.y, 110, 60)

                elif abs(self.x - targetx) < abs(targety - self.y):
                    self.dir = "up"
                    self.anim(self.attup)
                    self.rect = Rect(self.x, self.y, 55, 76)

"""
:'######::'##::: ##::::'###::::'##:::'##:'########:
'##... ##: ###:: ##:::'## ##::: ##::'##:: ##.....::
 ##:::..:: ####: ##::'##:. ##:: ##:'##::: ##:::::::
. ######:: ## ## ##:'##:::. ##: #####:::: ######:::
:..... ##: ##. ####: #########: ##. ##::: ##...::::
'##::: ##: ##:. ###: ##.... ##: ##:. ##:: ##:::::::
. ######:: ##::. ##: ##:::: ##: ##::. ##: ########:
:......:::..::::..::..:::::..::..::::..::........::"""


class snake:
    """ The snake enemy that moves on the x or y axis only"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = 2
        self.state = "alive"
        self.frame = 0
        self.interval = 10
        self.dir = "right"
        self.rect = Rect(x, y, 34, 38)

        # loading the sprites
        self.upAnim = []
        self.downAnim = []
        self.rightAnim = []
        self.leftAnim = []
        for i in range(1, 5):
            self.upAnim.append(
                transform.scale2x(image.load("snake/snakeUP%i.png" % (i))))
            self.downAnim.append(
                transform.scale2x(image.load("snake/snakeDOWN%i.png" % (i))))
            self.rightAnim.append(
                transform.scale2x(image.load("snake/snakeRIGHT%i.png" % (i))))
            self.leftAnim.append(transform.scale2x(
                transform.flip(image.load("snake/snakeRIGHT%i.png" % (i)), True, False)))

    def anim(self, sprites):
        """ Animating all the sprites"""
        self.frame += 0.1
        if self.frame > 3:
            self.frame = 0
        screen.blit(sprites[int(self.frame)], (self.x, self.y))

    def collide(self, hitx, hity, targetx, targety, colrect, enemrects, arrowlist):
        """ makes knockback, and death"""
        if self.rect.collidepoint(hitx, hity) and self.health > 0 and self.interval > 10:
            self.health -= 1
            self.interval = 0
        for arrows in arrowlist:
            if self.rect.collidepoint(arrows.x, arrows.y) and self.health > 0 and self.interval > 10:
                self.health -= 1
                self.interval = 0
                arrows.state = "done"
        if self.health == 0:
            Main.snakeKilled += 1
            self.state = "dead"
        self.move(targetx, targety, colrect, enemrects)
        if self.interval < 10:
            if self.dir == "right":
                self.x -= 10
                self.anim(self.rightAnim)
            if self.dir == "left":
                self.x += 10
                self.anim(self.leftAnim)
            if self.dir == "up":
                self.y += 10
                self.anim(self.upAnim)
            if self.dir == "down":
                self.y -= 10
                self.anim(self.downAnim)

    def move(self, targetx, targety, colrect, enemrects):
        """Makes snake move toward the player, and has ai to move around obsticles"""
        # makes sure the enemies dont hit eachother
        self.nmrects = []
        for i in range(len(enemrects)):
            self.nmrects.append(enemrects[i].rect)

        self.difx = self.x - targetx
        self.dify = self.y - targety
        dist = max(1, hypot(self.difx, self.dify))
        overRide = False
        overRightUp = True
        self.rect = Rect(self.x, self.y, 34, 38)

        global mask, currentMask
        # finds direction to move at
        if dist > 50:
            if abs(self.difx) > abs(self.dify) and int((self.interval / 10) % 2) != 1 and not overRide:
                if self.difx > 0:
                    self.dir = "left"
                else:
                    self.dir = "right"
            elif abs(self.difx) < abs(self.dify) and int((self.interval / 10) % 2) == 1 and not overRide:
                if self.dify > 0:
                    self.dir = "up"
                else:
                    self.dir = "down"
        # if close to the player, dosent go throught the player
        elif dist < 50:
            if abs(self.difx) > abs(self.dify) and int((self.interval / 10) % 2) != 1 and not overRide:
                if self.difx > 0:
                    self.dir = "right"
                else:
                    self.dir = "left"
            elif abs(self.difx) < abs(self.dify) and int((self.interval / 10) % 2) == 1 and not overRide:
                if self.dify > 0:
                    self.dir = "down"
                else:
                    self.dir = "up"
        # if close to another enemy dosent do throught the enemy
        for rects in self.nmrects:
            for rects2 in self.nmrects: 
                dx = self.x - rects2.centerx
                dy = self.y - rects2.centery

                dist = max(1, hypot(dx, dy))
                if dist < 50:
                    if abs(dx) > abs(dy) and int((self.interval / 10) % 2) != 1 and not overRide:
                        if dx > 0:
                            self.dir = "right"
                        else:
                            self.dir = "left"
                    elif abs(dx) < abs(dy) and int((self.interval / 10) % 2) == 1 and not overRide:
                        if dy > 0:
                            self.dir = "down"
                        else:
                            self.dir = "up"




        try:
            # moves towards the plaer if there are no obsticles in the way
            if self.dir == "up" and currentMask.get_at((self.x + 6, self.y)) != (0, 0, 0) and currentMask.get_at(
                    (self.x + 43, self.y)) != (0, 0, 0):  # and not enemrects.collidepoint((self.x + 6, self.y)) and not ((self.x + 43, self.y)):
                self.y -= 3
                self.anim(self.upAnim)
                self.overRightUp = True
                # if there is something in the way, tries to go right
            elif (not currentMask.get_at((self.x + 6, self.y)) != (0, 0, 0) or not currentMask.get_at(
                    (self.x + 43, self.y)) != (0, 0, 0)) and self.dir == "up":
                if self.overRightUp:
                    if currentMask.get_at((self.x + 48, self.y + 7)) != (0, 0, 0) and currentMask.get_at(
                            (self.x + 48, self.y + 58)) != (0, 0, 0):
                        self.x += 3
                        self.anim(self.rightAnim)
                    # if you cant do right, doesleft
                    else:
                        self.overRightUp = False
                        self.anim(self.upAnim)
                # goes left if you cant go right
                elif not self.overRightUp:
                    if currentMask.get_at((self.x, self.y + 7)) != (0, 0, 0) and currentMask.get_at(
                            (self.x, self.y + 58)) != (0, 0, 0):
                        self.x -= 3
                        self.anim(self.leftAnim)
                    # if you cant go left, it goes right
                    else:
                        self.overRightUp = True
                        self.anim(upAnim)

            if self.dir == "down" and currentMask.get_at((self.x + 6, self.y + 64)) != (0, 0, 0) and currentMask.get_at(
                    (self.x + 43, self.y + 64)) != (0, 0, 0):  # and not enemrects.collidepoint((self.x + 6, self.y + 64)) and not ((self.x + 43, self.y + 64)):
                self.y += 3
                self.anim(self.downAnim)
                self.overRightUp = True
            elif (not currentMask.get_at((self.x + 6, self.y + 64)) != (0, 0, 0) or not currentMask.get_at(
                    (self.x + 43, self.y + 64)) != (0, 0, 0)) and self.dir == "down":
                if self.overRightUp:
                    if currentMask.get_at((self.x + 48, self.y + 7)) != (0, 0, 0) and currentMask.get_at(
                            (self.x + 48, self.y + 58)) != (0, 0, 0):
                        self.x += 3
                        self.anim(rightAnim)
                    else:
                        self.overRightUp = False
                        self.anim(downAnim)
                elif not self.overRightUp:
                    if currentMask.get_at((self.x, self.y + 7)) != (0, 0, 0) and currentMask.get_at(
                            (self.x, self.y + 58)) != (0, 0, 0):
                        self.x -= 3
                        self.anim(leftAnim)
                    else:
                        self.overRightUp = True
                        self.anim(downAnim)


            if self.dir == "right" and currentMask.get_at((self.x + 48, self.y + 7)) != (0, 0, 0) and currentMask.get_at(
                    (self.x + 48, self.y + 58)) != (0, 0, 0):  # and not enemrects.collidepoint((self.x + 48, self.y + 7)) and not ((self.x + 48, self.y + 58)):
                self.x += 3
                self.anim(self.rightAnim)
                self.overRightUp = True
            elif (not currentMask.get_at((self.x + 48, self.y + 7)) != (0, 0, 0) or not currentMask.get_at(
                    (self.x + 48, self.y + 58)) != (0, 0, 0)) and self.dir == "right":
                if self.overRightUp:
                    if currentMask.get_at((self.x + 6, self.y)) != (0, 0, 0) and currentMask.get_at(
                            (self.x + 43, self.y)) != (0, 0, 0):
                        self.y -= 3
                        self.anim(upAnim)
                    else:
                        self.overRightUp = False
                        self.anim(rightAnim)
                elif not self.overRightUp:
                    if currentMask.get_at((self.x + 6, self.y + 64)) != (0, 0, 0) and currentMask.get_at(
                            (self.x + 43, self.y + 64)) != (0, 0, 0):
                        self.y += 3
                        self.anim(downAnim)
                    else:
                        self.overRightUp = True
                        self.anim(rightAnim)
            if self.dir == "left" and currentMask.get_at((self.x, self.y + 7)) != (0, 0, 0) and currentMask.get_at(
                    (self.x, self.y + 58)) != (0, 0, 0):  # and not enemrects.collidepoint((self.x, self.y + 7)) and not ((self.x, self.y + 58)):
                self.x -= 3
                self.anim(self.leftAnim)
                self.overRightUp = True
            elif (not currentMask.get_at((self.x, self.y + 7)) != (0, 0, 0) or not currentMask.get_at(
                    (self.x, self.y + 58)) != (0, 0, 0)) and self.dir == "left":
                if self.overRightUp:
                    if currentMask.get_at((self.x + 6, self.y)) != (0, 0, 0) and currentMask.get_at(
                            (self.x + 43, self.y)) != (0, 0, 0):
                        self.y -= 3
                        self.anim(upAnim)
                    else:
                        self.overRightUp = False
                        self.anim(leftAnim)
                elif not self.overRightUp:
                    if currentMask.get_at((self.x + 6, self.y + 64)) != (0, 0, 0) and currentMask.get_at(
                            (self.x + 43, self.y + 64)) != (0, 0, 0):
                        self.y += 3
                        self.anim(downAnim)
                    else:
                        self.overRightUp = True
                        self.anim(leftAnim)
        except:
            # if snake is too close to the edge, use this
            if self.dir == "up":
                self.anim(self.upAnim)
            elif self.dir == "down":
                self.anim(self.downAnim)
            elif self.dir == "right":
                self.anim(self.rightAnim)
            elif self.dir == "left":
                self.anim(self.leftAnim)



        self.rect = Rect(self.x, self.y, 34, 38)
        draw.rect(screen, (255, 0, 0), self.rect, 1)

"""
:'######::'##::::'##:'##::::'##::'######::'##::::'##:'##::::'##:
'##... ##: ##:::: ##: ##:::: ##:'##... ##: ##:::: ##: ##:::: ##:
 ##:::..:: ##:::: ##: ##:::: ##: ##:::..:: ##:::: ##: ##:::: ##:
 ##::::::: #########: ##:::: ##: ##::::::: #########: ##:::: ##:
 ##::::::: ##.... ##: ##:::: ##: ##::::::: ##.... ##: ##:::: ##:
 ##::: ##: ##:::: ##: ##:::: ##: ##::: ##: ##:::: ##: ##:::: ##:
. ######:: ##:::: ##:. #######::. ######:: ##:::: ##:. #######::
:......:::..:::::..:::.......::::......:::..:::::..:::.......:::"""
class chuchu:
    def __init__(self, x, y):
        self.x = x
        self.health = 3
        self.y = y
        self.rect = Rect(x,y,52,88)
        self.bullets = []
        self.sprite = []
        self.hurtSprite = []
        for i in range(16):
            self.sprite.append(transform.scale2x(transform.scale2x(image.load("chuchu/chuchu%s.png"%(str(i))))))
        for i in range(16):
            self.hurtSprite.append(transform.scale2x(transform.scale2x(image.load("chuchu/hurt/hurt%s.png"%(str(i))))))
        self.interval = 0
        self.hurtInterval = 0
        self.state = "alive"

    def collide(self, hitx, hity, targetx, targety, targetrect, enemrects, arrowlist):
        if self.interval > 60:
            self.interval = 0
        if self.state == "hurt":
            self.hurtInterval += 1
            if self.hurtInterval > 10:
                self.state = "alive"
                self.hurtInterval = 0
        if self.state == "alive":
            print(self.interval//4)
            screen.blit(self.sprite[(self.interval)//4], (self.x, self.y))
        elif self.state == "hurt":
            print(self.interval//4)
            screen.blit(self.hurtSprite[(self.interval)//4], (self.x, self.y))

        if self.state == "alive":
            if self.rect.collidepoint(hitx, hity) and self.health > 0:
                self.health -= 1
                self.state = "hurt"
            for arrows in arrowlist:
                if self.rect.collidepoint(arrows.x, arrows.y) and self.health > 0 and self.interval > 10:
                    self.health -= 1
                    self.state = "hurt"
                    arrows.state = "done"
        if self.interval > 63:
            self.interval = 0
        if self.state == "hurt":
            self.hurtInterval += 1
            if self.hurtInterval > 10:
                self.state = "alive"
                self.hurtInterval = 0
        if self.state == "alive":
            screen.blit(self.sprite[(self.interval)//4], (self.x, self.y))
        elif self.state == "hurt":
            screen.blit(self.hurtSprite[(self.interval)//4], (self.x, self.y))

        if self.state == "alive":
            if self.rect.collidepoint(hitx, hity) and self.health > 0:
                self.health -= 1
                self.state = "hurt"
            for arrows in arrowlist:
                if self.rect.collidepoint(arrows.x, arrows.y) and self.health > 0 and self.interval > 10:
                    self.health -= 1
                    self.state = "hurt"
                    arrows.state = "done"


        if self.interval == 40:
            self.bullets.append(projectile(self.x, self.y, targetx, targety, image.load("Ball.png"), 10))
        for p in self.bullets:
            p.move()
            if p.state == "dead":
                self.bullets.remove(p)
            if targetrect.colliderect(p.rect):
                if Main.char.interval2 >= 90:
                    Main.char.hp -= 1
                    Main.char.interval2 = 30
                    p.state = "dead"
        if self.health == 0:
            self.state = "dead"

""""
'##::: ##:'########:::'######::
 ###:: ##: ##.... ##:'##... ##:
 ####: ##: ##:::: ##: ##:::..::
 ## ## ##: ########:: ##:::::::
 ##. ####: ##.....::: ##:::::::
 ##:. ###: ##:::::::: ##::: ##:
 ##::. ##: ##::::::::. ######::
..::::..::..::::::::::......:::"""


class NPC:
    def __init__(self,words,x,y,width,height,sprites):
        #initializing all of its properties
        self.words=words
        self.textindex=0
        self.wordstyle = font.SysFont("Franklin Gothic Heavy", 40)
        self.text=""
        self.interval=0
        self.index=0
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.rect=Rect(x,y,self.width,self.height)
        self.player=rect
        self.cont=True
        self.state="run"
        self.sprites=sprites
        self.dir="down"


  
    #function to make blitting font easier
    def font_blit(self, string, x, y, colour, titlestyle):
        screen.blit(titlestyle.render(string, 1, colour), (x, y))


    def spriteupdate(self,player):
        """updates the sprite accordingly"""
        keys=key.get_pressed()
        draw.rect(screen,(0,255,255),self.rect,1)
 
   

        if keys[K_s] and self.state=="run":
            if self.rect.collidepoint(player.rect.topleft[0]+5,player.rect.topleft[1]) or self.rect.collidepoint(player.rect.topright[0]-5,player.rect.topleft[1]):
                if player.dir=="up":
                    self.dir="down"
        
            elif self.rect.collidepoint(player.rect.topleft[0],player.rect.topleft[1]+5) or self.rect.collidepoint(player.rect.topleft[0],player.rect.bottomleft[1]-5):
                if player.dir=="left":
                    self.dir="right"
                
            elif self.rect.collidepoint(player.rect.topright[0],player.rect.topright[1]+5) or self.rect.collidepoint(player.rect.topright[0],player.rect.bottomright[1]-5):
                if player.dir=="right":
                    self.dir="left"

            elif self.rect.collidepoint(player.rect.bottomleft[0]+5,player.rect.bottomleft[1]) or self.rect.collidepoint(player.rect.bottomright[0]-5,player.rect.bottomleft[1]):
                if player.dir=="down":
                    self.dir="up"

        if self.dir=="down":
            screen.blit(self.sprites[3],(self.x+2,self.y+6))

        if self.dir=="left":
            screen.blit(self.sprites[2],(self.x+2,self.y+6))

        if self.dir=="right":
            screen.blit(self.sprites[1],(self.x+2,self.y+6))

        if self.dir=="up":
            screen.blit(self.sprites[0],(self.x+2,self.y+6))

    #starts text accordingly too
    #made this a different function too since the rest of the sprites of the character
    #do not appear when start each of the textbox loops so I have to update all the sprites first
    #and then start all the textbox loops
    def textupdate(self,player):
        keys=key.get_pressed()

        
        if keys[K_s]==False:
            self.state="run"

        if keys[K_s] and self.state=="run":
            if self.rect.collidepoint(player.rect.topleft[0]+5,player.rect.topleft[1]) or self.rect.collidepoint(player.rect.topright[0]-5,player.rect.topleft[1]):
                if player.dir=="up":
                    self.textbox()
                    
            elif self.rect.collidepoint(player.rect.topleft[0],player.rect.topleft[1]+5) or self.rect.collidepoint(player.rect.topleft[0],player.rect.bottomleft[1]-5):
                if player.dir=="left":
                    self.textbox()
                    
            elif self.rect.collidepoint(player.rect.topright[0],player.rect.topright[1]+5) or self.rect.collidepoint(player.rect.topright[0],player.rect.bottomright[1]-5):
                if player.dir=="right":
                    self.textbox()
                    
            elif self.rect.collidepoint(player.rect.bottomleft[0]+5,player.rect.bottomleft[1]) or self.rect.collidepoint(player.rect.bottomright[0]-5,player.rect.bottomleft[1]):
                if player.dir=="down":
                    self.textbox()


    #function for the text appearing when talking
    def textbox(self):
        running=True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    display.flip()
                    quit()

            keys=key.get_pressed()
            

           
            #using interval to determine when the next letter will appear
            self.interval+=1
            #when there is first no lines or text, the box is drawn
            if self.index==0 and self.textindex==0:
                draw.rect(screen,(255,255,255),(10,650,1180,140))
                draw.rect(screen,(0,255,255),(10,650,1180,140),6)

            #while the letter index is less than the number of lines
            #the letters scroll through for the text effect
            if self.index<len(self.words[self.textindex]) and self.cont:
                #every 5000 milliseconds a new letter is added to what is displayed
                if self.interval%5000==0:
                    self.text+=self.words[self.textindex][self.index]
                    #they are blitted in different locations whether the line is odd or even
                    if self.textindex%2==0:
                        self.font_blit(self.text, 20, 660, (0,0,0), self.wordstyle)
                    else:
                        self.font_blit(self.text, 20, 720, (0,0,0), self.wordstyle)
                    self.index+=1
                    display.flip()
            #when the letters is done blitting for a line, it goes the the next line
            #and resets everything
            elif self.index>=len(self.words[self.textindex]) and self.textindex%2==0 and self.words[self.textindex]!=self.words[-1]:
                self.text=""
                self.textindex+=1
                self.index=0

            #when the text line is odd, self.cont is False, making the player have to press S to see the next line
            elif self.index>=len(self.words[self.textindex]) and self.textindex%2!=0 and self.words[self.textindex]!=self.words[-1]:
                self.text=""
                self.textindex+=1
                self.cont=False
                self.index=0
                
            #when it is false, the textbox is redrawn to go over the previous text
            if self.cont==False:
                draw.rect(screen,(255,255,255),(10,650,1180,140))
                draw.rect(screen,(0,255,255),(10,650,1180,140),6)

            #when on the last line, everything is reset and the textbox function ends
            if keys[K_s] and self.words[self.textindex]==self.words[-1] and self.index>=len(self.words[self.textindex]):
                self.index=0
                self.textindex=0
                self.text=""
                if self.words == ["Oh you look tired", "why dont you take a break."]:
                    Main.char.hp = 10
                    Main.fadeout(10)
                if self.words == ["Oh Link, I'm so glad to see you, I've been stuck in here ",
                                "ever since I entered this place, Malus did not accept our ",
                                "offerings and is now going on a rampages, I am sorry to make you ",
                                "do this, but please beat Malus, you're our only hope left "]:
                    Main.oldManTalked = True

                running=False
                self.state="done"
                
            #only continues when pressing S again
            if keys[K_s]:
                self.cont=True


"""
'##::::'##::::'###::::'########::
 ###::'###:::'## ##::: ##.... ##:
 ####'####::'##:. ##:: ##:::: ##:
 ## ### ##:'##:::. ##: ########::
 ##. #: ##: #########: ##.....:::
 ##:.:: ##: ##.... ##: ##::::::::
 ##:::: ##: ##:::: ##: ##::::::::
..:::::..::..:::::..::..:::::::::"""


class overworld:
    """
    uses an array to make the overworld. If he goes outside the boundries,
    it checks what is in the next cell 
    [ ][^][ ]
    [<]{X}[>]
    [ ][v][ ]"""
    def __init__(self):
        #all the maps, and their masks
        self.townTOP = image.load("townTOP.png").convert()
        self.townTOPmask = image.load("townTOPmask.png").convert()
        self.townBOT = image.load("townBOT.png").convert()
        self.townBOTmask = image.load("townBOTmask.png").convert()
        self.pathLEFT = image.load("pathLEFT.png").convert()
        self.pathLEFTmask = image.load("pathLEFTmask.png").convert()
        self.pathCENTER = image.load("pathCENTER.png").convert()
        self.pathCENTERmask = image.load("pathCENTERmask.png").convert()
        self.pathRIGHT = image.load("pathRIGHT.png").convert()
        self.pathRIGHTmask = image.load("pathRIGHTmask.png").convert()
        self.dungeonMID = image.load("dungeonMID.png").convert()
        self.dungeonMIDmask = image.load("dungeonMIDmask.png").convert()
        self.dungeonRIGHT = image.load("dungeonRIGHT.png").convert()
        self.dungeonRIGHTmask = image.load("dungeonRIGHTmask.png").convert()
        self.dungeonLEFT = image.load("dungeonLEFT.png").convert()
        self.dungeonLEFTmask = image.load("dungeonLEFTmask.png").convert()
        self.dungeonBOT = image.load("dungeonBOT.png").convert()
        self.dungeonBOTmask = image.load("dungeonBOTmask.png").convert()
        self.bossROOM = image.load("BossRoom.png").convert()
        self.bossROOMmask = image.load("BossRoomMask.png").convert()
        self.houseXTRA = image.load("House.png").convert()
        self.houseXTRAmask = image.load("HouseMask.png").convert()
                                   

        self.world = [[self.townTOP],
                      [self.townBOT],
                      [self.pathLEFT, self.pathCENTER, self.pathRIGHT],
                      [self.pathLEFT, self.dungeonLEFT, self.dungeonMID, self.dungeonRIGHT],
                      [self.houseXTRA, self.dungeonLEFT, self.dungeonBOT]]
        self.currentMAP = [-1, 0]
        global masks, currentMask
        masks = {self.townTOP: self.townTOPmask, self.townBOT: self.townBOTmask,
                 self.pathLEFT: self.pathLEFTmask, self.pathCENTER: self.pathCENTERmask,
                 self.pathRIGHT: self.pathRIGHTmask, self.dungeonBOT: self.dungeonBOTmask,
                 self.dungeonLEFT: self.dungeonLEFTmask, self.dungeonMID: self.dungeonMIDmask, 
                 self.dungeonRIGHT:self.dungeonRIGHTmask, self.bossROOM: self.bossROOMmask, 
                 self.houseXTRA:self.houseXTRAmask}
        currentMask = masks[self.world[self.currentMAP[0]][self.currentMAP[1]]]

        self.NPCsprites = []
        self.Garysprites = []
        self.Redsprites = []
        self.Momsprites = []
        self.Brendonsprites = []
        self.Dawnsprites = []
        self.Fmsprites = []
        for i in range(4):
            e = image.load(("NPC/g1/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.Garysprites.append(e)
        for i in range(4):
            e = image.load(("NPC/r1/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.Redsprites.append(e)
        for i in range(4):
            e = image.load(("NPC/s1/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.Momsprites.append(e)
        for i in range(4):
            e = image.load(("NPC/b1/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.Brendonsprites.append(e)
        for i in range(4):
            e = image.load(("NPC/d1/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.Dawnsprites.append(e)
        for i in range(4):
            e = image.load(("NPC/f1/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.Fmsprites.append(e)

        for num in range(4):
            e = image.load(("NPC/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.NPCsprites.append(e)

        for num in range(4):
            e = image.load(("NPC/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.NPCsprites.append(e)



        self.portalsprites=[]
        for num in range(15):
            p=transform.scale2x(image.load("portal/p%s.png" % (str(num))))
            self.portalsprites.append(p)

        self.portal = Rect(520,330,120,120)
        self.house = Rect(290,310,20,40)
        self.houseEXIT = Rect(600,780,50,20)
        self.portalframe = 0

    def drawMAP(self, x, y):
        dungeonsCleared = True
        move = False
        global masks, currentMask
        # print(x, y, self.currentMAP)

        if x + 64 > 1200:
            self.last = (self.world[self.currentMAP[0]][self.currentMAP[1]])
            self.currentMAP[1] += 1
            Main.char.x -= 1136
            currentMask = masks[
                self.world[self.currentMAP[0]][self.currentMAP[1]]]
            self.moveMap(
                self.world[self.currentMAP[0]][self.currentMAP[1]], self.last, "right")
            move = True
        if x < 0:
            self.last = (self.world[self.currentMAP[0]][self.currentMAP[1]])
            self.currentMAP[1] -= 1
            Main.char.x += 1136
            currentMask = masks[
                self.world[self.currentMAP[0]][self.currentMAP[1]]]
            self.moveMap(
                self.world[self.currentMAP[0]][self.currentMAP[1]], self.last, "left")
            move = True
        if y + 64 > 800:
            self.last = (self.world[self.currentMAP[0]][self.currentMAP[1]])
            self.currentMAP[0] += 1
            Main.char.y -= 736
            currentMask = masks[
                self.world[self.currentMAP[0]][self.currentMAP[1]]]
            self.moveMap(
                self.world[self.currentMAP[0]][self.currentMAP[1]], self.last, "down")
            move = True
        if y < 0:
            self.last = (self.world[self.currentMAP[0]][self.currentMAP[1]])
            self.currentMAP[0] -= 1
            Main.char.y += 736
            currentMask = masks[
                self.world[self.currentMAP[0]][self.currentMAP[1]]]
            self.moveMap(
                self.world[self.currentMAP[0]][self.currentMAP[1]], self.last, "up")
            move = True

        screen.blit(self.world[self.currentMAP[0]][self.currentMAP[1]], (0, 0))
        draw.rect(screen, (255,0,255), self.portal, 2)
        if self.world[self.currentMAP[0]][self.currentMAP[1]] == self.dungeonMID and Main.oldManTalked:
            self.portalframe+= 1
            if self.portalframe == 150:
                self.portalframe = 0
            screen.blit(self.portalsprites[self.portalframe//10],(520,330))
            
            
            if self.portal.colliderect(Main.char.rect):
                Main.char.hp = 10
                currentMask = self.bossROOMmask
                Main.bossloop()

        if self.world[self.currentMAP[0]][self.currentMAP[1]] == self.townTOP:
            
            draw.rect(screen, (255, 0, 255), self.house, 2)
            if self.house.colliderect(Main.char.rect):
                self.currentMAP[0] -= 1
                Main.fadeout(10)
                self.spawn()
                currentMask = masks[
                self.world[self.currentMAP[0]][self.currentMAP[1]]]
                Main.char.x = 600
                Main.char.y = 700
                screen.blit(self.world[self.currentMAP[0]][self.currentMAP[1]], (0, 0))
                move = True
                
        if self.world[self.currentMAP[0]][self.currentMAP[1]] == self.houseXTRA:
            draw.rect(screen, (255, 0, 255), self.houseEXIT, 2)
            if self.houseEXIT.colliderect(Main.char.rect):
                self.currentMAP[0] += 1
                Main.fadeout(10)
                self.spawn()
                currentMask = masks[
                self.world[self.currentMAP[0]][self.currentMAP[1]]]
                Main.char.x = 280
                Main.char.y = 350
                screen.blit(self.world[self.currentMAP[0]][self.currentMAP[1]], (0, 0))
                move = True

        
        return move
        #draw.circle(screen, (255, 255,255), (x,y), 100)

    def moveMap(self, lastMap, currentMap, dir):
        running = True
        self.movex = 0
        self.movey = 0
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False

            if dir == "down":
                screen.blit(currentMap, (self.movex, self.movey))
                screen.blit(lastMap, (self.movex, self.movey + 800))
                self.movey -= 4
            elif dir == "up":
                screen.blit(currentMap, (self.movex, self.movey))
                screen.blit(lastMap, (self.movex, self.movey - 800))
                self.movey += 4
            elif dir == "right":
                screen.blit(currentMap, (self.movex, self.movey))
                screen.blit(lastMap, (self.movex + 1200, self.movey))
                self.movex -= 4
            elif dir == "left":
                screen.blit(currentMap, (self.movex, self.movey))
                screen.blit(lastMap, (self.movex - 1200, self.movey))
                self.movex += 4
            if self.movey == -800 or self.movey == 800 or self.movex == -1200 or self.movex == 1200:
                running = False

            display.flip()

    def spawn(self):
        location = self.world[self.currentMAP[0]][self.currentMAP[1]]
        eList = []
        allNPCS = []
        
        if location == self.houseXTRA :
            allNPCS.append(NPC(["Oh you look tired",
                                "why dont you take a break."], 600,500,40,44,self.NPCsprites[0:4]))


        if location == self.pathLEFT and Main.snakeTask:
            allNPCS.append(NPC(["You should kill the snakes and head back."], 1150, 0, 50,800, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))
            eList.append(snake(300,600))
            eList.append(snake(900,400))

        if location == self.townTOP and Main.malusAwakened:
            Main.malusloop()

        if location == self.pathLEFT and not Main.snakeTask:
            eList.append(snake(300,600))
            eList.append(snake(900,400))

        if location == self.pathCENTER:
            eList.append(chuchu(195,170))
            eList.append(chuchu(640,200))
            eList.append(chuchu(980,525))

        if location == self.pathRIGHT:
            eList.append(snake(523, 713))
            eList.append(snake(950, 713))
            eList.append(snake(830, 375))
            eList.append(snake(380, 330))
            eList.append(snake(650, 215))


        if location == self.dungeonLEFT:
            eList.append(enemy(200,185))
            eList.append(enemy(200,615))
            eList.append(enemy(800,185))
            eList.append(enemy(800,615))
        if location == self.dungeonRIGHT:
            eList.append(wizard(130, 665))
            eList.append(wizard(130, 135))
            eList.append(wizard(1030, 135))
            eList.append(wizard(1030, 665))
        if location == self.dungeonBOT:
            allNPCS.append(NPC(["Oh Link, I'm so glad to see you, I've been stuck in here ",
                                "ever since I entered this place, Malus did not accept our ",
                                "offerings and is now going on a rampages, I am sorry to make you ",
                                "do this, but please beat Malus, you're our only hope left "], 600,390, 40,44,self.NPCsprites[0:4]))





        if location == self.dungeonMID and Main.dungeonPASS == "none":
            allNPCS.append(NPC(["An invisible force is blocking your way."],0,270,20,400, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))
            allNPCS.append(NPC(["An invisible force is blocking your way."], 1175,270,20,400, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))
            allNPCS.append(NPC(["An invisible force is blocking your way."], 540,780,500,500, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))

        if location == self.dungeonMID and Main.dungeonPASS == "moblin":
            allNPCS.append(NPC(["An invisible force is blocking your way."], 1175,270,20,400, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))
            allNPCS.append(NPC(["An invisible force is blocking your way."], 540,780,500,500, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))

        if location == self.dungeonMID and Main.dungeonPASS == "wizard":
            allNPCS.append(NPC(["An invisible force is blocking your way."], 0,270,20,400, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))
            allNPCS.append(NPC(["An invisible force is blocking your way."],  540,780,500,500, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))

        if location == self.dungeonMID and Main.dungeonPASS == "oldMan":
            allNPCS.append(NPC(["An invisible force is blocking your way."], 1175,270,50,400, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))
            allNPCS.append(NPC(["An invisible force is blocking your way."], 0,270,20,400, [image.load("invis.png"),
                image.load("invis.png"),image.load("invis.png"),image.load("invis.png")] ))

        return eList, allNPCS
"""elif location == self.pathLEFT:
            self.eList.append(chuchu(510,525))"""
"""
'########:::'#######:::'######:::'######::
 ##.... ##:'##.... ##:'##... ##:'##... ##:
 ##:::: ##: ##:::: ##: ##:::..:: ##:::..::
 ########:: ##:::: ##:. ######::. ######::
 ##.... ##: ##:::: ##::..... ##::..... ##:
 ##:::: ##: ##:::: ##:'##::: ##:'##::: ##:
 ########::. #######::. ######::. ######::
........::::.......::::......::::......:::"""
class boss:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.cooldown=550
        self.reset=600
        self.health=30
        self.pos=1
        self.rect=Rect(self.x,self.y,40,70)
        self.att=0
        self.hpinterval=60
        self.warning=[]
        self.damage=[]
        self.zap=""
        self.zapCoord=[(10,20,100,300),(210,40,100,300),(430,10,100,300),(600,50,100,300),(840,35,100,300),
                       (50,400,100,300),(230,420,100,300),(450,460,100,300),(670,310,100,300),(810,360,100,300),(310,390,100,300),
                       (70,320,100,300),(190,260,100,300),(350,370,100,300),(490,330,100,300),(900,290,100,300),(990,440,100,300)]
        self.zapindex=0
        self.zapanim=[]
        for num in range(1,11):
            zap=image.load("Zap/%s.png" %(str(num)))
            zap=transform.scale(zap,(200,300))
            self.zapanim.append(zap)

        self.sprite=[]
        for num in range(0,19):
            sprite=image.load("Boss Sprites/%s.png" %(str(num)))
            sprite=transform.scale2x(sprite)
            self.sprite.append(sprite)

        self.teleport=[]
        for num in range(0,10):
            sprite=image.load("Teleport/%s.png" %(str(num)))
            sprite=transform.scale(sprite,(150,150))
            self.teleport.append(sprite)

        self.horizontbeams=[]
        self.verticalbeams=[]
        for num in range(4):
            sprite=image.load("beam2/%s.png" %(str(num))).convert()
            sprite=transform.rotate(sprite,90)
            sprite=transform.scale(sprite,(40,1200))
            self.horizontbeams.append(sprite)
            sprite=transform.rotate(sprite,90)
            self.verticalbeams.append(sprite)

        self.horizontbeams[0]=transform.scale(self.horizontbeams[0],(8,1200))

        self.verticalbeams[0]=transform.scale(self.verticalbeams[0],(1200,8))


            
        self.clone=[]
        self.frame=0
        self.frame2=0
        self.dead=[]
        self.lasers=[]
        self.CLasers=[]
        self.indexlaser=-1
        self.disindex=0

        self.disCoord=[(300,500,1,1),(200,290,1,1),(580,410,1,1),
                       (800,710,1,1),(600,400,1,1),(900,300,1,1),
                       (420,480,1,1),(720,150,1,1),(320,320,1,1)]
        self.time=0
        self.state="alive"
        self.bulletsprite=transform.scale2x(image.load("shooting/ball.png"))
        self.bullets=[]
        self.bulletstate=1
        self.attlist=[1,2,3,4,5]
        self.attindex=4

        self.dyingsprites=[]
        for num in range(3):
            s = image.load("Boss Explode2/%s.png" % (str(num)))
            s = transform.scale(s,(150,150))
            self.dyingsprites.append(s)
        
                       
        

    def update(self,playerSword,arrowlist,targetrect):

    

        #self.anim2(self.teleport,0,0,0.75)
        #screen.blit(self.teleport[8],(0,0))
        #self.anim2(self.sprite[12:17],self.x,self.y,0.08)
        self.arrowlist=arrowlist
        self.playerSword=playerSword
        self.targetrect=targetrect
        
        for arrows in arrowlist:
            if self.rect.collidepoint(arrows.x, arrows.y) and self.hpinterval > 50 and self.health > 0:
                self.hpinterval=0
                self.health-=1
                arrows.state="done"
                print(self.health)

        if self.rect.collidepoint(playerSword) and self.hpinterval > 50 and self.health > 0:
            self.hpinterval=0
            self.health-=1
            print(self.health)

        if self.hpinterval == 0 and self.health ==0:
            self.frame = 0
            self.frame2 = 0
            self.damage=[]

        if self.hpinterval <= 70  and self.hpinterval>0 and self.health == 0:
            self.cooldown=666
            screen.blit(self.sprite[0],(self.x,self.y))
            self.anim(self.dyingsprites,self.x-55,self.y-35,0.3)
            

        if self.hpinterval > 70 and self.health == 0:
            Main.fadeout(2)
            if self.hpinterval==71:
                Main.endgame()
        
            
        if self.cooldown==self.reset:
            
            shuffle(self.zapCoord)
            shuffle(self.disCoord)
            self.zapindex=0
            self.frame2=0
            self.frame=0
            self.warp()
            self.cooldown=0
            self.clone=[]
            self.laserlist()
            self.indexlaser=-1
            self.disindex=0
            self.bullets=[]
            Main.heartspawn(self.rect.centerx,self.rect.centery)

        if self.cooldown<self.reset:
            self.randattack()

        self.rect=Rect(self.x,self.y,40,70)
        draw.rect(screen,(0,255,255),self.rect,1)
        
    def damaged(self):
        if self.hpinterval%13==0:
            screen.blit(self.sprite[0],(self.x,self.y))
        else:
            screen.blit(self.sprite[18],(self.x,self.y))

    def randattack(self):
        """self.damage=[]
            self.attindex+=1
            
            if self.attindex==5:
                shuffle(self.attlist)
                self.attindex=0
                
            self.att=self.attlist[self.attindex]"""
        if self.cooldown==1:
            self.damage=[]
            self.damage=[]
            self.attindex+=1
            
            if self.attindex==5:
                shuffle(self.attlist)
                self.attindex=0
                
            self.att=self.attlist[self.attindex]

        if self.att==1:
            self.thunderzap()
        elif self.att==2:
            self.cloneattack()
        elif self.att==3:
            self.laser()
        elif self.att==4:
            self.distortion()
        elif self.att==5:
            self.bullet()

    def bullet(self):
        if self.cooldown>30:
            if self.cooldown%201==0:
                self.bulletstate+=1
                if self.bulletstate==3:
                    self.bulletstate=1
                    
            if self.cooldown%50==0:
                if self.bulletstate==1:
                    for i in range(0,1200,240):
                        self.bullets.append(projectile(self.rect.centerx,self.rect.centery,i,0,self.bulletsprite,5))
                        self.bullets.append(projectile(self.rect.centerx,self.rect.centery,i,900,self.bulletsprite,5))

                    for i in range(0,800,240):
                        self.bullets.append(projectile(self.rect.centerx,self.rect.centery,0,i,self.bulletsprite,5))
                        self.bullets.append(projectile(self.rect.centerx,self.rect.centery,1200,i,self.bulletsprite,5))

                if self.bulletstate==2:
                    for i in range(0,1200,240):
                        self.bullets.append(projectile(self.rect.centerx,self.rect.centery,i+120,0,self.bulletsprite,5))
                        self.bullets.append(projectile(self.rect.centerx,self.rect.centery,i+120,900,self.bulletsprite,5))

                    for i in range(0,800,240):
                        self.bullets.append(projectile(self.rect.centerx,self.rect.centery,0,i+120,self.bulletsprite,5))
                        self.bullets.append(projectile(self.rect.centerx,self.rect.centery,1200,i+120,self.bulletsprite,5))
                    

        
        for bullets in self.bullets:
            bullets.move()
            if self.targetrect.colliderect(bullets.rect):
                if Main.char.interval2>=90:
                    Main.char.hp-=1
                    Main.char.interval2=30
                    bullets.state="dead"
                    
            if bullets.state=="dead":
                self.bullets.remove(bullets)

        self.charupdate()
    
    def distortion(self):

        if self.cooldown%50==0:
            self.time=1
            self.disindex+=1
            if self.disindex==5:
                self.disindex=0
            self.damage.append(Rect(self.disCoord[self.disindex]))
        for rects in self.damage:
            if rects[2]<900:
                rects[2]+=2
                rects[3]+=2
                rects[0]-=1
                rects[1]-=1
            self.distortrect(rects[0],rects[1],rects[2],rects[3],self.time)

        if len(self.damage)>5:
            self.damage=self.damage[1:]

        if self.cooldown%2==0:
            self.time+1
        if time==30:
            self.time=0

        self.charupdate()
        
    def distortrect(self,x,y,width,height,time):
        draw.rect(screen,(255,255,255),(x,y,width,height))
        for i in range(x-time,x+width,30):
            for j in range(y,y+height,10):
                
                draw.rect(screen,(0,0,0),(i,j,10,2))
                
                draw.rect(screen,(0,0,0),(i+15,j+5,10,2))      

            

    def laserlist(self):
        self.lasers=[]
        for i in range(0,1200,120):
            self.lasers.append(Rect(i+50,0,40,800))

        self.CLasers=[]
        self.CLasers.append(self.lasers)
        self.lasers=[]
        for i in range(0,800,120):
            self.lasers.append(Rect(0,i+50,1200,40))
            
        self.CLasers.append(self.lasers)
        self.lasers=[]
        for i in range(0,800,120):
            self.lasers.append(Rect(0,i+50,1200,40))
        for i in range(0,1200,120):
            self.lasers.append(Rect(i+50,0,40,800))

        self.CLasers.append(self.lasers)
        
    def laser(self):

        #adding all the lasers for wave of warning lasers

        if (self.cooldown-30)%166==0:
            
            self.indexlaser+=1
            if self.indexlaser>2:
                self.indexlaser=0
            self.warning.append(self.CLasers[self.indexlaser])

        #adding all the lasers for wave of warning lasers
            
        if self.cooldown%166==0:
            self.damage=[]
            for rects in self.CLasers[self.indexlaser]:
                self.damage.append(rects)
            self.warning=[]

     
            

        if self.cooldown>40:

            #all laser warning sprite blitting
            """if len(self.warning)>0:
                for rects in self.warning[-1]:
                    draw.rect(screen,(255,255,0),rects)"""
                    
            if self.indexlaser==0:
                for rects in self.CLasers[0]:
                    screen.blit(self.horizontbeams[0],(rects[0]+16,rects[1]-20))
            if self.indexlaser==1:
                for rects in self.CLasers[1]:
                    screen.blit(self.verticalbeams[0],(rects[0],rects[1]+16))
            if self.indexlaser==2:
                for rects in self.CLasers[0]:
                    screen.blit(self.horizontbeams[0],(rects[0]+16,rects[1]-20))
      

            """if len(self.damage)>0:
                for rects in self.damage:
                    draw.rect(screen,(255,0,0),rects)"""

            #all damaging laser sprite blitting
                    
            if len(self.damage)==10:
                 for i in range(0,1200,120):
                    self.anim(self.horizontbeams[1:4],i+50,0,0.45)
                
            if len(self.damage)==7:
                for i in range(0,1200,120):
                    self.anim(self.verticalbeams[1:4],0,i+50,0.45)

            if len(self.damage)==17:
                for i in range(0,1200,120):
                    self.anim(self.verticalbeams[1:4],0,i+50,0.45)
                for i in range(0,1200,120):
                    self.anim(self.horizontbeams[1:4],i+50,0,0.45)
                        
                           
                    


        self.charupdate()

    def warp(self):
        self.pos=randint(1,30)
        for pos in range(1,31):
            if self.pos<=10:
                if self.pos%2==0:
                    self.x=self.pos*100
                    self.y=200
                else:
                    self.x=self.pos*100
                    self.y=240
                

            if self.pos>10 and self.pos<=20:
                if self.pos%2==0:
                    self.x=(self.pos-10)*100
                    self.y=400
                else:
                    self.x=(self.pos-10)*100
                    self.y=440
                

            if self.pos>20 and self.pos<=30:
                if self.pos%2==0:
                    self.x=(self.pos-20)*100
                    self.y=600
                else:
                    self.x=(self.pos-20)*100
                    self.y=640

    def cloneattack(self):

        self.charupdate()
        if self.cooldown>25 and self.cooldown<40:
            self.anim(self.teleport,self.x-50,self.y-50,0.5)
        if self.cooldown==40:
            self.warp()

        if self.cooldown==40:
            for pos in range(1,31):
                if pos!=self.pos:
                    if pos<=10:
                        if pos%2==0:
                            self.clone.append(Rect(pos*100,200,40,70))
                            self.damage.append(Rect(pos*100,200,40,70))
                        else:
                            self.clone.append(Rect(pos*100,240,40,70))
                            self.damage.append(Rect(pos*100,240,40,70))
                            

                    elif pos>10 and pos<=20:

                        if pos%2==0:
                            self.clone.append(Rect((pos-10)*100,400,40,70))
                            self.damage.append(Rect((pos-10)*100,400,40,70))
                        else:
                            self.clone.append(Rect((pos-10)*100,440,40,70))
                            self.damage.append(Rect((pos-10)*100,440,40,70))
                            

                    elif pos>20 and pos<=30:
                        if pos%2==0:
                            self.clone.append(Rect((pos-20)*100,600,40,70))
                            self.damage.append(Rect((pos-20)*100,600,40,70))
                        else:
                            self.clone.append(Rect((pos-20)*100,640,40,70))
                            self.damage.append(Rect((pos-20)*100,640,40,70))
            
        if self.cooldown>40:
            for rects in self.clone:
                draw.rect(screen,(0,255,255),rects,1)
                screen.blit(self.sprite[0],(rects[0],rects[1]))
                for arrows in self.arrowlist:
                    if rects.collidepoint(arrows.x, arrows.y):
                        self.dead.append(rects)
                        self.damage.remove(rects)
                        self.explode(self.teleport,rects[0]-50,rects[1]-50,0,rects)
                        self.clone.remove(rects)

                if rects.collidepoint(self.playerSword):
                    self.dead.append(rects)
                    self.damage.remove(rects)
                    self.explode(self.teleport,rects[0]-50,rects[1]-50,0,rects)
                    self.clone.remove(rects)
                    
                

        """for rects in self.dead:
            self.explode(self.teleport,rects[0]-50,rects[1]-50,0,rects)
            
            self.dead.remove(rects)"""

    def explode(self,sprites,x,y,index,rects):
        if index>-1:
            index+=0.5
            if index>len(sprites):
                return False
            screen.blit(sprites[int(index)],(x,y))
        

        
        
        
    def thunderzap(self):
        
        if (self.cooldown-15)%40==0:
            self.zapindex+=1
            if self.zapindex>15:
                self.zapindex=0
            self.zap=(Rect(self.zapCoord[self.zapindex]))
            self.warning.append(self.zap)
            
        if self.cooldown%40==0:
            self.damage.append(self.zap)
            self.warning=[]

        for rects in self.warning:
            #draw.rect(screen,(255,255,255),rects)
            self.anim(self.zapanim[7:11],rects[0]-70,rects[1],0.05)
            

        for rects in self.damage:
            #draw.rect(screen,(255,0,0),rects)
            self.anim(self.zapanim[1:4],rects[0]-70,rects[1],0.024)

        if len(self.damage)>6:
            self.damage=self.damage[1:]

        self.charupdate()


    def anim(self, sprites,x,y,rate):
        self.frame += rate
        if self.frame > len(sprites):
            self.frame = 0
        screen.blit(sprites[int(self.frame)], (x,y))

    def anim2(self, sprites,x,y,rate):
        self.frame2 += rate
        if self.frame2 > len(sprites):
            self.frame2 = 0
        screen.blit(sprites[int(self.frame2)], (x,y))

    def charupdate(self):
      
        screen.blit(self.sprite[0],(self.x,self.y))

        if self.cooldown>self.reset-16 and self.cooldown<self.reset:
            self.anim2(self.teleport,self.x-50,self.y-50,0.5)

        if self.hpinterval <=50:
            self.damaged()

"""
'##::::'##::::'###::::'####:'##::: ##:
 ###::'###:::'## ##:::. ##:: ###:: ##:
 ####'####::'##:. ##::: ##:: ####: ##:
 ## ### ##:'##:::. ##:: ##:: ## ## ##:
 ##. #: ##: #########:: ##:: ##. ####:
 ##:.:: ##: ##.... ##:: ##:: ##:. ###:
 ##:::: ##: ##:::: ##:'####: ##::. ##:
..:::::..::..:::::..::....::..::::..:"""


class main:

    def __init__(self):
        # Getting Fonts
        self.titlestyle = font.SysFont("Franklin Gothic Heavy", 40)
        self.titlestyle2 = font.SysFont("Franklin Gothic Heavy", 20)
        self.titlestyle3 = font.SysFont("Comic Sans", 46)
        self.titlestyle4 = font.SysFont("Comic Sans", 22)
        self.titlestyle5 = font.SysFont("Comic Sans", 26)
        # standing animations
        self.spritesAnim = []
        self.spritesAnim = splitter(image.load("LinkTiles.png"), 8, 12)
        # slashing animationa
        self.slashAnim = []
        for num in range(7):
            s = image.load(("up%s.png" % (str(num + 1))))
            s = transform.scale2x(s)
            self.slashAnim.append(s)

        for num in range(7):
            s = image.load(("down%s.png" % (str(num + 1))))
            s = transform.scale2x(s)
            self.slashAnim.append(s)

        for num in range(6):
            s = image.load(("right%s.png" % (str(num + 1))))
            s = transform.scale2x(s)
            self.slashAnim.append(s)

        for num in range(6):
            s = image.load(("right%s.png" % (str(num + 1))))
            s = transform.scale2x(s)
            s = (transform.flip(s, True, False))
            self.slashAnim.append(s)

        # bow anim
        self.bowAnim = []

        for num in range(48):
            e = image.load(("bow and arrow/%s.png" % (str(num))))
            e = transform.scale2x(e)
            self.bowAnim.append(e)

        for num in range(16):
            e = image.load(("bow and arrow/%s.png" % (str(num))))
            e = transform.scale2x(e)
            e = transform.flip(e, True, False)
            self.bowAnim.append(e)
        # initializing character, enemies, etc
        self.BossSprites=[]
        self.BossSprites.append(transform.scale2x(image.load("Boss Sprites/0.png")))
        self.BossSprites.append(transform.scale2x(image.load("Boss Sprites/17.png")))
        self.BossSprites.append(transform.flip((transform.scale2x(image.load("Boss Sprites/17.png"))),True,False))
        self.BossSprites.append(transform.scale2x(image.load("Boss Sprites/5.png")))
        

        self.hearts = []
        self.heartsprite = transform.smoothscale(image.load("heart.png"), (20, 20))
        self.arrowbundle=[]
        self.arrowsprite=transform.rotate(image.load("bow and arrow/arrow.png"),90)
        self.bowsprite = transform.scale(image.load("bow icon.png"), (30, 30))
        self.char = Link(self.spritesAnim, 600, 550, self.bowAnim)
        self.xbutton = transform.smoothscale(image.load("x-button.jpg"), (35, 35))
        self.projectiles = []

        self.BossDefeat=transform.scale2x(image.load("Boss Sprites/19.png"))
        self.TBstate="running"
        self.vframe=0
        self.vortex=[]
        for num in range(4):
            s = image.load("Dark Portal/%s.png" % (str(num)))
            s = transform.scale(s,(90,90))
            self.vortex.append(s)
            
        self.repeat=0

        self.eframe=0
        self.Bexplode=[]
        for num in range(3):
            s = image.load("Boss Explode/%s.png" % (str(num)))
            s = transform.scale(s,(150,150))
            self.Bexplode.append(s)

        self.BossRoom=image.load("BossRoom.png").convert()
        self.startscreenIMAGE = image.load("start.png").convert()
        self.controllIMAGE = image.load("cont.png").convert()
        self.House=image.load("House.png").convert()
        self.townTOP=image.load("townTOP.png").convert()
        self.Mothersprite=transform.scale2x(image.load("NPC/3.png"))
        self.snakeKilled = 0
        self.moblinKilled = 0
        self.wizardKilled = 0
        self.malusAwakened = False
        self.dungeonPASS = "none"
        self.oldManTalked = False
        self.BossSprite=transform.scale2x(image.load("Boss Sprites/7.png"))



    def startscreen(self):
        start = True
        startRect = Rect(55,635, 245, 105)
        contRect = Rect(515, 635, 365, 105)
        while start:
            for e in event.get():
                if e.type == QUIT:
                    display.flip()
                    quit()
                mx, my  = mouse.get_pos()
                if e.type == MOUSEBUTTONUP:
                    if startRect.collidepoint((mx,my)):
                        start = False
                        self.startloop()
                    elif contRect.collidepoint((mx,my)):
                        self.contLoop()

            mx, my  = mouse.get_pos()
            screen.blit(self.startscreenIMAGE, (0,0))
            if startRect.collidepoint((mx,my)):
                draw.rect(screen, (255,0,0), startRect, 7)
            elif contRect.collidepoint((mx,my)):
                draw.rect(screen, (255,0,0), contRect, 7)
            
            press = False
            display.flip()

    def contLoop(self):
        start = True
        backRect = Rect(30,50,170,110)
        while start:
            for e in event.get():
                if e.type == QUIT:
                    display.flip()
                    quit()
                mx, my  = mouse.get_pos()
                if e.type == MOUSEBUTTONUP:
                    if backRect.collidepoint((mx,my)):
                        start = False
            screen.blit(self.controllIMAGE, (0,0))
            mx, my  = mouse.get_pos()
            if backRect.collidepoint((mx,my)):
                draw.rect(screen, (255,0,0), backRect, 5)
            display.flip()
    def startloop(self):
        time=0
        
        
        running = True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False
            
            if time<1:
                time+=1
                self.fadeout(18)
            else:
                screen.fill((255,255,255))
                
                if self.TBstate=="running":
                    self.textbox([
                              "There Once was a boy named Link",
                              "He lived in a peaceful village with his friends",
                              "and family, he is currently training to be a great swordsman ",
                              "just like his master so he can one day become a skilled",
                              "knight just like his father who has passed away",
                              "Until one day...    "])
                    
                if self.TBstate=="done":
                    self.fadeout(3)
                    self.mothertalk()
                        
            
            myClock.tick(60)

            display.flip()
        quit()

    def mothertalk(self):
        time=0
        self.TBstate="running"
        running = True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False


            screen.blit(self.House,(0,0))

            screen.blit(self.Mothersprite,(600,500))

            screen.blit(self.char.up[0],(600,550))

            if self.TBstate=="running":
                    self.textbox([
                              "Where are you going honey?",
                              "...",
                              "Oh, you are going to train with your Master. He came came by",
                              "this morning, and said that he's going to the ancient Temple,",
                              "since its time to give the annual offerings to Malus. ",
                              "...",
                              "Your master said to kill some snakes today in the absence ", 
                              "of your training so you will be prepared for tomorrow. ",
                              "The snakes located just outside the town.",
                              "Stay safe honey!"])
                    
            if self.TBstate=="done":
                self.snakeTask = True
                self.gameloop()





            myClock.tick(60)

            display.flip()
        quit()

    def malusloop(self):
        time=0
        self.TBstate="running"
        running = True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False


            screen.blit(self.townTOP,(0,0))

            screen.blit(self.BossSprite,(550,540))

            if time<1:
                time+=1
                self.fadeout(18)
            else:

                if self.TBstate=="running" and time<2:
                        self.textbox([
                                  "Greetings, residents of this extraneous village",
                                  "I have come to give you a proposition    ",
                                  "Starting today I am the ruler of this world and",
                                  "being the *generous* soul I am, I will let you choose,",
                                  "Join me and live the rest of your lives as my slaves",
                                  "or....",
                                  "PERISH!!! ", 
                                  "send a messanger to my domain to give me your answer ",
                                  "Farewell villagers and think carefully of your decision"])
                        
                if self.TBstate=="done":
                    time+=1
                    print(time)
                    if time>30 and time<33:
                        self.fadeout(3)
                        self.TBstate="running"
            if time>30:
                screen.blit(self.House,(0,0))

                screen.blit(self.Mothersprite,(600,500))

                screen.blit(self.char.up[0],(600,550))
                if self.TBstate=="running":
                    self.textbox([
                              "OH MY, MALUS HAS BEEN AWAKENED    ",
                              "all the offerings were to appease him and make sure ",
                              "this day never comes to fruition, please Link, ",
                              "go see what happened to your master ",
                              "and please don't do anything reckless!"])
                    
                if self.TBstate=="done":
                    self.snakeTask=False
                    self.malusAwakened = False
                    self.char.x=600
                    self.char.y=550
                    self.gameloop()





            myClock.tick(60)

            display.flip()
        quit()

    def textbox(self,words):
        interval=0
        index=0
        text=""
        cont=True
        textindex=0
        wordstyle = font.SysFont("Franklin Gothic Heavy", 40)
        self.TBstate="running"

        
        running=True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    display.flip()
                    quit()

            keys=key.get_pressed()

            interval+=1
            
            if index==0 and textindex==0:
                draw.rect(screen,(255,255,255),(10,650,1180,140))
                draw.rect(screen,(0,255,255),(10,650,1180,140),6)
            
            if index<len(words[textindex]) and cont:
                if interval%2000==0:
                    text+=words[textindex][index]
                    if textindex%2==0:
                        self.font_blit(text, 20, 660, (0,0,0), wordstyle)
                    else:
                        self.font_blit(text, 20, 720, (0,0,0), wordstyle)
                    index+=1
                    display.flip()

            elif index>=len(words[textindex]) and textindex%2==0 and words[textindex]!=words[-1]:
                text=""
                textindex+=1
                index=0

            elif index>=len(words[textindex]) and textindex%2!=0 and words[textindex]!=words[-1]:
                text=""
                textindex+=1
                cont=False
                index=0
    
    
            if cont==False:
                draw.rect(screen,(255,255,255),(10,650,1180,140))
                draw.rect(screen,(0,255,255),(10,650,1180,140),6)
                

                
            if keys[K_s] and words[textindex]==words[-1] and index>=len(words[textindex]):
                index=0
                textindex=0
                text=""
                running=False
                self.TBstate="done"
             
            if keys[K_s]:
                cont=True
        
    def font_blit(self, string, x, y, colour, titlestyle):
        screen.blit(titlestyle.render(string, 1, colour), (x, y))

    def hp(self):
        for i in range(700, 1100, 40):
            draw.circle(screen, (255, 255, 255), (i, 70), 12)
            draw.circle(screen, (0, 0, 0), (i, 70), 10)
        for i in range(700, 700 + self.char.hp * 40, 40):
            draw.circle(screen, (255, 0, 0), (i, 70), 10)

        draw.rect(screen, (205, 201, 201), (940, 110, 30, 30))
        draw.rect(screen, (0, 0, 0), (940, 110, 30, 30), 2)
        screen.blit(self.xbutton, (935, 105))
        screen.blit(self.bowsprite, (950, 120))
        self.font_blit(str(self.char.arrownum), 964, 134, (0, 0, 0), self.titlestyle5)
        self.font_blit(str(self.char.arrownum), 965, 135, (255, 255, 255), self.titlestyle4)

    def fadeout(self,rate):
        """Animate the screen fading to black for entering a new area"""
        clock = time.Clock()
        blackRect = Surface(screen.get_size())
        blackRect.set_alpha(100)
        blackRect.fill((0, 0, 0))
        # Continuously draw a transparent black rectangle over the screen
        # to create a fadeout effect
        for i in range(0, 5):
            clock.tick(rate)
            screen.blit(blackRect, (0, 0))
            display.flip()
        clock.tick(rate)
        screen.fill((255, 255, 255, 50))
        display.flip()

    def pause(self):
        pause = True
        press = False
        while pause:
            for e in event.get():
                if e.type == QUIT:
                    display.flip()
                    quit()
                if e.type == KEYDOWN:
                    press = True
            keys = key.get_pressed()
            if keys[K_SPACE] and press:
                press = not press
                pause = False

            self.font_blit("PAUSED", 500, 400, (0, 0, 255), self.titlestyle)
            display.flip()

    def gameover(self):
        running = True
        index = 0
        press = False
        
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False
                if e.type == KEYDOWN:
                    press = True

            keys = key.get_pressed()

            screen.blit(transform.scale(image.load("gameover.jpg"),(1200,800)),(0,0))
            self.font_blit("CONTINUE?", 550, 500, (255, 255, 255), self.titlestyle2)
            self.font_blit("QUIT?", 550, 520, (255, 255, 255), self.titlestyle2)

            if press and index == 0 and keys[K_RETURN]:
                # redo
                self.char = Link(self.spritesAnim, 400, 400, self.bowAnim)
                self.gameloop()

            elif press and index == 1 and keys[K_RETURN]:
                quit()

            if press and keys[K_UP]:
                index += 1
                press = False
            elif press and keys[K_DOWN]:
                index -= 1
                press = False

            if index % 2 == 0:
                index = 0
            else:
                index = 1
            if index == 0:
                draw.rect(screen, (0, 255, 255), (660, 505, 20, 20))
            if index == 1:
                draw.rect(screen, (0, 255, 255), (660, 525, 20, 20))

            display.flip()

    def heartspawn(self,x,y):
        #gonna reset hearts when entering new screen (set self.hearts=[])
        chance=randint(1,4)
        if chance==1 or chance==2:
            heartrect=Rect(x,y,20,20)
            self.hearts.append(heartrect)
        if chance==3:
            arrowrect=Rect(x,y,10,35)
            self.arrowbundle.append(arrowrect)
        else:
            return False

    def checkspawn(self):
        if len(self.hearts) > 0:
            for hearts in self.hearts:
                screen.blit(self.heartsprite, (hearts.x, hearts.y))
                if hearts.colliderect(self.char.rect):
                    if self.char.hp < 10:
                        self.char.hp += 1
                    self.hearts.remove(hearts)

        if len(self.arrowbundle)>0:
            for arrows in self.arrowbundle:
                screen.blit(self.arrowsprite,(arrows.x,arrows.y))
                if arrows.colliderect(self.char.rect):
                    if self.char.arrownum<20:
                        self.char.arrownum+=5
                    self.arrowbundle.remove(arrows)

    def gameloop(self):
        allNPCS = []
        #bad = enemy(140, 540, self.enemiesAnim)
        world = overworld()
        enemiess = []
        self.projectiles = []
        enemiess, allNPCS = world.spawn()
        # enemiess.append(bad)
        #enemiess.append(enemy(400, 700, self.enemiesAnim))

        hit = False
        press = False
        running = True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False
                if e.type == KEYDOWN:
                    press = True

            if world.drawMAP(self.char.x, self.char.y):
                self.hearts=[]
                self.arrowbundle=[]
                enemiess, allNPCS = world.spawn()

            mx, my = mouse.get_pos()
            mb = mouse.get_pressed()
            keys = key.get_pressed()

            if len(allNPCS) > 0:
                for NPCs in allNPCS:
                    NPCs.spriteupdate(self.char)

            self.char.update(self.slashAnim, enemiess, allNPCS, self.projectiles)
            self.char.interval += 1
            self.char.interval2 += 1


            if len(allNPCS) > 0:
                for NPCs in allNPCS:
                    NPCs.textupdate(self.char)

            if self.char.hp == 0:
                self.char.x = 600
                self.char.y = 550
                self.gameover()

  
            # block = draw.rect(screen, (255, 0, 0), (100, 400, 50, 50))

            if keys[K_SPACE] and press:
                press = not press
                self.pause()
            # if block.collidepoint(self.char.hitx, self.char.hity):f

            
            self.checkspawn()
            
            if len(enemiess) > 0:
                for enemy1 in enemiess:

                    if enemy1.state == "dead":
                        self.heartspawn(enemy1.x, enemy1.y)
                        enemiess.remove(enemy1)
                    else:

                        enemrects = list(enemiess)
                        enemrects.remove(enemy1)


                        enemy1.interval += 1
                        enemy1.collide(self.char.hitx, self.char.hity,
                                       self.char.rect.centerx, self.char.rect.centery,
                                       self.char.rect, enemrects, self.char.arrows)
            #story Elements
            if self.snakeTask and self.snakeKilled > 1:
                print("malus")
                self.malusAwakened = True
                self.dungeonPASS = "moblin"
            if self.moblinKilled > 3:
                self.dungeonPASS = "wizard"
            if self.wizardKilled >3:
                self.dungeonPASS = "oldMan"
            if self.oldManTalked:
                self.dungeonPASS = "none"

            self.hp()

            myClock.tick(45)

            display.flip()
        quit()

    def bossloop(self):
        #bad = enemy(40, 40, self.enemiesAnim)
        #world = overworld()

        time=0

        self.BossNPC=NPC(["......................",
                "...................... ",
                ".........................",
                "..........................",
                ".........."],580,290,44,58,self.BossSprites[0:4])

        FBoss=boss(570,290)
        
        FBosslist=[]
        FBosslist.append(FBoss)
        BossNPClist=[]
        BossNPClist.append(self.BossNPC)
        currentBossRect=BossNPClist
        talked=False
        teleport=True

        
        hit = False
        press = False
        running = True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False
                if e.type == KEYDOWN:
                    press = True

           

            
            keys = key.get_pressed()
            #screen.fill((0,0,0))
            screen.blit(self.BossRoom,(0,0))

            if teleport:
                self.fadeout(15)
                time+=1
                if time==3:
                    teleport=False

            if teleport==False:

                if len(BossNPClist)>0:
                    for NPCs in BossNPClist:
                        NPCs.spriteupdate(self.char)
                        
                
                self.char.interval += 1
                self.char.interval2 += 1

                #FBoss.update((self.char.hitx, self.char.hity),self.char.arrows)

                #FBoss.cooldown+=1

                #FBoss.hpinterval+=1
                if talked:
                    currentBossRect=FBosslist

                    for FBoss in FBosslist:
                        FBoss.update((self.char.hitx, self.char.hity),self.char.arrows,self.char.rect)

                        FBoss.cooldown+=1

                        FBoss.hpinterval+=1

                        if FBoss.state=="dead":
                            FBosslist.remove(FBoss)
                        
                self.char.update(self.slashAnim, FBoss.damage,currentBossRect,self.projectiles)
                    

                if len(BossNPClist)>0:
                    for NPCs in BossNPClist:
                        NPCs.textupdate(self.char)

                        if NPCs.state=="done":
                            talked=True
                            BossNPClist.remove(NPCs)
                            
                            

                '''if self.char.interval2<90:
                    if self.char.interval2%2==0:
                        world.drawMAP(self.char.x, self.char.y)'''



                if keys[K_SPACE] and press:
                    press = not press
                    self.pause()

                self.hp()
                
                self.checkspawn()
            
            myClock.tick(60)

            display.flip()
        quit()

    def vortexspin(self,x,y):
        screen.blit(self.vortex[int(self.vframe)],(x,y))
        self.vframe+=0.5
        if self.vframe>3:
            self.vframe=0
            self.repeat+=1

    def bossexplode(self,x,y):
        screen.blit(self.Bexplode[int(self.eframe)],(x,y))
        self.eframe+=0.5
        if self.eframe>2:
            return False
        
    def endgame(self):
        time=0
        
        flash1=True

        self.TBstate = "running"

        running = True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False
            
            keys = key.get_pressed()
            
            screen.blit(self.BossRoom,(0,0))
        
            screen.blit(self.char.up[0],(585,500))

            time+=1

            if flash1:
  
                self.fadeout(10)
                if time==1:
                    flash1=False
                    
            if time>1:
                if self.TBstate=="running":
                    screen.blit(self.BossDefeat,(585,300))
                    self.textbox(["I-I             ",
                                  "I can't beleive I have been defeated by a mere boy",
                                  "This can't be happening, I still have so much to do...",
                                  "The world was in my grasp...                ",
                                  "Curse y-you boy...                   ",
                                  "Curse you....."                                 ,
                                  "CURSE YOUUUUUUUUUUUUUUU                     "])

                elif self.TBstate=="done":
                    time+=1
                    if self.repeat<20:
                        self.vortexspin(565,275)
                        screen.blit(self.BossDefeat,(585,300))

                    if self.repeat>19 and int(self.eframe) < 3:
                        self.bossexplode(535,245)

                    if time>300 and time<303:
                        self.fadeout(3)

            if time>302:
                self.TBstate="running"
                
                screen.fill((255,255,255))
                
                if self.TBstate=="running":
                    self.textbox([
                              "And so, Link defeated Malus and all was well",
                              "The Villagers were safe and the town was happy",
                              "Link became the great swordsman his master wanted  ",
                              "him to be and his master was finally able to rest in peace",
                              "So ends our tale....."])
                    
                if self.TBstate=="done":
                    self.fadeout(3)
                    self.credit()
                    
                        

                        
        

            myClock.tick(60)

            display.flip()
        quit()

    def credit(self):
        running = True
        while running:
            for e in event.get():
                if e.type == QUIT:
                    running = False

            screen.fill((0,0,0))
            self.font_blit("THE END", 520, 300, (255, 255, 255), self.titlestyle)


            display.flip()
        quit()
    
Main = main()
Main.startscreen()
