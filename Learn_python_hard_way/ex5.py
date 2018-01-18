# Put variable into string

my_name = 'Zed A. Shaw'
my_age = 35  # not a lie
my_height = 74 # inches
my_weight = 180 # lbs
my_eyes = 'Blue'
my_teeth = 'White'
my_hair = 'Brown'

print(f"Let's talk about {my_name}.")
print(f"He's {my_height} inches tall.")
print(f"He's {my_weight} pounds heavy.")
print("Actually that's not too heavy.")
print(f"He's got {my_eyes} eyes and {my_hair} hair.")
print(f"His teeth are usually {my_teeth} depending on the coffee.")

# This line is tricky, try to get it exactly right

total = my_age + my_height + my_weight
print(f"If I add {my_age}, {my_weight}, and {my_weight} I get {total}.")

def inch_to_cm(inch_num):
    return inch_num * 2.54

def pd_to_kg(pd_num):
    return pd_num * 0.4536

height = inch_to_cm(my_height)
weight = pd_to_kg(my_weight)

print(f"Let's talk about {my_name}.")
print(f"He's {height} centimeters tall.")
print(f"He's {weight} kg heavy.")
print("Actually that's not too heavy.")
print(f"He's got {my_eyes} eyes and {my_hair} hair.")
print(f"His teeth are usually {my_teeth} depending on the coffee.")
