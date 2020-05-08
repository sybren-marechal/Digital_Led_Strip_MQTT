import time
import board
import neopixel


# pixel_pin = board.D18
# num_pixels = 144
# ORDER = neopixel.GRB


class Led:

    def __init__(self, PIXEL_PIN, NUM_PIXELS, BRIGHTNESS):
        self.pixel_pin = PIXEL_PIN
        self.num_pixels = NUM_PIXELS
        self.order = neopixel.RGB
        #self.order = neopixel.RGBW
        self.brightness = BRIGHTNESS
        self.pixels = neopixel.NeoPixel(self.pixel_pin, self.num_pixels, brightness=self.brightness, auto_write=False,
                                        pixel_order=self.order)
                                        
    def set_color(self,r,g,b):
        self.pixels.fill((r, g, b))
        self.pixels.show()
        time.sleep(1)

    def all_on(self):
        self.pixels.fill((255, 255, 255))
        #self.pixels.fill((255, 255, 255, 255))
        self.pixels.show()
        time.sleep(1)

    def all_off(self):
        self.pixels.fill((0, 0, 0))
        #self.pixels.fill((0, 0, 0, 0))
        self.pixels.show()
        time.sleep(1)

    def set_brightness(self,brightness):
        self.pixels.brightness = (brightness/100) 
        self.pixels.show()
        time.sleep(1)

    def wheel(self,pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 0 or pos > 255:
            r = g = b = 0
        elif pos < 85:
            r = int(pos * 3)
            g = int(255 - pos*3)
            b = 0
        elif pos < 170:
            pos -= 85
            r = int(255 - pos*3)
            g = 0
            b = int(pos*3)
        else:
            pos -= 170
            r = 0
            g = int(pos*3)
            b = int(255 - pos*3)
        return (r, g, b)

    def rainbow_cycle(self, wait=0.001):
        for j in range(255):
            for i in range(self.num_pixels):
                pixel_index = (i * 256 // self.num_pixels) + j
                self.pixels[i] = self.wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(wait)

    def set0(self):
        # self.all_off()
        pixel_index = 0
        pixel_jump = 1
        pixel_length = 10
        for i in range(self.num_pixels):
            if -(self.num_pixels - pixel_jump) < pixel_index < (self.num_pixels - pixel_jump):

                pixel_index1 = (-i * pixel_jump)
                pixel_index2 = (i * pixel_jump)
                pixel_index3 = ((-i+pixel_length*2) * pixel_jump)
                pixel_index4 = ((i+pixel_length*2) * pixel_jump)

                pixel_index = pixel_index4 
                # print (pixel_index1)
                # print (pixel_index2)
                # print ("samen", pixel_index2 + pixel_index1)
                self.pixels[int(pixel_index1)] = (255,255,255)
                self.pixels[int(pixel_index2)] = (255,255,255)
                self.pixels[int(pixel_index3)] = (255,255,255)
                self.pixels[int(pixel_index4)] = (255,255,255)
                self.pixels[int(pixel_index1)+pixel_length] = (0,0,0)
                self.pixels[int(pixel_index2)-pixel_length] = (0,0,0)
                self.pixels[int(pixel_index3)+pixel_length] = (0,0,0)
                self.pixels[int(pixel_index4)-pixel_length] = (0,0,0)

                self.pixels.show()
                time.sleep(0.1)
            else:
                i = 0
                
    def set1(self):
        self.all_on()
        time.sleep(0.1)
        self.all_off()

    def set2(self):
        self.all_on()
        time.sleep(0.1)
        self.all_off()

    def set3(self):    
        self.all_on()
        time.sleep(0.1)
        self.all_off()

def main():

    led = Led(board.D18, 100, 1)
    while True:
        led.all_off()
        led.all_on()
        led.set0()
        # # led.pixels.fill((255, 255, 255))
        # led.pixels.fill((255, 0, 0, 0))
        # led.pixels.show()
        # time.sleep(1)
        # led.pixels.fill((0, 255, 0))
        # #led.pixels.fill((0, 255, 0, 0))
        # led.pixels.show()
        # time.sleep(1)
        # # led.pixels.fill((0, 0, 255))
        # #led.pixels.fill((0, 0, 255, 0))
        # led.pixels.show()
        # time.sleep(1)
        # led.rainbow_cycle(0.001)    # rainbow cycle with 1ms delay per step


if __name__ == "__main__":
    main()
