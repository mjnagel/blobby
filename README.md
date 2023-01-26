# Icon Decorator

Simple python script to decorate an icon with maturity level and/or border

## Prerequisites

- Python 3
- Pip

## Quick start

```shell
cd scripts

# Install required modules
pip install -r requirements.txt

# Run script
python3 decorator.py -i icons/keycloak.png -mg -b

# View keycloak-decorated.png
```

## Options

```shell
usage: decorator.py [-h] [-b] -i IMAGE [-mg] [-mi] [-ms] [--show] [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  -b, --bigbang         Deocrate icon with Big Bang ornament
  -i IMAGE, --image IMAGE
                        Image to decorate
  -mg, --graduated      Decorate icon with Graudated Maturity ornament.
  -mi, --incubating     Decorate icon with Incubating Maturity ornament.
  -ms, --sandbox        Decorate icon with Sandbox Maturity ornament.
  --show                Show image instead of saving to file
  -o OUTPUT, --output OUTPUT
                        Output image (default is ./<image>-decorated.png)
```

## Icons

Icons are the base images that will be decorated by the script.  They are kept in the `icons` directory to make it easier to update when changes are needed.  The icons should be in the following format:

- Square (or as close as possible)
- Larger than 100px by 100px
- (Optional) Transparent background
- Named after the application or company it represents, using kebab-case

## Fonts

All fonts used by the script are stored in the `fonts` directory.  Big Bang uses the Ubuntu Mono font.