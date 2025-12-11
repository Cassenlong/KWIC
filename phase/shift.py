class ShiftModule:
    def __init__(self, line_module):
        self._line_module = line_module
        self._shift_results = {}
        self._check_new_lines()

    def _check_new_lines(self):
        current_lines = self._line_module.get_line_count()
        processed = len(self._shift_results)
        for line_num in range(processed + 1, current_lines + 1):
            self._process_line(line_num)

    def _process_line(self, line_number):
        data = self._line_module.get_full_line_data(line_number)
        if not data:
            return

        words, url = data
        shifts = []

        # 只对非URL部分进行轮换
        for i in range(len(words)):
            shifted = words[i:] + words[:i]
            # 添加URL到最后
            if url:
                shifted.append(url)
            shifts.append(shifted)
        self._shift_results[line_number] = shifts

    def get_shift_results(self, line_number):
        self._check_new_lines()
        return self._shift_results.get(line_number, [])

    def get_all_shifted_entries(self):
        self._check_new_lines()
        entries = []
        for line_num, shifts in self._shift_results.items():
            for idx, shifted in enumerate(shifts):
                entries.append((line_num, idx, shifted))
        return entries
