import tkinter as tk
import config

# 匯入各個遊戲模組
from game_blackjack import BlackjackGame
from game_slots import SlotsGame
from game_wheel import WheelGame


class GameLobbyApp:

    def __init__(self, root):
        self.root = root
        self.root.title("遊戲大廳 Game Lobby")
        self.root.geometry("410x550")
        self.root.configure(bg=config.BG_MAIN)

        # 讀取設定檔的初始籌碼
        self.chips = config.INITIAL_CHIPS

        # 主要的內容容器 (隨時清除並替換遊戲畫面)
        self.main_frame = tk.Frame(self.root, bg=config.BG_MAIN)
        self.main_frame.pack(fill="both", expand=True)

        self.create_main_menu()

    def clear_frame(self):
        """清空畫面的輔助函式"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        """顯示主大廳選單"""
        self.clear_frame()

        # 大廳標題
        tk.Label(
            self.main_frame,
            text="🎮 迷你遊戲大廳",
            font=config.FONT_TITLE,
            fg=config.FG_LIGHT,
            bg=config.BG_MAIN,
        ).pack(pady=30)

        # 籌碼顯示
        tk.Label(
            self.main_frame,
            text=f"目前籌碼: {self.chips} 💰",
            font=config.FONT_LARGE,
            fg=config.FG_GOLD,
            bg=config.BG_MAIN,
        ).pack(pady=10)

        # 按鈕共用樣式
        btn_style = {
            "font": config.FONT_BTN,
            "width": 20,
            "height": 2,
            "bd": 0,
            "cursor": "hand2",
            "fg": "white",
        }

        # 三個遊戲按鈕
        tk.Button(
            self.main_frame,
            text="🎡 抽獎轉盤",
            bg=config.BTN_WHEEL,
            command=self.start_wheel,
            **btn_style,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="🎰 幸運拉霸機",
            bg=config.BTN_SLOTS,
            command=self.start_slots,
            **btn_style,
        ).pack(pady=10)
        tk.Button(
            self.main_frame,
            text="🃏 21點撲克牌",
            bg=config.BTN_BJ,
            command=self.start_blackjack,
            **btn_style,
        ).pack(pady=10)

    # 點擊按鈕後，清除畫面並初始化對應的遊戲類別
    def start_wheel(self):
        self.clear_frame()
        WheelGame(self.main_frame, self)

    def start_slots(self):
        self.clear_frame()
        SlotsGame(self.main_frame, self)

    def start_blackjack(self):
        self.clear_frame()
        BlackjackGame(self.main_frame, self)


if __name__ == "__main__":
    root = tk.Tk()
    app = GameLobbyApp(root)
    root.mainloop()