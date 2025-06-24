from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Message in a Bottle API", version="1.0.0")

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
        
        # Log incoming request
        logger.info(f"Received {len(bottles)} bottles")
        for i, bottle in enumerate(bottles):
            logger.info(f"Bottle {i+1}: character='{bottle.character}' at ({bottle.coordinates.x}, {bottle.coordinates.y})")
        
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
        
        # Log the message and full response
        logger.info(f"Grid dimensions: {grid_width}x{grid_height}")
        logger.info(f"Revealed message:\n{message}")
        logger.info(f"Full response being sent: {json.dumps(response, indent=2)}")
        
        return response
        
    except Exception as e:
        logger.error(f"Error processing bottles: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 