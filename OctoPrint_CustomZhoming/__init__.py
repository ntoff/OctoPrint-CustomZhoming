# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import re

class CustomzhomingPlugin(octoprint.plugin.SettingsPlugin,
                          octoprint.plugin.TemplatePlugin):


	def get_settings_defaults(self):
		return dict(
			zHomeCommand="G28 Z0"
		)

	def rewrite_Zhome(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if gcode and gcode.startswith("G28"):
			homeZcmd = re.search("(X0)?\s?(Y0)?\s?(Z0)", cmd)
			if homeZcmd and homeZcmd.group(3) and not homeZcmd.group(1) and not homeZcmd.group(2):
				cmd = self._settings.get(["zHomeCommand"])
				return cmd,
		return cmd, #not entirely sure I need this line?

	def get_template_configs(self):
		return [
			dict(type="settings", name="Custom Home Z Command", template="customzhoming_settings.jinja2", custom_bindings=False)
			]

	def get_update_information(self):
		return dict(
			customzhoming=dict(
				displayName="Customzhoming Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="ntoff",
				repo="OctoPrint-CustomZhoming",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/ntoff/OctoPrint-CustomZhoming/archive/{target_version}.zip"
			)
		)


__plugin_name__ = "Customzhoming Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = CustomzhomingPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.rewrite_Zhome,
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

