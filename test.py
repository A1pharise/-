import tkinter as tk
from tkinter import messagebox, Frame, Label, Button
import numpy as np
import random

class MinesweeperGame:
    def __init__(self, root):
        self.root = root
        self.root.title("扫雷游戏")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f8ff")
        
        # 游戏难度设置
        self.difficulty_levels = [
            {"name": "初级", "size": 8, "mines": 10},
            {"name": "中级", "size": 10, "mines": 15},
            {"name": "高级", "size": 15, "mines": 25}
        ]
        
        # 初始化游戏状态变量
        self.game_over = False
        self.first_click = True
        self.uncovered_cells = 0
        self.cells = None  # 初始化 cells 属性
        
        # 创建主界面
        self.create_main_interface()
        
        # 显示难度选择对话框
        self.show_difficulty_dialog()
    
    def create_main_interface(self):
        """创建主游戏界面"""
        # 顶部状态栏
        self.status_frame = Frame(self.root, bg="#2c3e50", height=40)
        self.status_frame.pack(fill="x", padx=10, pady=5)
        
        self.mines_label = Label(
            self.status_frame, 
            text="地雷: 0", 
            fg="white", 
            bg="#2c3e50",
            font=("Arial", 12, "bold")
        )
        self.mines_label.pack(side="left", padx=20)
        
        self.status_label = Label(
            self.status_frame, 
            text="准备开始", 
            fg="#f1c40f", 
            bg="#2c3e50",
            font=("Arial", 12, "bold")
        )
        self.status_label.pack(side="left", expand=True)
        
        self.restart_button = Button(
            self.status_frame, 
            text="重新开始", 
            command=self.restart_game,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.restart_button.pack(side="right", padx=20)
        
        # 游戏主区域
        self.game_frame = Frame(self.root, bg="#ecf0f1")
        self.game_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_difficulty_dialog(self):
        """显示难度选择对话框"""
        self.dialog = tk.Toplevel(self.root)
        self.dialog.title("选择难度")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.root)  # 设置为模态对话框
        self.dialog.grab_set()  # 捕获所有事件
        
        Label(
            self.dialog, 
            text="请选择游戏难度", 
            font=("Arial", 14, "bold"),
            pady=10
        ).pack(fill="x")
        
        self.difficulty_var = tk.StringVar(value="0")
        
        # 难度选项
        for i, level in enumerate(self.difficulty_levels):
            frame = Frame(self.dialog)
            frame.pack(fill="x", padx=40, pady=5)
            
            tk.Radiobutton(
                frame,
                variable=self.difficulty_var,
                value=str(i),
                text=f"{level['name']} ({level['size']}x{level['size']}, {level['mines']}个地雷)",
                font=("Arial", 10),
                anchor="w"
            ).pack(side="left")
        
        # 确定按钮
        Button(
            self.dialog, 
            text="开始游戏", 
            command=self.start_game,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=5
        ).pack(pady=15)
        
        # 居中对话框
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.root.winfo_width() // 2) - (width // 2) + self.root.winfo_x()
        y = (self.root.winfo_height() // 2) - (height // 2) + self.root.winfo_y()
        self.dialog.geometry(f"+{x}+{y}")
    
    def start_game(self):
        """开始新游戏"""
        self.dialog.destroy()
        difficulty = int(self.difficulty_var.get())
        level = self.difficulty_levels[difficulty]
        
        self.board_size = level["size"]
        self.total_mines = level["mines"]
        self.uncovered_cells = 0
        self.game_over = False
        self.first_click = True
        
        # 更新状态栏
        self.mines_label.config(text=f"地雷: {self.total_mines}")
        self.status_label.config(text="游戏中...", fg="#2ecc71")
        
        # 创建游戏板
        self.create_game_board()
        
        # 初始化地雷列表
        self.mines = []
    
    def create_game_board(self):
        """创建游戏板"""
        # 清除现有游戏板
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        # 初始化 cells 数组
        self.cells = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # 创建网格
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = tk.Button(
                    self.game_frame,
                    width=2,
                    height=1,
                    bg="#3498db",
                    relief="raised",
                    font=("Arial", 10, "bold")
                )
                cell.grid(row=row, column=col, padx=1, pady=1)
                
                # 绑定事件
                cell.bind("<Button-1>", lambda e, r=row, c=col: self.cell_left_click(r, c))
                cell.bind("<Button-3>", lambda e, r=row, c=col: self.cell_right_click(r, c))
                
                self.cells[row][col] = cell
    
    def cell_left_click(self, row, col):
        """处理左键点击格子"""
        if self.game_over:
            return
            
        
        # 如果是第一次点击，生成地雷（避开点击位置）
        if self.first_click:
            self.place_mines(range(max(0, row-1), min(self.board_size, row+2)),range(max(0, col-1), min(self.board_size, col+2)))
            self.first_click = False

        # 判断是否标记为旗帜
        if(self.cells[row][col]["text"] == ""):
            # 如果格子是地雷
            if (row, col) in self.mines:
                self.game_over = True
                self.reveal_all_mines()
                self.status_label.config(text="Die", fg="#e74c3c")
                messagebox.showinfo("Game Over", "Your die :-(")
                return
            
            # 揭示格子
            self.reveal_cell(row, col)
            
            # 检查是否获胜
        if self.uncovered_cells == (self.board_size * self.board_size) - self.total_mines:
            self.game_over = True
            self.status_label.config(text="Win", fg="#f1c40f")
            messagebox.showinfo("Game Over", "Your Win :-)")
    
    def cell_right_click(self, row, col):
        """处理右键点击格子（标记地雷）"""
        if self.game_over or self.first_click:
            return
            
        cell = self.cells[row][col]
        
        # 如果格子是空的，标记为地雷
        if cell["text"] == "":
            cell.config(text="🚩", fg="#e74c3c")
        # 如果已经标记，取消标记
        elif cell["text"] == "🚩":
            cell.config(text="")
    
    def place_mines(self, safe_row, safe_col):
        """随机放置地雷，避开安全位置"""
        self.mines = []
        possible_positions = [
            (r, c) 
            for r in range(self.board_size) 
            for c in range(self.board_size)
            if not (r in safe_row and c in safe_col)
        ]
        
        # 随机选择地雷位置
        self.mines = random.sample(possible_positions, self.total_mines)
    
    def reveal_cell(self, row, col):
        """揭示格子内容"""
        if self.cells[row][col]["relief"] == "sunken":
            return  # 已经揭示的格子不再处理
        print(row,col)
        
        cell = self.cells[row][col]
        cell.config(relief="sunken", bg="#dfe6ea")
        self.uncovered_cells += 1
        
        # 计算周围地雷数量
        mine_count = 0
        for r in range(max(0, row-1), min(self.board_size, row+2)):
            for c in range(max(0, col-1), min(self.board_size, col+2)):
                if (r, c) in self.mines:
                    mine_count += 1
        
        # 显示地雷数量
        if mine_count > 0:
            colors = ["", "#3498db", "#27ae60", "#e74c3c", "#8e44ad", "#f39c12", "#16a085", "#2c3e50", "#7f8c8d"]
            cell.config(text=str(mine_count), fg=colors[mine_count])
        else:
            # 如果没有周围地雷，递归揭示周围格子
            for r in range(max(0, row-1), min(self.board_size, row+2)):
                for c in range(max(0, col-1), min(self.board_size, col+2)):
                    if (r, c) != (row, col) and (r, c) not in self.mines:
                        self.reveal_cell(r, c)
    
    def reveal_all_mines(self):
        """显示所有地雷"""
        for (row, col) in self.mines:
            cell = self.cells[row][col]
            cell.config(text="💣", relief="sunken", bg="#e74c3c")
    
    def restart_game(self):
        """重新开始游戏"""
        self.show_difficulty_dialog()

# 运行游戏
if __name__ == "__main__":
    root = tk.Tk()
    game = MinesweeperGame(root)
    root.mainloop()
