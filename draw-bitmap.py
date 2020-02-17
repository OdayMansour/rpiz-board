from PIL import Image

_width = 212
_height = 104
scale = 2

img = Image.new( 'RGB', (_width*scale,_height*scale), "black") # Create a new black image

pixels = img.load() # Create the pixel map
for i in range(img.size[0]):    # For every pixel:
    for j in range(img.size[1]):
        pixels[i,j] = (i, j, 100) # Set the colour accordingly

img.show()
