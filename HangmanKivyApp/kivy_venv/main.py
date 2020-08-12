'''Hangman game app
    using a base hangman game code written earlier, making a touch application to run a simple hangman game'''

'''add splash screen
    make different lists for different levels
    add levels and level screen'''
# import packages
import kivy
import random as rd
import numpy as np
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image, AsyncImage
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition, SlideTransition
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.loader import Loader

# require current kivy version
kivy.require('1.11.1')

# sizing the window to 750x1334 which is the most popular screen size in english speaking countries
from kivy.config import Config
Config.set('graphics', 'width', '750')
Config.set('graphics', 'height', '1334')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 200)
Config.set('graphics', 'top',  25)
Config.set('graphics', 'resizable', True)


Builder.load_string('''
#: import FadeTransition kivy.uix.screenmanager.FadeTransition
#: import NoTransition kivy.uix.screenmanager.NoTransition
#: import SlideTransition kivy.uix.screenmanager.SlideTransition

<MenuScreen>:
    on_enter:
        self.btnsound.seek(0)
    Float:
        size_hint: (1,1)
        canvas:
            Rectangle:
                source: r'imgs\\paperbkgd.jpg'
                pos: self.pos
                size: self.size
        Label:
            size_hint: (1, 0.5)
            pos_hint: {'x':0 , 'y':0.5}
            text: 'HANGMAN'
            color: 0, 0, 0, 1
            font_size: 100
            font_name: r'fonts\\PWPerspective.ttf'
        Button:
            size_hint: (0.3333, 0.15)
            pos_hint: {'x':0.333, 'y':0.4}
            background_normal: r'imgs\play_normal.png'
            background_down: r'imgs\play_pressed.png'
            on_press:
                self.parent.parent.btnsound.play()
                root.manager.transition = NoTransition()
                root.manager.current = 'load'
        Button:
            background_normal: r'imgs\settings_normal.png'
            background_down: r'imgs\settings_pressed.png'
            size_hint: (0.15, 0.15)
            pos_hint:{'x':0.425, 'y':0.15}
            on_press:
                root.manager.transition = SlideTransition()
                root.manager.transition.direction = "left"
                root.manager.current = 'settings'

<SettingsScreen>:
    Float:
        size_hint: (1,1)
        canvas:
            Rectangle:
                source: r'imgs\\paperbkgd.jpg'
                pos: self.pos
                size: self.size
        Label:
            text: 'More coming soon!'
            size_hint: (0.5, 0.5)
            pos_hint: {'x' : 0.25, 'y' : 0.5}
            font_name: r'fonts\\CabinSketch-Regular.ttf'
            color: 0, 0, 0, 1
            font_size: 50
        Button:
            background_normal: r'imgs\\credits_normal.png'
            background_down: r'imgs\\credits_pressed.png'
            size_hint: (0.5, 0.15)
            pos_hint: {'x': 0.25, 'y' : 0.15}
            on_press:
                root.manager.transition = SlideTransition()
                root.manager.transition.direction = 'left'
                root.manager.current = 'credits'
        Button:
            size_hint: (0.2, 0.07)
            pos_hint : {'x' : 0, 'y': 0.93}
            background_normal: r'imgs\small_back_normal.png'
            background_down: r'imgs\small_back_pressed.png'
            on_press:
                root.manager.transition = SlideTransition()
                root.manager.transition.direction = 'right' 
                root.manager.current = 'menu'

<LoadScreen>:
    on_enter:
        self.loadgame()
    canvas:
        Rectangle:
            source: r'imgs\\paperbkgd.jpg'
            pos: self.pos
            size: self.size
    Float:
        size_hint:(1, 1)
        AsyncImage:
            size_hint: (0.4, 0.4)
            pos_hint: {'x' : 0.3, 'y' : 0.3}
            source: r'img\\loading2.gif'
        Label:
            size_hint: (0.3, 0.3)
            pos_hint: {'x' : 0.35, 'y': 0.2}
            text: 'Loading...'
            font_name: 'fonts\\CabinSketch-Regular.ttf'
            font_size: 25
            color: 0, 0, 0, 1

<CreditsScreen>:
    Float:
        size_hint: (1, 1)
        canvas:
            Rectangle:
                source: r'imgs\\paperbkgd.jpg'
                pos: self.pos
                size: self.size
        Label:
            markup: True
            text: 'App by NK-Baocode\\nArt by MJKushKitty (Maddy Maes)\\nButtons by Roboxel (Fernanda Vergara), licensed under CC BY 4.0:\\n[ref=lic][u]https://creativecommons.org/licenses/by/4.0[/ref][/u]'
            on_ref_press:
                import webbrowser
                webbrowser.open('https://creativecommons.org/licenses/by/4.0/')
            size_hint: (0.7, 0.7) 
            pos_hint: {'x': 0.15, 'y': 0.15}
            text_size: self.size
            halign: 'left'
            valign: 'middle'
            font_name: r'fonts\\CabinSketch-Regular.ttf'
            color: 0, 0, 0, 1
            font_size: 25
        Button:
            size_hint: (0.2, 0.07)
            pos_hint : {'x' : 0, 'y': 0.93}
            background_normal: r'imgs\small_back_normal.png'
            background_down: r'imgs\small_back_pressed.png'
            on_press:
                root.manager.transition = SlideTransition()
                root.manager.transition.direction = 'right' 
                root.manager.current = 'settings'

<LevelButton>:
    on_press:
        root.manager.transition = NoTransition()
        root.manager.current = 'load'
    size_hint: (0.2, 0.2)


<Level1Screen>:
    Float:
        size_hint: (1,1)
        canvas:
            Rectangle:
                source: r'imgs\\paperbkgd.jpg'
                pos: self.pos
                size: self.size
        LevelButton:
            background_normal: r'imgs\\lilplay_normal.png'
            background_down: r'imgs\\lilplay_normal.png'
            pos_hint: {'x' : 0.3, 'y' : 0.5}
        LevelButton:
            background_normal: self.btn12
            background_down: self.btnp12
            pos_hint: {'x' : 0.6, 'y' : 0.5}

<TopRowKey>:
    font_size: 20
    on_press: 
        self.parent.inputlet = self.text
        self.parent.choose()
    size_hint: (0.1, 0.33)

<OtherKey>:
    font_size: 20
    on_press:
        self.parent.inputlet = self.text
        self.parent.choose()
    size_hint: (0.1111, 0.33)

<GameScreen>:
    Box:
        canvas:
            Rectangle:
                source: r'imgs\\paperbkgd.jpg'
                pos: self.pos
                size: self.size
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.75
            Label:
                size_hint_x: 1
                text: ''
            Label:
                size_hint_x: 4
                text: self.parent.parent.allwrongs
                id: wrongdis
                font_size: 45
                font_name: 'fonts\\CabinSketch-Regular.ttf'
                color: 0, 0, 0, 1
            Button:
                background_normal: r'imgs\\reload_normal.png'
                background_down: r'imgs\\reload_pressed.png'
                on_press:
                    self.parent.parent.children[0].btnsound.play()
                    self.parent.parent.children[0].btnsound.seek(0)
                    root.setup()
                size_hint_x: 1
        Image:
            source: self.parent.hangmanimg
            size_hint_y: 2
            id: poorguy
        Label:
            id: display
            size_hint_y: 1
            text: self.parent.distext
            font_size: 50
            font_name: 'fonts\\CabinSketch-Regular.ttf'
            color: 0, 0, 0, 1
        Keyboard:
            size_hint_y: 1
            orientation: 'lr-tb'
            padding: [0,0]
            id: keyboard
            TopRowKey:
                text: 'Q'
 
            TopRowKey:
                text: 'W'
 
            TopRowKey:
                text: 'E'
 
            TopRowKey:
                text: 'R'
 
            TopRowKey:
                text: 'T'
 
            TopRowKey:
                text: 'Y'
 
            TopRowKey:
                text: 'U'
 
            TopRowKey:
                text: 'I'
 
            TopRowKey:
                text: 'O'
 
            TopRowKey:
                text: 'P'
 
            OtherKey:
                text: 'A'
 
            OtherKey:
                text: 'S'
 
            OtherKey:
                text: 'D'
 
            OtherKey:
                text: 'F'
 
            OtherKey:
                text: 'G'
 
            OtherKey:
                text: 'H'
 
            OtherKey:
                text: 'J'
 
            OtherKey:
                text:'K'
 
            OtherKey:
                text: 'L'
 
            OtherKey:
                text: 'Z'
 
            OtherKey:
                text: 'X'
 
            OtherKey:
                text: 'C'
 
            OtherKey:
                text: 'V'
 
            OtherKey:
                text: 'B'
 
            OtherKey:
                text: 'N'
 
            OtherKey:
                text: 'M'
            Label:
                size_hint: (0.06, 0.33)
                text: ''
            Button:
                size_hint: (0.1622, 0.33)
                background_normal: r'imgs\small_back_normal.png'
                background_down: r'imgs\small_back_pressed.png'
                on_press:
                    root.manager.transition = SlideTransition()
                    root.manager.transition.direction = 'right' 
                    root.manager.current = 'menu'
''')
# Build the screens

