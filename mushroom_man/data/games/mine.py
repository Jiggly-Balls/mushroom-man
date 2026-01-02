import random
from enum import Enum, IntEnum, StrEnum, auto
from functools import cache
from typing import final


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class MineAssets(StrEnum):
    PLAYER = "<:player:1456646549697200251>"
    EMPTY = "<:empty:1456645997668204683>"
    STONE = "<:stone:1456646075388657725>"
    COBBLESTONE = "<:cobblestone:1456645975572742226>"
    COAL = "<:coal:1456645900767072320>"
    IRON = "<:iron:1456646173086711819>"
    GOLD = "<:gold:1456646041607868519>"
    DIAMOND = "<:diamond:1456646021445587189>"


class MineRates(IntEnum):
    STONE = 30
    COBBLESTONE = 27
    COAL = 20
    IRON = 15
    GOLD = 7
    DIAMOND = 1


@cache
def asset_rate_bind() -> tuple[list[MineAssets], list[int]]:
    names: list[MineAssets] = []
    rates: list[int] = []
    asset_map: dict[str, MineAssets] = MineAssets._member_map_  # pyright: ignore[reportAssignmentType]

    for name, rate in MineRates._member_map_.items():
        names.append(asset_map[name])
        rates.append(rate.value)

    return names, rates


@final
class MineEngine:
    def __init__(self, player_x: int = 10, player_y: int = 10) -> None:
        self.data: dict[tuple[int, int], MineAssets] = {}
        self.player_x = player_x
        self.player_y = player_y

    def create_block(self) -> MineAssets:
        """Returns a random block based on its respective weight"""

        assets, rates = asset_rate_bind()

        return random.choices(assets, rates, k=1)[0]

    def create_map(self) -> None:
        """Generates a new map of 100x100 units and stores it in `self.data`"""

        self.data.clear()

        for x in range(100):
            for y in range(100):
                self.data[x, y] = self.create_block()

        self.data[self.player_x, self.player_y] = MineAssets.PLAYER

    def create_image(self) -> str:
        """Creates the required string image to be displayed in discord (size=5x5)"""

        x, y = self.player_x, self.player_y

        image = ""

        image_coords: tuple[tuple[int, int], ...] = (
            (x - 2, y + 2),
            (x - 1, y + 2),
            (x, y + 2),
            (x + 1, y + 2),
            (x + 2, y + 2),
            (x - 2, y + 1),
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
            (x + 2, y + 1),
            (x - 2, y),
            (x - 1, y),
            (x, y),
            (x + 1, y),
            (x + 2, y),
            (x - 2, y - 1),
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
            (x + 2, y - 1),
            (x - 2, y - 2),
            (x - 1, y - 2),
            (x, y - 2),
            (x + 1, y - 2),
            (x + 2, y - 2),
        )

        for num, coord in enumerate(image_coords, start=1):
            try:
                block = self.data[coord]
            except KeyError:
                block = self.create_block()
                self.data[coord] = block

            image += block

            if num % 5 == 0:
                image += "\n"

        return image

    def move_player(self, direction: Direction) -> MineAssets:
        """Moves the player position in the respective direction.

        Parameter
        ---------
        direction
            The direction to move the player in.
        """

        current_block = self.data[self.player_x, self.player_y]
        self.data[self.player_x, self.player_y] = MineAssets.EMPTY

        if direction == Direction.UP:
            self.player_y += 1

        elif direction == Direction.DOWN:
            self.player_y -= 1

        elif direction == Direction.LEFT:
            self.player_x -= 1

        elif direction == Direction.RIGHT:
            self.player_x += 1

        self.data[self.player_x, self.player_y] = MineAssets.PLAYER

        return current_block
