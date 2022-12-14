#!/usr/bin/python
# -*- coding: utf-8 -*-

#########################################################################################
# Required variables for the game
#########################################################################################

global Configuration # Global value used in the whole code
Configuration = None # Value containing the informations about paths

global engine # Global value used in the whole code
engine = None # Value containing the engine module

global importer # Global value used in the whole code
importer = None # Value containing the importer module

global Current_Version_Data # Global value used in the whole code
Current_Version_Data = None # Value containing the number of build and version data


def init_Game () :

    importer = engine.importer

    logger = engine.logger

    class Game :

        # Debug

        Debug = True # Debug for developer

        ######################################

        # UI gestion

        Title_Params = ["Chest Rush","red","Helvetica",60] #  Parameters for the name of the game
        Window_Sizes = [[640,640],[224,78]] # Sizes of window (0:auth canvas, 1:auth entry,)
        Auth_Msgs = ["Welcome back","Launching","User authentified","Good bye"]
        Chat_Message = [""] * 10
        Chat_Labels = [0] * 10
        Colors = {"§4" : "#be0000", "§c" : "#fe3f3f", "§6" : "#d9a334", "§e" : "#fefe3f", "§2" : "#00be00", "§a" : "#3ffe3f", "§b" : "#3ffefe", "§3" : "#00bebe", "§1" : "#0000be", "§9" : "#3f3ffe", "§d" : "#fe3ffe", "§5" : "#be00be", "§f" : "#ffffff", "§7" : "#bebebe", "§8" : "#3f3f3f", "§0" : "#000000"}
        Chat_Colors = ["grey"] * 10
        ######################################

        # Displacement gestion

        Playername = "Z3R0xLEGEND"
        Radius = 10 # Radius of the player
        Player_Coords = None # Coordinates of the player in the game
        Rotation = 0 # Rotation of the player
        Movement = (0, 0)   # Type of movement on X,Y the player is doing
        Player_Speed = 2 # Speed of the player
        Fluidity = 10 # Reinitialisation time between keys

        Pressed_Keys = {100 : False, 113 : False, 122 : False, 115 : False} # All the keys pressed by the player

        ######################################

        # Cursor gestion

        X =  0 # Coordinate X of the cursor
        Y = 0 # Coordinate Y of the cursor
        Cursor_Size = 10 # Size of the player cursor

        ######################################
        

        # Shoot gestion

        Shoot_Stamp = 20 # Remaining time of shoot in canvas
        Shoot_Distance = 200 # Distance of the shoot
        Weapons = {"CANNON" : [3,"purple",10]}
        Weapon = "CANNON"
        load_time = 5 # time to reload the cannon
        next_shoot = importer.time.clock() + load_time # time for next shoot


        ######################################

        # Entities and colliders gestion

        Entity = {} # Entity who can take damage from shoot
        Colliders = {}  # Object who can collide with the player

        Spawn_Location = [[True,100,200],[True,500,400]]

        isle = ["Blue Lagoon","Chaos Bay","Hidden Bay","Little Pick","Thief's Bay" ] # all the isles
        visited_isle = list() # isles visited by the player with tresor collected

        ######################################

        # Player status
        
        Is_Alive  = True # If player is alive (True) or dead (False)
        Hidden = False # If player is hidden or not

        ######################################

        # AI gestion

        Detection = {}  # Collision area of each entity
        AI_Vision = {} # Detection of entity
        Proximity = [240,160] # When AI detect player

        ######################################

        # Audio gestion

        Audio = {"CHEST" : False, "ATTACK" : False, "APPEAR" : False}

        ######################################

        # Ressources for the game

        Object_Images = [] # Images created in the game

        if Debug :

            Build = "0.0.1.al.<DEV>.11.27.19" # Build number to identify different versions

        else :

            Build = "0.0.1.al.<PUBLIC>.11.27.19" # Build number to identify different versions

        ######################################

        Var_Used = None

        # User data

        Server_State = "Host"
        Player_Dict = {}
        Players_In_Game = {}
        Log = importer.time.strftime("%H-%M&%d-%m-%Y"), importer.time.strftime("the %d-%m-%Y at %Hh%M") # Time when the game was launched

        def __init__ (self,Master,auth = False) : # Initialisation of the game

            self.Master = Master # Attribution of master to the entire class

            logger.log_Operation("Master __init__ () set", op_time = importer.time.strftime("[%X] : ")) # Logging operation

            Master.title("Chest Rush") # Title of the window

            logger.log_Operation("Master title set", op_time = importer.time.strftime("[%X] : ")) # Logging operation

            if auth == False : # Player not authenticated

                self.log_Operation("Authentication not set")

                if self.Debug : # If developper mode is enabled

                    print("> Need authentication")

                ########################################################################################

                # UI gestion

                Coords = self.align_Window(self.Window_Sizes[0]) # Get the coordinates for the center of the screen

                logger.log_Operation("Coordinates added for window", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                Master.geometry("%dx%d+%d+%d" % (self.Window_Sizes[0][0], self.Window_Sizes[0][1], Coords[0], Coords[1])) # Align the window

                logger.log_Operation("Master alignated", op_time = importer.time.strftime("[%X] : ")) # Logging operation
                
                Master.overrideredirect(True) # Delete tkinter default UI

                logger.log_Operation("Master override activated", op_time = importer.time.strftime("[%X] : ")) # Logging operation
                
                Master.wm_attributes("-topmost",True) # Obligate the UI to be in the first position of the screen

                logger.log_Operation("Master topmost activated", op_time = importer.time.strftime("[%X] : ")) # Logging operation
                
                Master.wm_attributes("-transparentcolor","black") # Set the black color to transparent

                logger.log_Operation("Master transparentcolor activated", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                ########################################################################################

                # Canvas gestion

                self.Font = importer.tkinter.Canvas(Master,bg = "black",
                                            width = self.Window_Sizes[0][0],
                                            height = self.Window_Sizes[0][1],
                                            highlightthickness=0) # Canva for the auth window

                logger.log_Operation("Font canvas created", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                self.Icon = importer.ImageTk.PhotoImage(file = self.Ressource_Path + "/icons/tmfont.png") # Image to display

                logger.log_Operation("Icon set", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                self.Font.create_image(self.Window_Sizes[0][0]/2, self.Window_Sizes[0][1]/2, image = self.Icon) # Create an image on the canva

                logger.log_Operation("Background image created", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                self.Text_Label = self.Font.create_text(self.Window_Sizes[0][0]/2,
                                                            self.Window_Sizes[0][1]/2,
                                                            font = (self.Title_Params[2],self.Title_Params[3]),
                                                            fill = self.Title_Params[1],
                                                            text = self.Title_Params[0]) # Label displaying the name of the game

                logger.log_Operation("Text created", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                self.Font.pack() # Placement of the canva

                logger.log_Operation("Canvas placed on screen", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                logger.log_Operation("Verifying user", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                if not importer.os.path.exists("./userdata/user.json") : # If file is not existant

                    logger.log_Operation("*User not registered", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                    Master.after(1000,
                                     self.auth_Window)  # Authentify the user

                else :  #Sinon (fichier avec les informations utilisateur stockees)

                    Master.after(1000,
                                     self.update_Label,self.Auth_Msgs[0])    #Signale a l'utilisateur que le compte est enregistre

                    Master.after(2000,
                                     self.update_Label,self.Auth_Msgs[1]) #Alerte l'utilisateur du lancement de l'application

                    Master.after(3000,
                                     self.relaunch_App) #Relance l'application

            else : # Player already authenticated

                logger.log_Operation("Player authenticated", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                logger.log_Operation("Calculating window sizes", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                Screen_Width = self.Master.winfo_screenwidth() # Width of actual screen
                Screen_Height = self.Master.winfo_screenheight() # Height of actual screen

                logger.log_Operation("Window sizes calculated", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                logger.log_Operation("Initializing Pygame", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                importer.pygame.init()

                logger.log_Operation("Pygame initialised", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                logger.log_Operation("Getting coordinates for alignement", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                Coords = self.align_Window((Screen_Width,Screen_Height)) # Get the coordinates for the center of the screen

                logger.log_Operation("Coordinates set", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                Master.geometry("%dx%d+%d+%d" % (Screen_Width, Screen_Height, Coords[0], Coords[1])) # Align the window in the center of the screen

                logger.log_Operation("Window alignated", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                logger.log_Operation("Creating canvas", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                self.Canvas = importer.tkinter.Canvas(Master,
                                                 width = Screen_Width,
                                                 height = Screen_Height,
                                                 bg = "skyblue") # Creation of the canvas for drawing

                logger.log_Operation("Canvas created", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                self.Canvas.pack() # Placement of the canvas in the window

                logger.log_Operation("Canvas placed on screen", op_time = importer.time.strftime("[%X] : ")) # Logging operation

                self.Name_Var = importer.tkinter.StringVar() # Name variable

                self.Name_Var.set(self.Playername) # Name set to player input

                self.Server_Status = importer.tkinter.LabelFrame(Master,
                                                            text = self.Name_Var.get(),
                                                            bg = "gold",
                                                            width = 200,
                                                            height = 40) # Frame with player status

                self.Server_Status.place(x = 0, y = 0) # Placement of the player status in the window

                self.Server_Name = importer.tkinter.Label(self.Server_Status,
                                                    text = "00:00:00",
                                                    bg = "gold") # Frame with player name 

                self.Server_Name.place(x = 0, y = 0) # Placement of the player name in the window

                self.Score_Var = importer.tkinter.StringVar() # Score variable

                self.Score_Var.set("Score : 0") # Score set to 0

                self.Score_Label = importer.tkinter.Label(Master,
                                                    textvariable = self.Score_Var,
                                                    bg ="gold", width = 30) # Label with score

                self.Score_Label.place(x = self.Master.winfo_screenwidth() - 200, y = 0) # Placement of the score in the window

                Background = importer.Image.open(Configuration["STORAGE"]["Path"] + "fonts/ocean.png") # Reading data from background image loading or ocean

                self.Font = importer.ImageTk.PhotoImage(Background) # Creating an instance for tkinter

                self.Background = self.Canvas.create_image((960, 540), image = self.Font) # Drawing image on the screen

                self.Health_Bar = self.Canvas.create_rectangle(60,self.Master.winfo_screenheight()- 130, 540, self.Master.winfo_screenheight()- 110, width = 2, fill = "white", outline = "black") # Create a health bar

                self.Health_Bar_Fill = self.Canvas.create_rectangle(60,self.Master.winfo_screenheight()- 130, 540, self.Master.winfo_screenheight()- 110, fill = "seagreen1", width = 1, outline = "black") # Create a health bar fill

                self.Gun_Infos_FRAME = importer.tkinter.Frame(Master,
                                                        width = 300,
                                                        height = 100) # Informations of the holded gun

                self.Gun_Infos_FRAME.place(x = self.Master.winfo_screenwidth() - 455, y = self.Master.winfo_screenheight() - 140) # Placement of the frame in the window

                self.Gun_Var = importer.tkinter.StringVar() # Gun variable

                Gun_Name = "|| " + self.Weapon # Name of the weapon

                self.Gun_Var.set(Gun_Name) # Gun variable set to weapon name

                self.Gun_Name_Label = importer.tkinter.Label(self.Gun_Infos_FRAME,
                                                        textvariable = self.Gun_Var,
                                                        font=("Eurofighter", 24),
                                                        bg = "seagreen1",
                                                        fg = "green") # Gun name label

                self.Gun_Name_Label.grid(row = 0,column = 1) # Placement of the gun name in the window

                self.Gun_Munition_Var = importer.tkinter.StringVar() # Ammo variable

                self.Gun_Munition_Var.set("8/8") # Ammo variable set to ammo of the gun

                self.Gun_Munition_Label = importer.tkinter.Label(self.Gun_Infos_FRAME,
                                                        textvariable = self.Gun_Munition_Var,
                                                        font=("Eurofighter", 24),
                                                        bg = "seagreen1",
                                                        fg = "green") # Ammo of the gun

                self.Gun_Munition_Label.grid(row = 0,column = 0) # Placement of the label in the window

                self.Chat_Label = importer.tkinter.LabelFrame(Master,
                                                    text = "Chat textuel",
                                                    width = 30) # Label with messages

                for iteration in range(len(self.Chat_Labels)) :

                    self.Chat_Labels[iteration] = importer.tkinter.Label(self.Chat_Label,
                                                                            width = 30,
                                                                            height = 1,
                                                                            bg = "grey",
                                                                            text = self.Chat_Message[iteration])

                    self.Chat_Labels[iteration].grid(row = iteration)

                self.Sending_Frame = importer.tkinter.Frame(self.Chat_Label,
                                                                width = 30,
                                                                height = 1,
                                                                bg = "grey")

                self.Sending_Frame.grid(row = iteration + 1)

                self.Message = importer.tkinter.StringVar()

                self.Message.set("")

                self.Message_Entry = importer.tkinter.Entry(self.Sending_Frame,
                                                                width = 24,
                                                                textvariable = self.Message)

                self.Message_Entry.pack(side = importer.tkinter.LEFT)

                self.Send_Button = importer.tkinter.Button(self.Sending_Frame,
                                                            width = 6,
                                                            height = 1,
                                                            text = "SEND",
                                                            command = self.send_Message)

                self.Send_Button.pack(side = importer.tkinter.RIGHT)

                self.Chat_Label.place(x = self.Master.winfo_screenwidth() - 230, y = self.Master.winfo_screenheight() - 350)

                # create isles and ammo_box

                self.create_Image("Blue Lagoon",(400,300))

                self.create_Image("Blue Lagoon2",(800,500))

                self.create_Image("Chaos Bay",(600,600))

                self.create_Image("Chaos Bay2",(86,458))

                self.create_Image("Hidden Bay",(1100,100))

                self.create_Image("Hidden Bay2",(1050,800))

                self.create_Image("Little Pick",(300,600))

                self.create_Image("Little Pick2",(438,128))

                self.create_Image("Thief's Bay",(400,900))

                self.create_Image("Rock Four",(836,150))

                self.create_Image("Rock Four",(200,530))

                self.create_Image("Rock Four",(508,756))

                self.create_Image("Rock Three",(260,250))

                self.create_Image("Rock Three",(660,330))

                self.create_Image("Rock Three",(190,854))

                self.create_Image("Rock Three",(1196,582))

                self.create_Image("Rock Two",(730,860))

                self.create_Image("Rock Two",(1100,860))

                self.create_Image("Rock Two",(200,9800))

                self.create_Image("Rock Two",(1080,280))

                self.create_Image("Rock One",(960,339))

                self.create_Image("Rock One",(480,380))

                self.create_Image("Rock One",(708,544))

                self.create_Image("Rock One",(638,126))

                self.create_Image("Rock One",(296,442))

                self.create_Image("ammo_box",(60,865))

                self.create_Image("ammo_box",(490,290))

                self.create_Image("ammo_box",(890,186))

                self.create_Image("ammo_box",(1288,676))

                self.create_Image("ammo_box",(880,870))

                self.create_Image("ammo_box",(738,666))

                self.bind_Controls()

            ########################################################################################

        def align_Window (self,window_size) :   # Center windows and object on the screen

            Screen_width = self.Master.winfo_screenwidth() # Get the width of the screen
            Screen_height = self.Master.winfo_screenheight() # Get the height of the screen

            if self.Debug :
                print("Screen size: (",Screen_width,", ",Screen_height,")")

            X = (Screen_width/2) - (window_size[0]/2) # Coordinate x for the alignation

            Y = (Screen_height/2) - (window_size[1]/2) # Coordinate y for the coordination

            return [X, Y]



    #################################################################################################################################
        # COLLISION DETECTION

        def object_Collide (self, object_coords, movement) :

            logger.log_Operation("Testing collide on function object_Collide()", op_time = importer.time.strftime("[%X] : ")) # Logging operation

            # self.Colliders[Entity] = center_coords, Box_Size, "ammo_box", Entity

            #self.Canvas.itemconfig(self.Player[0],fill = "dark blue")

            for collider in self.Colliders :

                try :

                    self.Canvas.delete(self.AI_Vision[collider])

                except :

                    pass

                for area in range (3) :

                    try :

                        self.Canvas.delete(self.Detection[collider][area])

                    except :

                        pass

                Player_Center = (int(object_coords[2] - object_coords[0]) / 2) + object_coords[0], (int(object_coords[3] - object_coords[1]) / 2) + object_coords[1]

                self.Detection[collider] = [0,0,0]

                if self.Colliders[collider][2] != "ammo_box" and self.Colliders[collider][2] not in self.isle and self.Debug == True:

                    self.AI_Vision[collider] = self.Canvas.create_line(Player_Center[0], Player_Center[1], self.Colliders[collider][0][0], self.Colliders[collider][0][1], width = 2, fill = "yellow")

                    Distance = abs((self.Canvas.coords(self.Player[0])[0] + self.Radius) - self.Colliders[collider][0][0]), abs((self.Canvas.coords(self.Player[0])[1] + self.Radius) - self.Colliders[collider][0][1])

                    if Distance[0] <= self.Proximity[0] and Distance[1] <= self.Proximity[0] :

                        self.Detection[collider][1] = self.Canvas.create_rectangle(self.Colliders[collider][0][0] - self.Proximity[0], self.Colliders[collider][0][1] - self.Proximity[0], self.Colliders[collider][0][0] + self.Proximity[0], self.Colliders[collider][0][1] + self.Proximity[0], width = 4, outline = "lightblue")
                    
                    if Distance[0] <= self.Proximity[1] and Distance[1] <= self.Proximity[1] :

                        self.Detection[collider][2] = self.Canvas.create_rectangle(self.Colliders[collider][0][0] - self.Proximity[1], self.Colliders[collider][0][1] - self.Proximity[1], self.Colliders[collider][0][0] + self.Proximity[1], self.Colliders[collider][0][1] + self.Proximity[1], width = 4, outline = "blue")                

                Collision = abs(Player_Center[0] - self.Colliders[collider][0][0] + movement[0]), abs(Player_Center[1] - self.Colliders[collider][0][1] + movement[1])
                
                if Collision[0] <= self.Colliders[collider][1] and Collision[1] <= self.Colliders[collider][1] :

                    if self.Debug == True :

                        self.Detection[collider][0] = self.Canvas.create_rectangle(self.Colliders[collider][0][0] -self.Colliders[collider][1], self.Colliders[collider][0][1] - self.Colliders[collider][1], self.Colliders[collider][0][0] + self.Colliders[collider][1], self.Colliders[collider][0][1] + self.Colliders[collider][1], width = 3, outline = "red")

                    self.Canvas.update()

                    if self.Colliders[collider][2] == "ammo_box" :

                        Remaining_Ammo = self.Gun_Munition_Var.get()

                        Remaining_Ammo = Remaining_Ammo.split("/")

                        if int(Remaining_Ammo[0]) != int(Remaining_Ammo[1]) :

                            Difference = int(Remaining_Ammo[1]) - int(Remaining_Ammo[0])

                            Addition = int(Remaining_Ammo[0]) + 5

                            if Difference > Addition :

                                Ammo = Addition

                            else :

                                Ammo = int(Remaining_Ammo[0]) + Difference

                            Display = str(Ammo) + "/" + str(Remaining_Ammo[1])

                            if self.Debug:

                                print(self.Player, self.Playername,"found a ammo_box")

                            self.Gun_Munition_Var.set(Display)

                            self.Canvas.delete(self.Colliders[collider][3])

                            del self.Colliders[collider]

                            self.Canvas.delete(self.Detection[collider][0])

                            del self.Detection[collider]

                        return False

                    elif self.Colliders[collider][2] in self.isle :

                        if self.Colliders[collider][2] not in self.visited_isle :

                            ChestLoading = importer.pygame.mixer.Sound(Configuration["STORAGE"]["Path"] + "sounds/chestLoad.wav")

                            ChestLoading.play()

                            Score = int(self.Score_Var.get()[8:])

                            Score += 500

                            Score = "SCORE : " + str(Score)

                            self.Score_Var.set(Score)

                            self.visited_isle.append(self.Colliders[collider][2])


                        return True

                        if self.Debug :

                            print("Chest on Isle")

                        try :

                            for entity in self.Entity :
                                
                                self.Canvas.delete(self.AI_Vision[entity])

                                for area in range (3) :
                                    
                                    self.Canvas.delete(self.Detection[entity][area])

                                    self.Canvas.update()

                        except :

                            pass

                    else :
                        if self.Debug :
                            print(self.Player,"gets damage after collide")
                            
                        self.damage_Player(amount = 20)
                    
                        return True
            
            return False

    #################################################################################################################################
        # KEYBOARD GESTION AND SETTINGS

        def pressed_Key (self, args = None) :

            logger.log_Operation("Key pressed", op_time = importer.time.strftime("[%X] : ")) # Logging operation

            self.Pressed_Keys[args.keysym_num] = True

        def released_Key (self, args = None) :

            logger.log_Operation("Key released", op_time = importer.time.strftime("[%X] : ")) # Logging operation

            self.Pressed_Keys[args.keysym_num] = False

        def bind_Controls (self) :

            self.Var_Used = importer.tkinter.StringVar()

            self.Var_Used.set("00:10:00")

            self.Server_Name.config(textvariable = self.Var_Used)

            if self.Server_State == "Host" :

                Name = importer.socket.gethostbyname(importer.socket.gethostname())

                print(Name)

                self.Server = engine.server.Server("Aldoria","Bienvenue cher utilisateur dans la cave du marabou !",Name,8800,10,time_var = self.Var_Used,locations = self.Spawn_Location, player_dict = self.Players_In_Game)

                self.Server.start_Server()

                self.Master.after(6000,self.connect_To_Server,Name)

            else :

                self.connect_To_Server(host = "192.168.43.234")

        def connect_To_Server (self,host) :

            self.Connection = engine.client.Client(self.Playername,host,8800,push = self.analyze_Message)

            self.Connection.connect()

        def update_Player_Pos (self) :

            if self.Is_Alive == False :

                return

            Coords = self.Canvas.coords(self.Player[0])

            Object = self.Player

            # Object[0] = image and Object[1] = nickname

            Movement = [0,0]

            if self.Pressed_Keys[100] == True and Coords[2] < self.Master.winfo_screenwidth() +5 : # D

                if self.Debug :
                    print("Moving : RIGHT")

                if self.object_Collide(Coords, (self.Player_Speed, 0)) == False :

                    Movement = self.Player_Speed, 0

            if self.Pressed_Keys[113] == True and Coords[0] > -10 : # Q

                if self.Debug :
                    print("Moving : LEFT")

                if self.object_Collide(Coords, (- self.Player_Speed, 0)) == False :

                    Movement = - self.Player_Speed, 0

            if self.Pressed_Keys[122] == True and Coords[1] > 0: # # Z

                if self.Debug :
                    print("Moving : FORWARD")

                if self.object_Collide(Coords, (0, - self.Player_Speed)) == False :

                    Movement = 0, - self.Player_Speed

            if self.Pressed_Keys[115] == True and Coords[3] < self.Master.winfo_screenheight() -70 : # When user want to go down

                if self.Debug :
                    print("Moving : DOWN")

                if self.object_Collide(Coords, (0, self.Player_Speed)) == False :

                    Movement = 0, self.Player_Speed

            if Movement != [0,0] :

                Format = "." + "[" + str(Movement[0]) + "," + str(Movement[1]) + "]" + "/" + self.Playername

                self.Connection.send(Format)

                for player_object in self.Player :

                    self.Canvas.move(player_object,Movement[0],Movement[1])

            self.Canvas.update()

            Screen_Width = self.Master.winfo_screenwidth() / 2
            Screen_Height = self.Master.winfo_screenheight() / 2

            self.Master.after(self.Fluidity,
                                self.update_Player_Pos)

        def move_Player (self,name,movement) :

            for player_object in self.Player_Dict[name] :

                self.Canvas.move(player_object,movement[0],movement[1])

    #################################################################################################################################
        # SHOOT GESTION AND SETTINGS

        def shooting_Cursor (self,args) :   # Create and update the player cursor

            try :   # Try to do next line

                self.Canvas.delete(self.Cursor) # Destroy the cursor if exist

            except :    # If try failed

                pass # Pass the error

            self.X, self.Y = args.x, args.y # Get the coordinates where the player is looking

            self.Cursor = self.Canvas.create_oval(self.X + self.Cursor_Size, self.Y + self.Cursor_Size, self.X - self.Cursor_Size, self.Y - self.Cursor_Size, width = 3, outline = "blue") # Create a new cursor

        def getAngle(self,corner1, middle, corner2):

            Angle = abs(math.degrees(math.atan2(corner2[1]-middle[1], corner2[0]-middle[0]) - math.atan2(corner1[1]-middle[1], corner1[0]-middle[0])))

            return Angle

        def shoot_At (self,args) :

            shoot_time = importer.time.clock() # time when the player want to shoot

            if shoot_time > self.next_shoot: # reloading finish

                self.next_shoot = shoot_time + self.load_time

                Ammo = self.Gun_Munition_Var.get()

                Ammo = Ammo.split("/")
                
                if int(Ammo[0]) != 0 :

                    if self.Debug :
                        print("Player : (",self.Canvas.coords(self.Player[0])[0] + self.Radius,", ",self.Canvas.coords(self.Player[0])[1] + self.Radius,")")
                        print("Shoot at : (",self.X,", ",self.Y,")")

                    distancetir = ((abs(self.Canvas.coords(self.Player[0])[0] + self.Radius - self.X))**2 + (abs(self.Canvas.coords(self.Player[0])[1] + self.Radius - self.Y))**2)**0.5 #distance de tir

                    if distancetir != self.Shoot_Distance:

                        self.X = round((self.X - self.Canvas.coords(self.Player[0])[0] - self.Radius) * (self.Shoot_Distance/distancetir) + self.Canvas.coords(self.Player[0])[0] + self.Radius)
                        self.Y = round((self.Y - self.Canvas.coords(self.Player[0])[1] - self.Radius) * (self.Shoot_Distance/distancetir) + self.Canvas.coords(self.Player[0])[1] + self.Radius)

                        distancetir = ((abs(self.Canvas.coords(self.Player[0])[0] + self.Radius - self.X))**2 + (abs(self.Canvas.coords(self.Player[0])[1] + self.Radius - self.Y))**2)**0.5

                    if self.Debug :    
                        print("Ball fell to : (",self.X,", ",self.Y,") Shoot distance :", distancetir)

                    Line = self.Canvas.create_line(self.Canvas.coords(self.Player[0])[0] + self.Radius, self.Canvas.coords(self.Player[0])[1] + self.Radius, self.X, self.Y, width = self.Weapons[self.Weapon][0], fill = self.Weapons[self.Weapon][1])

                    for entity in self.Entity :

                        if self.X in range (abs(int(self.Entity[entity][0][0])), abs(int(self.Entity[entity][0][2]))) :

                            if self.Y in range (abs(int(self.Entity[entity][0][1])), abs(int(self.Entity[entity][0][3]))) :

                                self.player_Tomb(self.Entity[entity][1])

                                if self.Debug == True :

                                    self.Canvas.delete(self.AI_Vision[entity])

                                    del self.AI_Vision[entity]

                                    del self.Detection[entity]

                                    for area in range (3) :

                                        try :

                                            self.Canvas.delete(self.Detection[collider][area])

                                        except :

                                            pass

                                else :

                                    self.Canvas.delete(self.Detection[entity][0])

                                del self.Colliders[entity]

                                del self.Entity[entity]

                                Score = int(self.Score_Var.get()[8:])

                                Score += 1000

                                Score = "SCORE : " + str(Score)

                                self.Score_Var.set(Score)

                                Hit = importer.pygame.mixer.Sound(Configuration["STORAGE"]["Path"] + "Sounds/Hitmarker.wav")

                                Hit.set_volume(2)

                                Hit.play()

                                break

                    for entity in self.Entity:

                        Angle = self.getAngle((self.X,self.Y), self.Canvas.coords(self.Player[0]), self.Entity[entity][0])

                        if Angle <= 5:

                            self.player_Tomb(self.Entity[entity][1])

                            if self.Debug == True :

                                self.Canvas.delete(self.AI_Vision[entity])

                                del self.AI_Vision[entity]

                                del self.Detection[entity]

                                for area in range (3) :

                                    try :

                                        self.Canvas.delete(self.Detection[collider][area])

                                    except :

                                        pass

                            else :

                                self.Canvas.delete(self.Detection[entity][0])

                            del self.Colliders[entity]

                            del self.Entity[entity]

                            Score = int(self.Score_Var.get()[8:])

                            Score += 500

                            Score = "SCORE : " + str(Score)

                            self.Score_Var.set(Score)

                            break

                    Remaining_Ammo = str(int(Ammo[0]) - 1) + "/" + Ammo[1]

                    self.Gun_Munition_Var.set(Remaining_Ammo)

                    Shoot = importer.pygame.mixer.Sound(Configuration["STORAGE"]["Path"] + "sounds/fire.wav")

                    Shoot.set_volume(1.0)

                    Shoot.play()

                    self.Master.after(self.Weapons[self.Weapon][2],
                                        self.Canvas.delete, Line)
            else:

                if self.Debug:

                    print("Reloading, next shoot ready at :", self.next_shoot, ", actual time :", shoot_time)

        def damage_Player (self, amount) :

            if self.Debug:
                print("Damage :",self.Playername, amount)

            Is_Dead = self.Canvas.coords(self.Health_Bar_Fill)[2] - amount - self.Canvas.coords(self.Health_Bar_Fill)[0]

            if Is_Dead <= 0 :

                self.Canvas.coords(self.Health_Bar_Fill, self.Canvas.coords(self.Health_Bar_Fill)[0], self.Canvas.coords(self.Health_Bar_Fill)[1], self.Canvas.coords(self.Health_Bar_Fill)[0], self.Canvas.coords(self.Health_Bar_Fill)[3])

                self.play_Death()

            else :

                self.Canvas.coords(self.Health_Bar_Fill, self.Canvas.coords(self.Health_Bar_Fill)[0], self.Canvas.coords(self.Health_Bar_Fill)[1], self.Canvas.coords(self.Health_Bar_Fill)[2] - amount, self.Canvas.coords(self.Health_Bar_Fill)[3])


        def play_Death (self) :

            self.Is_Alive = False

            if self.Debug:
                print(self.Playername, "is death")

            self.Canvas.itemconfig(self.Player[0], fill = "yellow")

            self.Master.unbind("<KeyPress>")
                
            self.Master.unbind("<KeyRelease>")

            self.Canvas.unbind("<Motion>")

            self.Canvas.unbind("<ButtonPress-1>")

            try :

                self.Canvas.delete(self.Cursor)

            except :

                pass

            self.Canvas.config(cursor = "arrow")

            self.Pressed_Keys = {100 : False, 113 : False, 122 : False, 115 : False}

            for entity in self.Entity :

                try :

                    self.Canvas.delete(self.AI_Vision[entity])

                except :

                    pass

                for area in range (3) :

                    try :

                        self.Canvas.delete(self.Detection[collider][area])

                    except :

                        pass    

                self.Canvas.delete(self.Detection[entity][0])

                self.Canvas.delete(self.Detection[entity][1])

                self.Canvas.delete(self.Detection[entity][2])

            self.Master.after(1000,
                                  self.player_Tomb, self.Player)

        def player_Tomb (self, entity) :    # Create a tomb where the entity died

            coords = self.Canvas.coords(entity[0])  # Get the coords of the entity killed

            self.Master.after(10,
                                  self.Canvas.delete, entity[0]) # Delete the entity after 10 ms

            self.Master.after(10,
                                  self.Canvas.delete, entity[2]) # Delete the shoot indicator after 10 ms
            
            Tomb = self.Canvas.create_line(coords[0], coords[1], coords[2], coords[3], width = 4, fill = "red"), self.Canvas.create_line(coords[0], coords[3], coords[2], coords[1], width = 4, fill = "red") # Create a cross where the entity died

            self.Master.after(20000,
                                  self.Canvas.delete, entity[1]) # Delete the entity name after 20 sec

            self.Master.after(20000,
                                  self.Canvas.delete, Tomb[0]) # Delete the tomb after 20 sec

            self.Master.after(20000,
                                  self.Canvas.delete, Tomb[1])  # Delete the tombs after 20 sec

        def create_Player (self,coords,name) :

            if self.Debug :

                print("Create player launch")

            print("Created")

            if name == self.Playername :

                self.Player = self.Canvas.create_oval(coords[0] - self.Radius, coords[1] - self.Radius, coords[0] + self.Radius, coords[1] + self.Radius, width = 2, fill = "lightblue"), self.Canvas.create_text(coords[0], coords[1] - 30, fill = "purple", font = "Times 10 italic bold", text = self.Name_Var.get()),self.Canvas.create_oval(coords[0] - self.Shoot_Distance, coords[1] - self.Shoot_Distance, coords[0] + self.Shoot_Distance, coords[1] + self.Shoot_Distance, outline = "yellow", width = 2)

                self.Canvas.update()

                if self.Debug :

                    print(self.Canvas.coords(self.Player[0]))

                self.Master.bind("<KeyPress>", self.pressed_Key)
                
                self.Master.bind("<KeyRelease>", self.released_Key)

                self.Canvas.bind("<Motion>", self.shooting_Cursor)

                self.Canvas.bind("<ButtonPress-1>", self.shoot_At)

                self.Canvas.config(cursor = "none")

                self.update_Player_Pos()

            else :

                print("OTHER PLAYER")

                self.Player_Dict[name] = self.Canvas.create_oval(coords[0] - self.Radius, coords[1] - self.Radius, coords[0] + self.Radius, coords[1] + self.Radius, width = 2, fill = "blue"), self.Canvas.create_text(coords[0], coords[1] - 30, fill = "purple", font = "Times 10 italic bold", text = name),self.Canvas.create_oval(coords[0] - self.Shoot_Distance, coords[1] - self.Shoot_Distance, coords[0] + self.Shoot_Distance, coords[1] + self.Shoot_Distance, outline = "yellow", width = 2)

                self.Canvas.update()

        def create_Entity (self, name = None, center_coords = None) :

            if center_coords == None :

                X = self.Master.winfo_screenwidth() / 2
                
                Y = self.Master.winfo_screenheight() / 2

            else :

                X = center_coords[0]

                Y = center_coords[1]

            Entity = self.Canvas.create_oval(X - self.Radius, Y - self.Radius, X + self.Radius, Y + self.Radius, width = 2, fill = "red"), self.Canvas.create_text(X, Y - 25, fill = "yellow", font = "Times 10 italic bold", text = name)

            self.Canvas.update()

            self.Entity[name] = self.Canvas.coords(Entity[0]), Entity

            self.Colliders[name] = center_coords, self.Radius, "entity", Entity[0]

        def create_Image (self, img_type, center_coords) :

            if img_type == "ammo_box" :

                Path = Configuration["STORAGE"]["Path"] + "objects/barrels.png"

            else :

                Path = Configuration["STORAGE"]["Path"] + "isles/" + img_type + ".png"

            Object = importer.Image.open(Path)

            self.Object_Images.append(importer.ImageTk.PhotoImage(Object))

            Entity = self.Canvas.create_image((center_coords[0], center_coords[1]), image = self.Object_Images[len(self.Object_Images)-1])

            self.Colliders[Entity] = center_coords, 20, img_type, Entity

        def update_Label (self,txt) : # affiche un champ pour saisir la classe à creer

            self.Font.itemconfigure(self.Text_Label, text = txt)    #Met a jour le label affiche avec le contenu changé

        def analyze_Message (self,message) :

            if message.startswith("<") or message.startswith("[") :

                self.Chat_Message = self.Chat_Message[1:]

                try :

                    Format = message.split(":")[1][1:3] # Color format

                    self.Chat_Colors = self.Chat_Colors[1:]

                    if Format in self.Colors : # If color detected

                        self.Chat_Colors.append(self.Colors[Format])

                        Reformater = message.split(":")[0] + ": " + message.split(":")[1][3:]

                        self.Chat_Message.append(Reformater)

                    else :

                        self.Chat_Colors.append("grey")

                        self.Chat_Message.append(message)

                except :

                    self.Chat_Message.append(message)

                for iteration in range (len(self.Chat_Message)) :

                    self.Chat_Labels[iteration].config(text = self.Chat_Message[iteration])

                    self.Chat_Labels[iteration].config(bg = self.Chat_Colors[iteration])

            else :

                print("ELSE")

                print(message)

                if message.startswith("_") :

                    print("SPAWNING")

                    Command = message[1:]

                    print(Command)

                    Command = Command.split("/")

                    print("SPLIT",Command)

                    Coordinates = eval(Command[1])

                    print("Coords : ",Coordinates)

                    self.create_Player(Coordinates,name = Command[2])

                    self.update_Timer(Command[0])

                elif message.startswith(".") :

                    Command = message[1:]

                    Command = Command.split("/")

                    if Command[1] != self.Playername :

                        Coordinates = eval(Command[0])

                        self.move_Player(name = Command[1],movement = Coordinates)

        def send_Message (self) :

            if self.Message.get() != "" :

                self.Connection.send(self.Message.get())

                self.Message.set("")

        def update_Timer (self, time) :

            if time == "00:00:00" :
            
                var.set("00:00:00")

                self.Var_Used = None

            else :

                time = time.split(":")

                hour = int(time[0])

                minut = int(time[1])

                sec = int(time[2])

                if sec == 0 :

                    sec = "59"

                    if minut == 0 :

                        hour -= 1

                        minut = "59"

                    else :

                        minut -= 1

                else :

                    sec -= 1

                if int(sec) < 10 :

                    sec = "0" + str(sec)

                if int(minut) < 10 and str(minut) != "00" :

                    minut = "0" + str(minut)

                if int(hour) < 10 :

                    hour = "0" + str(hour)

                value = str(hour) + ":" + str(minut) + ":" + str(sec)

                self.Var_Used.set(value)

                self.Master.after(1000,
                                    self.update_Timer, value)


    Root = importer.tkinter.Tk()

    Game(Root, True)

    Root.mainloop()
