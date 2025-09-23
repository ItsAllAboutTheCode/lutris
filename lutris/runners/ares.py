# Standard Library
import shlex
from gettext import gettext as _
from typing import Any, Callable, Dict, List

# Lutris Modules
from lutris.exceptions import MissingGameExecutableError
from lutris.runners.runner import Runner
from lutris.util import system

AppendFunction = Callable[[List[str], Any, Dict[str, Any]], None]


def _append_args_string(arguments: List[str], option_dict: Any, config: Dict[str, Any]):
    option_key = option_dict.get("option")
    if option_value := config.get(option_key):
        if option_arg := option_dict.get("argument"):
            arguments.append(option_arg)
        arguments.append(option_value)


def _append_args_bool(arguments: List[str], option_dict: Any, config: Dict[str, Any]):
    option_key = option_dict.get("option")
    value = config.get(option_key)
    option_arg = option_dict.get("argument")
    if value and isinstance(option_arg, str):
        arguments.append(option_arg)


def _append_args_choice(arguments: List[str], option_dict: Any, config: Dict[str, Any]):
    option_key = option_dict.get("option")
    value = config.get(option_key)
    if value is not None:
        option_arg = option_dict.get("argument")
        if isinstance(option_arg, str):
            arguments.append(option_arg)
        arguments.append(value)


def _append_args_multi_string(arguments: List[str], option_dict: Any, config: Dict[str, Any]):
    option_key = option_dict.get("option")
    if option_arg := option_dict.get("argument"):
        arguments.append(option_arg)
    arguments.extend(shlex.split(str(config.get(option_key))))


def _append_args_mapping(arguments: List[str], option_dict: Any, config: Dict[str, Any]):
    option_key = option_dict.get("option")
    option_arg = option_dict.get("argument")
    option_value = config.get(option_key)
    if not isinstance(option_value, dict):
        return
    for name, value in option_value.items():
        if option_arg:
            arguments.append(option_arg)
        arguments.append(f"{name}={value}")


_argument_append_funcs: Dict[str, AppendFunction] = {
    # adds arguments from the supplied option dictionary to the arguments list
    "label": lambda _, _1, _2: None,
    "string": _append_args_string,
    "bool": _append_args_bool,
    "range": _append_args_string,
    "choice": _append_args_choice,
    "choice_with_entry": _append_args_choice,
    "choice_with_search": _append_args_choice,
    "file": _append_args_string,
    "multiple_file": _append_args_multi_string,
    "directory": _append_args_string,
    "mapping": _append_args_mapping,
    "command_line": _append_args_multi_string,
}


def append_args(
    arguments: List[str],
    options_dict_list: List[Dict[str, Any]],
    config: Dict[str, Any],
):
    for option_dict in options_dict_list:
        option_key = option_dict.get("option")
        if option_key not in config:
            continue

        option_type = option_dict.get("type")
        if append_func := _argument_append_funcs.get(str(option_type)):
            append_func(arguments, option_dict, config)
        else:
            raise RuntimeError(f"Unhandled option type {option_dict.get('type')}")


