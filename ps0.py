import math

#get values of x and y from command line and store as float
x = float(input("Enter number x"))
y = float(input("Enter number y"))

#print value of x raised to y power
power = x**y
print("x**y = ", power)

#calculate log of x with math module
log = math.log(x,2)
print("log base 2 of x = ",log)

