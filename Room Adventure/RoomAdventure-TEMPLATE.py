###########################################################################################
# Name: Zachary, Alayna, Justus, Grayson
# Date: 4/22/2024
# Description: 
###########################################################################################
from tkinter import *
from random import choice

class Entities:
    def __init__(self,playerHealth,enemyHealth):
        self.playerHealth = playerHealth
        self.enemyHealth = enemyHealth
    

    @property
    def playerHealth(self):
        return self._playerHealth
    @playerHealth.setter
    def playerHealth(self,value):
        self._playerHealth = value
        
    @property
    def enemyHealth(self):
        return self._enemyHealth
    @enemyHealth.setter
    def enemyHealth(self,value):
        self._enemyHealth = value

# the room class
# note that this class is fully implemented with dictionaries as illustrated in the lesson "More on Data Structures"
class Room:
	# the constructor
	def __init__(self, name, image):
		# rooms have a name, an image (the name of a file), exits (e.g., south), exit locations
		# (e.g., to the south is room n), items (e.g., table), item descriptions (for each item),
		# and grabbables (things that can be taken into inventory)
		self.name = name
		self.image = image
		self.exits = {}
		self.items = {}
		self.grabbables = []
		self.enemy = {}

	# getters and setters for the instance variables
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, value):
		self._name = value

	@property
	def image(self):
		return self._image

	@image.setter
	def image(self, value):
		self._image = value

	@property
	def exits(self):
		return self._exits

	@exits.setter
	def exits(self, value):
		self._exits = value

	@property
	def items(self):
		return self._items

	@items.setter
	def items(self, value):
		self._items = value

	@property
	def grabbables(self):
		return self._grabbables

	@grabbables.setter
	def grabbables(self, value):
		self._grabbables = value

	# adds an exit to the room
	# the exit is a string (e.g., north)
	# the room is an instance of a room
	def addExit(self, exit, room):
		# append the exit and room to the appropriate dictionary
		self._exits[exit] = room

	# adds an item to the room
	# the item is a string (e.g., table)
	# the desc is a string that describes the item (e.g., it is made of wood)
	def addItem(self, item, desc):
		# append the item and description to the appropriate dictionary
		self._items[item] = desc

	# adds a grabbable item to the room
	# the item is a string (e.g., key)
	def addGrabbable(self, item):
		# append the item to the list
		self._grabbables.append(item)

	# removes a grabbable item from the room
	# the item is a string (e.g., key)
	def delGrabbable(self, item):
		# remove the item from the list
		self._grabbables.remove(item)
	
	def addEnemy(self,baddy,desc):
		self.enemy[baddy] = desc
     
	# returns a string description of the room
	def __str__(self):
		# first, the room name
		s = "You are in {}.\n".format(self.name)

		# next, the items in the room
		s += "You see: "
		for item in self.items.keys():
			s += item + " "
		s += "\n"

		# if an enemy is seen
		for baddy in self.enemy:
			if(baddy == "Baby-Gronk"):
				s += "You also see: "
				s+= baddy
				descrip = self.enemy["Baby-Gronk"]
				s+= f"\n{descrip}"	
				s+= "\n"
			
		# next, the exits from the room
		s += "Exits: "
		for exit in self.exits.keys():
			s += exit + " "

		return s
     
     
     
