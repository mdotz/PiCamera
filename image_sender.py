#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import chardet
import os
import sys 
import time
import logging
import spidev as SPI
sys.path.append(".")
from lib import LCD_2inch4
from PIL import Image,ImageDraw,ImageFont

class ImageSender:
    def __init__(self, image_path):
        self.image_path = image_path

    def call(self):
        logging.basicConfig(level=logging.DEBUG)
        try:
            # display with hardware SPI:
            ''' Warning!!!Don't  creation of multiple displayer objects!!! '''
            #disp = LCD_2inch4.LCD_2inch4(spi=SPI.SpiDev(bus, device),spi_freq=10000000,rst=RST,dc=DC,bl=BL)
            disp = LCD_2inch4.LCD_2inch4()
            # Initialize library.
            disp.Init()
            # Clear display.
            disp.clear()
            #Set the backlight to 100
            disp.bl_DutyCycle(50)

    # Create blank image for drawing.
            image1 = Image.new("RGB", (disp.width, disp.height ), "WHITE")
            draw = ImageDraw.Draw(image1)

            logging.info("show image")
            image = Image.open(self.image_path)
            image = image.rotate(0)
            disp.ShowImage(image)
            #time.sleep(3)
            disp.module_exit()
            logging.info("quit:")
        except IOError as e:
            logging.info(e)    
        except KeyboardInterrupt:
            disp.module_exit()
            logging.info("quit:")

ImageSender(sys.argv[1]).call()
