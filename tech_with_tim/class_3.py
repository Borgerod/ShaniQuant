
#CLASSMETHODS & variables outside of functions/methods

class Person: 
	number_of_people = 0
	GRAVITY = -9.8

	@classmethod
	def number_of_people_(cls):
		return cls.number_of_people

	@classmethod
	def add_person(cls):
		cls.number_of_people += 1

	def __init__(self, name):
		self.name = name
		Person.add_person()


			

p1 = Person("Tim")
p2 = Person ("Jill")
		
print(p1.name)
print(Person.number_of_people_())