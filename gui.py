#! -*- coding utf-8 -*-
#@Kris @Alex

import pygame, sys, random
from pygame.locals import *
from chat_client_class import *
import textrect as trect


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

keyboard=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0',' ',',','.','/','[',']']
skeyboard=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','!','@','#','$','%','^','&','*','(',')',' ','<','>','?','{','}']


class Chat:

    def __init__(self):

        pygame.init()
        #---------------------------------
        #Your code here
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
        self.fontObj30 = pygame.font.Font('freesansbold.ttf', 30)
        self.windowSurface = pygame.display.set_mode((WINDOWW, WINDOWH), 0, 32)
        pygame.display.set_caption('ICS Chat System')
        self.chatlog=[]
        self.logobj=[]
        self.first=True
        self.name=''
        self.shift=False
        self.page=0
        self.color=PURPLE
        #---------------------------------

    def run_client(self, args):
        self.client = Client(args)
        c_thread = threading.Thread(target = self.client.run_chat)
        c_thread.daemon = True
        c_thread.start()


    def read(self):
        #---------------------------------
        #Your code here
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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
            if event.type == KEYDOWN:
                if event.key == K_RSHIFT or event.key== K_LSHIFT:
                    if self.shift:
                        self.shift=False
                    else:
                        self.shift=True
                if event.key == K_LEFT and self.page > 0:
                    self.page-=1
                if event.key == K_RIGHT:
                    self.page+=1
                #if textobj.right < WINDOWW*.9:
                if True:
                    #if text have not exceeded right bound,enter text onto screen
                    if self.shift:
                        if chr(event.key) in keyboard:
                            self.text+=skeyboard[keyboard.index(chr(event.key))]
                    elif chr(event.key) in keyboard:
                        self.text+=chr(event.key)
                if len(self.text) > 0 and event.key == K_BACKSPACE:
                    self.text=self.text[:-1]
                if len(self.text) > 0 and event.key == K_RETURN:
                    if self.first:
                        self.name=self.text
                        self.text=''
                        #client.login(name)
                        self.first=False
                        self.text=''
                        return self.name
                    else:
                        self.chatlog.append('['+self.name+']'+self.text)
                        #insert function to send msg to chat server
                        #client.read_input(text)
                        self.temp=self.text
                        self.text=''
                        return self.temp
                        
                        
                    self.text=''

                    
            if event.type == KEYUP:
                #quit program
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        #---------------------------------
        

    def update(self, msg):
        if msg != None:
            if len(msg) >120:
                self.chatlog.append(msg[:60])
                self.chatlog.append(msg[60:120])
                self.chatlog.append(msg[120:])
            elif len(msg) >60:
                self.chatlog.append(msg[:60])
                self.chatlog.append(msg[60:])
            else:
                self.chatlog.append(msg)
        #----------------------------------
        #Your code here
        if self.first:
            self.windowSurface.fill(LBLUE)
            background=pygame.image.load('login.png')
            background=pygame.transform.scale(background, (WINDOWW,WINDOWH))
            self.windowSurface.blit(background,(0,0))
            
            #pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*.05, WINDOWH*.5, WINDOWW*.85, WINDOWH*0.09))
            #pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*.9, WINDOWH*.5, WINDOWW*.05, WINDOWW*0.054))
            textSurfaceObj1 = self.fontObj.render("Name: "+str(self.text), True,BLACK)
            textobj = textSurfaceObj1.get_rect()
            textobj.left = (WINDOWW*.05)
            textobj.top=(WINDOWH*.5)
            self.windowSurface.blit(textSurfaceObj1, textobj)

            


            
            #enter=pygame.image.load('enter.png')
            #enter=pygame.transform.scale(enter, (int(WINDOWW*0.05), int(WINDOWW*0.05)))
            #self.windowSurface.blit(enter,(WINDOWW*0.9,WINDOWH*0.5))
##            if self.shift:
##                pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*0, WINDOWH*.5, WINDOWW*.05, WINDOWW*0.054))
##                shiftkey=pygame.image.load('Shift.png')
##                shiftkey=pygame.transform.scale(shiftkey, (int(WINDOWW*0.05), int(WINDOWW*0.05)))
##                self.windowSurface.blit(shiftkey,(WINDOWW*0,WINDOWH*0.5))


                
        elif self.chatting:



            
            
            #print to screen
            self.windowSurface.fill(LBLUE)
            #background
            background=pygame.image.load(self.wallpaper)
            background=pygame.transform.scale(background, (WINDOWW,WINDOWH))
            self.windowSurface.blit(background,(0,0))

            #print chatbar
            #pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*.05, WINDOWH*.9, WINDOWW*.85, WINDOWH*0.09))
            #pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*.9, WINDOWH*.9, WINDOWW*.05, WINDOWW*0.054))
            #white rect^
