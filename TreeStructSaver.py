import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class TreeStructSaver:
    def __init__(self, root):
        self.root = root
        self.root.title("TreeStructSaver")
        self.root.geometry("600x400")

        # フレームの初期設定
        self.setup_frames()
        # ツリービューの設定
        self.setup_treeview()
        # ボタンの設定
        self.setup_buttons()

        # 現在のディレクトリパスを保持
        self.current_dir = None

    def setup_frames(self):
        """フレームの初期設定"""
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.button_frame = ttk.Frame(self.root)
        self.button_frame.pack(fill='x', padx=10, pady=10)

    def setup_treeview(self):
        """ツリービューとスクロールバーの初期設定"""
        self.tree = ttk.Treeview(self.frame)
        self.tree.pack(fill='both', expand=True, side='left')

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side='right', fill='y')

        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.heading("#0", text="Directory Structure", anchor='w')

    def setup_buttons(self):
        """操作ボタンの初期設定"""
        open_button = ttk.Button(self.button_frame, text="フォルダを選択", command=self.open_directory)
        open_button.pack(side='left')

        save_button = ttk.Button(self.button_frame, text="構造をファイルに保存", command=self.save_structure)
        save_button.pack(side='left')

    def open_directory(self):
        """フォルダ選択ダイアログを開き、ツリービューに構造を表示"""
        try:
            dir_path = filedialog.askdirectory()
            if dir_path:
                # ツリービューをクリア
                self.clear_treeview()
                # ツリービューを更新
                self.populate_treeview('', dir_path)
                self.current_dir = dir_path
        except Exception as e:
            messagebox.showerror("エラー", f"ディレクトリを開く際にエラーが発生しました: {e}")

    def clear_treeview(self):
        """ツリービューの内容をクリア"""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def populate_treeview(self, parent, path):
        """ディレクトリ構造を再帰的にツリービューに追加"""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    node = self.tree.insert(parent, 'end', text=item, open=False)
                    self.populate_treeview(node, item_path)
                else:
                    self.tree.insert(parent, 'end', text=item)
        except PermissionError:
            messagebox.showwarning("アクセスエラー", f"アクセス権がありません: {path}")
        except Exception as e:
            messagebox.showerror("エラー", f"ツリービューに構造を追加する際にエラーが発生しました: {e}")

    def save_structure(self):
        """ディレクトリ構造をテキストファイルに保存"""
        if not self.current_dir:
            messagebox.showwarning("警告", "保存するディレクトリ構造がありません。")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if save_path:
            try:
                with open(save_path, 'w', encoding='utf-8') as file:
                    self.write_structure(file, self.current_dir)
                messagebox.showinfo("成功", f"ディレクトリ構造が '{save_path}' に保存されました。")
            except Exception as e:
                messagebox.showerror("エラー", f"ファイルの保存中にエラーが発生しました: {e}")

    def write_structure(self, file, path, indent_level=0):
        """ディレクトリ構造を再帰的にファイルに書き込む"""
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                indent = ' ' * indent_level * 4
                file.write(f"{indent}{item}\n")
                if os.path.isdir(item_path):
                    self.write_structure(file, item_path, indent_level + 1)
        except PermissionError:
            file.write(f"{indent}アクセス権がありません: {path}\n")
        except Exception as e:
            file.write(f"{indent}エラーが発生しました: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = TreeStructSaver(root)
    root.mainloop()