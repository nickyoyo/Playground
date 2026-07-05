import random
import tkinter as tk
from tkinter import messagebox
import config


class BlackjackGame:

    def __init__(self, parent_frame, app_instance):
        self.frame = parent_frame
        self.app = app_instance

        tk.Label(
            self.frame,
            text="🃏 21點撲克牌",
            font=config.FONT_SUBTITLE,
            fg=config.FG_LIGHT,
            bg=config.BG_MAIN,
        ).pack(pady=10)

        self.deck = []
        self.player_hand = []
        self.dealer_hand = []

        # UI元件
        self.dealer_label = tk.Label(
            self.frame,
            text="莊家的牌: ",
            font=config.FONT_NORMAL,
            fg=config.FG_LIGHT,
            bg=config.BG_MAIN,
        )
        self.dealer_label.pack(pady=5)

        self.player_label = tk.Label(
            self.frame,
            text="你的牌: ",
            font=config.FONT_NORMAL,
            fg=config.FG_LIGHT,
            bg=config.BG_MAIN,
        )
        self.player_label.pack(pady=5)

        self.status_label = tk.Label(
            self.frame,
            text="下注 200 開始遊戲",
            font=config.FONT_LARGE,
            fg=config.FG_GOLD,
            bg=config.BG_MAIN,
        )
        self.status_label.pack(pady=10)

        # 按鈕區域
        btn_frame = tk.Frame(self.frame, bg=config.BG_MAIN)
        btn_frame.pack(pady=10)

        self.btn_hit = tk.Button(
            btn_frame,
            text="要牌 (Hit)",
            state="disabled",
            bg=config.BTN_ACTION,
            fg="white",
            command=self.hit,
        )
        self.btn_hit.grid(row=0, column=0, padx=5)

        self.btn_stand = tk.Button(
            btn_frame,
            text="停牌 (Stand)",
            state="disabled",
            bg=config.BTN_SLOTS,
            fg="white",
            command=self.stand,
        )
        self.btn_stand.grid(row=0, column=1, padx=5)

        tk.Button(
            self.frame,
            text="開始新對局 (下注 200)",
            font=config.FONT_BTN,
            bg=config.BTN_BJ,
            fg="white",
            command=self.start_game,
        ).pack(pady=5)
        tk.Button(
            self.frame,
            text="返回主選單",
            font=config.FONT_BTN,
            bg=config.BTN_BACK,
            fg="white",
            command=self.app.create_main_menu,
        ).pack(pady=15)

    def calc_score(self, hand):
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

    def update_ui(self, show_all_dealer=False):
        if show_all_dealer:
            d_text = (
                "莊家的牌: "
                + " ".join([f"{r}{s}" for r, s in self.dealer_hand])
                + f" (點數: {self.calc_score(self.dealer_hand)})"
            )
        else:
            d_text = f"莊家的牌: {self.dealer_hand[0][0]}{self.dealer_hand[0][1]} [隱藏]"

        p_text = (
            "你的牌: "
            + " ".join([f"{r}{s}" for r, s in self.player_hand])
            + f" (點數: {self.calc_score(self.player_hand)})"
        )
        self.dealer_label.config(text=d_text)
        self.player_label.config(text=p_text)

    def start_game(self):
        if self.app.chips < 200:
            messagebox.showwarning("餘額不足", "21點最低下注 200 籌碼！")
            return
        self.app.chips -= 200

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
        self.deck = [(r, s) for r in ranks for s in suits]
        random.shuffle(self.deck)

        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.dealer_hand = [self.deck.pop(), self.deck.pop()]

        self.status_label.config(text="請選擇要牌或停牌...")
        self.btn_hit.config(state="normal")
        self.btn_stand.config(state="normal")
        self.update_ui()

    def hit(self):
        self.player_hand.append(self.deck.pop())
        self.update_ui()
        if self.calc_score(self.player_hand) > 21:
            self.status_label.config(text="💥 你爆掉了！ 莊家獲勝！")
            self.end_game(False)

    def stand(self):
        self.update_ui(show_all_dealer=True)
        while self.calc_score(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
            self.update_ui(show_all_dealer=True)

        p_score = self.calc_score(self.player_hand)
        d_score = self.calc_score(self.dealer_hand)

        if d_score > 21:
            self.status_label.config(text="🎉 莊家爆掉了！你贏了！")
            self.end_game(True)
        elif p_score > d_score:
            self.status_label.config(text="🎉 你贏了！")
            self.end_game(True)
        elif p_score < d_score:
            self.status_label.config(text="❌ 莊家獲勝！")
            self.end_game(False)
        else:
            self.status_label.config(text="🤝 平手！籌碼退回。")
            self.app.chips += 200
            self.btn_hit.config(state="disabled")
            self.btn_stand.config(state="disabled")

    def end_game(self, player_won):
        if player_won:
            self.app.chips += 400
        self.btn_hit.config(state="disabled")
        self.btn_stand.config(state="disabled")