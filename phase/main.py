from input import InputModule
from output import OutputModule
from line import LineModule
from shift import ShiftModule
from sort import SortModule


class MainController:
    def __init__(self):
        self.line_module = LineModule()
        self.input_module = InputModule(self.line_module)
        self.shift_module = ShiftModule(self.line_module)
        self.sort_module = SortModule(self.shift_module, self.input_module)
        self.output_module = OutputModule(self.shift_module, self.sort_module)
        self.sorted_results = []  # 存储排序结果

    def run(self):
        print("欢迎使用单词移位排序系统!")
        print("输入文本行或命令。可用命令:")
        print("  /sort - 显示所有移位结果和排序结果")
        print("输入文本行进行排序处理。")

        while True:
            user_input = input("> ")
            if not user_input:
                continue

            if user_input.strip().startswith('/'):
                command = user_input.strip()[1:]
                if command == 'sort':
                    # 直接显示排序结果，跳过每行的移位结果
                    print("\n排序结果 (包含URL):")
                    self.output_module.print_sorted_results()
                    print("\n-------------------结束-------------------")
                    self._keyword_search()
                    return
                else:
                    print(f"未知命令: /{command}")
            else:
                success = self.input_module.process_input(user_input)
                if not success:
                    print("(该行不包含有效单词，已忽略)")

    def _keyword_search(self):
        """关键词检索功能 - 支持多关键词（每行一个）"""
        sorted_entries = self.sort_module.get_sorted_results()

        print("\n---------多关键词检索模式-------------")
        print("提示：每行输入一个搜索关键词（支持带引号的短语）")
        print("输入完成后输入 /search 开始检索")
        print("输入 /exit 退出此模式")

        keywords = []
        while True:
            user_input = input("(搜索词)>> ").strip()

            if user_input == '/exit':
                print("退出关键词检索")
                break
            if user_input == '/search':
                if not keywords:
                    print("未输入关键词")
                    continue

                # 开始搜索并输出结果
                for keyword in keywords:
                    # 去除可能的引号
                    clean_keyword = keyword.strip()
                    if (len(clean_keyword) >= 2 and
                            ((clean_keyword[0] == '"' and clean_keyword[-1] == '"') or
                             (clean_keyword[0] == "'" and clean_keyword[-1] == "'"))):
                        clean_keyword = clean_keyword[1:-1]

                    matching_lines = []
                    for i, (line_num, _, shifted) in enumerate(sorted_entries, 1):
                        text = ' '.join(shifted)
                        # 在文本前后添加空格，确保完整单词匹配
                        search_text = f" {text.lower()} "
                        search_phrase = f" {clean_keyword.lower()} "
                        if search_phrase in search_text:
                            matching_lines.append(str(i))

                    print(f'"{clean_keyword}": {" ".join(matching_lines) if matching_lines else "未找到匹配"}')

                # 清空关键词列表准备下次查询
                keywords = []
                print("再次输入关键词或命令...")

            else:
                keywords.append(user_input)


if __name__ == "__main__":
    controller = MainController()
    try:
        controller.run()
    except KeyboardInterrupt:
        print("\n程序被用户终止。")
        print("-------------------结束-------------------")
