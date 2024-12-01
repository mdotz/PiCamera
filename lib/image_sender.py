#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append(".")
from PIL import Image, ImageDraw,ImageFont

class ImageSender:
    def __init__(self, image_path, display, image):
        self.image_path = image_path
        self.display = display
        # self.disp = LCD_2inch4.LCD_2inch4()
        # self.disp.Init()
        # self.disp.clear()
        # self.disp.bl_DutyCycle(50)
        logging.basicConfig(level=logging.DEBUG)
        # image1 = Image.new("RGB", (display.width, display.height ), "WHITE")
        # draw = ImageDraw.Draw(image1)

    def call(self):
        #self.disp.clear()
        try:
            # self.disp.Init()
            #self.disp.clear()
            print("open")
            # self.disp.bl_DutyCycle(50)

            # display with hardware SPI:
            ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
            #disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
            # Initialize library.
            # Clear display.
            #Set the backlight to 100

    # Create blank image for drawing.

            # logging.info("show image")
            print("open")
            image = Image.open(self.image_path)
            print("rotate")
            image = image.rotate(0)
            print("show")
            self.display.ShowImage(image)
            #time.sleep(3)
            print("close")
            # image.close()
            # self.disp.module_exit()
            # logging.info("quit:")
        except IOError as e:
            logging.info(e)
        # except KeyboardInterrupt:
            # self.disp.module_exit()
            # logging.info("quit:")
    def close(self):
        self.disp.module_exit()

# ImageSender(sys.argv[1]).call()
