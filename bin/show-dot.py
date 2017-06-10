#!/usr/bin/env python3

import subprocess
import argparse
import pathlib
import os
import sys
import tempfile

def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('file', type=argparse.FileType('r'))
  args = parser.parse_args()

  print(sys.version)
  args.file.close()

  svgfile = tempfile.NamedTemporaryFile(suffix='.svg')
  print(svgfile.name)

  dot_cmd = ["dot", "-Tsvg", args.file.name]
  svg = subprocess.run(dot_cmd, stdout=svgfile)
  svg_uri = pathlib.Path(svgfile.name).as_uri()
  #eog_cmd = ["eog", svgfile.name]
  eog_cmd = ["epiphany", svg_uri]
  subprocess.call(eog_cmd)
  input("Press Enter to continue...")

if __name__ == '__main__':
  main(sys.argv)


