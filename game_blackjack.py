import random
import streamlit as st


def calc_score(hand):
    score = 0
    aces = 0
    for rank, _ in hand:
        if rank in ["J", "Q", "K"]:
            score += 10
        elif rank == "A":
            aces += 1
            score += 11
        else:
            score += int(rank)
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score


def run_blackjack(back_to_lobby):
    st.title("🃏 21點撲克牌")
    st.subheader(f"目前籌碼: {st.session_state.chips} 💰")

    if "bj_game_over" not in st.session_state:
        st.session_state.bj_game_over = True
        st.session_state.player_hand = []
        st.session_state.dealer_hand = []
        st.session_state.deck = []

    if st.session_state.bj_game_over:
        if st.button("開始新對局 (下注 200)", type="primary"):
            if st.session_state.chips < 200:
                st.error("21點最低下注 200 籌碼！")
            else:
                st.session_state.chips -= 200
                suits = ["♠", "♥", "♦", "♣"]
                ranks = [
                    "2",
                    "3",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "J",
                    "Q",
                    "K",
                    "A",
                ]
                st.session_state.deck = [(r, s) for r in ranks for s in suits]
                random.shuffle(st.session_state.deck)

                st.session_state.player_hand = [
                    st.session_state.deck.pop(),
                    st.session_state.deck.pop(),
                ]
                st.session_state.dealer_hand = [
                    st.session_state.deck.pop(),
                    st.session_state.deck.pop(),
                ]
                st.session_state.bj_game_over = False
                st.rerun()
    else:
        p_score = calc_score(st.session_state.player_hand)

        st.write(
            f"**莊家的牌：** {st.session_state.dealer_hand[0][0]}{st.session_state.dealer_hand[0][1]} ＋ [隱藏]"
        )
        st.write(
            f"**你的牌：** {' '.join([f'{r}{s}' for r, s in st.session_state.player_hand])} (點數: {p_score})"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("要牌 (Hit)", width="stretch"):
                st.session_state.player_hand.append(st.session_state.deck.pop())
                if calc_score(st.session_state.player_hand) > 21:
                    st.error("💥 你爆掉了！莊家獲勝！")
                    st.session_state.bj_game_over = True
                st.rerun()

        with col2:
            if st.button("停牌 (Stand)", width="stretch"):
                while calc_score(st.session_state.dealer_hand) < 17:
                    st.session_state.dealer_hand.append(
                        st.session_state.deck.pop()
                    )

                d_score = calc_score(st.session_state.dealer_hand)
                p_score = calc_score(st.session_state.player_hand)

                st.write(
                    f"**莊家最終牌：** {' '.join([f'{r}{s}' for r, s in st.session_state.dealer_hand])} (點數: {d_score})"
                )

                if d_score > 21:
                    st.success("🎉 莊家爆掉了！你贏了！")
                    st.session_state.chips += 400
                elif p_score > d_score:
                    st.success("🎉 你贏了！")
                    st.session_state.chips += 400
                elif p_score < d_score:
                    st.error("❌ 莊家獲勝！")
                else:
                    st.info("🤝 平手！籌碼退回。")
                    st.session_state.chips += 200

                st.session_state.bj_game_over = True
                if st.button("確認結果", width="stretch"):
                    st.rerun()

    st.write("---")
    if st.button("返回主選單", width="content"):
        back_to_lobby()
        st.rerun()