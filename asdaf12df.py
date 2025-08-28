import streamlit as st
import random

# Game settings
BOARD_SIZE = 8  # Size of the board (8x8)
NUM_MINES = 10  # Number of mines

# Function to initialize the board state
def initialize_board():
    """Initializes the game board and state."""
    # The hidden board (contents: 'M' for mine, 0-8 for numbers)
    st.session_state.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    # The board displayed to the user (state: 'H' hidden, 'R' revealed, 'F' flagged)
    st.session_state.display_board = [['H' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.game_over = False
    st.session_state.game_won = False

    # Randomly place mines
    mine_positions = random.sample(range(BOARD_SIZE * BOARD_SIZE), NUM_MINES)
    for pos in mine_positions:
        row, col = divmod(pos, BOARD_SIZE)
        st.session_state.board[row][col] = 'M'

    # Calculate the number of adjacent mines for each cell
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if st.session_state.board[r][c] != 'M':
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and st.session_state.board[nr][nc] == 'M':
                            count += 1
                st.session_state.board[r][c] = count

# Recursive function to reveal empty cells
def reveal_cell(r, c):
    """Reveals a cell and its neighbors if it is a zero."""
    if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
        return
    if st.session_state.display_board[r][c] != 'H':
        return

    st.session_state.display_board[r][c] = 'R'
    if st.session_state.board[r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if not (dr == 0 and dc == 0):
                    reveal_cell(r + dr, c + dc)

# Check for win condition
def check_win():
    """Checks if all non-mine cells have been revealed."""
    revealed_count = sum(row.count('R') for row in st.session_state.display_board)
    if revealed_count == BOARD_SIZE * BOARD_SIZE - NUM_MINES:
        st.session_state.game_won = True
        st.session_state.game_over = True
        st.experimental_rerun()

# Handle user clicks
def handle_click(r, c, is_flag_mode):
    """Handles a user's click on a cell."""
    if st.session_state.game_over:
        return

    if is_flag_mode:
        # Flag mode: toggle flag on and off
        if st.session_state.display_board[r][c] == 'H':
            st.session_state.display_board[r][c] = 'F'
        elif st.session_state.display_board[r][c] == 'F':
            st.session_state.display_board[r][c] = 'H'
    else:
        # Standard click mode: reveal the cell
        if st.session_state.display_board[r][c] == 'F':
            return  # Do not reveal a flagged cell

        if st.session_state.board[r][c] == 'M':
            # Stepped on a mine
            st.session_state.game_over = True
            st.session_state.game_won = False
            st.experimental_rerun()
        else:
            # Revealed a non-mine cell
            reveal_cell(r, c)
            check_win()

# --- Streamlit App UI ---
st.title("지뢰찾기 💣")

# Initialize the game if it hasn't been already
if 'game_over' not in st.session_state:
    initialize_board()

# Display game status
if st.session_state.game_won:
    st.success("🎉 축하합니다! 모든 지뢰를 피하고 승리했습니다!")
elif st.session_state.game_over:
    st.error("💥 게임 오버! 지뢰를 밟았습니다.")
else:
    st.info("게임을 진행 중입니다. 지뢰를 찾아보세요!")

# "New Game" button
if st.button("새 게임 시작", key="reset_button"):
    initialize_board()

# Checkbox for flag mode
is_flag_mode = st.checkbox("🚩 깃발 모드")
st.markdown("---")

# Draw the game board
for r in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for c in range(BOARD_SIZE):
        with cols[c]:
            cell_state = st.session_state.display_board[r][c]

            button_label = "⬜" # Default hidden cell
            if cell_state == 'R':
                value = st.session_state.board[r][c]
                if value == 'M':
                    button_label = "💣"
                elif value > 0:
                    button_label = str(value)
                else: # value == 0
                    button_label = " "
            elif cell_state == 'F':
                button_label = "🚩"

            # Show all mines when the game is over
            if st.session_state.game_over and cell_state == 'H' and st.session_state.board[r][c] == 'M':
                button_label = "💣"

            # Create the button and handle the click event
            if st.button(button_label, key=f"cell_{r}_{c}"):
                handle_click(r, c, is_flag_mode)

