import streamlit as st
import random

# Attack on Titan characters with their strengths and image URLs
# NOTE: The images are placeholders for demonstration.
AOT_CHARACTERS = {
    "에렌 예거 (Eren Yeager)": {"strength": 90, "titan": True, "image": "https://upload.wikimedia.org/wikipedia/en/2/23/Eren_Yeager_%28character%29.png"},
    "미카사 아커만 (Mikasa Ackerman)": {"strength": 95, "titan": False, "image": "https://upload.wikimedia.org/wikipedia/en/e/e0/Mikasa_Ackermann.png"},
    "리바이 아커만 (Levi Ackerman)": {"strength": 100, "titan": False, "image": "https://upload.wikimedia.org/wikipedia/en/d/d3/Levi_Ackerman.png"},
    "아르민 알레르토 (Armin Arlert)": {"strength": 70, "titan": True, "image": "https://upload.wikimedia.org/wikipedia/en/0/07/Armin_Arlert.png"},
    "엘빈 스미스 (Erwin Smith)": {"strength": 85, "titan": False, "image": "https://upload.wikimedia.org/wikipedia/en/8/87/Erwin_Smith.png"},
    "한지 조에 (Hange Zoe)": {"strength": 80, "titan": False, "image": "https://upload.wikimedia.org/wikipedia/en/a/a2/Hange_Zoe.png"},
    "라이너 브라운 (Reiner Braun)": {"strength": 88, "titan": True, "image": "https://upload.wikimedia.org/wikipedia/en/a/a2/Reiner_Braun.png"},
    "베르톨트 후버 (Bertholdt Hoover)": {"strength": 92, "titan": True, "image": "https://upload.wikimedia.org/wikipedia/en/a/a3/Bertholdt_Hoover.png"},
    "지크 예거 (Zeke Yeager)": {"strength": 91, "titan": True, "image": "https://upload.wikimedia.org/wikipedia/en/8/88/Zeke_Yeager.png"},
    "케니 아커만 (Kenny Ackerman)": {"strength": 96, "titan": False, "image": "https://static.wikia.nocookie.net/shingekinokyojin/images/e/e5/Kenny_Ackerman_%28Anime%29_character_image.png"},
    "장 키르슈타인 (Jean Kirschtein)": {"strength": 83, "titan": False, "image": "https://upload.wikimedia.org/wikipedia/en/d/df/Jean_Kirstein.png"},
    "코니 스프링거 (Connie Springer)": {"strength": 75, "titan": False, "image": "https://upload.wikimedia.org/wikipedia/en/a/a0/Connie_Springer.png"},
    "사샤 블라우스 (Sasha Blouse)": {"strength": 78, "titan": False, "image": "https://upload.wikimedia.org/wikipedia/en/e/ed/Sasha_Blouse.png"},
    "페트라 라르 (Petra Ral)": {"strength": 82, "titan": False, "image": "https://static.wikia.nocookie.net/shingekinokyojin/images/9/90/Petra_Ral_%28Anime%29_character_image.png"},
    "애니 레온하트 (Annie Leonhart)": {"strength": 90, "titan": True, "image": "https://upload.wikimedia.org/wikipedia/en/e/e4/Annie_Leonhart.png"},
    "피크 핑거 (Pieck Finger)": {"strength": 89, "titan": True, "image": "https://upload.wikimedia.org/wikipedia/en/3/36/Pieck_Finger.png"},
}

def get_winner(character1, character2):
    """
    Determines the winner of a battle between two characters based on their strength.
    A small random factor is added to make battles less predictable.
    """
    strength1 = AOT_CHARACTERS[character1]["strength"] + random.randint(-5, 5)
    strength2 = AOT_CHARACTERS[character2]["strength"] + random.randint(-5, 5)

    st.markdown(f"**{character1}**의 전투력: {strength1}")
    st.markdown(f"**{character2}**의 전투력: {strength2}")
    
    if strength1 > strength2:
        return character1
    elif strength2 > strength1:
        return character2
    else:
        return "무승부"

st.title("⚔️ 진격의 거인 캐릭터 왕중왕전")
st.markdown("두 캐릭터를 선택하여 누가 더 강한지 겨뤄보세요!")
st.markdown("---")

# Get list of character names
character_names = list(AOT_CHARACTERS.keys())

# Let the user select two characters
col1, col2 = st.columns(2)

with col1:
    st.header("캐릭터 1")
    char1 = st.selectbox("첫 번째 캐릭터를 선택하세요:", character_names, key="char1_select")
    st.image(AOT_CHARACTERS[char1]["image"], caption=char1, width=200)

with col2:
    st.header("캐릭터 2")
    # Ensure the second character cannot be the same as the first
    char2_options = [name for name in character_names if name != char1]
    char2 = st.selectbox("두 번째 캐릭터를 선택하세요:", char2_options, key="char2_select")
    st.image(AOT_CHARACTERS[char2]["image"], caption=char2, width=200)

st.markdown("---")

# Battle button
if st.button("왕중왕전 시작!", use_container_width=True):
    st.subheader("🔥🔥 배틀 결과 🔥🔥")
    
    winner = get_winner(char1, char2)
    
    st.markdown("### 결과")
    if winner == "무승부":
        st.warning("무승부입니다! 두 캐릭터의 실력은 비슷하네요.")
    else:
        st.success(f"**🥇 승자: {winner}**")
        if winner == char1:
            loser = char2
        else:
            loser = char1
        st.error(f"**💀 패자: {loser}**")

    # Display additional info about the characters
    st.markdown("---")
    st.subheader("캐릭터 정보")
    
    st.write(f"**{char1}**")
    st.write(f"전투력: {AOT_CHARACTERS[char1]['strength']}")
    st.write(f"거인 능력 여부: {'있음' if AOT_CHARACTERS[char1]['titan'] else '없음'}")

    st.write(f"**{char2}**")
    st.write(f"전투력: {AOT_CHARACTERS[char2]['strength']}")
    st.write(f"거인 능력 여부: {'있음' if AOT_CHARACTERS[char2]['titan'] else '없음'}")

