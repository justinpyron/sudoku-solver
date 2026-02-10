import base64
import json
import os

from openai import OpenAI


def extract_sudoku_board(image_bytes: bytes) -> list[list[str]]:
    """
    Extract a 9x9 sudoku grid from an image using OpenAI's vision API.

    Args:
        image_bytes: Raw bytes of the image file containing a sudoku board

    Returns:
        A 9x9 array where each cell is a string (1-9 for filled cells, "." for empty cells)
    """
    # Encode image to base64
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Initialize OpenAI client
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY_DEFAULT"])

    # Prompt for extracting sudoku grid
    prompt = """
Extract the 9x9 sudoku grid from this image and return it as JSON.

Requirements:
- Return a JSON object with a single key "board" containing a 9x9 array
- Each cell must be a string: 1-9 for filled cells, "." for empty cells
- Row-major order: board[0] is the top row, board[8] is the bottom row
- Each inner array must have exactly 9 elements
- Return ONLY valid JSON, no markdown, no explanations, no additional text

Example format:
{"board":[["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]}
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
