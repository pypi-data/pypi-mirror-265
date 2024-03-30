import pygame
from dataclasses import dataclass

from graphics import Graphics
from typing import Self
from grid import Grid


class Scail:
    grid: Grid | None = None


class Defaults:
    GAME_WIDTH = 200  # Specified
    GAME_HEIGHT = 150  # Specified
    CELL_SIZE = 4  # optional
    INITIAL_FPS = 8  # optional
    MAX_FPS = 128  # optional
    MIN_FPS = 1  # optional
    MUTATE = False
    PAUSED = False


# None of these are scail-specific, so they will come from the "Settings constants"
@dataclass
class Settings:
    game_width: int
    game_height: int
    cell_size: int
    unpaused_fps: int  # The fps when the game is not paused
    # The actual fps at which the screen updates. Needs to be separated from unpaused fps because
    # if fps is changed when the game is paused, its effects should take place after it is unpaused
    current_fps: int
    paused: bool
    mutate: bool  # whether the autamaton does check-and-update or mutation

    @staticmethod
    def default():
        return Settings(
            Defaults.GAME_WIDTH,
            Defaults.GAME_HEIGHT,
            Defaults.CELL_SIZE,
            Defaults.INITIAL_FPS,
            Defaults.INITIAL_FPS,
            paused=Defaults.PAUSED,
            mutate=Defaults.MUTATE,
        )

    def set_dimensions(self, width: int, height: int, cell_size: int) -> Self:
        """Sets the dimensions of the program and returns the mutated object

        The resolution will be (width * cell_size) x (height * cell_size)
        """
        self.game_width = width
        self.game_height = height
        self.cell_size = cell_size
        return self

    def set_initial_fps(self, fps: int):
        """Sets the initial fps of the program and returns the mutated object

        FPS must be between 1 and 128, inclusive
        """

        self.current_fps = self.unpaused_fps = fps
        return self

    def set_mutate(self, mutate: bool):
        """Sets the mutate of the scail and returns the mutated object"""
        self.mutate = mutate
        return self

    def __str__(self) -> str:
        return f"Settings(width: {self.game_width}, height: {self.game_height}, cell_size = {self.cell_size}, ...)"


def mainLoop(initialize, update, settings: Settings):
    """Initializes all the classes and then updates them in a loop until the game is over"""

    settings.current_fps = settings.unpaused_fps
    grid = Grid(settings.game_width, settings.game_height, initialize, settings.mutate)
    Scail.grid = grid
    clock = pygame.time.Clock()
    graphics = Graphics(settings)

    gameExit = False
    while not gameExit:
        clock.tick(settings.current_fps)

        graphics.render_grid(grid)
        if not settings.paused:
            grid.step_grid()
            update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                break


def run(initialize, update, settings: Settings):
    """Runs the specified cellular automaton

    initialize - a function to initialize the grid,
    with parameters i, j, width, height

    update - a function that is run every generation. No parameters
    """

    pygame.init()
    pygame.display.set_caption("SCAIL")
    mainLoop(initialize, update, settings)
    pygame.quit()


def cells(indices):

    return [Scail.grid.cells[i][j] for (i, j) in indices]
