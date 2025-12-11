class LineModule:
    def __init__(self):
        self._lines = []    # 存储(words, url)元组

    def add_line(self, data):
        self._lines.append(data)

    def get_line(self, line_number):
        if 1 <= line_number <= len(self._lines):
            return self._lines[line_number-1][0]  # 只返回单词部分
        return None

    def get_full_line_data(self, line_number):
        if 1 <= line_number <= len(self._lines):
            return self._lines[line_number-1]
        return (None, None)

    def get_line_url(self, line_number):
        if 1 <= line_number <= len(self._lines):
            return self._lines[line_number-1][1]  # 返回URL
        return None

    def get_line_count(self):
        return len(self._lines)

    def get_all_lines(self):
        return [data[0] for data in self._lines]
