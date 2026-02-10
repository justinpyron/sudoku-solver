import copy

import streamlit as st

from algo import solve_sudoku
from ocr import extract_sudoku_board

EMPTY = "."


def render_board_html(
    board: list[list[str]],
    original_board: list[list[str]] | None = None,
) -> str:
    """
    Render a sudoku board as an HTML table.

    Args:
        board: The 9x9 board to display.
        original_board: If provided, cells that were empty in the original board
            (i.e. solved cells) are styled in blue. Cells that were given are
            styled in black/bold.
    """
    css = """
    <style>
    table.sudoku {
        border-collapse: collapse;
        margin: 0 auto;
        width: 100%;
        max-width: 400px;
        aspect-ratio: 1;
        font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
    }
    table.sudoku td {
        border: 1px solid #bbb;
        text-align: center;
        vertical-align: middle;
        font-size: clamp(1rem, 4vw, 1.6rem);
        padding: 0;
        width: 11.11%;
        aspect-ratio: 1;
    }
    /* Thick borders for 3x3 box separators */
    table.sudoku td.box-right  { border-right:  2.5px solid #333; }
    table.sudoku td.box-bottom { border-bottom: 2.5px solid #333; }
    table.sudoku td.box-left   { border-left:   2.5px solid #333; }
    table.sudoku td.box-top    { border-top:    2.5px solid #333; }
    /* Cell styles */
    table.sudoku td.given  { color: #111; font-weight: 700; }
    table.sudoku td.solved { color: #2563eb; font-weight: 400; }
    </style>
    """
    rows_html = ""
    for i in range(9):
        cells = ""
        for j in range(9):
            value = board[i][j] if board[i][j] != EMPTY else ""

            # CSS classes for thick box borders
            classes = []
            if j % 3 == 0:
                classes.append("box-left")
            if j % 3 == 2:
                classes.append("box-right")
            if i % 3 == 0:
                classes.append("box-top")
            if i % 3 == 2:
                classes.append("box-bottom")

            # Given vs solved styling
            if original_board is not None and original_board[i][j] == EMPTY:
                classes.append("solved")
            else:
                classes.append("given")

            cls = " ".join(classes)
            cells += f'<td class="{cls}">{value}</td>'
        rows_html += f"<tr>{cells}</tr>"

    return f'{css}<table class="sudoku">{rows_html}</table>'


st.set_page_config(
    page_title="Sudoku Solver",
    page_icon="🧩",
    layout="centered",
)

# --- Header ---
st.title("Sudoku Solver 🧩")
st.caption("Snap a photo. Get the solution.")

# --- Image uploader ---
uploaded_file = st.file_uploader(
    "Upload a puzzle screenshot or photo",
    type=["png", "jpg", "jpeg"],
)

if uploaded_file is not None:
    st.image(uploaded_file, use_container_width=True)

    # Run OCR automatically on upload (only if not already extracted)
    if "original_board" not in st.session_state:
        with st.spinner("Reading puzzle..."):
            image_bytes = uploaded_file.getvalue()
            board = extract_sudoku_board(image_bytes)
            st.session_state.original_board = board
            st.rerun()

# --- Display board ---
if "solved_board" in st.session_state:
    st.markdown(
        render_board_html(
            st.session_state.solved_board,
            original_board=st.session_state.original_board,
        ),
        unsafe_allow_html=True,
    )
elif "original_board" in st.session_state:
    st.markdown(
        render_board_html(st.session_state.original_board),
        unsafe_allow_html=True,
    )

    if st.button("Solve", use_container_width=True):
        board_copy = copy.deepcopy(st.session_state.original_board)
        solutions = solve_sudoku(board_copy)
        if solutions:
            st.session_state.solved_board = solutions[0]
            st.rerun()
        else:
            st.error("No solution found. The extracted puzzle may contain errors.")
