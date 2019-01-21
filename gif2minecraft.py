# -*- coding: utf-8 -*-

import operator
import argparse
import math
from PIL import Image
from jinja2 import Template

def _green_screen_check(rgb, sensibility, reverse=False):
    """Checks if this pixel needs to be green"""
    if sensibility is None:
        return False
    op = operator.gt if reverse else operator.le
    for x in rgb:
        if not op(x, sensibility):
            return False
    return True

def minecraft_color_converter(rgb):
  rgbArr = []
  colorStr = "black"
  prefix = ""
  prefixInt = 0
  tempColor = ""
  for x in rgb:
    rgbArr.append(int(math.ceil(x/85)))
  sumColor = rgbArr[0] + rgbArr[1] + rgbArr[2]
  
  for colorInt in rgbArr:
    if(colorInt):
      prefixInt += 1
  if(prefixInt >= 2):
    prefix = ""
  else:
    prefix = "dark_"
  red = rgbArr[0]
  green = rgbArr[1]
  blue = rgbArr[2]
  
  color = ""
  
  

  if red:
    color = "red"
    if blue:
      if(red == 3 or blue == 3):
        color = "light_purple"
      else:
        color = "dark_purple"
    if green:
      if (green < red):
        color = "gold"
      else:
        if (green == 3 or red == 3):
          color = "yellow"
        else:
          if(green == red):
            if(green == 2 or red == 2):
              color = "dark_gray"
            else:
              color = "gray"
          else:
            color = "gold"
  
  if green:
    color = "green"
    if red:
      if (green < red):
        color = "gold"
      else:
        if (green == 3 or red == 3):
          color = "yellow"
        else:
          if(green == red):
            if(green == 2 or red == 2):
              color = "dark_gray"
            else:
              color = "gray"
          else:
            color = "gold"
    if blue:
      color = "aqua"
    
  if blue:
    color = "blue"
    if green:
      color = "aqua"
    if blue:
      if(red == 3 or blue == 3):
        color = "light_purple"
      else:
        if(blue > red):
          color = "blue"
        else:
          color = "dark purple"
        
  if (red == 0 and green == 0 and blue == 0):
    color = "black"
  
  if (red and green and blue):
    if (red == green and green == blue):
      if(red == 3 or green == 3 or blue == 3):
        color = "white"
      else:
        if(red == 2 or green == 2 or blue == 2):
          color = "gray"
        else:
          if(red == 1 or green == 1 or blue == 1):
            color = "dark_gray"
        
  if (not (color == "yellow" or color == "gold" or color == "light_purple" or color == "dark_purple" or color == "dark_gray" or color == "gray" or color == "black")):
    tempColor = prefix + color
    color = tempColor
  print(color)
  return color
    
