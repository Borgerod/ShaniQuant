
#STATIC METHODS	- unchangeable methods
# 
# 		Static not changing, all they do is do_somthing and thats it.
#       (they dont have acsess to anything and cant change anything)
#		Creating a class that organize functions together


class Math:
	
	@staticmethod
	def add5(x):
		return x + 5	
	@staticmethod
	def add5p(x):
		return print(x + 5)
	@staticmethod
	def add10(x):
		return x + 10
	@staticmethod
	def pr():
		print("run")

# print(Math.add5(5))
Math.add5p(2)
# Math.pr()