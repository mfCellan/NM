
from PIL import Image


image = Image.open('/Users/rock1/Desktop/Pixel/in.png')
x, y = image.size
k = int(x/4)
n = int(y/5)
i1 = 1
j1 = 1
for i in range(0, x, k):
    for j in range(0, y, n):
        new_image = image.crop((i, j, i+k, j+n))
        new_image.save("/Users/rock1/Desktop/Pixel/out"+str(i1)+str(j1)+".png")
        j1 += 1
    i1 += 1
##new_image = image.crop((0, 0, 20, 20))
#new_image.show()