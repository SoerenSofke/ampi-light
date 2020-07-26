import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["DISPLAY"] = ":0"

import pygame
import pygame.camera
import pygame.time

import board
import busio

DEVICE = '/dev/video0'
SIZE_CAPTURE = (640, 480)
SIZE_LED = (41, 32)
FILENAME = 'capture.png'
FPS_SHOW = 1

def ampilight():
    try:
        spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
        spi.try_lock()
        spi.configure(baudrate=16000000)
        spi.unlock()        

        pygame.init()
        pygame.time.set_timer(FPS_SHOW, 1000)
        pygame.camera.init()

        camera = pygame.camera.Camera(DEVICE, SIZE_CAPTURE)    
        screen = pygame.surface.Surface(SIZE_CAPTURE)
        screen_ = pygame.surface.Surface(SIZE_LED)
        
        clock = pygame.time.Clock()
        camera.start()    
        while (True):
            clock.tick()
                    
            camera.get_image(screen)
            pygame.transform.smoothscale(screen, SIZE_LED, screen_)

            spi.write(bytes(range(64)))

            for event in pygame.event.get():
                if event.type == FPS_SHOW:            
                    print(clock.get_fps())
                    pygame.image.save(screen_, FILENAME)

    finally:
        print('stopping')
        camera.stop()
        pygame.quit()
    return

if __name__ == '__main__':
    ampilight()