def gif2minecraft(filename, maxLen=19, maxColumns=15, author='DavidTheNewKid', title = "Animated Book" ,output_file='output.txt', with_color=False,
        green_screen_sensibility=None, reverse_green_screen=False, remove_black_background = False):
    if with_color:
      try:
         maxLen = int(maxLen)
         if(maxLen > 12):
           maxLen = 12
      except:
          maxLen = 12
    else:
      try:
         maxLen = int(maxLen)
      except:
          maxLen = 19
    try:
        maxColumns = int(maxHeight)
    except:
        maxColumns = 15

    chs = "MNHQ$OC?7>!:-;. "

    try:
        img = Image.open(filename)
        if filename.find(".gif") == -1:
          rgb_im = img.convert('RGB')
          rgb_im.save("photoConvert.gif")
          filename = "photoConvert.gif"
          img = Image.open(filename)
    except IOError:
        exit("file not found: {}".format(filename))

    width, height = img.size
    rateHeight = float(maxColumns) / height
    rateWidth = float(maxLen) / width
    width = int(rateWidth * width)
    height = int(rateHeight * height)
    
    print(width)
    print(height)

    palette = img.getpalette()
    '''
    written_book{pages:["{\"text\":\"Minecraft Tools book\\ntest\"}","{\"text\":\"test\"}"],title:Book,author:"AUTHOR_NAME"}
    '''
    
    book = []
    commandStr = "/give @p "
    pagesStr = "pages:["
    pagesColorStr = "pages:[\"[\\\"\\\","
    beginColorStr = "\"[\\\"\\\","
    textStr = "\"{\\\"text\\\":\\\""
    updateColorTextStr = "{\\\"text\\\":\\\""
    bookStr = "minecraft:written_book{"
    authorString = ("author:\"" + author + "\"")
    titleStr = ("title:\"" + title + "\"")
    lastColor = ""
    firstRun = 1
    updateColor = 0
    colorText = ""
    utfencode = ""
    
    try:
        while 1:
            firstRun = 1
            img.putpalette(palette)
            im = Image.new('RGB', img.size)
            im.paste(img)
            im = im.resize((width, height))
            if with_color:
              currpage = updateColorTextStr
            else:
              currpage = textStr
            ''' book json format: "{\"text\":\"Minecraft Tools book\\ntest\"}" '''
            for h in range(height):
                for w in range(width):
                    rgb = im.getpixel((w, h))
                    if firstRun:
                      lastColor = minecraft_color_converter(rgb)
                      colorText = "\\\",\\\"color\\\":\\\"" + lastColor + "\\\"}"
                    
                    newColor = minecraft_color_converter(rgb)
                    if _green_screen_check(rgb,
                                           green_screen_sensibility,
                                           reverse_green_screen):
                        rgb = (0, 255, 0)
                    if with_color:
                        '''Colors: ["[\"\",{\"text\":\"M\",\"color\":\"dark_red\"},{\"text\":\"inecraft Tools book\",\"color\":\"reset\"}]"]'''
                        utfencode = "▇"
                        if isinstance(utfencode, bytes):
                          utfencode = utfencode.decode('utf-8')
                        currpage += utfencode
                        if(firstRun):
                          colorText = "\\\",\\\"color\\\":\\\"" + lastColor + "\\\"}"
                        else:
                          if(newColor != lastColor):
                            colorText = "\\\",\\\"color\\\":\\\"" + lastColor + "\\\"}"
                            currpage += colorText + "," + updateColorTextStr
                            lastColor = newColor
                    else:
                        utfencode = chs[int(sum(rgb) / 3.0 / 256.0 * 16)]
                        if remove_black_background:
                          if int(sum(rgb)) == 0:
                            utfencode = " "
                        if isinstance(utfencode, bytes):
                          utfencode = utfencode.decode('utf8')
                        currpage += utfencode
                firstRun = 0
                if h < maxLen:
                  currpage += "\\\\n"
            if with_color:
              currpage += colorText
            if not with_color:
              currpage += "\\\"}\""
            book.append(currpage)
            img.seek(img.tell() + 1)
            firstRun = 0
            
    except EOFError:
        pass
		
    ''' pages:["{\"text\":\"Minecraft Tools book\\ntest\"}","{\"text\":\"test\"}"] '''
    pagecounter = 1
    for page in book:
      if with_color:
        if(pagecounter == 1):
          pagesColorStr += page
          pagesColorStr += "]\""
        else:
          pagesColorStr += ","
          pagesColorStr += beginColorStr
          pagesColorStr += page
          pagesColorStr += "]\""
      else:
        if(pagecounter == 1):
          pagesStr += page
        else:
          pagesStr += ","
          pagesStr += page
      pagecounter = 2
    if with_color:
      pagesStr = pagesColorStr
      pagesStr += "]"
    else:
      pagesStr += "]"
    
    bookStr += (pagesStr+","+titleStr+","+authorString + "}")
    
    commandStr += bookStr
    
    if(len(commandStr) > 32500):
      print("Try to disable color mode if you have it enabled")
      exit("Expected Error: The command/gif is to long to fit into the command block (32500 char limit)")
    else:
      file = open(output_file,"w")
      if not isinstance(commandStr, str):
        commandStr = commandStr.encode('utf-8')
      file.write(commandStr)
      file.close()
    

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename', help='Gif input file')
    parser.add_argument('-l', '--maxLen', type=int, help='Max width of the output gif')
    parser.add_argument('-c', '--maxColumns', type=int, help='Max height of the output gif (12 if color is on)')
    parser.add_argument('-a', '--author', 
                        help= 'Name of the author')
    parser.add_argument('-t', '--title',
                          help='Title of the book')
    parser.add_argument('-o', '--output',
                        help='Name of the output file')
    parser.add_argument('-r', '--color', action='store_true',
                        default=False,
                        help='With color')
    parser.add_argument('-s', '--green-screen-sensibility',
                        type=int, default=None,
                        help='convert black and grey into green, '
                             'sensibility between 1 and 255, suggested 128')
    parser.add_argument('-u', '--reverse-green-screen',
                        action='store_true', default=False,
                        help='white (instead of black) is converted into '
                             'green, you can still use -g option to set sensibility')
    parser.add_argument('-b', '--remove_black_background',
                       action='store_true', default=False,
                       help='removes blackbackgrounds from gifs (or tries to at least)')
    args = parser.parse_args()

    if not args.maxLen:
        args.maxLen = 19
    if not args.maxColumns:
		    args.maxColumns = 15
    if not args.author:
        args.author = "DavidTheNewKid"
    if not args.title:
        args.title = "Animated Book"
    if not args.output:
        args.output = 'output.txt'
    if args.reverse_green_screen and not args.green_screen_sensibility:
        args.green_screen_sensibility = 128
    if args.green_screen_sensibility:
        args.color = True

    gif2minecraft(
        filename=args.filename,
        maxLen=args.maxLen,
        maxColumns = args.maxColumns,
        author = args.author,
        title = args.title,
        output_file=args.output,
        with_color=args.color,
        green_screen_sensibility=args.green_screen_sensibility,
        reverse_green_screen=args.reverse_green_screen,
        remove_black_background=args.remove_black_background
    )

if __name__ == '__main__':
    main()