class ares(Runner):
    human_name = _("ares")
    description = _("Multi System Emulator: focusing on accuracy and preservation...")
    runnable_alone = True
    platforms = [
        _("Arcade"),
        _("Atari 2600"),
        _("Bandai WonderSwan"),
        _("Bandai WonderSwan Color"),
        _("Benesse Pocket Challenge V2"),
        _("ColecoVision"),
        _("Nichibutsu My Vision"),
        _("Microsoft MSX"),
        _("Microsoft MSX2"),
        _("NEC PC Engine TurboGrafx-16"),
        _("NEC PC Engine CD"),
        _("NEC SuperGrafx"),
        _("NEC SuperGrafx CD"),
        _("Nintendo NES"),
        _("Nintendo Famicom Disk System"),
        _("Nintendo SNES"),
        _("Nintendo 64"),
        _("Nintendo 64 DD"),
        _("Nintendo Game Boy"),
        _("Nintendo Game Boy (Color)"),
        _("Nintendo Game Boy Advance"),
        _("Sega SG-1000"),
        _("Sega SC-3000"),
        _("Sega Master System"),
        _("Sega Genesis/Mega Drive"),
        _("Sega Game Gear"),
        _("Sega Mega 32X"),
        _("Sega Mega CD"),
        _("Sega Mega CD 32X"),
        _("Sega Mega LD"),
        _("SNK Neo Geo AES"),
        _("SNK Neo Geo MVS"),
        _("SNK Neo Geo Pocket"),
        _("SNK Neo Geo Pocket (Color)"),
        _("Sony PlayStation"),
        _("Sinclair ZX Spectrum"),
        _("Sinclair ZX Spectrum 128"),
    ]
    system_choices = (
        (_("None"), None),
        (_("Arcade"), "Arcade"),
        (_("Atari 2600"), "Atari 2600"),
        (_("Bandai WonderSwan"), "WonderSwan"),
        (_("Bandai WonderSwan Color"), "WonderSwan Color"),
        (_("Benesse Pocket Challenge V2"), "Pocket Challenge V2"),
        (_("ColecoVision"), "ColecoVision"),
        (_("Nichibutsu My Vision"), "MyVision"),
        (_("Microsoft MSX"), "MSX"),
        (_("Microsoft MSX2"), "MSX2"),
        (_("NEC PC Engine"), "PC Engine"),
        (_("NEC PC Engine CD"), "PC Engine CD"),
        (_("NEC SuperGrafx"), "SuperGrafx"),
        (_("NEC SuperGrafx CD"), "SuperGrafx CD"),
        (_("Nintendo NES"), "Famicom"),
        (_("Nintendo Famicom Disk System"), "Famicom Disk System"),
        (_("Nintendo SNES"), "Super Famicom"),
        (_("Nintendo 64"), "Nintendo 64"),
        (_("Nintendo 64 DD"), "Nintendo 64DD"),
        (_("Nintendo Game Boy"), "Game Boy"),
        (_("Nintendo Game Boy (Color)"), "Game Boy Color"),
        (_("Nintendo Game Boy Advance"), "Game Boy Advance"),
        (_("Sega SG-1000"), "SG-1000"),
        (_("Sega SC-3000"), "SC-3000"),
        (_("Sega Master System"), "Master System"),
        (_("Sega Mega Drive (Genesis)"), "Mega Drive"),
        (_("Sega Game Gear"), "Game Gear"),
        (_("Sega Mega 32X"), "Mega 32X"),
        (_("Sega Mega CD"), "Mega CD"),
        (_("Sega Mega CD 32X"), "Mega CD 32X"),
        (_("Sega Mega LD"), "Mega LD"),
        (_("SNK Neo Geo MVS"), "Neo Geo MVS"),
        (_("SNK Neo Geo AES"), "Neo Geo AES"),
        (_("SNK Neo Geo Pocket"), "Neo Geo Pocket"),
        (_("SNK Neo Geo Pocket Color"), "Neo Geo Pocket Color"),
        (_("Sony PlayStation"), "PlayStation"),
        (_("Sinclair ZX Spectrum"), "ZX Spectrum"),
        (_("Sinclair ZX Spectrum 128"), "ZX Spectrum 128"),
    )
    flatpak_id = "dev.ares.ares"
    download_url = "https://github.com/pkgforge-dev/ares-emu-appimage/releases/download/v146%402025-09-15_1757920610/ares-v146-anylinux-x86_64.AppImage"
    runner_executable = "ares/ares-v146-anylinux-x86_64.AppImage"
    game_options = [
        {
            "option": "platform",
            "type": "choice_with_entry",
            "label": _("System"),
            "argument": "--system",
            "choices": system_choices,
            "help": _("The system to emulate.\nEx. Super Famicom, PlayStation, Mega Drive, etc..."),
            "default": None,
        },
        {
            "option": "main_file",
            "type": "file",
            "label": _("ROM/ISO file"),
            "help": _("The game data, commonly called a ROM or ISO image."),
        },
    ]
    runner_options = [
        {
            "option": "fullscreen",
            "type": "bool",
            "section": _("Graphics"),
            "label": _("Fullscreen"),
            "argument": "--fullscreen",
            "help": _("Start in full screen mode"),
            "default": False,
        },
        {
            "option": "shader",
            "type": "string",
            "section": _("Graphics"),
            "label": _("Shader"),
            "argument": "--shader",
            "help": _("Specify the name of the shader to use"),
        },
        {
            "option": "settings",
            "type": "mapping",
            "section": _("Settings"),
            "label": _("Settings"),
            "argument": "--setting",
            "help": _(
                "Specify a value for a setting. This can be used to override settings per game\n"
                "Available Settings are in the $XDG_DATA_HOME/ares/settings.bml file"
            ),
            "advanced": True,
        },
        {
            "option": "dump_all_settings",
            "type": "bool",
            "section": _("Settings"),
            "label": _("Dump all settings"),
            "argument": "--dump-all-settings",
            "help": _("Dumps list of all existing settings to the lutris log and exit the emulator"),
            "default": False,
            "advanced": True,
        },
        {
            "option": "no_file_prompt",
            "type": "bool",
            "section": _("Settings"),
            "label": _("No file prompt"),
            "argument": "--no-file-prompt",
            "help": _("Do not prompt to load (optional) additional roms (eg: Nintendo 64DD)"),
            "default": False,
            "advanced": True,
        },
    ]

    def get_platform(self):
        emu_system = self.game_config.get("platform")
        if emu_system:
            for platform, system_choice in self.system_choices:
                if system_choice == emu_system:
                    return platform
        return ""

    def play(self):
        """Runs the game"""
        rom = self.game_config.get("main_file", "")
        if not system.path_exists(rom):
            raise MissingGameExecutableError(filename=rom)

        arguments = self.get_command()

        # Append the runner arguments first, and game arguments afterwards
        append_args(arguments, self.runner_options, self.runner_config)
        append_args(arguments, self.game_options, self.game_config)
        return {"command": arguments}
