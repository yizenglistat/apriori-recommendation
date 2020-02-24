import random

print("Hello World!")

a = 10
b = 3
print("a is %d" % a)
print("b is %d" % b)
print("a*b is %d" % (a*b))

print("Random list: ")
rand_list = []
for x in range(10):
       rand_list.append(random.randint(1,100))
print(rand_list)
print("List sorted: ")
print(sorted(rand_list))

