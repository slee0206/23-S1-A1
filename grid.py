from __future__ import annotations
from data_structures.referential_array import ArrayR

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.

        logic for creating grid:

        1. get an horizontal array of length x
        2. create vertical array for each element in horizontal array
        3. which makes x * y as a whole grid. 


        """

        self.draw_style = draw_style # intialising draw style as instance
        self.x = x 
        self.y = y
        self.grid = ArrayR(x)

        for i in range(self.x):
            self.grid[i] = ArrayR(self.y)  

        self.brush_size = self.DEFAULT_BRUSH_SIZE # setting the brush size


    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """

        if self.DEFAULT_BRUSH_SIZE < self.MAX_BRUSH:
            self.brush_size =+ 1 # brush size is increased by 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.DEFAULT_BRUSH_SIZE > self.MIN_BRUSH:
            self.brush_size -= 1 # brush size is decreased by 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        raise NotImplementedError()