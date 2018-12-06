#! -*- coding utf-8 -*-
#@Kris @Alex

import pygame, sys, random
from pygame.locals import *
from chat_client_class import *
import textrect as trect


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 51, 51)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DPURPLE = (150,0,80)
PURPLE = (200,0,200)
YELLOW =(255,255,51)
LBLUE =(204,255,255)
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
        temp=''
        self.run=True
        self.chatting=True
        self.text= ''
        self.fontObj = pygame.font.Font('freesansbold.ttf', 50)
        self.fontObj30 = pygame.font.Font('freesansbold.ttf', 30)
        self.windowSurface = pygame.display.set_mode((WINDOWW, WINDOWH), 0, 32)
        pygame.display.set_caption('Chat')
        self.chatlog=[]
        self.logobj=[]
        self.first=True
        self.name=''
        self.shift=False
        self.page=0
        #---------------------------------

    def run_client(self, args):
        self.client = Client(args)
        c_thread = threading.Thread(target = self.client.run_chat)
        c_thread.daemon = True
        c_thread.start()

        clock = pygame.time.Clock()
        while True:
            self.update_members()
            msg=self.read()
            #if msg: print(msg)
            if msg: self.client.read_input(msg)
            msg = self.client.output()
            #print(msg)
            self.update(msg)
            clock.tick(100)


    def read(self):
        #---------------------------------
        #Your code here
        """
        Add states and modify the read function
        block keyboard input before click on a button
        """

        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
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
                        self.chatlog.append(self.text)
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
            self.chatlog.append(msg)
        #----------------------------------
        #Your code here

        """
        Modify, in chat mode or not in chat mode
        """




        
        if self.first:
            self.windowSurface.fill(LBLUE)
            background=pygame.image.load('background3.jpg')
            background=pygame.transform.scale(background, (WINDOWW,WINDOWH))
            self.windowSurface.blit(background,(0,0))
            
            pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*.05, WINDOWH*.5, WINDOWW*.85, WINDOWH*0.09))
            pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*.9, WINDOWH*.5, WINDOWW*.05, WINDOWW*0.054))
            textSurfaceObj1 = self.fontObj.render("Name: "+str(self.text), True,BLACK)
            textobj = textSurfaceObj1.get_rect()
            textobj.left = (WINDOWW*.05)
            textobj.top=(WINDOWH*.5)
            self.windowSurface.blit(textSurfaceObj1, textobj)

            


            
            enter=pygame.image.load('enter.png')
            enter=pygame.transform.scale(enter, (int(WINDOWW*0.05), int(WINDOWW*0.05)))
            self.windowSurface.blit(enter,(WINDOWW*0.9,WINDOWH*0.5))
            if self.shift:
                pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*0, WINDOWH*.5, WINDOWW*.05, WINDOWW*0.054))
                shiftkey=pygame.image.load('Shift.png')
                shiftkey=pygame.transform.scale(shiftkey, (int(WINDOWW*0.05), int(WINDOWW*0.05)))
                self.windowSurface.blit(shiftkey,(WINDOWW*0,WINDOWH*0.5))


                
        elif self.chatting: 
            
            #print to screen
            self.windowSurface.fill(LBLUE)
            #background
            background=pygame.image.load('background.jpg')
            background=pygame.transform.scale(background, (WINDOWW,WINDOWH))
            self.windowSurface.blit(background,(0,0))

            #print chatbar
            pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*.05, WINDOWH*.9, WINDOWW*.85, WINDOWH*0.09))
            pygame.draw.rect(self.windowSurface, WHITE, pygame.Rect(WINDOWW*.9, WINDOWH*.9, WINDOWW*.05, WINDOWW*0.054))
            #white rect^
            textSurfaceObj1 = self.fontObj.render(self.name+": "+str(self.text), True,BLACK)
            textobj = textSurfaceObj1.get_rect()
            textobj.left = (WINDOWW*.05)
            textobj.top=(WINDOWH*.9)
            self.windowSurface.blit(textSurfaceObj1, textobj)

            #print page no.
            textSurfaceObjpage = self.fontObj30.render("Page "+str(self.page), True,WHITE)
            textobjpage = textSurfaceObjpage.get_rect()
            textobjpage.left = (WINDOWW*.85)
            textobjpage.top=(WINDOWH*.05)
            self.windowSurface.blit(textSurfaceObjpage, textobjpage)
            
            #print current member
            textSurfaceObjmember = self.fontObj30.render("member:", True,WHITE)
            textobjmember = textSurfaceObjmember.get_rect()
            textobjmember.left = (WINDOWW*.85)
            textobjmember.top=(WINDOWH*.3)
            self.windowSurface.blit(textSurfaceObjmember, textobjmember)

            textSurfaceObjname = self.fontObj30.render(self.name, True,WHITE)
            textobjname = textSurfaceObjpage.get_rect()
            textobjname.left = (WINDOWW*.85)
            textobjname.top=(WINDOWH*.4)
            self.windowSurface.blit(textSurfaceObjname, textobjname)

            

            #print enter key
            enter=pygame.image.load('enter.png')
            enter=pygame.transform.scale(enter, (int(WINDOWW*0.05), int(WINDOWW*0.05)))
            self.windowSurface.blit(enter,(WINDOWW*0.9,WINDOWH*0.9))


            #test
            hi=trect.render_textrect('hi', self.fontObj30, pygame.Rect((40, 40, 300, 300)), (216, 216, 216), (48, 48, 48), 0)
            self.windowSurface.blit(hi,(60,60))

                        

            #print chat log
            if ((len(self.chatlog)-1) % 17)==0:
                self.page=int((len(self.chatlog)-1)/17)
            if len(self.chatlog) > (self.page+1)*17:
                counter=(self.page+1)*17
            else:
                counter=len(self.chatlog)
            for i in range(self.page*17,counter):
                logobj=['']*len(self.chatlog)
                logobj[i]=self.fontObj30.render(str(self.chatlog[i]), True,BLACK).get_rect()
                logobj[i].left = WINDOWW*0.05
                logobj[i].top = 20+WINDOWH*0.05*(i-self.page*17)
                self.windowSurface.blit(self.fontObj30.render(str(self.chatlog[i]), True,WHITE),logobj[i])
        pygame.display.update()
        #-----------------------------------

        def get_members(self):
            return list(self.client.sm.get_members())

        def create_button(self, name):
            #----------------------------------
            #Your code here:
            pass
            """
            Create a button with name and click event
            (which is calling g.client.read_input(msg),
            where msg is e name if a member
            or open a chat window to input index if is ? ... or p ... etc
            the )
            I don't know if you need to build a Button class 
            """
            #-----------------------------------
            return button

        def update_members(self):
            member_list = self.get_members()
            #-----------------------------------
            #Your code here:
            pass
            """
            show members
            if people are chatting, put them together
            also remember to show the ?, p, and a door to exit program etc ...
            """
            #update()
            #------------------------------------

        def show_chat_window(self):
            #------------------------------------
            #Your code here:
            pass
            """
            show chat window
            with an exit button (on click event is g.client.read_input('bye')
            """
            #------------------------------------




            
def main(args):
    g = Chat()
    g.run_client(args)


if __name__ == "__main__":
    g = Chat()
    g.run_client('0.0.0.0')
    
