## Idea

- Get a list of instructions to perform from a solution board
- Execute those instructions on screen (move cursor and click essentially).

## Get Image

## Retrieve Instructions

## Execute Instructions


## Websites
- [puzzles](https://tryhardguides.com/linkedin-zip-answer-today/)
- [test](https://k4l397.github.io/zip-puzzle-game/)



## Images for Zip

Grid: can be 6 or 7
Size: 410x410 px

Scale image to 420x420. If image is 6x6, we chunk by 70px. If 7x7, we chunk by 60px

Create a loop that will grab 70x70px chunks and horizontally go through
them. Once it gets to an ending piece (a chunk that only has pixels on
the edge of one side) it will check if the correct 1 pattern is
identified. If it is, we know that this is a 6x6, if it is not, it
is a 7x7. Those seem to be the only format that is used. Store the location of the 1.

Create another loop that will start at the one location. Back track 
until you arrive at the other end piece. Mark the locations as a
series of increasing digits starting at 1. This is now our list of 
instructions.


