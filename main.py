import streamlit as st
import config

# 匯入各個遊戲頁面
from game_blackjack import run_blackjack
from game_slots import run_slots
from game_wheel import run_wheel

# 初始化 Session State (確保重新整理時籌碼和頁面狀態不會消失)
if "chips" not in st.session_state:
    st.session_state.chips = config.INITIAL_CHIPS

if "page" not in st.session_state:
    st.session_state.page = "lobby"

st.set_page_config(page_title="迷你遊戲大廳", page_icon="🎮", layout="centered")


# 返回大廳的函式
def go_to_lobby():
    st.session_state.page = "lobby"


# --- 遊戲大廳畫面 ---
if st.session_state.page == "lobby":
    st.title("🎮 迷你遊戲大廳")
    st.subheader(f"目前籌碼: {st.session_state.chips} 💰")
    st.write("---")

    # 🎮 遊戲選單區
    st.write("### 🎰 請選擇遊戲")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🎡 抽獎轉盤", width="stretch"):
            st.session_state.page = "wheel"
            st.rerun()

    with col2:
        if st.button("🎰 幸運拉霸機", width="stretch"):
            st.session_state.page = "slots"
            st.rerun()

    with col3:
        if st.button("🃏 21點撲克牌", width="stretch"):
            st.session_state.page = "blackjack"
            st.rerun()

    st.write("---")

    # 💰 儲值中心區
    st.write("### 💳 籌碼儲值中心")
    
    # 建立輸入框，預設為 500 籌碼，最小可輸入 1
    deposit_amount = st.number_input(
        "請輸入欲儲值的籌碼金額：",
        min_value=1,
        value=500,
        step=100
    )
    
    if st.button("💵 確認儲值", type="primary"):
        st.session_state.chips += int(deposit_amount)
        st.success(f"🎉 成功儲值 {deposit_amount} 籌碼！祝您發大財！")
        # 停頓一下讓玩家看見成功訊息，隨後重新整理同步頂部籌碼
        import time
        time.sleep(1)
        st.rerun()

# --- 路由切換 ---
elif st.session_state.page == "wheel":
    run_wheel(go_to_lobby)
elif st.session_state.page == "slots":
    run_slots(go_to_lobby)
elif st.session_state.page == "blackjack":
    run_blackjack(go_to_lobby)