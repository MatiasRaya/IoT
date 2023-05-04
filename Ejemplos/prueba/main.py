import math

lat = -31.436
long = -64.19352

aux = math.sqrt(math.pow(lat,2)+math.pow(long,2))
x = long/aux
y = lat/aux

print(x,y)
print("-----------------")
print(math.cos(x/aux))
print("-----------------")
x = x * (-1)
print(math.cos(x/aux))