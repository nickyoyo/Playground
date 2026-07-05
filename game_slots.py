import os
import random
import time
import streamlit as st


def run_slots(back_to_lobby):
    st.title("🎰 幸運拉霸機")
    st.subheader(f"目前籌碼: {st.session_state.chips} 💰")

    img_dir = "slot_images"
    images = []

    # 1. 讀取資料夾內的圖片
    if os.path.exists(img_dir):
        valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
        images = [
            os.path.join(img_dir, f)
            for f in os.listdir(img_dir)
            if f.lower().endswith(valid_extensions)
        ]

    # 防呆機制：如果圖片不夠，改用 Emoji
    use_fallback = len(images) < 3
    symbols = ["🍎", "🍌", "🍒", "🍇", "🍋"]

    # 2. 建立三個欄位的「動態容器」
    slot_cols = st.columns(3)
    placeholders = []
    with slot_cols[0]:
        placeholders.append(st.empty())
    with slot_cols[1]:
        placeholders.append(st.empty())
    with slot_cols[2]:
        placeholders.append(st.empty())

    # 初始靜態畫面顯示
    for i in range(3):
        if use_fallback:
            placeholders[i].markdown(
                "<h1 style='text-align: center;'>❓</h1>",
                unsafe_allow_html=True,
            )
        else:
            placeholders[i].image(images[0], width=150)

    # 建立結果與訊息通知專用的空白容器
    msg_placeholder = st.empty()
    msg_placeholder.info("試試連成一線！(消費 100 籌碼)")

    # 3. 按下按鈕開始轉動
    if st.button("🎰 拉下搖桿！", type="primary"):
        if st.session_state.chips < 100:
            msg_placeholder.error("點數不夠連拉霸機都玩不起囉！")
        else:
            # 扣除籌碼
            st.session_state.chips -= 100
            msg_placeholder.warning("🌀 滾動中... 祝你好運！")

            # --- 🎢 圖片旋轉過程 (動畫效果) ---
            # 滾動 12 次，每次稍微停留一下，營造動態感
            for _ in range(12):
                for i in range(3):
                    if use_fallback:
                        current_sym = random.choice(symbols)
                        placeholders[i].markdown(
                            f"<h1 style='text-align: center;'>{current_sym}</h1>",
                            unsafe_allow_html=True,
                        )
                    else:
                        current_img = random.choice(images)
                        placeholders[i].image(current_img, width=150)
                time.sleep(0.1)  # 控制滾動速度 (秒)

            # --- 🛑 最終開獎結果 ---
            final_res = []
            for i in range(3):
                if use_fallback:
                    chosen = random.choice(symbols)
                    placeholders[i].markdown(
                        f"<h1 style='text-align: center;'>{chosen}</h1>",
                        unsafe_allow_html=True,
                    )
                    final_res.append(chosen)
                else:
                    chosen = random.choice(images)
                    placeholders[i].image(chosen, width=150)
                    # 擷取檔名來做為中獎判斷依據，避免記憶體圖案物件對比失敗
                    final_res.append(os.path.basename(chosen))

            # 判斷是否三張圖片/文字完全相同
            is_win = final_res[0] == final_res[1] == final_res[2]

            # 顯示對應的獎懲與特效
            if is_win:
                st.session_state.chips += 1000
                st.balloons()  # 噴全螢幕氣球慶祝！
                msg_placeholder.success("🎉 中大獎了！連成一線獲得 1000 籌碼！")
            else:
                msg_placeholder.error("❌ 殘念！沒中獎，再接再厲！")

            # 為了即時更新大廳頂部的籌碼文字，重新引導畫面
            time.sleep(1.5)
            st.rerun()

    st.write("---")
    if st.button("返回主選單"):
        back_to_lobby()
        st.rerun()