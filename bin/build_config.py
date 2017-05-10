import argparse
import itertools
import json
import os
import os.path
import sys
import stat
from subprocess import check_output
import re
import shutil

class ConfigHelper:

  def ensure_icecc_clang_env(self):
    if 'icecc_clang_version' in self.config:
      if (os.path.isfile(self.config['icecc_clang_version'])):
        return

    output = check_output(['/usr/bin/clang', '--version'])
    version = output.split()[2]

    print "Creating Icecream toolchain"
    createEnvCmd = ['/usr/libexec/icecc/icecc-create-env', '--clang', '/usr/bin/clang']
    output = check_output(createEnvCmd)
    print output
    generatedEnv = re.search(r'creating ([0-9a-f]+)\.tar.gz', output)
    if generatedEnv is None:
      print "Failed to find created env."
      sys.exit(2)

    generatedFileName = generatedEnv.group(1) + '.tar.gz'
    targetFileName = os.path.join(self.resource_dir, "icecc_clang_" + version + "_" + generatedEnv.group(1) + ".tar.gz")

    shutil.move(generatedFileName, targetFileName)
    self.config['icecc_clang_version'] = targetFileName
    self.write_config_to_file()

  def ensure_icecc_gcc_env(self):
    if 'icecc_gcc_version' in self.config:
      if (os.path.isfile(self.config['icecc_gcc_version'])):
        return

    output = check_output(['/usr/bin/gcc', '--version'])
    version = output.split()[2]

    print "Creating Icecream toolchain"
    createEnvCmd = ['/usr/libexec/icecc/icecc-create-env', '--gcc', '/usr/bin/gcc', '/usr/bin/g++']
    output = check_output(createEnvCmd)
    print output
    generatedEnv = re.search(r'creating ([0-9a-f]+)\.tar.gz', output)
    if generatedEnv is None:
      print "Failed to find created env."
      sys.exit(2)

    generatedFileName = generatedEnv.group(1) + '.tar.gz'
    targetFileName = os.path.join(self.resource_dir, "icecc_gcc_" + version + "_" + generatedEnv.group(1) + ".tar.gz")

    print generatedFileName + "  " + targetFileName
    shutil.move(generatedFileName, targetFileName)
    self.config['icecc_gcc_version'] = targetFileName
    self.write_config_to_file()

  def write_config_to_file(self):
    with open(self.config_file, 'w') as configFile:
      print "writing to config file"
      json.dump(self.config, configFile, sort_keys=True, indent=4, separators=(',', ': '))

  def get_webkit_dir(self, options, use_custom_jhbuild = False):
    if options.debug:
      name = 'Debug'
    elif not options.debug:
      name = 'Release'

    if not use_custom_jhbuild:
      return os.path.join(self.build_dir, name + '/')
    else:
      return os.path.join(self.custom_build_dir, name + '/')

  def set_llvmpipe_env(self, environment):
    llvmpipe_libgl_path = os.path.abspath(os.path.join(self.install_dir, 'softGL', 'lib'))
    dri_libgl_path = os.path.join(llvmpipe_libgl_path, "dri")

    if os.path.exists(os.path.join(llvmpipe_libgl_path, "libGL.so")) and os.path.exists(os.path.join(dri_libgl_path, "swrast_dri.so")):
      print "found llvmpipe " + dri_libgl_path + ", " + llvmpipe_libgl_path
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
    if environment.get('XDG_RUNTIME_DIR'):
      environment['XDG_RUNTIME_DIR'] = self.xdg_runtime_dir
      if not os.path.exists(self.xdg_runtime_dir):
        os.makedirs(self.xdg_runtime_dir,  stat.S_IREAD | stat.S_IEXEC | stat.S_IWUSR)

  def set_weston_env_for_client(self, environment):
    #environment['XDG_RUNTIME_DIR'] = self.xdg_runtime_dir
    environment['WAYLAND_DISPLAY'] = self.wayland_socket
    #environment['GDK_BACKEND'] = 'wayland'

  def get_argument_parser(self):

    # Options to build WebKitGtk
    argParser = argparse.ArgumentParser(description='Webkit dev script using custom jhbuild env')
    argParser.add_argument('--release', action='store_false', dest='debug', default=False, help='Compile with Debug configuration (default: Release)')
    argParser.add_argument('--debug', action='store_true', default=False, help='Compile with Debug configuration (default: Release)')
    argParser.add_argument('--install', action='store_true', default=False, help='Install Webkit to jhbuild')
    argParser.add_argument('--all', action='store_true', default=False, help='Build WebKit with all possible configurations (default: False)')
    argParser.add_argument('--fast', action='store_true', default=False, help='Compile only selected components (default: False)')
    argParser.add_argument('-j', '--jobs', type=int, default=0, help='Number of compiling jobs')
    argParser.add_argument('--clang', action='store_true', default=True, help='Use clang instead of gcc (default: True)')

    argParser.add_argument('--disable-threaded-compositor', action='store_true', dest='disable_threaded_compositor', default=False, help='Disable Threaded Compositor (default: False)')
    argParser.add_argument('--disable-gst-gl', action='store_true', dest='disable_gstgl', default=False, help='Disable Gst GL (default: False)')
    argParser.add_argument('--use-opengles', action='store_true', dest='use_gles', default=False, help='Use OpenGLES (default: False)')

    # Options to build WebKitWPE
    argParser.add_argument('--wpe', action='store_true', dest='wpe', default=False, help='Build WebKitWPE (default: False)')

    # Options to run MiniBrowser
    argParser.add_argument('--url', help='URL to open  (for MiniBrowser)')
    argParser.add_argument('--weston', action='store_true', default=False, help='Open MiniBrowser inside of Weston (default: False)')
    argParser.add_argument('--llvmpipe', action='store_true', default=False, help='Use llvmpipe as a gl backend (default: False)')
    argParser.add_argument('--gdb', action='store_true', default=False, help='execute gdb for MiniBrowser')
    argParser.add_argument('--pause', action='store_true', default=False, help='Pause WebKitWebProcess to attache gdb')
    argParser.add_argument('--test', action='store_true', default=False, help='execute WebKitTestRunner instead of MiniBrowser')
    argParser.add_argument('--scale', type=int, default=0, help='Apply custom device scale using nested compositor (defaule: use current compositor)')
    argParser.add_argument('--wrapper', help='The wrapper to analize WebProcess. (e.g. valgrind)')
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
    self.project_settings_dir = os.path.join(self.script_dir, 'projects/WebKitGtk/')
    self.config_file = os.path.join(self.script_dir, "config.json")
    self.build_finished_sound_file = os.path.join(self.resource_dir, "build_finished.wav")

    self.base_workspace_dir = os.path.abspath(os.path.join(self.script_dir, os.pardir))
    #Settings for default jhbuild sets
    self.workspace_dir = os.path.join(self.base_workspace_dir, 'WebKitGtk/')
    self.jhbuild_wrapper = os.path.join(self.workspace_dir, "Tools/jhbuild/jhbuild-wrapper")
    self.build_dir = os.path.join(self.workspace_dir, 'WebKitBuild/')

    #Settings for custom jhbuild sets
    self.custom_build_dir = os.path.join(self.base_workspace_dir, 'out/')
    self.install_dir = os.path.join(self.base_workspace_dir, 'Dependencies/Root')
    self.jhbuild_src_dir = os.path.join(self.base_workspace_dir, 'Dependencies/Source')
    self.jhbuildrc = os.path.join(self.script_dir, "jhbuildrc")

    self.wayland_socket = 'wpe-test'
    self.xdg_runtime_dir = '/tmp/weston-runtime-dir'

    self.llvm_install_prefix = '/usr/local'

    if not os.path.isfile(self.config_file):
      with open(self.config_file, 'w') as configFile:
        print "creating config file"
        self.config = {}
    else:
      with open(self.config_file, 'r') as configFile:
        self.config = json.load(configFile)


