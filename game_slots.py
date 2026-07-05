import os
import random
import tkinter as tk
from tkinter import messagebox
import config
from PIL import Image, ImageTk


class SlotsGame:

    def __init__(self, parent_frame, app_instance):
        self.frame = parent_frame
        self.app = app_instance

        tk.Label(
            self.frame,
            text="🎰 幸運拉霸機",
            font=config.FONT_SUBTITLE,
            fg=config.FG_LIGHT,
            bg=config.BG_MAIN,
        ).pack(pady=10)

        # 讀取圖片
        img_dir = "slot_images"
        self.slot_images = []

        if os.path.exists(img_dir):
            valid_extensions = (".png", ".jpg", ".jpeg", ".bmp")
            for f in os.listdir(img_dir):
                if f.lower().endswith(valid_extensions):
                    try:
                        img = Image.open(os.path.join(img_dir, f))
                        img = img.resize((80, 80), Image.Resampling.LANCZOS)
                        self.slot_images.append(ImageTk.PhotoImage(img))
                    except Exception as e:
                        print(f"無法讀取圖片 {f}: {e}")

        # 防呆文字模式
        self.use_fallback = len(self.slot_images) < 3
        if self.use_fallback:
            self.fallback_symbols = ["🍎", "🍌", "🍒", "🍇", "🍋"]

        # 建立拉霸滾輪畫面
        slot_frame = tk.Frame(self.frame, bg=config.BG_MAIN)
        slot_frame.pack(pady=20)

        self.slots = []
        for i in range(3):
            lbl = tk.Label(
                slot_frame,
                width=80,
                height=80,
                bg="white",
                bd=3,
                relief="sunken",
            )
            if self.use_fallback:
                lbl.config(
                    text="❓", font=("Helvetica", 36), width=3, height=1
                )
            lbl.grid(row=0, column=i, padx=10)
            self.slots.append(lbl)

        self.result_label = tk.Label(
            self.frame,
            text="試試連成一線！(消費 100)",
            font=config.FONT_NORMAL,
            fg=config.FG_GOLD,
            bg=config.BG_MAIN,
        )
        self.result_label.pack(pady=10)

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
            text="🎰 拉下搖桿！",
            font=config.FONT_BTN,
            bg=config.BTN_SLOTS,
            fg="white",
            command=self.pull_lever,
        ).pack(pady=10)
        tk.Button(
            self.frame,
            text="返回主選單",
            font=config.FONT_BTN,
            bg=config.BTN_BACK,
            fg="white",
            command=self.app.create_main_menu,
        ).pack(pady=10)

    def pull_lever(self):
        if self.app.chips < 100:
            messagebox.showwarning("餘額不足", "點數不夠囉！")
            return
        self.app.chips -= 100
        self.chips_display.config(text=f"目前籌碼: {self.app.chips} 💰")

        def animate(count):
            if count > 0:
                if self.use_fallback:
                    for s in self.slots:
                        s.config(text=random.choice(self.fallback_symbols))
                else:
                    for s in self.slots:
                        s.config(image=random.choice(self.slot_images))
                self.frame.after(80, lambda: animate(count - 1))
            else:
                if self.use_fallback:
                    res = [
                        random.choice(self.fallback_symbols) for _ in range(3)
                    ]
                    for i in range(3):
                        self.slots[i].config(text=res[i])
                    is_win = res[0] == res[1] == res[2]
                else:
                    res_idx = [
                        random.randint(0, len(self.slot_images) - 1)
                        for _ in range(3)
                    ]
                    for i in range(3):
                        self.slots[i].config(image=self.slot_images[res_idx[i]])
                    is_win = res_idx[0] == res_idx[1] == res_idx[2]

                if is_win:
                    self.app.chips += 1000
                    self.result_label.config(text="🎉 中大獎了！獲得 1000 籌碼！")
                else:
                    self.result_label.config(text="❌ 槓龜！再接再厲！")
                self.chips_display.config(text=f"目前籌碼: {self.app.chips} 💰")

        animate(15)