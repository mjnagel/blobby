# Blobby (the blobifier)

Simple python script to make a blob from a given product/company logo (or anything else)

## Prerequisites

- Python 3
- Pip

## Quick start

```shell
# Install required modules
pip install -r requirements.txt

# Run script
python3 blobby.py -i icons/keycloak.png

# View keycloak-decorated.png
```

## Options

```shell
usage: blobby.py [-h] [-b] -i IMAGE [--show] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -i IMAGE, --image IMAGE
                        Image to blobify
  --show                Show image instead of saving to file
  -o OUTPUT, --output OUTPUT
                        Output image (default is ./<image>-blob.png)
```

## Icons

The icons folder stores the base blob (170x170) plus an example logo (keycloak.png).

When using a new company/product logo you should keep these considerations in mind:
- Transparent backgrounds will offer the best results (https://www.remove.bg/ is an easy way to make this happen)
- High quality is good, but the image will be resized to 72x72 to fit in with the blob template properly
- If your logo is a strange shape it may not work well with the resizing (might turn out really small), you can adjust the `LOGO_SIZE` parameter
