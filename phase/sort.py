class SortModule:
    _priority = {}
    letters_order = []
    for c in 'abcdefghijklmnopqrstuvwxyz':
        letters_order.append(c)
        letters_order.append(c.upper())
    for idx, char in enumerate(letters_order):
        _priority[char] = idx

    def __init__(self, shift_module, input_module):
        self._shift_module = shift_module
        self._input_module = input_module

    def get_sorted_results(self):
        entries = self._shift_module.get_all_shifted_entries()
        return sorted(entries, key=lambda x: self._get_key(x[2]))

    def _get_key(self, words):
        """为忽略URL的词组创建排序键值"""
        # 检测并移除URL
        clean_words = words.copy()
        for i in range(len(clean_words)):
            if clean_words[i].startswith("http://") or clean_words[i].startswith("https://"):
                clean_words.pop(i)
                break

        # 标准排序逻辑
        if not clean_words:
            return (float('inf'),)

        result = []
        for word in clean_words:
            if not word:
                word_key = (float('inf'),)
            else:
                word_key = tuple(self._get_char_priority(c) for c in word)
            result.append(word_key)
        return tuple(result)

    def get_alphabetical_sorted_words(self):
        # 获取所有单词（忽略URL）
        all_words = set()
        entries = self._shift_module.get_all_shifted_entries()
        for entry in entries:
            for word in entry[2]:
                if not word.startswith(("http://", "https://")):
                    all_words.add(word)

        words_with_leading_space = self._input_module.get_words_with_leading_space()

        def sort_key(word):
            has_leading_space = 0 if word in words_with_leading_space else 1
            return (has_leading_space,) + tuple(self._get_char_priority(c) for c in word)

        return sorted(all_words, key=sort_key)

    def _get_char_priority(self, char):
        if 'a' <= char <= 'z':
            return (ord(char) - ord('a')) * 2
        elif 'A' <= char <= 'Z':
            return (ord(char) - ord('A')) * 2 + 1
        else:
            return float('inf')
