import argparse, os
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Arguments
def file(string):
  if os.path.isfile(string):
    return string
  else:
    raise argparse.ArgumentTypeError(f"{string} is not a valid file.")

def validpath(string):
  if os.path.isdir(os.path.split(string)[0]):
    return string
  else:
    raise argparse.ArgumentTypeError(f"{string} does not point to an existing directory.")

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bigbang", help="Deocrate icon with Big Bang ornament", action="store_true")
parser.add_argument("-i", "--image", help="Image to decorate", type=file, required=True)
parser.add_argument("-mg", "--graduated", help="Decorate icon with Graudated Maturity ornament.", action="store_true")
parser.add_argument("-mi", "--incubating", help="Decorate icon with Incubating Maturity ornament.", action="store_true")
parser.add_argument("-ms", "--sandbox", help="Decorate icon with Sandbox Maturity ornament.", action="store_true")
parser.add_argument("--show", help="Show image instead of saving to file", action="store_true")
parser.add_argument("-o", "--output", help="Output image (default is ./<image>-decorated.png)", type=validpath)
args = parser.parse_args()

# Constants
BBCOLOR = (96, 100, 188, 255)  # Main color that Big Bang Logo uses
MGCOLOR = (0, 100, 0, 192)     # Maturity graduated color (dark green)
MICOLOR = (255, 191, 0, 192)   # Maturity incubating color (mustard)
MSCOLOR = (255, 64, 0, 192)    # Maturity sandbox color (orange)
MTCOLOR = (255, 255, 255, 255) # Maturity text color (white)
MGTEXT = "Graduated"
MITEXT = "Incubating"
MSTEXT = "Sandbox"
IMGSIZE = 200  # Size of final image (square)
MFONTSIZE = int(IMGSIZE*.17)  # (Maturity) 17 point font for 100 pixel image
MOFFSET = int(IMGSIZE*.15) # (Maturity) Move triangle up/left by 15 points for 100 pixel image
BBORDERSIZE = int(IMGSIZE*.08) # (Big Bang) 8 point border for 100 pixel image
SCALAR = 16 # Amount to oversize temporary images so resampling will not show jagginess.  Should be exponential to 4.

# Final image
imgfinal = Image.new("RGBA", (IMGSIZE,IMGSIZE))

# Base image
imgbase = Image.open(args.image).convert("RGBA")
imgbase.thumbnail((IMGSIZE, IMGSIZE))
imgfinal.paste(imgbase, (int((IMGSIZE - imgbase.width)/2), int((IMGSIZE - imgbase.height)/2)), imgbase) # Centered

# Border
if args.bigbang:
  imgfinal = ImageOps.expand(imgfinal, border=BBORDERSIZE, fill=BBCOLOR)
  imgfinal.thumbnail((IMGSIZE, IMGSIZE))

  # Quarter circle
  # draw = ImageDraw.Draw(imgfinal)
  # draw.ellipse((-30,-30,30,30), fill=BBCOLOR)

  # Triangle flag
  # draw = ImageDraw.Draw(imgfinal)
  # draw.polygon([(0, int(imgbigbang.height - fontsize)), (imgbigbang.width, int(imgbigbang.height - fontsize)), (imgbigbang.width, imgbigbang.height), (0, imgbigbang.height)], fill=BBCOLOR)

# Maturity Banner
maturitytext = ""
if args.graduated:
  maturitytext = MGTEXT
  maturitybgcolor = MGCOLOR
  maturityfgcolor = MTCOLOR
if args.incubating:
  maturitytext = MITEXT
  maturitybgcolor = MICOLOR
  maturityfgcolor = MTCOLOR
if args.sandbox:
  maturitytext = MSTEXT
  maturitybgcolor = MSCOLOR
  maturityfgcolor = MTCOLOR

if maturitytext:
  fontsize = MFONTSIZE*SCALAR
  font = ImageFont.truetype("/mnt/c/Users/MichaelMcLeroy/Downloads/Restore/UbuntuMono-Regular.ttf", fontsize)
  imgmaturitysize = IMGSIZE*SCALAR
  imgmaturity = Image.new("RGBA", (imgmaturitysize, imgmaturitysize))

  # Rotate to expand canvas, draw horizontally, rotate back, crop and scale down
  imgmaturity = imgmaturity.rotate(-45, expand = 1)
  draw = ImageDraw.Draw(imgmaturity)
  draw.rectangle((0,0,imgmaturity.width, int(imgmaturity.height/2 + fontsize/2)), fill = maturitybgcolor)
  draw.text((int((imgmaturity.width - font.getlength(maturitytext))/2), int((imgmaturity.height - fontsize)/2)), maturitytext, font=font, fill = maturityfgcolor)
  imgmaturity = imgmaturity.rotate(45)
  imgmaturity = imgmaturity.crop((int((imgmaturity.width - imgmaturitysize)/2), int((imgmaturity.height - imgmaturitysize)/2), int((imgmaturity.width + imgmaturitysize)/2), int((imgmaturity.height + imgmaturitysize)/2)))
  imgmaturity.thumbnail((IMGSIZE, IMGSIZE))
  imgfinal.paste(imgmaturity, (-MOFFSET, -MOFFSET), imgmaturity) # Offset towards upper left

if args.show:
  # imgfinal.thumbnail((32, 32))
  imgfinal.show()
else:
  if args.output:
    outfile = args.output
  else:
    outfile = './' + os.path.splitext(os.path.basename(args.image))[0] + '-decorated.png'
  imgfinal.save(outfile, format="png")
  print("Decorated file saved to " + outfile)