# -*- coding: utf-8 -*-

import operator
import argparse
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
  tempColor = ""
  for x in rgb:
    rgbArr.append(int(x/85))
  sumColor = rgbArr[0] + rgbArr[1] + rgbArr[2]
  
  for colorInt in rgbArr:
    if(colorInt == 2):
      prefix = "dark_"
    if(colorInt == 3):
      prefix = ""
  red = rgbArr[0]
  green = rgbArr[1]
  blue = rgbArr[2]
  
  color = ""

  if red:
    if green:
      color= "gray"
    else:
      if blue:
        color= "purple"
      else:
        color = "red"
  else:
    if green and blue:
      color = "aqua"
    else:
      if blue:
        color = "blue"
      if green:
        color = "green"
  
  tempColor = color
  color = prefix + tempColor
  
  if sumColor == 0:
    color = "black"
  if sumColor == 7:
    color = "white"
    
  return color
    
def gif2txt(filename, maxLen=18, maxColumns=14, author='DavidTheNewKid', title = "Animated Book" ,output_file='output.txt', with_color=False,
        green_screen_sensibility=None, reverse_green_screen=False):
    try:
        maxLen = int(maxLen)
    except:
        maxLen = 18
    try:
        maxColumns = int(maxHeight)
    except:
        maxColumns = 14

    chs = "MNHQ$OC?7>!:-;. "

    try:
        size = (18, 14)
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

    palette = img.getpalette()
    '''
    written_book{pages:["{\"text\":\"Minecraft Tools book\\ntest\"}","{\"text\":\"test\"}"],title:Book,author:"AUTHOR_NAME"}
    '''
    
    book = []
    commandStr = "/give @p "
    pagesStr = "pages:["
    textStr = "\"{\\\"text\\\":\\\""
    updateColorTextStr = "{\\\"text\\\":\\\""
    bookStr = "minecraft:written_book{"
    authorString = ("author:\"" + author + "\"")
    titleStr = ("title:\"" + title + "\"")
    lastColor = ""
    firstRun = 1
    updateColor = 0
    colorText = ""
    
    try:
        while 1:
            img.putpalette(palette)
            im = Image.new('RGB', img.size)
            im.paste(img)
            im = im.resize((width, height))
            currpage = textStr
            ''' book json format: "{\"text\":\"Minecraft Tools book\\ntest\"}" '''
            for h in range(height):
                for w in range(width):
                    rgb = im.getpixel((w, h))
                    if firstRun:
                      lastColor = minecraft_color_converter(rgb)
                      colorText = "\\\",\\\"color\\\":\\\"" + lastColor + "\\\"}"
                    if _green_screen_check(rgb,
                                           green_screen_sensibility,
                                           reverse_green_screen):
                        rgb = (0, 255, 0)
                    if with_color:
                        '''Colors: ["[\"\",{\"text\":\"M\",\"color\":\"dark_red\"},{\"text\":\"inecraft Tools book\",\"color\":\"reset\"}]"]'''
                        currpage += chs[int(sum(rgb) / 3.0 / 256.0 * 16)]
                        if(firstRun):
                          colorText = "\\\",\\\"color\\\":\\\"" + lastColor + "\\\"}"
                        else:
                          newColor = minecraft_color_converter(rgb)
                          if(newColor != lastColor):
                            currpage += colorText + "," + updateColorTextStr
                            lastColor = newColor
                            print(lastColor)
                        firstRun = 0
                    else:
                        currpage += chs[int(sum(rgb) / 3.0 / 256.0 * 16)]
                if(h < 13):
									currpage = currpage + "\\\\n"
            if(with_color):
              currpage += colorText
            currpage += "\\\"}\""
            book.append(currpage)
            img.seek(img.tell() + 1)
            firstRun = 0
            
    except EOFError:
        pass
		
    ''' pages:["{\"text\":\"Minecraft Tools book\\ntest\"}","{\"text\":\"test\"}"] '''
    print(book[0])
    pagecounter = 1
    for page in book:
      if(pagecounter == 1):
        pagesStr += page
      else:
        pagesStr += ","
        pagesStr += page
      pagecounter = 2
    pagesStr += "]"
    
    bookStr += (pagesStr+","+titleStr+","+authorString + "}")
    
    commandStr += bookStr
    
    print(output_file)
    file = open(output_file,"w")
    file.write(commandStr)
    file.close()
    

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename', help='Gif input file')
    parser.add_argument('-l', '--maxLen', type=int, help='Max width of the output gif')
    parser.add_argument('-c', '--maxColumns', type=int, help='Max height of the output gif')
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
    args = parser.parse_args()

    if not args.maxLen:
        args.maxLen = 18
    if not args.maxColumns:
		    args.maxColumns = 14
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

    gif2txt(
        filename=args.filename,
        maxLen=args.maxLen,
        maxColumns = args.maxColumns,
        author = args.author,
        title = args.title,
        output_file=args.output,
        with_color=args.color,
        green_screen_sensibility=args.green_screen_sensibility,
        reverse_green_screen=args.reverse_green_screen,
    )

if __name__ == '__main__':
    main()
