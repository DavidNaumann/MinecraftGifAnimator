gif2minecraft
=======

Made by: DavidTheNewKid


GIF image to minecraft book for animation in 1.14


USAGE
-----

```
usage: gif2minecraft.py [-h] [-l MAXLEN] [-c MAXCOLUMNS] [-a AUTHOR] [-t TITLE]
                  [-o OUTPUT] [-r] [-s GREEN_SCREEN_SENSIBILITY] [-u]
                  filename

positional arguments:
  filename              Gif input file

optional arguments:
  -h, --help            show this help message and exit
  -l MAXLEN, --maxLen MAXLEN
                        Max width of the output gif (maxed at 18 characters)
  -c MAXCOLUMNS, --maxColumns MAXCOLUMNS
                        Max height of the output gif (maxed at 14 colums)
  -a AUTHOR, --author AUTHOR
                        Name of the author
  -t TITLE, --title TITLE
                        Title of the book
  -o OUTPUT, --output OUTPUT
                        Name of the output file
  -r, --color           With color (ONLY FOR USE FOR VERY SMALL GIFS AND NORMAL PHOTOS)
  -s GREEN_SCREEN_SENSIBILITY, --green-screen-sensibility GREEN_SCREEN_SENSIBILITY
                        convert black and grey into green, sensibility between
                        1 and 255, suggested 128
  -u, --reverse-green-screen
                        white (instead of black) is converted into green, you
                        can still use -g option to set sensibility

  ex:
    python gif2minecraft.py sample.gif -l 5 -c 10 -a DavidTheNewKid -t Nameofmybook -o sample.txt (takes the sample gif down to 5x10, sets author and title then outputs at sample.txt)
    
    Defaultly: the output will be output.txt and this is where you will go to pick up the command for MC
```

Requirements
-----------

* Jinja2
* Pillow

```
pip install -r requirements.txt
```

-----------

Original gif2text idea/code by: hit9 on Github
See also [gif2txt](https://github.com/hit9/gif2txt).
