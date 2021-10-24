import os
from dataclasses import dataclass
from PIL import Image

from .base import ButtonListScreen, LargeButtonScreen
from ..components import load_icon, TextArea, GUIConstants

from seedsigner.helpers import B



@dataclass
class SeedsMenuScreen(ButtonListScreen):
    # Customize defaults
    title: str = "In-Memory Seeds"
    is_button_text_centered: bool = False
    seeds: list = None

    def __post_init__(self):
        # Programmatically set up other args
        self.button_data = []
        for seed in self.seeds:
            self.button_data.append((seed["fingerprint"], "fingerprint_inline"))
        self.button_data.append("Load a seed")

        # Initialize the base class
        super().__post_init__()


@dataclass
class SeedValidScreen(ButtonListScreen):
    fingerprint: str = None
    title: str = "Seed Valid"
    is_bottom_list: bool = False

    def __post_init__(self):
        # Customize defaults
        self.button_data = [
            # ("Scan PSBT or Seed", "scan_inline"),
            "Home",
            ("Advanced", "settings_inline"),
        ]

        # Initialize the base class
        super().__post_init__()

        self.fingerprint_icon = load_icon("fingerprint")

        self.text_line_1 = TextArea(
            text="Fingerprint:",
            width=self.canvas_width
        )
        self.text_line_2 = TextArea(
            text=self.fingerprint,
            width=self.canvas_width
        )

        # Position the TextAreas
        total_text_height = self.text_line_1.height + int(self.text_line_1.height * GUIConstants.BODY_LINE_SPACING) + self.text_line_2.height
        main_area_height = self.buttons[0].screen_y - self.top_nav.height
        self.text_line_1.screen_y = self.top_nav.height + int((main_area_height - total_text_height) / 2)
        self.text_line_2.screen_y = self.text_line_1.screen_y + int(self.text_line_1.height * (1.0 + GUIConstants.BODY_LINE_SPACING))

        # Have to shift line 2 over to accomodate the fingerprint icon
        self.text_line_2.screen_x += int((self.fingerprint_icon.width) / 2)

        self.fingerprint_icon_x = int((self.canvas_width - (self.fingerprint_icon.width + 4 + self.text_line_2.text_width)) / 2)
        self.fingerprint_icon_y = self.text_line_2.screen_y


    def _render(self):
        super()._render()

        self.text_line_1.render()
        self.text_line_2.render()
        self.renderer.canvas.paste(self.fingerprint_icon, (self.fingerprint_icon_x, self.fingerprint_icon_y))

        # Write the screen updates
        self.renderer.show_image()



@dataclass
class SeedOptionsScreen(ButtonListScreen):
    # Customize defaults
    title: str = "Seed Options"
    is_bottom_list: bool = True
    fingerprint: str = None
    has_passphrase: bool = False

    def __post_init__(self):
        # Programmatically set up other args
        self.button_data = [
            "View Seed Words",
            "Export Xpub",
            "Export Seed as QR",
        ]

        # Initialize the base class
        super().__post_init__()



@dataclass
class SeedExportXpub1Screen(LargeButtonScreen):
    # Customize defaults
    title: str = "Export Xpub"

    def __post_init__(self):
        # Programmatically set up other args
        self.button_data = [
            "Single Sig",
            "Multisig",
        ]

        # Initialize the base class
        super().__post_init__()



@dataclass
class SeedExportXpub2Screen(ButtonListScreen):
    # Customize defaults
    title: str = "Export Xpub"
    is_button_text_centered: bool = False
    is_bottom_list: bool = True

    def __post_init__(self):
        # Programmatically set up other args
        self.button_data = [
            "Native Segwit",
            "Nested Segwit (legacy)",
            "Taproot",
            "Custom Derivation",
        ]

        # Initialize the base class
        super().__post_init__()

