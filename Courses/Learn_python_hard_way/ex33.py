# While loops

def list_cre(comp):
    numbers = []
    i=0
    while i<int(comp):
        print(f"At the top i is {i}")
        numbers.append(i)

        i = i + 1

    print("Numbers now:", numbers)
    print(f"At the bottom i is {i}")

    return numbers


test_num = input("Pleas enter length of the list: ")
numbers = list_cre(test_num)
print("The numbers:")
for num in numbers:
    print(num)
