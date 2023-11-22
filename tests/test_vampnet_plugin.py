# -*- encoding: utf-8 -*-
"""Tests for the Nendo VampNet plugin."""
import unittest

from nendo import Nendo, NendoConfig, NendoTrack

nd = Nendo(
    config=NendoConfig(
        library_path="./library",
        log_level="INFO",
        plugins=["nendo_plugin_vampnet"],
    )
)


class VampnetPluginTest(unittest.TestCase):
    def test_run_vampnet_generation(self):
        nd.library.reset(force=True)
        track = nd.library.add_track(file_path="tests/assets/test.wav")

        outpainting = nd.plugins.vampnet(track=track, duration=10)

        self.assertEqual(len(nd.library.get_tracks()), 2)
        self.assertEqual(outpainting.sr, track.sr)
        self.assertTrue(type(outpainting) == NendoTrack)

    def test_run_process_vampnet_generation(self):
        nd.library.reset(force=True)
        track = nd.library.add_track(file_path="tests/assets/test.wav")

        outpainting = track.process("nendo_plugin_vampnet", duration=10)

        self.assertEqual(len(nd.library.get_tracks()), 2)
        self.assertEqual(outpainting.sr, track.sr)
        self.assertTrue(type(outpainting) == NendoTrack)


if __name__ == "__main__":
    unittest.main()
