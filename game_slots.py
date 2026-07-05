import os
import random
import time
import streamlit as st


def run_slots(back_to_lobby):
    st.title("🎰 幸運拉霸機")
    st.subheader(f"目前籌碼: {st.session_state.chips} 💰")

    img_dir = "slot_images"
    images = []

    # 讀取圖片檔案路徑列表
    if os.path.exists(img_dir):
        valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
        images = [
            os.path.join(img_dir, f)
            for f in os.listdir(img_dir)
            if f.lower().endswith(valid_extensions)
        ]

    use_fallback = len(images) < 3
    symbols = ["🍎", "🍌", "🍒", "🍇", "🍋"]

    # 顯示目前格子的容器
    slot_cols = st.columns(3)

    if st.button("🎰 拉下搖桿！ (消費 100)", type="primary"):
        if st.session_state.chips < 100:
            st.error("點數不夠連拉霸機都玩不起囉！")
        else:
            st.session_state.chips -= 100

            # 滾動動畫
            for _ in range(6):
                for i in range(3):
                    with slot_cols[i]:
                        if use_fallback:
                            st.heading(random.choice(symbols))
                        else:
                            st.image(random.choice(images), width=100)
                time.sleep(0.15)

            # 最終開獎
            if use_fallback:
                res = [random.choice(symbols) for _ in range(3)]
                is_win = res[0] == res[1] == res[2]
            else:
                res = [random.choice(images) for _ in range(3)]
                is_win = res[0] == res[1] == res[2]

            st.rerun()  # 重新整理整理籌碼與狀態

    st.write("---")
    if st.button("返回主選單"):
        back_to_lobby()
        st.rerun()