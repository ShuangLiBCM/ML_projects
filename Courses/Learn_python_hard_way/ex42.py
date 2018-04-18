# Is A, has A, Objects, and Classes

## Animal is-a object (yes, sort of confusing) look at the extra credit
class Animal(object):
    pass

# Dog is-a class of animal
class Dog(Animal):

    def __init__(self, name):
        ## Dog has-a name attribute
        self.name = name

# Cat is a class of animal
class Cat(Animal):

    def __init__(self, name):
        # Cat has a name attribute
        self.name = name

## Person is a class
class Person(object):

    def __init__(self, name):
        # Person has a name attribute
        self.name = name
        self.pet = None

## Employee is a class of person
class Employee(Person):

    def __init__(self, name, salary):
        # hmm what is this strange magic?
        super(Employee, self).__init__(name)
        self.salary = salary

##
class Fish(object):
    pass

class Salmon(Fish):
    pass

class Halibut(Fish):
    pass

rover = Dog("Rover")

satan = Cat("Satan")

mary = Person("Mary")

mary.pet = satan

frank = Employee("Frank", 120000)

frank.pet = rover

flipper = Fish()

crouse = Salmon()

harry = Halibut()