class MenuScreen(Screen):
    btnsound = SoundLoader.load('sounds\\pop.wav')

class SettingsScreen(Screen):
    pass

class CreditsScreen(Screen):
    pass

class Level1Screen(Screen):
    btnsound=SoundLoader.load('sounds\\pop.wav')

# establish a dictionary of booleans to
Level_Wins_Dictionary = {'lvl11' : False, 'lvl12' : False, 'lvl13' : False}

class LevelLoadScreen(Screen):
    '''def loadlevelscreen(self):
        for level in Level_Wins_Dictionary:
            if level == True:'''


class LoadScreen(Screen):

    def loadgame(self):
        global usedlet
        global inputlet
        global fail1
        global fail2
        global fail3
        global fail4
        global fail5
        global lose
        global win
        global wronglet
        global wrongdis
        global isright
        global blanks
        global secretlen
        global secretlist
        global secretword

        game = sm.get_screen('game')


        # open text file of secret words
        swtxt=open(r'words.txt',
                   "r")  # words.txt has 742 lines
        words=list(swtxt)

        # pick random integer to out of possible 742 entries, then index out of sowpods
        wordnum=rd.randint(0,741)
        secretword=words[wordnum]

        # our secret word has been selected!

        '''
        create a list to be filled with blanks, a system must be created which can read each letter and print a blank for each one

        send each letter in the secret word to a list, each letter the user inputs will be checked against that list
        '''
        # the secret word length is really one lower than python value (python starts count at 0)
        secretlen=len(secretword)-1

        blanks=[]
        for i in range(secretlen):  # read each letter and make blank for each
            blanks.append('_')

        # add each letter of secret word to new secret list
        secretlist=[]
        for i in range(secretlen):
            secretlist.append(secretword[i])

        # create another list to store previous guesses
        usedlet=[]

        # create checks for each failed attempt, on startup these would all be False
        fail1=False
        fail2=False
        fail3=False
        fail4=False
        fail5=False
        lose=False
        win=False

        gameover=False  # check to see if player has lost

        game.children[0].distext = ''.join(blanks)
        game.children[0].allwrongs = ''
        game.children[0].hangmanimg = r'imgs\IWONYAY.jpg'

        #load sounds, for some reason keyboard is 0, 0
        game.children[0].children[0].btnsound.seek(0)
        game.children[0].children[0].errorsd.seek(0)
        game.children[0].children[0].wrongsd.seek(0)
        game.children[0].children[0].winsd.seek(0)
        game.children[0].children[0].losesd.seek(0)

        sm.transition = FadeTransition()
        sm.current='game'

        return

