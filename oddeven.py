import streamlit as st
import random
import time

# --- 게임 상태 관리 ---
if 'balance' not in st.session_state:
    st.session_state.balance = 10000
    st.session_state.game_in_progress = False
    st.session_state.bet_amount = 0
    st.session_state.player_choice = None
    st.session_state.game_result = None

# --- UI 컴포넌트 ---
st.title("홀짝홀짝홀짝")

# 현재 잔액 표시
st.markdown(f"**현재 잔액:** **{st.session_state.balance}** 원")
st.markdown("---")

# 베팅 섹션
if not st.session_state.game_in_progress:
    st.subheader("베팅하기")
    
    # 플레이어가 홀 또는 짝을 선택
    player_choice = st.radio("홀 또는 짝을 선택하세요:", ["홀 (Odd)", "짝 (Even)"])
    st.session_state.player_choice = player_choice
    
    # 베팅 금액 입력
    bet_amount = st.number_input(
        "베팅 금액을 입력하세요:", 
        min_value=100, 
        max_value=st.session_state.balance, 
        step=100
    )
    st.session_state.bet_amount = bet_amount

    # 게임 시작 버튼
    if st.button("게임 시작!", use_container_width=True):
        if st.session_state.balance >= st.session_state.bet_amount:
            st.session_state.balance -= st.session_state.bet_amount
            st.session_state.game_in_progress = True
            st.experimental_rerun()
        else:
            st.warning("잔액이 부족합니다!")
            
# 게임 진행 중
if st.session_state.game_in_progress:
    st.subheader("결과 확인 중...")
    
    # 스피너를 사용하여 앱이 작업 중임을 표시
    with st.spinner("결과를 계산하는 중..."):
        # 무작위 숫자 결정
        winning_number = random.randint(1, 100)
        
        # 결과 (홀 또는 짝) 결정
        if winning_number % 2 == 0:
            winning_result = "짝 (Even)"
        else:
            winning_result = "홀 (Odd)"
        
        # 긴장감을 위해 1.5초 대기
        time.sleep(1.5)

    st.session_state.game_result = winning_result
    
    # 승패 확인
    if st.session_state.player_choice == st.session_state.game_result:
        win = True
        st.session_state.balance += st.session_state.bet_amount * 2
    else:
        win = False
    
    st.markdown("---")
    
    # 결과 표시
    if win:
        st.balloons()
        st.success(f"🎉 **축하합니다!** 게임에서 이겼습니다!")
        st.success(f"나온 숫자: {winning_number} ({winning_result})")
        st.markdown(f"**{st.session_state.bet_amount * 2}**원을 획득했습니다. 현재 잔액: **{st.session_state.balance}**원")
    else:
        st.error(f"💀 **아쉽네요...** 게임에서 졌습니다.")
        st.error(f"나온 숫자: {winning_number} ({winning_result})")
        st.markdown(f"베팅 금액 **{st.session_state.bet_amount}**원을 모두 잃었습니다. 현재 잔액: **{st.session_state.balance}**원")

    # 새 게임 시작 버튼
    if st.button("새 게임 시작", use_container_width=True):
        # 게임 상태 초기화 및 재실행
        st.session_state.game_in_progress = False
        st.experimental_rerun()
