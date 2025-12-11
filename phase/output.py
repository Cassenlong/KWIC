class OutputModule:
    def __init__(self, shift_module, sort_module):
        self._shift_module = shift_module
        self._sort_module = sort_module

    def print_shift_results(self, line_number):
        results = self._shift_module.get_shift_results(line_number)
        if not results:
            return
        print(f"移位结果 #{line_number}:")
        for idx, shifted in enumerate(results, 1):
            print(f"{idx}: {' '.join(shifted)}")

    def print_all_shift_results(self):
        line_count = self._shift_module._line_module.get_line_count()
        if line_count == 0:
            return

        for line_num in range(1, line_count + 1):
            self.print_shift_results(line_num)
            if line_num < line_count:
                print()

    def print_sorted_results(self):
        sorted_entries = self._sort_module.get_sorted_results()
        if not sorted_entries:
            print("没有可显示的结果")
            return

        for idx, (line_num, _, shifted) in enumerate(sorted_entries, 1):
            print(f"{idx} {' '.join(shifted)}")

    def get_sorted_results(self):
        """返回带连续编号的排序结果"""
        sorted_entries = self._sort_module.get_sorted_results()
        return [
            (idx, ' '.join(shifted), line_num)
            for idx, (line_num, _, shifted) in enumerate(sorted_entries, 1)
        ]