class GameScreen(Screen):
    # define game setup

    def setup(self):
        global usedlet
        global inputlet
        global fail1
        global fail2
        global fail3
        global fail4
        global fail5
        global lose
        global win
        global wronglet
        global wrongdis
        global isright
        global blanks
        global secretlen
        global secretlist
        global secretword
        # open text file of secret words
        swtxt=open(r'C:\Users\maddy\PycharmProjects\HangmanKivyApp\kivy_venv\words.txt',
                   "r")  # words.txt has 742 lines
        words=list(swtxt)

        # pick random integer to out of possible 742 entries, then index out of sowpods
        wordnum=rd.randint(0,741)
        secretword=words[wordnum]

        # our secret word has been selected!

        '''
        create a list to be filled with blanks, a system must be created which can read each letter and print a blank for each one

        send each letter in the secret word to a list, each letter the user inputs will be checked against that list
        '''
        # the secret word length is really one lower than python value (python starts count at 0)
        secretlen=len(secretword)-1

        blanks=[]
        for i in range(secretlen):  # read each letter and make blank for each
            blanks.append('_')

        # add each letter of secret word to new secret list
        secretlist=[]
        for i in range(secretlen):
            secretlist.append(secretword[i])

        # create another list to store previous guesses
        usedlet=[]

        # create checks for each failed attempt, on startup these would all be False
        fail1=False
        fail2=False
        fail3=False
        fail4=False
        fail5=False
        #checks for lose/win as well
        lose=False
        win=False


        gameover=False  # check to see if player has lost

        self.children[0].distext = ''.join(blanks)
        self.children[0].allwrongs = ''
        self.children[0].hangmanimg = r'imgs\IWONYAY.jpg'

        #load sounds, for some reason keyboard is 0, 0
        self.children[0].children[0].btnsound.seek(0)
        self.children[0].children[0].errorsd.seek(0)
        self.children[0].children[0].wrongsd.seek(0)
        self.children[0].children[0].winsd.seek(0)
        self.children[0].children[0].losesd.seek(0)


        return

