import os
import random
import time
import streamlit as st


def run_slots(back_to_lobby):
    # 主介面頂部資訊
    st.title("🎰 幸運拉霸機")
    st.subheader(f"目前籌碼: {st.session_state.chips} 💰")

    # 1. 讀取資料夾內的圖片
    img_dir = "slot_images"
    images = []
    if os.path.exists(img_dir):
        valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
        images = [
            os.path.join(img_dir, f)
            for f in os.listdir(img_dir)
            if f.lower().endswith(valid_extensions)
        ]

    use_fallback = len(images) < 3
    symbols = ["🍎", "🍌", "🍒", "🍇", "🍋"]

    # 2. 建立乾淨的三個欄位
    slot_cols = st.columns(3)
    placeholders = []

    with slot_cols[0]:
        placeholders.append(st.empty())
    with slot_cols[1]:
        placeholders.append(st.empty())
    with slot_cols[2]:
        placeholders.append(st.empty())

    # 3. 使用 session_state 記錄最後畫面，確保結果不跳回
    if "last_slot_res" not in st.session_state:
        st.session_state.last_slot_res = [0, 0, 0] if use_fallback else []

    # 初始化或維持上一次的畫面
    for i in range(3):
        if use_fallback:
            current_sym = (
                st.session_state.last_slot_res[i]
                if st.session_state.last_slot_res[i] != 0
                else "❓"
            )
            placeholders[i].markdown(
                f"<h1 style='text-align: center; margin: 0;'>{current_sym}</h1>",
                unsafe_allow_html=True,
            )
        else:
            current_img = (
                st.session_state.last_slot_res[i]
                if st.session_state.last_slot_res
                else images[0]
            )
            placeholders[i].image(current_img, width="stretch")

    # 狀態與結果訊息區
    msg_placeholder = st.empty()

    # 4. 按下按鈕開始轉動
    if st.button("🎰 拉下搖桿！ (消費 100 籌碼)", type="primary"):
        if st.session_state.chips < 100:
            msg_placeholder.error("點數不夠連拉霸機都玩不起囉！")
        else:
            # 扣除籌碼
            st.session_state.chips -= 100
            msg_placeholder.warning("🌀 滾動中... 祝你好運！")

            # --- 🎢 圖片旋轉過程動畫 ---
            for _ in range(12):
                for i in range(3):
                    if use_fallback:
                        current_sym = random.choice(symbols)
                        placeholders[i].markdown(
                            f"<h1 style='text-align: center; margin: 0;'>{current_sym}</h1>",
                            unsafe_allow_html=True,
                        )
                    else:
                        current_img = random.choice(images)
                        placeholders[i].image(current_img, width="stretch")
                time.sleep(0.1)

            # --- 🛑 最終開獎結果 ---
            final_res = []
            final_displays = []
            for i in range(3):
                if use_fallback:
                    chosen = random.choice(symbols)
                    placeholders[i].markdown(
                        f"<h1 style='text-align: center; margin: 0;'>{chosen}</h1>",
                        unsafe_allow_html=True,
                    )
                    final_displays.append(chosen)
                    final_res.append(chosen)
                else:
                    chosen = random.choice(images)
                    placeholders[i].image(chosen, width="stretch")
                    final_displays.append(chosen)
                    final_res.append(os.path.basename(chosen))

            # 將結果存入記憶
            st.session_state.last_slot_res = final_displays

            # 判斷是否中獎
            is_win = final_res[0] == final_res[1] == final_res[2]

            if is_win:
                st.session_state.chips += 1000
                st.balloons()
                msg_placeholder.success("🎉 中大獎了！連成一線獲得 1000 籌碼！")
            else:
                msg_placeholder.error("❌ 殘念！沒中獎。再拉一輪拼手氣！")

            # 2026年最新規範：使用 height=1 的 iframe 完美隱形刷新
            st.iframe("javascript:parent.window.location.reload();", height=1)
            st.rerun()

    st.write("---")
    if st.button("返回主選單", width="content"):
        if "last_slot_res" in st.session_state:
            del st.session_state.last_slot_res
        back_to_lobby()
        st.rerun()