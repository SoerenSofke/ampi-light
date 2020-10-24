import adafruit_dotstar as dotstar
import board
import random
import pygame.time
import pygame.camera
import pygame
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.environ["DISPLAY"] = ":0"


DEVICE = '/dev/video0'
SIZE_CAPTURE = (640, 480)
X = 41
Y = 24
SIZE_LED = (X, Y)
pixelArray = ()
MIN_BRIGTHNESS = 8
OFFSET = 2


def isPixekBlack(pixelColorRgb):
    if pixelColorRgb[0] <= MIN_BRIGTHNESS and pixelColorRgb[1] <= MIN_BRIGTHNESS and pixelColorRgb[2] <= MIN_BRIGTHNESS:
        isBlack = True
    else:
        isBlack = False

    return isBlack


def blackLevelCorrection(pixelArray):

    for idx, pixelColorRgb in enumerate(pixelArray):
        if isPixekBlack(pixelColorRgb):
            pixelArray[idx] = (0, 0, 0)

    return pixelArray


def ampilight():
    try:
        pixelArray = dotstar.DotStar(
            board.SCK, board.MOSI, X + 2 * Y, brightness=0.3, auto_write=False, baudrate=20000000)
        pixelArray.fill((0, 0, 0))

        pygame.init()
        pygame.camera.init()
        camera = pygame.camera.Camera(DEVICE, SIZE_CAPTURE)
        screen = pygame.surface.Surface(SIZE_CAPTURE)
        tiny = pygame.surface.Surface((10, 5))
        pixelMatrix = pygame.surface.Surface(SIZE_LED)

        camera.start()
        while True:
            camera.get_image(screen)
            pygame.transform.smoothscale(screen, (10, 5), tiny)
            pygame.transform.smoothscale(tiny, SIZE_LED, pixelMatrix)

            # right panel
            if True:
                idx = 0
                for y in range(Y-1):
                    pixelArray[idx] = pixelMatrix.get_at(
                        (X-1-OFFSET, Y-1-y))[:3]
                    idx += 1

            # top panel
            if True:
                idx = 23
                for x in range(X):
                    pixelArray[idx] = pixelMatrix.get_at((X-1-x, OFFSET))[:3]
                    idx += 1

            # left panel
            if True:
                idx = 64
                for y in range(Y-1):
                    pixelArray[idx] = pixelMatrix.get_at((0+OFFSET, y+1))[:3]
                    idx += 1

            pixelArray = blackLevelCorrection(pixelArray)
            pixelArray.show()

    finally:
        print('stopping ...')
        pixelArray.fill((0, 0, 0))
        camera.stop()
        pygame.quit()
    return


if __name__ == '__main__':
    ampilight()
