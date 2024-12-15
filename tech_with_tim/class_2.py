
# THE INHERITANCE - cats & dogs example:
#
#		betyr å "arve" instances fra en upper level class 
#       (bokstavelig talt en class som ligger over dem)

import time
class Pet:
	def __init__(self, name, age):
		self.name = name
		self.age = age

	def show(self):
		Pet.show.was_called = True
		if name=="Bubbles":
			pass
		else:
			print(f'"I am {self.name} and I am {self.age} years old."')
	show.was_called = False

	def speak(self):
		print("It doesn't understand you, what are you doing? People are looking..")

class Cat(Pet):
	def __init__(self, name, age, color):
		super().__init__(name,age)
		self.color = color

	def show(self):
		Cat.show.was_called = True
		print(f'"I am {self.name}, I am {self.age} years old and I am {self.color}."')
	show.was_called = False

	def speak(self):
		Cat.speak.was_called = True
		time.sleep(1)
		print('"... I mean Meow!"')
	speak.was_called = False


class Dog(Pet):
	def speak(self):
		print('"		-I MEAN BARK!!"')



class Fish(Pet):
	pass



def action():
	return "*talk to the"


class Investigate:
	def talk_to_cat(self):
		print(action() + " cat*")
		c = Cat("Mittens", 12, "Brown")
		c.show()
		if c.show.was_called:
			Cat.speak(c)
			print("")

	def talk_to_dog(self):
		print(action() + " dog*")
		p = Pet("Tim", 19)
		p.show()
		if p.show.was_called:
			Cat.speak(p)
			if Cat.speak.was_called==True:
				Dog.speak(p)
				print("")

	def talk_to_fish(self):
		f = Fish("Bubbles", 10)
		f.speak()
		print("")



def first_mission():
	I=Investigate()
	input_=input("Type your answer:  ")
	if input_=="Cat":
		I.talk_to_cat()
	elif input_=="Dog":
		I.talk_to_dog()
	elif input_=="Fish":
		I.talk_to_fish()
	elif input_=="Myself": 
		print("Then go ahead, do it")
		time.sleep(5)
		print("there, are you done? great")
		first_mission()
	elif input_=="Yourself":
		print("No, not myself.. YOURself!")
		first_mission()
	else:
		print("Just answer the fucking question..")
		first_mission()



def start_game():
	print(
		"Who should I investigate:"
		" Cat,"+
		" Dog,"+
		" Fish,"+
		" or Yourself. "
		)
	first_mission()



def menu():
	input_=input("Type your answer:  ")
	if input_=="yes":
		start_game()
	if input_=="no":
		print("oh, sorry.. I'll wait")
		time.sleep(2)
		print("...")
		time.sleep(1)
		print("how about now?")
		menu()
	if input_=="view credits":
		print("Mind your own business!")
		menu()

def main():
	print(f"Would you like to start the game? [ yes / no / view credits ]")
	menu()


if __name__ == '__main__':
	main()
