class InputModule:
    def __init__(self, line_module):
        self._line_module = line_module
        self._raw_lines = []
        self._words_with_leading_space = set()
        self._line_urls = {}  # 存储每行的URL

    def process_input(self, line_str):
        words, words_with_space, url = self._process_line(line_str)
        if words or url:
            self._line_module.add_line((words, url))
            self._raw_lines.append(line_str)
            self._words_with_leading_space.update(words_with_space)
            return True
        return False

    def _process_line(self, line_str):
        tokens = line_str.split()
        url_str = None
        common_tokens = []
        found_url = False

        # 从右向左查找第一个URL
        for token in reversed(tokens):
            if token.startswith("http://") or token.startswith("https://"):
                url_str = token
                found_url = True
                break

        if found_url:
            # 提取非URL部分
            url_index = len(tokens) - tokens[::-1].index(url_str) - 1
            common_tokens = tokens[:url_index]
            common_str = ' '.join(common_tokens)
        else:
            common_str = line_str

        # 处理非URL部分
        processed_str = ""
        for char in common_str:
            if 'a' <= char.lower() <= 'z' or char.isspace():
                processed_str += char

        words = []
        words_with_space = set()
        parts = processed_str.split()

        for part in parts:
            if part:
                words.append(part)
                # 检查原始字符串中的前导空格
                if common_str.find(part) > 0 and common_str[common_str.find(part) - 1].isspace():
                    words_with_space.add(part)

        return words if words else None, words_with_space, url_str

    def get_words_with_leading_space(self):
        return self._words_with_leading_space

    def get_line_url(self, line_number):
        return self._line_module.get_line_url(line_number)
