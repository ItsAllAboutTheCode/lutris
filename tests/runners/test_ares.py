import unittest
from unittest.mock import MagicMock, patch

from lutris.exceptions import MissingGameExecutableError
from lutris.runners.ares import ares


class TestAresRunner(unittest.TestCase):
    def setUp(self):
        self.runner = ares()
        self.runner.get_executable = lambda: "ares"
        self.runner.get_command = lambda: ["ares"]

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_main_file_only_launches(self, mock_isfile, mock_path_exists):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = MagicMock()
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    def test_no_main_file_raises_error(self, mock_path_exists):
        main_file = ""
        mock_path_exists.return_value = False
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = MagicMock()
        self.runner.config = mock_config
        with self.assertRaises(MissingGameExecutableError):
            self.runner.play()

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_main_file_with_valid_system_add_arg(self, mock_isfile, mock_path_exists):
        main_file = "/path/to/game"
        system = "Arcade"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file, "system": system}
        mock_config.runner_config = MagicMock()
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), "--system", system, main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_main_file_with_invalid_system_does_not_add_arg(self, mock_isfile, mock_path_exists):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file, "system": None}
        mock_config.runner_config = MagicMock()
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_fullscreen_true_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"fullscreen": True}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), "--fullscreen", main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_fullscreen_false_does_not_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"fullscreen": False}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_shader_non_empty_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        shader = "bilinear"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"shader": shader}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), "--shader", shader, main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_shader_empty_does_not_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"shader": ""}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_setting_adds_multiple_args(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        settings = {"key1": "value1", "key2": "value2"}
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"settings": settings}
        self.runner.config = mock_config

        actual = self.runner.play()
        self.assertGreater(len(actual["command"]), 2)
        self.assertEqual(actual["command"][0], self.runner.get_executable())
        self.assertEqual(actual["command"][-1], main_file)
        assert f"key1={settings['key1']}" in actual["command"]
        assert f"key2={settings['key2']}" in actual["command"]

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_setting_empty_does_not_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"settings": {}}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_dump_all_settings_true_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"dump_all_settings": True}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), "--dump-all-settings", main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_dump_all_settings_false_does_not_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"dump_all_settings": False}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_no_file_prompt_true_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"no_file_prompt": True}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), "--no-file-prompt", main_file]}
        self.assertEqual(self.runner.play(), expected)

    @patch("lutris.util.system.path_exists")
    @patch("os.path.isfile")
    def test_play_no_file_prompt_false_does_not_add_arg(self, mock_path_exists, mock_isfile):
        main_file = "/path/to/game"
        mock_isfile.return_value = True
        mock_path_exists.return_value = True
        mock_config = MagicMock()
        mock_config.game_config = {"main_file": main_file}
        mock_config.runner_config = {"no_file_prompt": False}
        self.runner.config = mock_config
        expected = {"command": [self.runner.get_executable(), main_file]}
        self.assertEqual(self.runner.play(), expected)
