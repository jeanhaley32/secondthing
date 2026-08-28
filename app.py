from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Message in a Bottle API", version="1.0.0")

# Bound the grid an attacker can force us to allocate. Coordinates are used
# directly as grid dimensions, so an unbounded value (e.g. x=10**9) would make
# us build a multi-billion-cell grid and OOM the pod. 1000 gives a generous
# 1001x1001 ceiling for any legitimate message.
MAX_COORD = 1000

class Coordinates(BaseModel):
    x: int
    y: int

class Bottle(BaseModel):
    character: str
    coordinates: Coordinates

class BottleCollection(BaseModel):
    bottles: List[Bottle]

@app.get("/")
async def root():
    return {"message": "Message in a Bottle API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/collect-bottles")
async def collect_bottles(bottles: List[Bottle]):
    """
    Process bottles with characters and coordinates to reveal the hidden message.
    """
    try:
        if not bottles:
            raise HTTPException(status_code=400, detail="No bottles provided")

        logger.info(f"Received {len(bottles)} bottles")

        # Reject out-of-range coordinates before sizing the grid. Negative
        # values would corrupt indexing and oversized values would blow up
        # allocation, so both are rejected as bad input rather than trusted.
        for bottle in bottles:
            x, y = bottle.coordinates.x, bottle.coordinates.y
            if not (0 <= x <= MAX_COORD and 0 <= y <= MAX_COORD):
                raise HTTPException(
                    status_code=400,
                    detail=f"Coordinates must be between 0 and {MAX_COORD}",
                )

        # Find grid dimensions
        max_x = max(bottle.coordinates.x for bottle in bottles)
        max_y = max(bottle.coordinates.y for bottle in bottles)

        # Create grid (add 1 because coordinates are 0-indexed)
        grid_width = max_x + 1
        grid_height = max_y + 1
        
        # Initialize grid with spaces
        grid = [[' ' for _ in range(grid_width)] for _ in range(grid_height)]
        
        # Place characters on the grid
        for bottle in bottles:
            x, y = bottle.coordinates.x, bottle.coordinates.y
            if 0 <= x < grid_width and 0 <= y < grid_height:
                grid[y][x] = bottle.character
            else:
                logger.warning(f"Bottle coordinates ({x}, {y}) out of bounds")
        
        # Convert grid to string representation
        message_lines = []
        for row in grid:
            message_lines.append(''.join(row))
        
        message = '\n'.join(message_lines)
        
        # Create response
        response = {
            "message": message,
            "grid_dimensions": {"width": grid_width, "height": grid_height},
            "bottles_processed": len(bottles)
        }
        
        # Log only a bounded summary. The message/grid are attacker-influenced
        # and can be large, so we don't echo their full contents into the logs.
        logger.info(f"Grid dimensions: {grid_width}x{grid_height}, bottles: {len(bottles)}")

        return response

    except HTTPException:
        # Client errors (e.g. the 400s above) are intentional — let them through
        # rather than masking them as a 500 in the generic handler below.
        raise
    except Exception as e:
        logger.error(f"Error processing bottles: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 