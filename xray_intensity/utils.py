from PIL import Image

def get_average_pixel_value(img: Image) -> float | list[float]:
    '''Takes an image and returns the average pixel value, as float if grayscale, or list of floats if RGB.'''
    assert img.mode in ["L", "RGB"], "Please input an image in grayscale or RGB format"

    if img.mode == "L":
        total = 0
        for x in range(img.width):
            for y in range(img.height):
                total += img.getpixel((x, y))
        
        return total / img.width / img.height
                
    if img.mode == "RGB":
        total = [0, 0, 0]
        for x in range(img.width):
            for y in range(img.height):
                for i in range(3):
                    total[i] += img.getpixel((x, y))[i]
        
        return [i / img.width / img.height for i in total]