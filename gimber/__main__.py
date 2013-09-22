import argparse
import sys


parser = argparse.ArgumentParser()
parser.description = """
Run gimber.py in the selected mode
"""

parser.add_argument("mode", help="Running mode of gimber",
                    choices=["tilesgen", "interactive", "webserver"])

conf = parser.parse_args(sys.argv[1:2])
argv = sys.argv[2:]

if conf.mode == "tilesgen":
    import tilesgen
    tilesgen.run(argv)

elif conf.mode == "webserver":
    import webserver
    webserver.run(argv)

elif conf.mode == "interactive":
    import interactive
    interactive.run(argv)