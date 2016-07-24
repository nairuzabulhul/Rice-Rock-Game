#Imported Libraries 
import random 
import math
import simplegui


#Global Variables:
CANVAS_HEIGHT = 600   #canvas Hight 
CANVAS_WIDTH  = 900    #canvas Width
TIME          = 0.5
START         = False
SCORE         = 0
LIVES          = 3

#Class # 1 for Image information 
class Image_info:
    
    def __init__(self, Center , Size , Radius= 0 , Life_span= None , Animated = False):
        self.Center = Center
        self.Size =  Size
        self.Radius = Radius 
        
        if Life_span :
            self.Life_span = Life_span
        else:
            self.Life_span = float ('inf')
        
        self.Animated = Animated 
   
    def get_center(self):
            return self.Center
        
    def get_size (self):
            return self.Size
        
    def get_radius (self):
            return self.Radius 
        
    def get_life_span (self):
            return self.Life_span
   
    def get_animated (self):
            return self.Animated
        
        
        


###########################Art of the Game######################################

#Background Image:
#number one 
Background_image = simplegui.load_image ("http://www.hdwallwide.com/wp-content/uploads/2014/03/fantasy-space-HD-wallpaper-1080p.jpg")

#purple
#Background_image = simplegui.load_image ("http://fc02.deviantart.net/fs71/f/2014/243/5/3/galaxy_17088_by_sonadowroxmyworld-d7xe6tc.jpg")
#colorful
#Background_image = simplegui.load_image ("http://i.imgur.com/9QYyv6B.jpg")

Background_Info = Image_info([1920 /2 ,1080/2],[1920,1080])


#Debris Image by 
#Debris_Info = Image_info ([320, 240], [640, 480])
#Debris_image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
Debris_image = simplegui.load_image ("http://i.imgur.com/Bb8tjOD.png")
Debris_Info  = Image_info ([320, 240], [640, 480])

#Ship Image :
Ship_Info  = Image_info([45, 45], [90, 90], 35)
Ship_Image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

#Astroid :
Astroid_Image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")
Astroid_Info  = Image_info ([45,45],[90,90],50)

#Missiles Images :
Missile_Info  = Image_info([5, 5], [10, 10], 3, 50)
Missile_Image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")
Missile_Sound = simplegui.load_sound ("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")


#Explosion 
Explosion_Image  = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
Explosion_Info   = Image_info([64, 64], [128, 128], 17, 24, True)
Explosion_Sound  = simplegui.load_sound ("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")


#Introduction Image :
Intro_Image = simplegui.load_image ("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")
Intro_Info  = Image_info([200, 150], [400, 300])

#Backgorund Sound of the Game :
Sound = simplegui.load_sound ("http://www.sounddogs.com/previews/3972/mp3/616644_SOUNDDOGS__sp.mp3")

#Sounds of the Game :
Ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")



###################################################################################################
#EXTRA VARIABLE :
#Sound.play()

def Angle_to_Vector(ANGLE):
    return [math.cos(ANGLE), math.sin(ANGLE)] #using math library to find the cosign and sin 


def Distance (point_X, point_Y):
    
    return math.sqrt((point_X[0] - point_Y [0])** 2 + (point_X [1] - point_Y[1]) **2 )
    
    
def Sprite_Group (Group, canvas):
    #A functiont that holds the astroids in one SET
    
    for one in set (Group):
        one.draw(canvas)
        if one.UP_date():
            Group.remove(one)
            
def Collision_Group (Group, Other_Object):
    global Explosion_Group
    
    Collide = False
    for i in set (Group):
        if i.Collision (Other_Object):
            Group.remove (i)
            Collide = True
            Explosion_Group.add (Sprite(i.Position,[0,0],0,0,Explosion_Image , Explosion_Info,Explosion_Sound))
            
    return Collide
   
 
def Collision_Group2 (Group, Other_Group):    
    Counter = 0
    for one in set (Group):
        Collision = Collision_Group (Other_Group, one)
        if Collision:
            Group.remove(one)
            Counter += 1
    return Counter    


def LIVES_IMAGE(canvas, position, lives, width, space , image, im_infos):
    #drawing lives as images instead of scores 
    #Iterate through the loop 
    for one_live in range (lives):
        canvas.draw_image (image, im_infos.get_center (), im_infos.get_size(),[position[0] +  one_live *(width+space) , position [1]], [width,width],math.pi *1.5  )