class LevelButton(Button):
    btn12 = StringProperty('')
    btnp12 = StringProperty('')

class TopRowKey(Button):
    pass

class OtherKey(Button):
    pass


class Keyboard(StackLayout):
    # create a list to store failed guesses to display to player
    wronglet = StringProperty('')
    inputlet = StringProperty('')

    #add sounds
    btnsound = SoundLoader.load('sounds\\pop.wav')
    errorsd = SoundLoader.load('sounds\\error.wav')
    wrongsd = SoundLoader.load('sounds\\nonobuzz.wav')
    losesd = SoundLoader.load('sounds\\lose.wav')
    winsd = SoundLoader.load('sounds\\win.wav')

    def choose(self):  # define onpress action as making selected letter the input
        global inputlet
        global usedlet
        global isright
        global fail1
        global fail2
        global fail3
        global fail4
        global fail5
        global lose
        global win
        global wronglet
        global wrongdis
        global gameover
        global secretlen
        global secretlist
        global secretword
        global blanks

        isright=False

        #check if letter has been used before
        for i in range(len(usedlet)):
            if usedlet[i] == self.inputlet or lose == True or win == True:
                self.errorsd.play()
                self.errorsd.seek(0)
                return
            else:
                pass

        usedlet += self.inputlet

        for i in range(secretlen):  # go through blanks and replace blanks where letter is correct
            if secretlist[i] == self.inputlet:
                self.btnsound.play()
                self.btnsound.seek(0)
                blanks[i]=self.inputlet
                self.parent.distext=''.join(blanks)
                isright=True
            else:
                pass

        #  function to check if the letter is right, if wrong, if else tree for appropriate response

        if isright == False:
            if fail1 == True:
                if fail2 == True:
                    if fail3 == True:
                        if fail4 == True:
                            if fail5 == True: #player has lost
                                lose = True
                                self.losesd.play()
                                self.wronglet = self.inputlet
                                self.parent.allwrongs += self.wronglet
                                self.parent.distext=f'{secretword} You Lose!'
                                self.parent.hangmanimg = r'imgs\IWONYAY.jpg'
                            else:
                                fail5=True
                                self.wrongsd.play()
                                self.wrongsd.seek(0)
                                self.wronglet = self.inputlet
                                self.parent.allwrongs += self.wronglet
                                self.parent.hangmanimg = r'imgs\IWONYAY.jpg'
                        else:
                            fail4=True
                            self.wrongsd.play()
                            self.wrongsd.seek(0)
                            self.wronglet = self.inputlet
                            self.parent.allwrongs += self.wronglet
                            self.parent.hangmanimg = r'imgs\IWONYAY.jpg'
                    else:
                        fail3=True
                        self.wrongsd.play()
                        self.wrongsd.seek(0)
                        self.wronglet = self.inputlet
                        self.parent.allwrongs += self.wronglet
                        self.parent.hangmanimg = r'imgs\IWONYAY.jpg'
                else:
                    fail2=True
                    self.wrongsd.play()
                    self.wrongsd.seek(0)
                    self.wronglet = self.inputlet
                    self.parent.allwrongs += self.wronglet
                    self.parent.hangmanimg = r'imgs\IWONYAY.jpg'
            else:
                fail1=True
                self.wrongsd.play()
                self.wrongsd.seek(0)
                self.wronglet = self.inputlet
                self.parent.allwrongs += self.wronglet
                self.parent.hangmanimg = r'imgs\IWONYAY.jpg'
        else:
            if blanks.count('_') == 0: #player has won
                win = True
                self.winsd.play()
                self.parent.distext=f'{secretword}'
                self.parent.hangmanimg = r'imgs\IWONYAY.jpg'
            else:
                pass
        return

class Float(FloatLayout):
    pass

class Box(BoxLayout):
    allwrongs = StringProperty('')
    distext = StringProperty('')
    hangmanimg = StringProperty('')
# build screen manager

sm = ScreenManager()

#add screens to the manager
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(GameScreen(name='game'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(LoadScreen(name='load'))
sm.add_widget(CreditsScreen(name='credits'))
sm.add_widget(Level1Screen(name='level1'))


sm.current = 'menu'

#build app

class HangmanApp(App):

    def build(self):
        return sm

HangmanApp().run()