#! -*- coding utf-8 -*-
#@Kris @Alex

import pygame, sys, random
from pygame.locals import *
from chat_client_class import *
from textrect import *

from pasting import paste
#Work Cited: Al Sweigart


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 51, 51)
GREEN = (131,233,138)
BLUE = (0, 0, 255)
DPURPLE = (150,0,80)
PURPLE = (201,167,223)
YELLOW =(255,255,51)
LBLUE =(124,161,247)
DBLUE=(0,0,102)
ORANGE=(255, 100, 50)
GREEN2=(0,153,76)
GOLD=(255,215,0)
GREY=(180,180,180)
DGREY=(100,100,100)

WINDOWW = 1000
WINDOWH = 600

keyboard = \
['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0',' ',',','.','/','[',']',';','\\','=','-','`',"'"]
skeyboard = \
['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*','(',')',' ','<','>','?','{','}',':','|','+','_','~','"']

TALL = 18

class Chat:

    def __init__(self):

        pygame.init()

        self.button = pygame.Rect(100, 250, 200, 200)
        self.button2 = pygame.Rect(400, 250, 200, 200)
        self.button3 = pygame.Rect(700, 250, 200, 200)
        self.counters=[0]*100
        self.tstring=''
        self.wallpaper='background.jpg'
        temp=''
        self.run=True
        self.chatting=False
        self.text= ''
        self.fontObj = pygame.font.Font('freesansbold.ttf', 50)
        self.fontObj30 = pygame.font.Font('freesansbold.ttf', 20)
        self.windowSurface = pygame.display.set_mode((WINDOWW, WINDOWH), 0, 32)
        pygame.display.set_caption('Find Love')
        self.chatlog=[]
        self.logobj=[]
        self.first=True
        self.name=''
        self.shift=False
        self.capslock = False
        self.page=0
        self.lockpage = False
        self.color=PURPLE
        self.ctrl = False

    def run_client(self, args):
        self.client = Client(args)
        c_thread = threading.Thread(target = self.client.run_chat)
        c_thread.daemon = True
        c_thread.start()

        clock = pygame.time.Clock()
        while "Kris":
            try:
                msg = self.read()
                if msg: print(msg)
                if msg: self.client.read_input(msg)
                msg = self.client.output()
                #print(msg)
                self.update(msg)
                clock.tick(100)
            except Exception as err:
                print(err)


    def read(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not(self.chatting)and not(self.first):
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if self.button.collidepoint(mouse_pos):
                    #NYU Skin
                    self.wallpaper='background.jpg'
                    self.chatting = True
                    self.color=PURPLE
                if self.button2.collidepoint(mouse_pos):
                    #Chrismas Skin
                    self.wallpaper='xmas.jpg'
                    self.chatting = True
                    self.color=LBLUE
                if self.button3.collidepoint(mouse_pos):
                    #theme 3
                    self.wallpaper='green.jpg'
                    self.color=GREEN
                    self.chatting = True

            self.capslock = pygame.key.get_mods() & pygame.KMOD_CAPS
            self.ctrl = pygame.key.get_mods() & (KMOD_LCTRL | KMOD_RCTRL | KMOD_CTRL)
            self.shift = pygame.key.get_mods() & (KMOD_LSHIFT | KMOD_RSHIFT | KMOD_SHIFT)

            if event.type == KEYDOWN:
                if event.key == K_LEFT and self.page > 0:
                    self.page-=1
                    self.lockpage = True
                if event.key == K_RIGHT:
                    self.page+=1
                    self.lockpage = True
                if self.ctrl and event.key == K_v:
                    self.text += paste()
                elif self.shift or self.capslock:
                    if chr(event.key) in keyboard:
                        self.text += skeyboard[keyboard.index(chr(event.key))]
                elif chr(event.key) in keyboard:
                    self.text+=chr(event.key)
                if len(self.text) > 0 and event.key == K_BACKSPACE:
                    self.text=self.text[:-1]
                if len(self.text) > 0 and event.key == K_RETURN:
                    if self.first:
                        self.name=self.text
                        self.text=''
                        self.first=False
                        self.text=''
                        return self.name
                    else:
                        self.chatlog.append('['+self.name+']'+self.text)
                        self.temp=self.text
                        self.text=''
                        return self.temp
                        
                        
                    self.text=''

                    
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    if self.chatting: self.client.read_input('bye')
                    self.client.read_input('q')
                    pygame.quit()
                    sys.exit()

        

    def update(self, msg):
        if msg != None:
            self.pagelock = False
            self.chatlog += msg.split('\n')

        if self.first:
            self.windowSurface.fill(LBLUE)
            background=pygame.image.load('login.png')
            background=pygame.transform.scale(background, (WINDOWW,WINDOWH))
            self.windowSurface.blit(background,(0,0))
            
            textSurfaceObj1 = self.fontObj.render("Name: "+str(self.text), True,BLACK)
            textobj = textSurfaceObj1.get_rect()
            textobj.left = (WINDOWW*.05)
            textobj.top=(WINDOWH*.5)
            self.windowSurface.blit(textSurfaceObj1, textobj)

            
                
        elif self.chatting:     
            
            #print to screen
            self.windowSurface.fill(LBLUE)
            #background
            background=pygame.image.load(self.wallpaper)
            background=pygame.transform.scale(background, (WINDOWW,WINDOWH))
            self.windowSurface.blit(background,(0,0))

            try:

                bar = render_textrect(self.name+": "+str(self.text), self.fontObj30, pygame.Rect(WINDOWW*.05, WINDOWH*.9, WINDOWW*.9, WINDOWH*0.2),  (20, 20, 20),(216, 216, 216), 0)
                self.windowSurface.blit(bar,(50,480))
            except:
                self.text=''
                bar = render_textrect(self.name+": "+str(self.text), self.fontObj30, pygame.Rect(WINDOWW*.05, WINDOWH*.9, WINDOWW*.9, WINDOWH*0.2),  (20, 20,20),(216, 216, 216), 0)
                self.windowSurface.blit(bar,(50,480))

            #print page no.
            textSurfaceObjpage = self.fontObj30.render("Page "+str(self.page), True,self.color)
            textobjpage = textSurfaceObjpage.get_rect()
            textobjpage.left = (WINDOWW*.85)
            textobjpage.top=(WINDOWH*.04)
            self.windowSurface.blit(textSurfaceObjpage, textobjpage)

            
            
#            if not (len(self.chatlog)) % TALL:
            if not self.lockpage: self.page = max(self.page, int((len(self.chatlog) - 1) / TALL))
            if len(self.chatlog) > (self.page + 1) * TALL:
                counter = (self.page + 1) * TALL
            else:
                counter = len(self.chatlog)


            turn = self.page
            filtr = 0
            aturn = -1
            while 1:               
                try:
                    for k in range(self.page * TALL, filtr):
                        self.tstring += self.chatlog[k] + '\n'
                    prehi = render_textrect(self.tstring, self.fontObj30, pygame.Rect((40, 40, 900, 420)), (220, 220, 220),(48,48,48),0)
                    self.tstring = ''
                    for i in range(self.page * TALL + filtr ,counter):
                        self.tstring += self.chatlog[i]+'\n'
                    hi = render_textrect(self.tstring, self.fontObj30, pygame.Rect((40, 40, 900, 420)), (220, 220, 220),(48,48,48),0)
                    self.tstring=''
                    break
                except TextRectException as err:
                    print(err)
                    filtr = -~filtr
                    if aturn:
                        turn = -~self.page
                        aturn = -~aturn
            self.page = turn


            self.windowSurface.blit(prehi,(50,60))            
            self.windowSurface.blit(hi,(50,60))


        else:
            background2=pygame.image.load('background2.jpg')
            background2=pygame.transform.scale(background2, (WINDOWW,WINDOWH))
            self.windowSurface.blit(background2,(0,0))

            textSurfaceObjpage = self.fontObj.render("Welcome to ICS Chat "+ self.name, True,WHITE)
            textobjpage = textSurfaceObjpage.get_rect()
            textobjpage.left = 100
            textobjpage.top=50
            self.windowSurface.blit(textSurfaceObjpage, textobjpage)
            textSurfaceObjpage = self.fontObj.render("Pick a color", True,WHITE)
            textobjpage = textSurfaceObjpage.get_rect()
            textobjpage.left = 350
            textobjpage.top=150
            self.windowSurface.blit(textSurfaceObjpage, textobjpage)
            
            
            pygame.draw.rect(self.windowSurface, [207,44,237], self.button)
            pygame.draw.rect(self.windowSurface, [32,157,246], self.button2)
            pygame.draw.rect(self.windowSurface, [54,237,54], self.button3)

            #colortags
            
            ptag= self.fontObj.render("Purple", True,WHITE)
            btag= self.fontObj.render("Blue", True,WHITE)
            gtag= self.fontObj.render("Green", True,WHITE)
            self.windowSurface.blit(ptag, pygame.Rect(120, 330, 200, 200))
            self.windowSurface.blit(btag, pygame.Rect(440, 330, 200, 200))
            self.windowSurface.blit(gtag, pygame.Rect(720, 330, 200, 200))
            
            
                
                
        pygame.display.update()

def main(args):
    g = Chat()
    g.run_client(args)


if __name__ == "__main__":
    g = Chat()
    while True:
        msg = g.read()
        g.update(msg)
    
