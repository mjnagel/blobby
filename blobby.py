import argparse, os
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence

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
parser.add_argument("--cheer", help="Show image of blob cheering instead of normal blob", action="store_true")
parser.add_argument("-o", "--output", help="Output image (default is ./blob-<image>.png or ./old-man-yells-at-<image>.png)", type=validpath)
args = parser.parse_args()

# Constants
IMGSIZE = 170  # Size of final image (square)
YELL_IMGSIZE = 128  # Size of final image (square)
CHEER_IMGSIZE = 170  # Size of final image (square)
SCALAR = 16 # Amount to oversize temporary images so resampling will not show jagginess.  Should be exponential to 4.
SCRIPT_DIR = os.path.dirname(__file__)
BLOB_FILE = f"{SCRIPT_DIR}/icons/blob.png"
YELL_FILE = f"{SCRIPT_DIR}/icons/old-man-yells-at.png"
CHEER_FILE = f"{SCRIPT_DIR}/icons/blob-cheer.gif"
LOGO_SIZE = (78,78)
YELL_LOGO_SIZE = (50,50)
CHEER_LOGO_SIZE = (60,60)
FILE_BASE = 'blob-'
YELL_FILE_BASE = 'old-man-yells-at-'
CHEER_FILE_BASE = 'blob-cheer-'

if args.yell:
  IMGSIZE = YELL_IMGSIZE
  BLOB_FILE = YELL_FILE
  LOGO_SIZE = YELL_LOGO_SIZE
  FILE_BASE= YELL_FILE_BASE

if args.cheer:
    IMGSIZE = CHEER_IMGSIZE
    BLOB_FILE = CHEER_FILE
    LOGO_SIZE = CHEER_LOGO_SIZE
    FILE_BASE= CHEER_FILE_BASE

def process_frame(frame, logo, IMGSIZE, LOGO_SIZE): # Process individual gif frames
    frame = frame.convert("RGBA")
    frame.thumbnail((IMGSIZE, IMGSIZE))
    imgfinal = Image.new("RGBA", (IMGSIZE, IMGSIZE))
    imgfinal.paste(frame, (int((IMGSIZE - frame.width) / 2), int((IMGSIZE - frame.height) / 2)), frame)  # Centered
    logo.thumbnail(LOGO_SIZE)
    imgfinal.paste(logo, (0, 0), logo)  # Top left corner aligned
    return imgfinal


logo = Image.open(args.image).convert("RGBA")
if args.cheer: # Gif processing
    img = Image.open(BLOB_FILE)
    frames = []
    durations = []
    for frame in ImageSequence.Iterator(img):
        durations.append(frame.info.get('duration', 100))  # Get frame duration
        frames.append(process_frame(frame, logo, IMGSIZE, LOGO_SIZE)) # Adds image to individual frame and appends
    
    if args.show:
        frames[0].show()
    else:
        if args.output:
            outfile = args.output
        else:
            outfile = './' + FILE_BASE + os.path.splitext(os.path.basename(args.image))[0] + '.gif'
        frames[0].save(outfile, save_all=True, append_images=frames[1:], loop=0, duration=durations, disposal=2)
        print("Blobified logo saved to " + outfile)
else: # PNG processing
    imgfinal = Image.new("RGBA", (IMGSIZE, IMGSIZE))
    imgbase = Image.open(BLOB_FILE).convert("RGBA")
    imgbase.thumbnail((IMGSIZE, IMGSIZE))
    imgfinal.paste(imgbase, (int((IMGSIZE - imgbase.width) / 2), int((IMGSIZE - imgbase.height) / 2)), imgbase)  # Centered

    # Add Logo
    logo.thumbnail(LOGO_SIZE)
    imgfinal.paste(logo, (0, 0), logo)  # Top left corner aligned
    
    if args.show:
        imgfinal.show()
    else:
        if args.output:
            outfile = args.output
        else:
            outfile = './' + FILE_BASE + os.path.splitext(os.path.basename(args.image))[0] + '.png'
        imgfinal.save(outfile, format="png")
        print("Blobified logo saved to " + outfile)