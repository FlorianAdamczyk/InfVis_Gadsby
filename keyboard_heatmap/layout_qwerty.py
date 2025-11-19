"""QWERTY layout data and helper geometry derived from Patrick Wied's heatmap."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 373


@dataclass(frozen=True)
class KeyRect:
    label: str
    x: float
    y: float
    width: float
    height: float

    @property
    def center(self) -> Tuple[float, float]:
        return (self.x + self.width / 2.0, self.y + self.height / 2.0)


# Raw coordinate tuples copied from patrick-wied.at keyboard layouts (QWERTY section).
# Each list stores x/y pairs in sequence, representing all hotspots tied to a key.
_QWERTY_COORDS_RAW: Dict[str, Sequence[int]] = {
    "~": [35, 120, 70, 275],
    "`": [35, 120],
    "1": [90, 120],
    "!": [90, 120, 70, 275],
    "2": [144, 120],
    "@": [144, 120, 70, 275],
    "3": [198, 120],
    "#": [198, 120, 70, 275],
    "4": [253, 120],
    "$": [253, 120, 70, 275],
    "5": [307, 120],
    "%": [307, 120, 70, 275],
    "6": [361, 120],
    "^": [361, 120, 70, 275],
    "7": [415, 120],
    "&": [415, 120, 70, 275],
    "8": [469, 120],
    "*": [469, 120, 70, 275],
    "9": [524, 120],
    "(": [524, 120, 70, 275],
    "0": [579, 120],
    ")": [579, 120, 70, 275],
    "-": [630, 120],
    "_": [630, 120, 70, 275],
    "+": [685, 120, 70, 275],
    "=": [685, 120],
    "Q": [115, 174],
    "W": [169, 174],
    "E": [224, 174],
    "R": [278, 174],
    "T": [332, 174],
    "Y": [386, 174],
    "U": [440, 174],
    "I": [494, 174],
    "O": [548, 174],
    "P": [602, 174],
    "[": [656, 174],
    "{": [656, 174, 70, 275],
    "]": [710, 174],
    "}": [710, 174, 70, 275],
    "\\": [764, 174],
    "|": [764, 174, 70, 275],
    "A": [130, 225],
    "S": [184, 225],
    "D": [238, 225],
    "F": [292, 225],
    "G": [346, 225],
    "H": [400, 225],
    "J": [454, 225],
    "K": [508, 225],
    "L": [562, 225],
    ";": [616, 225],
    ":": [616, 225, 70, 275],
    "'": [670, 225],
    '"': [670, 225, 70, 275],
    "Z": [158, 275],
    "X": [212, 275],
    "C": [266, 275],
    "V": [320, 275],
    "B": [374, 275],
    "N": [428, 275],
    "M": [482, 275],
    ",": [536, 275],
    "<": [536, 275, 70, 275],
    ".": [590, 275],
    ">": [590, 275, 70, 275],
    "/": [644, 275],
    "?": [644, 275, 70, 275],
    " ": [500, 300],
}


def _chunk(coords: Sequence[int]) -> List[Tuple[int, int]]:
    return [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]


QWERTY_LAYOUT: Dict[str, List[Tuple[int, int]]] = {
    key: _chunk(values) for key, values in _QWERTY_COORDS_RAW.items()
}


# Keyboard rectangles are approximate but proportionally aligned to the 800x373 canvas.
BASE_KEY_WIDTH = 62
BASE_KEY_HEIGHT = 62
KEY_GAP = 6

_ROW_SPEC = [
    {
        "y": 70,
        "start_x": 30,
        "keys": [
            {"labels": ["`", "~"]},
            {"labels": ["1", "!"]},
            {"labels": ["2", "@"]},
            {"labels": ["3", "#"]},
            {"labels": ["4", "$"]},
            {"labels": ["5", "%"]},
            {"labels": ["6", "^"]},
            {"labels": ["7", "&"]},
            {"labels": ["8", "*"]},
            {"labels": ["9", "("]},
            {"labels": ["0", ")"]},
            {"labels": ["-", "_"]},
            {"labels": ["=", "+"]},
        ],
    },
    {
        "y": 140,
        "start_x": 60,
        "keys": [
            {"labels": ["Q"]},
            {"labels": ["W"]},
            {"labels": ["E"]},
            {"labels": ["R"]},
            {"labels": ["T"]},
            {"labels": ["Y"]},
            {"labels": ["U"]},
            {"labels": ["I"]},
            {"labels": ["O"]},
            {"labels": ["P"]},
            {"labels": ["[", "{"]},
            {"labels": ["]", "}"]},
            {"labels": ["\\", "|"]},
        ],
    },
    {
        "y": 210,
        "start_x": 80,
        "keys": [
            {"labels": ["A"]},
            {"labels": ["S"]},
            {"labels": ["D"]},
            {"labels": ["F"]},
            {"labels": ["G"]},
            {"labels": ["H"]},
            {"labels": ["J"]},
            {"labels": ["K"]},
            {"labels": ["L"]},
            {"labels": [";", ":"]},
            {"labels": ["'", '"']},
        ],
    },
    {
        "y": 280,
        "start_x": 110,
        "keys": [
            {"labels": ["Z"]},
            {"labels": ["X"]},
            {"labels": ["C"]},
            {"labels": ["V"]},
            {"labels": ["B"]},
            {"labels": ["N"]},
            {"labels": ["M"]},
            {"labels": [",", "<"]},
            {"labels": [".", ">"]},
            {"labels": ["/", "?"]},
        ],
    },
]

# Space bar (centered)
_SPACE_SPEC = {"y": 340, "start_x": 210, "width": 380, "labels": [" "]}


KEYBOXES: Dict[str, KeyRect] = {}


def _build_keyboxes() -> Dict[str, KeyRect]:
    boxes: Dict[str, KeyRect] = {}
    for row in _ROW_SPEC:
        x = row["start_x"]
        for key in row["keys"]:
            width = key.get("width", BASE_KEY_WIDTH)
            rect = KeyRect(label=key["labels"][0], x=x, y=row["y"], width=width, height=BASE_KEY_HEIGHT)
            for label in key["labels"]:
                boxes[label] = KeyRect(label=label, x=x, y=row["y"], width=width, height=BASE_KEY_HEIGHT)
            x += width + KEY_GAP
    space_rect = KeyRect(
        label=" ",
        x=_SPACE_SPEC["start_x"],
        y=_SPACE_SPEC["y"],
        width=_SPACE_SPEC["width"],
        height=BASE_KEY_HEIGHT,
    )
    boxes[" "] = space_rect
    return boxes


KEYBOXES.update(_build_keyboxes())


def iter_key_rects() -> Iterable[KeyRect]:
    """Helper to iterate unique rectangles (deduplicates multi-label keys)."""
    seen = set()
    for rect in KEYBOXES.values():
        if rect.center in seen:
            continue
        seen.add(rect.center)
        yield rect
