# Inheritance versus Composition

# # Implicit Inheritance
#
# class Parent(object):
#
#     def implicit(self):
#         print("PARENT implicit()")
#
# class Child(Parent):
#     pass
#
# dad = Parent()
# son = Child()
#
# dad.implicit()
# son.implicit()

# Override explicitly
#
# class Parent(object):
#
#     def override(self):
#         print("PARENT override()")
#
# class Child(Parent):
#
#     def override(self):
#         print("CHILD override()")
#
# dad = Parent()
# son = Child()
#
# dad.override()
# son.override()

# Alter before or After
#
# class Parent(object):
#
#     def altered(self):
#         print("PARENT altered()")
#
# class Child(Parent):
#
#     def altered(self):
#         print("CHILD, BEFORE PARENT altered()")
#         super(Child, self).altered()
#         print("CHILD AFTER PARENT altered()")
#
# dad = Parent()
# son = Child()
#
# dad.altered()
# son.altered()

# All three combined
#
# class Parent(object):
#
#     def __init__(self):
#         print("Parent initialization()")
#
#     def override(self):
#         print("PARENT override()")
#
#     def implicit(self):
#         print("PARENT implicit()")
#
#     def altered(self):
#         print("PARENT altered()")
#
#
# class Child(Parent):
#
#     def __init__(self):
#         super(Child, self).__init__()   # Make sure that the child init won't override parent init
#         print("Child initialization")
#     #
#     # def override(self):
#     #     print("CHILD overried()")
#
#     def altered(self):
#         print("CHILD, BEFORE PARENT altered()")
#         super(Child, self).altered()
#         print("CHILD, AFTER PARAENT altered()")
#
# dad = Parent()
# son = Child()
#
# # dad.implicit()
# # son.implicit()
# #
# dad.override()
# son.override()
# #
# # dad.altered()
# # son.altered()

# Composition

class Other(object):

    def override(self):
        print("OTHER override()")

    def implicit(self):
        print("OTHER implicit()")

    def altered(self):
        print("OTHER altered()")

class Child(object):

    def __init__(self):
        self.other = Other()

    def implicit(self):
        self.other.implicit()

    def override(self):
        print("CHILD override()")

    def altered(self):
        print("CHILD, BEFORE OTHER altered")
        self.other.altered()
        print("CHILD, after other altered")

son = Child()

son.implicit()
son.override()
son.altered()