##            textSurfaceObj1 = self.fontObj.render(self.name+": "+str(self.text), True,BLACK)
##            textobj = textSurfaceObj1.get_rect()
##            textobj.left = (WINDOWW*.05)
##            textobj.top=(WINDOWH*.9)
##            self.windowSurface.blit(textSurfaceObj1, textobj)

            try:

                bar=trect.render_textrect(self.name+": "+str(self.text), self.fontObj30, pygame.Rect(WINDOWW*.05, WINDOWH*.9, WINDOWW*.9, WINDOWH*0.2),  (20, 20, 20),(216, 216, 216), 0)
                self.windowSurface.blit(bar,(50,480))
            except:
                self.text=''
                bar=trect.render_textrect(self.name+": "+str(self.text), self.fontObj30, pygame.Rect(WINDOWW*.05, WINDOWH*.9, WINDOWW*.9, WINDOWH*0.2),  (20, 20,20),(216, 216, 216), 0)
                self.windowSurface.blit(bar,(50,480))

            #print page no.
            textSurfaceObjpage = self.fontObj30.render("Page "+str(self.page), True,self.color)
            textobjpage = textSurfaceObjpage.get_rect()
            textobjpage.left = (WINDOWW*.85)
            textobjpage.top=(WINDOWH*.04)
            self.windowSurface.blit(textSurfaceObjpage, textobjpage)
            
            #print current member
##            textSurfaceObjmember = self.fontObj30.render("member:", True,WHITE)
##            textobjmember = textSurfaceObjmember.get_rect()
##            textobjmember.left = (WINDOWW*.85)
##            textobjmember.top=(WINDOWH*.3)
##            self.windowSurface.blit(textSurfaceObjmember, textobjmember)
##
##            textSurfaceObjname = self.fontObj30.render(self.name, True,WHITE)
##            textobjname = textSurfaceObjpage.get_rect()
##            textobjname.left = (WINDOWW*.85)
##            textobjname.top=(WINDOWH*.4)
##            self.windowSurface.blit(textSurfaceObjname, textobjname)

            

            #print enter key
            #enter=pygame.image.load('enter.png')
            #enter=pygame.transform.scale(enter, (int(WINDOWW*0.05), int(WINDOWW*0.05)))
            #self.windowSurface.blit(enter,(WINDOWW*0.9,WINDOWH*0.9))


            

            
 

            

            #print chat log
            #if ((len(self.chatlog)-1) % 17)==0:
            #    self.page=int((len(self.chatlog)-1)/17)
            #if len(self.chatlog) > (self.page+1)*17:
            #    counter=(self.page+1)*17
            #else:
            #    counter=len(self.chatlog)
##            for i in range(self.page*17,counter):
##                logobj=['']*len(self.chatlog)
##                logobj[i]=self.fontObj30.render(str(self.chatlog[i]), True,BLACK).get_rect()
##                logobj[i].left = WINDOWW*0.05
##                logobj[i].top = 20+WINDOWH*0.05*(i-self.page*17)
##                self.windowSurface.blit(self.fontObj30.render(str(self.chatlog[i]), True,WHITE),logobj[i])

##            loop=True
##            while loop:
##                try:
##                    self.counters[self.page]=len(self.chatlog)
##                    if page!= 0:
##                        for i in range(self.counters[self.page-1],self.counters[self.page]):
##                            self.tstring+=self.chatlog[i]+'\n'
##
##                        #test
##                        hi=trect.render_textrect(self.tstring, self.fontObj30, pygame.Rect((40, 40, 900, 400)), (216, 216, 216), (48, 48, 48), 0)
##                        self.windowSurface.blit(hi,(60,60))
##                        self.tstring=''
##                        loop=False
##                    else:
##                        for i in range(0,self.counters[self.page]):
##                            self.tstring+=self.chatlog[i]+'\n'
##
##                        #test
##                        hi=trect.render_textrect(self.tstring, self.fontObj30, pygame.Rect((40, 40, 900, 400)), (216, 216, 216), (48, 48, 48), 0)
##                        self.windowSurface.blit(hi,(60,60))
##                        self.tstring=''
##                        loop=False
##                        
##                except:
##                    self.counters[self.page]-=1
            
            if ((len(self.chatlog)-1) % 12)==0:
                self.page=int((len(self.chatlog)-1)/12)
            if len(self.chatlog) > (self.page+1)*12:
                counter=(self.page+1)*12
            else:
                counter=len(self.chatlog)
            for i in range(self.page*12,counter):
                self.tstring+=self.chatlog[i]+'\n'
            hi=trect.render_textrect(self.tstring, self.fontObj30, pygame.Rect((40, 40, 900, 420)), (220, 220, 220),(48,48,48),0)
            self.windowSurface.blit(hi,(50,60))
            self.tstring=''

##            for i in self.chatlog:
##                self.tstring+=i+'\n'
##            hi=trect.render_textrect(self.tstring, self.fontObj30, pygame.Rect((40, 40, 900, 400)), (216, 216, 216), (48, 48, 48), 0)
##            self.windowSurface.blit(hi,(60,60))
##            self.tstring=''
        else:
            #choose chat skin theme
            #self.windowSurface.fill(LBLUE)
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
        #-----------------------------------
def main(args):
    g = Chat()
    g.run_client(args)
    clock = pygame.time.Clock()
    while True:
        msg=g.read()
        if msg: print(msg)
        if msg: g.client.read_input(msg)
        msg = g.client.output()
        #print(msg)
        g.update(msg)
        clock.tick(100)

if __name__ == "__main__":
    g = Chat()
    while True:
        msg = g.read()
        g.update(msg)
    