class Ship:
    #Specification for the Ship:
    #The ship variables include 5 parameters , position of the ship, it velocity , angle of the ship , picture of the ship, info includes the size of the image
    def __init__(self, Position, Velocity, Angle, Image, Info ):
            self.Position       = [Position[0], Position[1]]
            self.Velocity       = [Velocity[0], Velocity [1]] 
            self.Thrust         = False
            self.Angle          = Angle 
            self.Angle_velocity = 0 
            self.Image          = Image 
            self.Image_size     = Info.get_size()
            self.Image_center   = Info.get_center()
            
            #Center_go is to draw the seocnd position of the picture
            self.Image_center_go = [self.Image_center [0]+ self.Image_size[0], self.Image_center[1]]
            self.Radius = Info.get_radius() 
            
          
    def draw (self,canvas):
        #This function is how to draw cnavas on the screen,
        #if the self.Thurst is equal to True , draw the second image , and if it is False , draw the first image 
        if self.Thrust :
            canvas.draw_image(self.Image, self.Image_center_go, self.Image_size, self.Position, self.Image_size, self.Angle)
            
        else:
            canvas.draw_image(self.Image, self.Image_center , self.Image_size, self.Position , self.Image_size, self.Angle)
    
    
    def UPDATE(self):
        
        #Update the angle :
        self.Angle +=  self.Angle_velocity
        
        
        #Update position of the ship
        self.Position [0] =(self.Position [0] + self.Velocity [0]) % CANVAS_WIDTH 
        self.Position [1] =(self.Position [1] + self.Velocity [1]) % CANVAS_HEIGHT
        
        #Update Velocity of the ship:
        if self.Thrust:
            Vector = Angle_to_Vector (self.Angle)
            self.Velocity [0] += Vector [0] * .1
            self.Velocity [1] += Vector [1] * .1
            
        self.Velocity [0] *= .99
        self.Velocity [1] *= .99
        
       
        
    def Thrust_Switch (self, on):
        #The function workd on the sound of the ship if the sound is on 
            self.Thrust = on
            if on :
                Ship_thrust_sound.rewind()
                Ship_thrust_sound.play ()
        
            else:
                Ship_thrust_sound.pause()
        
        
        
    def Increase_angle_velocity (self):
        self.Angle_velocity += .05
        
        
    def Decrease_angle_velocity (self):
        self.Angle_velocity -= .05
        
                

    def Shooting_missile (self):
        
        global Missiles        
        
        #Shooting the missiles using the Angle to Vector function 
        Shooting_missiles = Angle_to_Vector (self.Angle)
        
        #Calculating the missile position 
        Missile_Position = [self.Position[0] + self.Radius * Shooting_missiles [0], self.Position [1] + self.Radius * Shooting_missiles [1]]
        
        #The velocity of the missile shooting #the length of the shooting 
        Missile_Velocity = [self.Velocity[0] + 20* Shooting_missiles [0], self.Velocity[1] + 20 * Shooting_missiles[1]]
        
        #Group of missiles:
        Missiles_Group.add (Sprite (Missile_Position, Missile_Velocity, self.Angle, 0 , Missile_Image, Missile_Info,Missile_Sound))
        
class Sprite :

    #first step : create 7 variables     
    def __init__ (self, Position,Velocity, Angle, Angle_Velocity, Image , Infos, Sound = None):
    
        self.Position 		  = [Position [0] , Position [1]]
        self.Velocity         = [Velocity [0] , Velocity [1]]
        self.Initial_Velocity = [Velocity [0] , Velocity [1]]
        self.Angle            = Angle 
        self.Angle_Velocity   = Angle_Velocity 
        self.Image            = Image 
        self.Image_center     = Infos.get_center()
        self.Image_size       = Infos.get_size ()
        self.Radius           = Infos.get_radius () 
        self.Life_span        = Infos.get_life_span()
        self.Animated         = Infos.get_animated ()
        self.Age = 0
        
        #if sound == True 
        if Sound:
                Sound.rewind()
                Sound.play()          
    
    #Drawing the Sprites 
    def draw (self,canvas):
        
        Center = list (self.Image_center)  #creating a list of the position of the image
        
        if self.Animated :
             Center [0] = self.Image_center [0] +  (self.Image_size [0] * self.Age)
        
        canvas.draw_image (self.Image, Center, self.Image_size, self.Position, self.Image_size, self.Angle )
       
 
    #UPDATE THE SPRITE :
    def UP_date (self):
        
        #Update the angle:
        self.Angle += self.Angle_Velocity 
        
        #Update Position:
        self.Position [0] = (self.Position[0] + self.Velocity[0] ) % CANVAS_WIDTH
        self.Position [1] = (self.Position[1] + self.Velocity[1] ) % CANVAS_HEIGHT
        
        self.Age += 1
        
        return self.Age > self.Life_span 
         
    #
    def Collision (self,Other_Object):
            #
            return Distance (self.Position, Other_Object.Position ) <= self.Radius + Other_Object.Radius
     
      
        
#Key Strokes (Keyboard): when the key is pressses
def Key_Down (key):
    
    if key == simplegui.KEY_MAP ["left"]:
        my_ship.Decrease_angle_velocity ()
        
    elif key == simplegui.KEY_MAP ["right"]:
        my_ship.Increase_angle_velocity ()
        
    elif key == simplegui.KEY_MAP ["up"]:
        my_ship.Thrust_Switch (True)
        
    elif key == simplegui.KEY_MAP ["space"]:
        my_ship.Shooting_missile () 
        
        
