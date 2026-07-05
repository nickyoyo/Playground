import random
import tkinter as tk
import config


class WheelGame:

    def __init__(self, parent_frame, app_instance):
        self.frame = parent_frame
        self.app = app_instance

        # 標題
        tk.Label(
            self.frame,
            text="🎡 抽獎轉盤",
            font=config.FONT_SUBTITLE,
            fg=config.FG_LIGHT,
            bg=config.BG_MAIN,
        ).pack(pady=20)

        # 獎項設定
        self.prizes = [
            ("銘謝惠顧", 0),
            ("小獎 (+50)", 50),
            ("中獎 (+100)", 100),
            ("大獎 (+500)", 500),
        ]

        self.result_var = tk.StringVar(value="試試你的手氣吧！")
        tk.Label(
            self.frame,
            textvariable=self.result_var,
            font=config.FONT_LARGE,
            fg=config.FG_GOLD,
            bg=config.BG_MAIN,
        ).pack(pady=40)

        # 籌碼顯示
        self.chips_display = tk.Label(
            self.frame,
            text=f"目前籌碼: {self.app.chips} 💰",
            font=config.FONT_NORMAL,
            fg=config.FG_LIGHT,
            bg=config.BG_MAIN,
        )
        self.chips_display.pack()

        # 按鈕
        tk.Button(
            self.frame,
            text="花費 50 籌碼旋轉！",
            font=config.FONT_BTN,
            bg=config.BTN_WHEEL,
            fg="white",
            command=self.spin,
        ).pack(pady=10)
        tk.Button(
            self.frame,
            text="返回主選單",
            font=config.FONT_BTN,
            bg=config.BTN_BACK,
            fg="white",
            command=self.app.create_main_menu,
        ).pack(pady=20)

    def spin(self):
        if self.app.chips < 50:
            from tkinter import messagebox

            messagebox.showwarning(
                "餘額不足", "轉一次需要 50 籌碼，你點數不夠囉！"
            )
            return

        self.app.chips -= 50
        self.chips_display.config(text=f"目前籌碼: {self.app.chips} 💰")

        def animate(count):
            if count > 0:
                self.result_var.set(
                    f"🌀 旋轉中... {random.choice(self.prizes)[0]} 🌀"
                )
                self.frame.after(100, lambda: animate(count - 1))
            else:
                prize_name, prize_value = random.choice(self.prizes)
                self.app.chips += prize_value
                self.result_var.set(f"🎉 結果：{prize_name}！")
                self.chips_display.config(text=f"目前籌碼: {self.app.chips} 💰")

        animate(10)