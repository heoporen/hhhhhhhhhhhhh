import streamlit as st
import random
import time

# --- Game State Management ---
if 'balance' not in st.session_state:
    st.session_state.balance = 10000
    st.session_state.game_started = False
    st.session_state.bet_amount = 0
    st.session_state.ladder = None
    st.session_state.result_path = None
    st.session_state.final_result = None

# --- Game Logic ---
def generate_ladder(width, height):
    """Generates a random ladder grid with horizontal rungs."""
    ladder = [[0] * width for _ in range(height)]
    for r in range(height):
        for c in range(width - 1):
            if random.random() < 0.3:  # 30% chance for a rung
                ladder[r][c] = 1
                ladder[r][c+1] = -1 # Mark the right side to prevent overlapping
    return ladder

def get_ladder_path(ladder, start_col):
    """Calculates the path from top to bottom."""
    path = [(0, start_col)]
    current_col = start_col
    for r in range(len(ladder)):
        if current_col < len(ladder[0]) - 1 and ladder[r][current_col] == 1:
            current_col += 1
        elif current_col > 0 and ladder[r][current_col-1] == 1:
            current_col -= 1
        path.append((r + 1, current_col))
    return path, current_col

def run_game():
    """Runs a single game session."""
    st.session_state.game_started = True
    st.session_state.ladder = generate_ladder(5, 10)
    st.session_state.result_path, final_col = get_ladder_path(st.session_state.ladder, random.randint(0, 4))
    st.session_state.final_result = (final_col == 0) # Win if it lands on the first column

# --- UI Components ---
st.title("🎢 사다리 게임")

st.markdown(f"**현재 잔액:** {st.session_state.balance} 원")
st.markdown("---")

# Betting Section
if not st.session_state.game_started:
    st.subheader("베팅하기")
    bet_amount = st.number_input("베팅 금액을 입력하세요:", min_value=100, max_value=st.session_state.balance, step=100)
    st.session_state.bet_amount = bet_amount
    
    if st.button("게임 시작!", use_container_width=True):
        if st.session_state.balance >= st.session_state.bet_amount:
            st.session_state.balance -= st.session_state.bet_amount
            run_game()
            st.experimental_rerun()
        else:
            st.warning("잔액이 부족합니다!")

# Game in Progress
if st.session_state.game_started:
    st.subheader("게임 진행 중...")

    # Display the ladder
    for r in range(10):
        cols = st.columns([1] * 5)
        for c in range(5):
            with cols[c]:
                # Draw vertical lines
                st.write("|", unsafe_allow_html=True)
                
                # Draw horizontal rungs
                if c < 4 and st.session_state.ladder[r][c] == 1:
                    st.write("---", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Animate the path reveal
    placeholder = st.empty()
    for i in range(len(st.session_state.result_path)):
        # Clear previous path
        with placeholder.container():
            st.markdown("### 결과를 찾아가는 중...")
            
            # Draw the ladder with the current path
            for r in range(10):
                cols = st.columns([1] * 5)
                for c in range(5):
                    with cols[c]:
                        if (r, c) in st.session_state.result_path[:i+1]:
                            st.markdown("🔴", unsafe_allow_html=True)
                        else:
                            st.write("|", unsafe_allow_html=True)
                            if c < 4 and st.session_state.ladder[r][c] == 1:
                                st.write("---", unsafe_allow_html=True)
        time.sleep(0.3)
    
    st.balloons()
    
    # Game Result
    if st.session_state.final_result:
        st.success(f"🎉 **축하합니다!** 게임에서 이겼습니다! 베팅 금액의 2배인 {st.session_state.bet_amount * 2}원을 얻었습니다.")
        st.session_state.balance += st.session_state.bet_amount * 2
    else:
        st.error(f"💀 **아쉽네요...** 게임에서 졌습니다. 베팅 금액 {st.session_state.bet_amount}원을 모두 잃었습니다.")
    
    st.markdown("---")
    if st.button("새 게임 시작", use_container_width=True):
        st.session_state.game_started = False
        st.experimental_rerun()

 