def Key_Up (key):
    """Keys when the keys are up """
        
    if key == simplegui.KEY_MAP["left"]:
        my_ship.Increase_angle_velocity ()
        
    elif key == simplegui.KEY_MAP ["right"]:
        my_ship.Decrease_angle_velocity ()
        
    elif key == simplegui.KEY_MAP ["up"]:
        my_ship.Thrust_Switch (False)
        
        
         
        

def Moving_Astroids ():
    
    global Astroids, START
    
    # len of Astroids is the number of astroids that appear on the screen 
    if len(Astroids) > 30 or not START:
        pass
    #0.6
    Astroid_Velocity = [random.random() * 0.3 , random.random() * 0.3 ] #the speed of the astroid 
    Speed_Astroid_Rotation =  random.random() * 0.2  # the speed of the astroid rotation 
    Astroid_Position = [random.randrange (0, CANVAS_WIDTH), random.randrange(0,CANVAS_HEIGHT)]
    
    #Ensure the ship away from the rock by 100 pixels 
    while Distance (Astroid_Position , my_ship.Position) < 100:
        Astroid_Position = [random.randrange (0, CANVAS_WIDTH), random.randrange (0,CANVAS_HEIGHT) ]
    
    Astroids.add (Sprite (Astroid_Position , Astroid_Velocity, 0 ,Speed_Astroid_Rotation, Astroid_Image, Astroid_Info ) )
    
    


def draw(canvas):
    global TIME, Astroids, START, SCORE, LIVES
    
    #Animated background Images:
    TIME += 2
    W_Time = (TIME /  4 ) %CANVAS_WIDTH
    
    center = Debris_Info.get_center ()
    size   = Debris_Info.get_size ()
    
    canvas.draw_image(Background_image,Background_Info.get_center(),Background_Info.get_size(),[CANVAS_WIDTH // 2, CANVAS_HEIGHT //2],[CANVAS_WIDTH, CANVAS_HEIGHT] )
    canvas.draw_image(Debris_image, center, size, (W_Time - CANVAS_WIDTH //2 , CANVAS_HEIGHT //2),(CANVAS_WIDTH,CANVAS_HEIGHT))
    canvas.draw_image(Debris_image, center, size, (W_Time + CANVAS_WIDTH //2 , CANVAS_HEIGHT //2),(CANVAS_WIDTH , CANVAS_HEIGHT))
    
    #Draw the Ship :
    my_ship.draw(canvas)
    Sprite_Group (Astroids, canvas)
    Sprite_Group (Missiles_Group, canvas)
    Sprite_Group (Explosion_Group, canvas)
    
    #Increase the Astroid's velocity using score:
    for i in Astroids:
        for j in range (2):
            i.Velocity [j] = i.Initial_Velocity [j] + (i.Initial_Velocity [j] * SCORE * 0.03)
    
    #UPDATES 
    my_ship.UPDATE ()

    
    #Splash Image 
    if not START :
        canvas.draw_image (Intro_Image, Intro_Info.get_center (), Intro_Info.get_size (),[CANVAS_WIDTH /2,CANVAS_HEIGHT /2], Intro_Info.get_size())
    
    
    #Process Collisions:
    if Collision_Group (Astroids, my_ship):
        LIVES -= 1
    
    #Score is out of 10
    SCORE += Collision_Group2 ( Missiles_Group, Astroids) * 10
    
    
    #Gameover after three attempts:    
    if LIVES == 0 :
        Astroids = set ()
        START = False
        
        
    #Draw the text on the canvas for LIVES and SCORE
    canvas.draw_text ("Lives", [50,50],30,"White")
    
    #
    LIVES_IMAGE (canvas,[50,80], LIVES,40 ,10, Ship_Image, Ship_Info)
    #canvas.draw_image (image, im_infos.get_center (), im_infos.get_size(),[position[0] +  one_live *(width+space) , position [1]], [width,width],math.pi *1.5  )

    #Draw the score on the screen :
    canvas.draw_text ("Scores", [750,50],30, "White")
    canvas.draw_text (str (SCORE ), [750,80],30, "White")
    
    
#Click on the Intro image to start playing the game :
def Mouse_Click (Clicking ):
    
    #making the variables global so it can be used 
    global START, LIVES, SCORE
    
    if START == False :
        START = True 
        LIVES = 3
        SCORE = 0
        Sound.rewind()
        Sound.play ()




#Initializing the Game :
my_ship = Ship ([CANVAS_WIDTH / 2, CANVAS_HEIGHT /2 ], [0,0], 0 , Ship_Image, Ship_Info)

#Frame work:
Frame = simplegui.create_frame ("Spaceship", CANVAS_WIDTH, CANVAS_HEIGHT)
Frame.set_keydown_handler(Key_Down)
Frame.set_keyup_handler (Key_Up)
Frame.set_draw_handler(draw)
Frame.set_mouseclick_handler (Mouse_Click)

#sets 
Astroids        = set () # creating a set 
Missiles_Group  = set () #creating a set for the missiles
Explosion_Group = set () #creating a set for the explosion

#The time in milliseconds which controlls when the Astroids appear 
Timer = simplegui.create_timer (1000.0, Moving_Astroids)

Timer.start()
Frame.start()
