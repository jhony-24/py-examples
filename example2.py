import subprocess
from PIL import Image, ImageFont, ImageDraw
import requests
import termcolor

subprocess.call("",shell=True)

def averageColour(image):
  mainColors = [None, None, None]
  for channel in range(3):
      pixels = image.getdata(band=channel)
      values = []
      for pixel in pixels:
          values.append(pixel)
      mainColors[channel] = sum(values) / len(values)
  colours = ( int(mainColors[0]), int(mainColors[1]), int(mainColors[2]) )     
  return colours

def parseParagraphInMultilines(paragraph : str):
  maxInLine = 8
  words = paragraph.split(" ")
  counterInLine = 1
  newParagraph = ""
  for index, word in enumerate(words): 
    temporalParagraph = ""
    if(index < (maxInLine * counterInLine)):
        temporalParagraph += f" {word}"
    else:
        counterInLine += 1
        temporalParagraph += "\n"
    newParagraph += temporalParagraph
  return newParagraph


try:
    imageUrl = input(termcolor.colored("Ingresa una url de una imagen: ","yellow"))
    imageNameUrl = input(termcolor.colored("Ingresa una descripción para la imagen: ","yellow"))
        
    originalImage = Image.open(requests.get(imageUrl,stream=True).raw)

    averageColorInImage = averageColour(originalImage)
    red = averageColorInImage[0]
    green = averageColorInImage[1]
    blue = averageColorInImage[2]

    newImageSize = (500,500) 
    newImage = originalImage.resize(newImageSize)
    font = ImageFont.truetype("arial.ttf",size=16)
    textImage = ImageDraw.Draw(newImage)

    draw = ImageDraw.Draw(newImage,"RGBA")
    drawWidth = 40
    draw.line((0,0,newImage.width,0),width=drawWidth,fill=averageColorInImage)
    draw.line((0,newImage.height,newImage.width,newImage.height),width=drawWidth,fill=averageColorInImage)
    draw.line((0,0,0,newImage.height),width=drawWidth,fill=averageColorInImage)
    draw.line((newImage.width,0,newImage.width,newImage.height),width=drawWidth,fill=averageColorInImage)
    draw.rectangle(
        (
        drawWidth / 2,
        (newImage.height / 2) + (drawWidth*2), 
        newImage.width - (drawWidth / 2), 
        newImage.height - (drawWidth / 2)
        ),
        fill=(red,green,blue,red)
    )
    textImage.multiline_text(
        (
        drawWidth,
        (newImage.height / 2) + (drawWidth*3)
        ), 
        parseParagraphInMultilines(imageNameUrl), 
        font=font,
        fill=(255,255,255)
    )

    newImage.show()
    newImage.save("imagen.jpg")

except:
    print(termcolor.colored("Ocurrió un error","red"))
