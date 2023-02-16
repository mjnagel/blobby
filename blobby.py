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
parser.add_argument("-i", "--image", help="Image to decorate", type=file, required=True)
parser.add_argument("--show", help="Show image instead of saving to file", action="store_true")
parser.add_argument("--yell", help="Make old man yelling at X emoji instead of blob", action="store_true")
parser.add_argument("-o", "--output", help="Output image (default is ./blob-<image>.png)", type=validpath)
args = parser.parse_args()

# Constants
IMGSIZE = 170  # Size of final image (square)
YELL_IMGSIZE = 128  # Size of final image (square)
SCALAR = 16 # Amount to oversize temporary images so resampling will not show jagginess.  Should be exponential to 4.
SCRIPT_DIR = os.path.dirname(__file__)
BLOB_FILE = f"{SCRIPT_DIR}/icons/blob.png"
YELL_FILE = f"{SCRIPT_DIR}/icons/old-man-yells-at.png"
LOGO_SIZE = (78,78)
YELL_LOGO_SIZE = (50,50)

if args.yell:
  IMGSIZE = YELL_IMGSIZE
  BLOB_FILE = YELL_FILE
  LOGO_SIZE = YELL_LOGO_SIZE

imgfinal = Image.new("RGBA", (IMGSIZE,IMGSIZE))
imgbase = Image.open(BLOB_FILE).convert("RGBA")
imgbase.thumbnail((IMGSIZE, IMGSIZE))
imgfinal.paste(imgbase, (int((IMGSIZE - imgbase.width)/2), int((IMGSIZE - imgbase.height)/2)), imgbase) # Centered

# Add logo
logo = Image.open(args.image).convert("RGBA")
logo.thumbnail(LOGO_SIZE)
imgfinal.paste(logo) # Top left corner aligned

if args.show:
  # imgfinal.thumbnail((32, 32))
  imgfinal.show()
else:
  if args.output:
    outfile = args.output
  else:
    outfile = './' + 'blob-' + os.path.splitext(os.path.basename(args.image))[0] + '.png'
  imgfinal.save(outfile, format="png")
  print("Blobified logo saved to " + outfile)