# the game class
# inherits from the Frame class of Tkinter
class Game(Frame,Entities):
	# the constructor
	def __init__(self, parent):
		# call the constructor in the superclass
		Frame.__init__(self, parent)
		Entities.__init__(self,playerHealth = 150, enemyHealth = 300)
		self.playerHealth = 150
		self.enemyHealth = 300

	# creates the rooms
	def createRooms(self):
		#change before we put in 
	
		r1 = Room("Room 1", "Room Adventure/roomImage/ZachRoom1.gif")
		r2 = Room("Room 2", "Room Adventure/roomImage/Alaynaroom2.gif")
		r3 = Room("Room 3", "Room Adventure/roomImage/ZachRoom3.gif")
		r4 = Room("Room 4", "Room Adventure/roomImage/Alaynaroom4.gif")
		r5 = Room("Room 5", "Room Adventure/roomImage/Armory.gif")
		r6 = Room("Room 6", "Room Adventure/roomImage/BabyGronkRoom.gif")

		r1.addExit("east", r2)
		r1.addExit("south", r3)
		r1.addGrabbable("key")
		r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
		r1.addItem("table", "It is made of oak. A golden key rests on it.")
		
		r2.addExit("west", r1)
		r2.addExit("south", r4)
		r2.addItem("rug", "It is nice and Indian. It also needs to be vacuumed.")
		r2.addItem("fireplace", "It is full of ashes.")

		r3.addExit("north", r1)
		r3.addExit("east", r4)
		r3.addGrabbable("book")
		r3.addItem("bookshelves", "They are empty. Go figure.")
		r3.addItem("statue", "There is nothing special about it.")
		r3.addItem("desk", "The statue is resting on it. So is a book.")

		r4.addExit("north", r2)
		r4.addExit("west", r3)
		r4.addExit("south", None)
		r4.addExit("up-stairs", r5)
		r4.addGrabbable("6-pack")
		r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout \
			 on the brew rig. A 6-pack is resting beside it.")
		
		r5.addExit("north", r6)
		r5.addExit("down-stairs", r4)
		r5.addItem("sword", "A very sharp sword it might come in handy against football players")
		r5.addGrabbable("sword")
		r5.addItem("shield", "Might be helpful to have saving a princess!")
		r5.addGrabbable("shield")
		r5.addItem("fire-flower","You feel its embers inside of you")
		r5.addGrabbable("fire-flower")
		r5.addItem("beans",'You feel a great sense of power from these beans, they say the owner is somebody named Goku')
		r5.addGrabbable("beans")

		r6.addEnemy("Baby-Gronk", "A powerful foe who rizzes up Livy Dunne in Ohio\nwith level 100 rizz, he also has a PHD \nin Rizzonomics")
		
		Game.currentRoom = r1
		Game.inventory = []

	def attack(self,name):
		num1 = choice[0,45,70,125,20,20,20]
		num2 = choice[0,5,10,20,3,3]
		if(name == "player"):
			Game.text.insert(f"You did {(num1)} damage to Baby-Gronk!")
			self.enemyHealth -= num1
			return choice(num1)
		else:
			Game.text.insert(f"The boss did {(num2)} damage to you!")
			self.playerHealth -= num2

	def commenceBattle(self):
		while(self.playerHealth > 0 and self.enemyHealth > 0):
			self.attack("player")
			self.attack("boss")
   
		if(self.playerHealth == 0):
			#player loses return True
			return True 
		else:
			#player wins return False
			return False
			
			
	
	# sets up the GUI
	def setupGUI(self):
		#organize the GUI
		self.pack(fill=BOTH, expand=1)

		# setup the player input at the bottom of the GUI
		# the widget is a Tkinter Entry
		# set its background to white and bind the return key to the
		# function process in the class
		# push it to the bottom of the GUI and let it fill
		# horizontally
		# give it focus so the player doesn't have to click on it
		Game.player_input = Entry(self, bg="white")
		Game.player_input.bind("<Return>", self.process)
		Game.player_input.pack(side=BOTTOM, fill=X)
		Game.player_input.focus()
  
		# setup the image to the left of the GUI
		# the widget is a Tkinter Label
		# don't let the image control the widget's size
		img = None
		Game.image = Label(self, width=WIDTH // 2, image=img)
		Game.image.image = img
		Game.image.pack(side=LEFT, fill=Y)
		Game.image.pack_propagate(False)
  
		# setup the text to the right of the GUI
		# first, the frame in which the text will be placed
		text_frame = Frame(self, width = WIDTH // 2)
  
		# the widget is a Tkinter Text
		# disable it by default
		# don't let the widget control the frame's size
  
		Game.text = Text(text_frame, bg = "lightgrey", state = DISABLED)
		Game.text.pack(fill=Y, expand=1)
		text_frame.pack(side=RIGHT, fill=Y)
		text_frame.pack_propagate(False)
  
	# sets the current room image
	def setRoomImage(self):
		if (Game.currentRoom == None):
			# if dead, set the skull image
			Game.img = PhotoImage(file = "Room Adventure/roomImage/skull.gif")
		else:
			# otherwise grab the image for the current room
			Game.img = PhotoImage(file = Game.currentRoom.image)
		# display the image on the left of the GUI
		Game.image.config(image=Game.img)
		Game.image.image = Game.img
   
	# sets the status displayed on the right of the GUI
	def setStatus(self, status):
		# sets the status displayed on the right of the GUI
		Game.text.config(state=NORMAL)
		Game.text.delete("1.0", END)
		if (Game.currentRoom == None):
			# if dead, let the player know
			Game.text.insert(END, "You are dead. The only thing you can do now is quit.\n")
   
		else:
			# otherwise, display the appropriate status
			Game.text.insert(END, f"{Game.currentRoom} \nYou are carrying: {Game.inventory}\n\n {status}")
                
		Game.text.config(state=DISABLED)
  
	# plays the game
	def play(self):
		# add the rooms to the game
		self.createRooms()
		# configure the GUI
		self.setupGUI()
		# set the current room
		self.setRoomImage()
		# set the current status
		self.setStatus("")

	# processes the player's input
	def process(self, event):
		# grab the player's input from the input at the bottom of
		# the GUI
		action = Game.player_input.get()
		# set the user's input to lowercase to make it easier to
		# compare the verb and noun to known values
		action = action.lower()
		# set a default response
		response = "I don't understand. Try verb noun. Valid verbs are go, look, take, and attack"
		# exit the game if the player wants to leave (supports quit,
		# exit, and bye)
  
		if (action == "quit" or action == "exit" or action == "bye" or action == "sionara!"):
			exit(0)
   
		# if the player is dead if goes/went south from room 4
		if (Game.currentRoom == None):
			# clear the player's input
			Game.player_input.delete(0, END)
			return 
   
		# split the user input into words (words are separated by
		# spaces) and store the words in a list
		words = action.split()
		# the game only understands two word inputs
		if (len(words) == 2):
			# isolate the verb and noun
			verb = words[0]
			noun = words[1]
   
			# the verb is: go
			if (verb == "go"):
				# set a default response
				response = "Invalid exit."
     
				# check for valid exits in the current room
				if (noun in Game.currentRoom.exits):
					# if one is found, change the current room to
					# the one that is associated with the
					# specified exit
					Game.currentRoom = Game.currentRoom.exits[noun] 
					# set the response (success)
					response = "Room changed."
    
			# the verb is: look
			elif (verb == "look"):
				# set a default response
				response = "I don't see that item."
    
				# check for valid items in the current room
				if (noun in Game.currentRoom.items):
					# if one is found, set the response to the item's description
					response = Game.currentRoom.items[noun]
    
			# the verb is: take
			elif (verb == "take"):
			# set a default response
				response = "I don't see that item."
   
				# check for valid grabbable items in the current
				# room
				for grabbable in Game.currentRoom.grabbables:
				# a valid grabbable item is found
					if (noun == grabbable):
						# add the grabbable item to the player's
						# inventory
						Game.inventory.append(grabbable)
						# remove the grabbable item from the
						# room
						Game.currentRoom.delGrabbable(grabbable)
						# set the response (success)
						response = "Item grabbed."
						# no need to check any more grabbable
						# items
						break
  
			elif(verb == "attack"):
				response = "I don't know what enemy you're talking about."

				for enemy in Game.currentRoom.enemy:
					self.setStatus("Battle has commenced")
					result = Game.commenceBattle(enemy)


					if(result == False):
						response = "Congratulations you won the game! \nYou can continue exploring or quit the game."
						exit(0)
					else:
						response = "You lost goodbye..."
						Game.img = PhotoImage(file = "Room Adventure/roomImage/skull.gif")
					break
 
		# display the response on the right of the GUI
		# display the room's image on the left of the GUI
		# clear the player's input
		self.setStatus(response)
		self.setRoomImage()
		Game.player_input.delete(0,END)
  
##########################################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("Room Adventure")

# create the GUI as a Tkinter canvas inside the window
g = Game(window)
# play the game
g.play()

# wait for the window to close
window.mainloop()

