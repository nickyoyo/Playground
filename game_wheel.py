import random
import time
import streamlit as st


def run_wheel(back_to_lobby):
    st.title("🎡 抽獎轉盤")
    st.subheader(f"目前籌碼: {st.session_state.chips} 💰")

    prizes = [
        ("銘謝惠顧", 0),
        ("小獎 (+50)", 50),
        ("中獎 (+100)", 100),
        ("大獎 (+500)", 500),
    ]

    if st.button("花費 50 籌碼旋轉！", type="primary"):
        if st.session_state.chips < 50:
            st.error("籌碼不足囉！")
        else:
            st.session_state.chips -= 50

            # 模擬轉動動效
            status = st.empty()
            for _ in range(5):
                status.write(f"🌀 旋轉中... {random.choice(prizes)[0]}")
                time.sleep(0.2)

            prize_name, prize_value = random.choice(prizes)
            st.session_state.chips += prize_value

            status.empty()
            st.balloons() if prize_value > 0 else None
            st.success(f"🎉 結果：{prize_name}！")
            st.rerun()

    st.write("---")
    if st.button("返回主選單"):
        back_to_lobby()
        st.rerun()