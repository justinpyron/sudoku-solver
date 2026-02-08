import base64
import json
import os

from openai import OpenAI


def extract_sudoku_board(image_path: str) -> list[list[int]]:
    """
    Extract a 9x9 sudoku grid from an image using OpenAI's vision API.

    Args:
        image_path: Path to the image file containing a sudoku board

    Returns:
        A 9x9 array where each cell is an integer (1-9 for filled cells, 0 for empty cells)
    """
    # Encode image to base64
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY_DEFAULT"])

    # Prompt for extracting sudoku grid
    prompt = """
Extract the 9x9 sudoku grid from this image and return it as JSON.

Requirements:
- Return a JSON object with a single key "board" containing a 9x9 array
- Each cell must be an integer: 1-9 for filled cells, 0 for empty cells
- Row-major order: board[0] is the top row, board[8] is the bottom row
- Each inner array must have exactly 9 elements
- Return ONLY valid JSON, no markdown, no explanations, no additional text

Example format:
{"board":[[5,3,0,0,7,0,0,0,0],[6,0,0,1,9,5,0,0,0],[0,9,8,0,0,0,0,6,0],[8,0,0,0,6,0,0,0,3],[4,0,0,8,0,3,0,0,1],[7,0,0,0,2,0,0,0,6],[0,6,0,0,0,0,2,8,0],[0,0,0,4,1,9,0,0,5],[0,0,0,0,8,0,0,7,9]]}
"""

    # Call OpenAI API
    completion = client.chat.completions.create(
        model="gpt-5.2",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
    )

    # Parse and return the board
    response = json.loads(completion.choices[0].message.content)
    return response["board"]
