
import json
import os.path

class ConfigHelper:

  def write_config_to_file(self):
    with open(self.config_file, 'w') as configFile:
      print "writing to config file"
      json.dump(self.config, configFile, sort_keys=True, indent=4, separators=(',', ': '))

  def __init__(self):
    self.resource_dir = os.path.dirname(os.path.realpath(__file__))
    self.workspace_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
    self.build_dir = os.path.join(self.workspace_dir, 'out/')
    self.install_dir = os.path.join(self.workspace_dir, 'Dependencies/Root')
    self.config_file = os.path.join(self.resource_dir, "config.json")
    self.build_finished_sound_file = os.path.join(self.resource_dir, "build_finished.wav")
    self.llvm_install_prefix = '/usr/local'

    if not os.path.isfile(self.config_file):
      with open(self.config_file, 'w') as configFile:
        print "creating config file"
        self.config = {}
    else:
      with open(self.config_file, 'r') as configFile:
        print "reading from config file"
        self.config = json.load(configFile)


