import streamlit as st
import random
import time

# --- Game State Management ---
if 'balance' not in st.session_state:
    st.session_state.balance = 10000
    st.session_state.game_in_progress = False
    st.session_state.bet_amount = 0
    st.session_state.player_choice = None
    st.session_state.game_result = None

# --- UI Components ---
st.title("홀짝홀짝홀짝홀짝")

# Display current balance
st.markdown(f"**현재 잔액:** **{st.session_state.balance}** 원")
st.markdown("---")

# Betting Section
if not st.session_state.game_in_progress:
    st.subheader("베팅하기")
    
    # User selects Odd or Even
    player_choice = st.radio("홀 또는 짝을 선택하세요:", ["홀 (Odd)", "짝 (Even)"])
    st.session_state.player_choice = player_choice
    
    # User inputs bet amount
    bet_amount = st.number_input(
        "베팅 금액을 입력하세요:", 
        min_value=100, 
        max_value=st.session_state.balance, 
        step=100
    )
    st.session_state.bet_amount = bet_amount

    # Start Game Button
    if st.button("게임 시작!", use_container_width=True):
        if st.session_state.balance >= st.session_state.bet_amount:
            st.session_state.balance -= st.session_state.bet_amount
            st.session_state.game_in_progress = True
            st.experimental_rerun()
        else:
            st.warning("잔액이 부족합니다!")
            
# Game in Progress
if st.session_state.game_in_progress:
    st.subheader("결과 확인 중...")
    
    # Placeholder for displaying the animation
    placeholder = st.empty()
    
    # Simple animation to create tension
    with placeholder.container():
        st.info("카드를 섞는 중... 🃏")
    time.sleep(1)
    
    with placeholder.container():
        st.info("결정 중... 🤔")
    time.sleep(1)

    # Determine a random number
    winning_number = random.randint(1, 100)
    
    # Determine the result (Odd or Even)
    if winning_number % 2 == 0:
        winning_result = "짝 (Even)"
    else:
        winning_result = "홀 (Odd)"
        
    st.session_state.game_result = winning_result
    
    # Check if the player won
    if st.session_state.player_choice == st.session_state.game_result:
        win = True
        st.session_state.balance += st.session_state.bet_amount * 2
    else:
        win = False
    
    st.markdown("---")
    
    # Display results
    if win:
        st.balloons()
        st.success(f"🎉 **축하합니다!** 게임에서 이겼습니다!")
        st.success(f"나온 숫자: {winning_number} ({winning_result})")
        st.markdown(f"**{st.session_state.bet_amount * 2}**원을 획득했습니다. 현재 잔액: **{st.session_state.balance}**원")
    else:
        st.error(f"💀 **아쉽네요...** 게임에서 졌습니다.")
        st.error(f"나온 숫자: {winning_number} ({winning_result})")
        st.markdown(f"베팅 금액 **{st.session_state.bet_amount}**원을 모두 잃었습니다. 현재 잔액: **{st.session_state.balance}**원")

    # Start New Game button
    if st.button("새 게임 시작", use_container_width=True):
        st.session_state.game_in_progress = False
        st.experimental_rerun()
