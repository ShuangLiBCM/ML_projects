# Printing, Printing

formatter = "{} {} {} {}"

print(formatter.format(1,2,3,4))
print(formatter.format("one", "twp", "three", "four"))
print(formatter.format(True, False, False, True))
print(formatter.format(formatter, formatter, formatter, formatter))
print(formatter.format(
    "Try your \n",
    "Own text here \n",
    "Maybe a poem \n",
    "Or a song about fear \n"
))
