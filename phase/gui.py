import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk
from line import LineModule
from input import InputModule
from shift import ShiftModule
from sort import SortModule
from output import OutputModule
import os


class KWICGUI:
    def __init__(self, master):
        self.master = master
        master.title("KWIC - 单词移位排序工具")
        master.geometry("800x700")
        self.master.minsize(650, 600)

        # 风格配置
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TFrame', background='#f0f0f0')

        # 创建笔记本控件（分页）
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 输入页面
        self.input_page = ttk.Frame(self.notebook)
        self.output_page = ttk.Frame(self.notebook)
        self.notebook.add(self.input_page, text="输入区")
        self.notebook.add(self.output_page, text="结果区")

        # 初始化模块
        self.line_module = LineModule()
        self.input_module = InputModule(self.line_module)
        self.shift_module = ShiftModule(self.line_module)
        self.sort_module = SortModule(self.shift_module, self.input_module)
        self.output_module = OutputModule(self.shift_module, self.sort_module)

        # 初始化结果存储
        self.sorted_results = []
        self.processed_lines = []

        # ====== 输入页面 ======
        input_frame = ttk.LabelFrame(self.input_page, text="输入区域")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 输入框和按钮
        input_controls_frame = ttk.Frame(input_frame)
        input_controls_frame.pack(fill=tk.X, padx=10, pady=5)

        # 多行输入文本框
        ttk.Label(input_controls_frame, text="输入多行文本(每行单独处理):").pack(anchor=tk.W)
        self.text_input = scrolledtext.ScrolledText(input_controls_frame, width=50, height=10)
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 添加文本按钮
        self.add_text_btn = ttk.Button(input_controls_frame, text="添加文本", command=self.add_multiple_lines)
        self.add_text_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        # 文件导入区域
        file_frame = ttk.LabelFrame(input_frame, text="导入文件")
        file_frame.pack(fill=tk.X, padx=10, pady=5)

        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var, width=50).pack(
            side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="选择文件", command=self.select_file).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(file_frame, text="导入", command=self.import_file).pack(side=tk.LEFT, padx=5, pady=5)

        # 单行输入区域
        single_input_frame = ttk.Frame(input_frame)
        single_input_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(single_input_frame, text="输入单行文本:").pack(side=tk.LEFT, padx=(0, 5))
        self.single_input = ttk.Entry(single_input_frame, width=50)
        self.single_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(single_input_frame, text="添加行", command=self.add_single_line).pack(side=tk.LEFT)

        # 处理按钮
        process_frame = ttk.Frame(input_frame)
        process_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(process_frame, text="显示移位结果", command=self.show_shift).pack(side=tk.LEFT, padx=5)
        ttk.Button(process_frame, text="显示排序结果", command=self.show_sorted).pack(side=tk.LEFT, padx=5)
        ttk.Button(process_frame, text="导出结果", command=self.download_results).pack(side=tk.LEFT, padx=5)

        # ====== 结果页面 ======
        # 选项卡控制
        self.result_notebook = ttk.Notebook(self.output_page)
        self.result_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 移位结果选项卡
        shift_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(shift_frame, text="移位结果")

        self.shift_text = scrolledtext.ScrolledText(shift_frame, wrap=tk.WORD)
        self.shift_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 排序结果选项卡
        sorted_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(sorted_frame, text="排序结果")

        self.sorted_text = scrolledtext.ScrolledText(sorted_frame, wrap=tk.WORD)
        self.sorted_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 搜索选项卡
        search_frame = ttk.Frame(self.result_notebook)
        self.result_notebook.add(search_frame, text="关键词搜索")

        # 搜索控件
        search_controls = ttk.Frame(search_frame)
        search_controls.pack(fill=tk.X, padx=10, pady=5)

        # 多行输入框
        ttk.Label(search_controls, text="搜索关键词 (每行一个):").pack(side=tk.TOP, padx=(0, 5), anchor=tk.W)

        # 使用更大的多行输入框
        self.search_entry = scrolledtext.ScrolledText(search_controls, height=5, width=30)
        self.search_entry.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 搜索按钮
        btn_frame = ttk.Frame(search_controls)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(btn_frame, text="搜索", command=self.keyword_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清除",
                   command=lambda: self.search_entry.delete("1.0", tk.END)).pack(side=tk.LEFT, padx=5)

        # 搜索结果显示区
        results_frame = ttk.Frame(search_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 创建带滚动条的结果显示
        self.search_results = scrolledtext.ScrolledText(results_frame)
        self.search_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.search_results.config(state=tk.DISABLED)

        # 创建汇总结果的标签
        self.summary_label = ttk.Label(search_frame, text="等待搜索...")
        self.summary_label.pack(fill=tk.X, padx=10, pady=5)

    # ====== 输入页面功能 ======
    def add_single_line(self):
        """添加单行文本"""
        line = self.single_input.get()
        if not line.strip():
            messagebox.showwarning("警告", "请输入有效文本行。")
            return

        if self.input_module.process_input(line):
            self.processed_lines.append(line)
            self.single_input.delete(0, tk.END)
        else:
            messagebox.showinfo("信息", "该行不包含有效单词，已忽略。")

    def add_multiple_lines(self):
        """添加多行文本"""
        content = self.text_input.get("1.0", tk.END)
        lines = [line.strip() for line in content.split('\n') if line.strip()]

        for line in lines:
            if self.input_module.process_input(line):
                self.processed_lines.append(line)

        if lines:
            messagebox.showinfo("完成", f"成功添加 {len(lines)} 行文本")
            self.text_input.delete("1.0", tk.END)

    def select_file(self):
        """选择文本文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.file_path_var.set(file_path)

    def import_file(self):
        """导入文本文件"""
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showwarning("警告", "请选择有效的文本文件。")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = [line.strip() for line in file.readlines() if line.strip()]

            added_count = 0
            for line in lines:
                if self.input_module.process_input(line):
                    self.processed_lines.append(line)
                    added_count += 1

            messagebox.showinfo("导入完成", f"成功导入 {added_count} 行文本")
        except Exception as e:
            messagebox.showerror("错误", f"导入文件时出错: {str(e)}")

    # ====== 结果页面功能 ======
    def show_shift(self):
        """显示所有移位结果"""
        self.shift_text.config(state=tk.NORMAL)
        self.shift_text.delete(1.0, tk.END)

        content = ""
        line_count = self.line_module.get_line_count()
        if line_count == 0:
            self.shift_text.insert(tk.END, "没有可显示的移位结果")
        else:
            for line_num in range(1, line_count + 1):
                shifts = self.shift_module.get_shift_results(line_num)
                if not shifts:
                    continue

                content += f"移位结果 #{line_num}:\n"
                for idx, words in enumerate(shifts, 1):
                    content += f"{idx}: {' '.join(words)}\n"
                content += "\n"

            self.shift_text.insert(tk.END, content.strip() or "没有有效的移位结果")

        self.shift_text.config(state=tk.DISABLED)
        self.result_notebook.select(0)  # 切换到移位结果页面

    def show_sorted(self):
        """显示排序结果"""
        self.sorted_text.config(state=tk.NORMAL)
        self.sorted_text.delete(1.0, tk.END)

        self.sorted_results = self.output_module.get_sorted_results()
        if not self.sorted_results:
            self.sorted_text.insert(tk.END, "没有可显示的排序结果")
            return

        content = ""
        for idx, text, _ in self.sorted_results:
            content += f"{idx} {text}\n"
        self.sorted_text.insert(tk.END, content.strip())
        self.sorted_text.config(state=tk.DISABLED)

        self.result_notebook.select(1)  # 切换到排序结果页面

    def keyword_search(self):
        """关键词搜索 - 支持多关键词（每行一个）"""
        self.search_results.config(state=tk.NORMAL)
        self.search_results.delete(1.0, tk.END)

        if not self.sorted_results:
            messagebox.showinfo("警告", "请先生成排序结果")
            self.search_results.config(state=tk.DISABLED)
            return

        # 获取多行输入的关键词
        keyword_input = self.search_entry.get("1.0", tk.END).strip()
        if not keyword_input:
            messagebox.showinfo("提示", "请输入搜索关键词")
            self.search_results.config(state=tk.DISABLED)
            return

        # 按行分割关键词
        keywords = [k.strip() for k in keyword_input.split('\n') if k.strip()]
        if not keywords:
            messagebox.showinfo("提示", "未检测到有效关键词")
            self.search_results.config(state=tk.DISABLED)
            return

        results = {}
        for keyword in keywords:
            # 去除首尾引号（如果有）
            clean_keyword = keyword
            if (len(clean_keyword) >= 2 and
                    ((clean_keyword[0] == '"' and clean_keyword[-1] == '"') or
                     (clean_keyword[0] == "'" and clean_keyword[-1] == "'"))):
                clean_keyword = clean_keyword[1:-1]

            keyword_lower = clean_keyword.lower()
            matching_indices = []

            for idx, text, _ in self.sorted_results:
                text_lower = text.lower()
                # 在文本前后添加空格，确保完整单词匹配
                if f" {keyword_lower} " in f" {text_lower} ":
                    matching_indices.append(str(idx))

            results[clean_keyword] = matching_indices

        # 显示搜索结果
        self.search_results.delete(1.0, tk.END)
        summary_lines = []

        for keyword, indices in results.items():
            result_line = f'"{keyword}": {" ".join(indices) if indices else "未找到匹配"}'
            self.search_results.insert(tk.END, result_line + "\n")
            summary_lines.append(result_line)

        # 更新汇总信息
        summary_text = "\n".join(summary_lines)
        self.summary_label.config(text=summary_text)

        self.search_results.config(state=tk.DISABLED)
        self.result_notebook.select(2)  # 切换到搜索页面

    def download_results(self):
        """导出排序结果为文件"""
        if not self.sorted_results:
            messagebox.showwarning("警告", "没有内容可导出")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt")],
            title="保存排序结果"
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                for idx, text, _ in self.sorted_results:
                    f.write(f"{idx}\t{text}\n")
            messagebox.showinfo("成功", f"结果已保存到: {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        gui = KWICGUI(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("程序被用户终止。")

