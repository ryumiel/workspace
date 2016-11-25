import argparse
import itertools
import json
import os
import os.path
import sys

class ConfigHelper:

  def write_config_to_file(self):
    with open(self.config_file, 'w') as configFile:
      print "writing to config file"
      json.dump(self.config, configFile, sort_keys=True, indent=4, separators=(',', ': '))

  def get_webkit_dir(self, options):
    if options.debug:
      name = 'Debug'
    elif not options.debug:
      name = 'Release'

    if options.use_gles:
      name = name + 'GLES'
    if options.disable_threaded_compositor:
      name = name + 'NoTC'
    if options.disable_gstgl:
      name = name + 'NoGstGL'

    return os.path.join(self.build_dir, name + '/')

  def set_llvmpipe_env(self, environment):
    llvmpipe_libgl_path = os.path.abspath(os.path.join(self.install_dir, 'softGL', 'lib'))
    dri_libgl_path = os.path.join(llvmpipe_libgl_path, "dri")

    if os.path.exists(os.path.join(llvmpipe_libgl_path, "libGL.so")) and os.path.exists(os.path.join(dri_libgl_path, "swrast_dri.so")):
      # Force the Gallium llvmpipe software rasterizer
      environment['LIBGL_ALWAYS_SOFTWARE'] = "1"
      environment['LIBGL_DRIVERS_PATH'] = dri_libgl_path
      environment['LD_LIBRARY_PATH'] = llvmpipe_libgl_path
      if os.environ.get('LD_LIBRARY_PATH'):
        environment['LD_LIBRARY_PATH'] += ':%s' % os.environ.get('LD_LIBRARY_PATH')
    else:
      print("Can't find Gallium llvmpipe driver. Try to run update-webkitgtk-libs")
      sys.exit(2)

  def set_weston_env_for_server(self, environment):
    environment['XDG_RUNTIME_DIR'] = self.xdg_runtime_dir

  def set_weston_env_for_client(self, environment):
    environment['XDG_RUNTIME_DIR'] = self.xdg_runtime_dir
    environment['WAYLAND_DISPLAY'] = self.wayland_socket
    environment['GDK_BACKEND'] = 'wayland'

  def get_argument_parser(self):
    argParser = argparse.ArgumentParser(description='Webkit dev script using custom jhbuild env')
    argParser.add_argument('--release', action='store_false', dest='debug', default=False, help='Compile with Debug configuration (default: Release)')
    argParser.add_argument('--debug', action='store_true', default=False, help='Compile with Debug configuration (default: Release)')
    argParser.add_argument('--install', action='store_true', default=False, help='Install Webkit to jhbuild')
    argParser.add_argument('--all', action='store_true', default=False, help='Build WebKit with all possible configurations (default: False)')

    argParser.add_argument('--disable-threaded-compositor', action='store_true', dest='disable_threaded_compositor', default=False, help='Disable Threaded Compositor (default: False)')
    argParser.add_argument('--disable-gst-gl', action='store_true', dest='disable_gstgl', default=False, help='Disable Gst GL (default: False)')
    argParser.add_argument('--use-opengles', action='store_true', dest='use_gles', default=False, help='Use OpenGLES (default: False)')

    # Options to run MiniBrowser
    argParser.add_argument('--url', help='URL to open  (for MiniBrowser)')
    argParser.add_argument('--weston', action='store_true', default=False, help='Open MiniBrowser inside of Weston (default: False)')
    argParser.add_argument('--llvmpipe', action='store_true', default=False, help='Use llvmpipe as a gl backend (default: False)')
    return argParser

  def all_possible_build_options(self):
    options = ['--disable-threaded-compositor', '--disable-gst-gl', '--use-opengles']
    for L in range(0, len(options) + 1):
        for subset in itertools.combinations(options, L):
          yield self.get_argument_parser().parse_args(subset)
          for_debug = ('--debug', ) + subset
          yield self.get_argument_parser().parse_args(for_debug)

  def __init__(self):
    self.script_dir = os.path.dirname(os.path.realpath(__file__))
    self.resource_dir = os.path.join(self.script_dir, 'resource/')
    self.workspace_dir = os.path.abspath(os.path.join(self.script_dir, os.pardir))
    self.build_dir = os.path.join(self.workspace_dir, 'out/')
    self.install_dir = os.path.join(self.workspace_dir, 'Dependencies/Root')
    self.jhbuild_src_dir = os.path.join(self.workspace_dir, 'Dependencies/Source')
    self.config_file = os.path.join(self.script_dir, "config.json")
    self.build_finished_sound_file = os.path.join(self.resource_dir, "build_finished.wav")

    self.wayland_socket = 'wpe-test'
    self.xdg_runtime_dir = os.path.join(self.script_dir, 'tmp')

    self.llvm_install_prefix = '/usr/local'
    self.jhbuildrc = os.path.join(self.script_dir, "jhbuildrc")

    if not os.path.isfile(self.config_file):
      with open(self.config_file, 'w') as configFile:
        print "creating config file"
        self.config = {}
    else:
      with open(self.config_file, 'r') as configFile:
        print "reading from config file"
        self.config = json.load(configFile)


