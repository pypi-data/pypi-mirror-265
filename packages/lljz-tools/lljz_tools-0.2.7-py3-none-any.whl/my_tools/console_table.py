# coding=utf-8
from typing import Iterable, Any
from my_tools.color import _Color
from my_tools.log_manager import LogManager

logger = LogManager('ConsoleTable').get_logger()


class ConsoleTable:

    def __init__(self, data: Iterable[dict[str, Any]], max_width=100):
        def init_value(val):
            if isinstance(val, str | _Color):
                return val
            if val is None:
                return ''
            return str(val)

        self.data = [{str(k): init_value(v) for k, v in row.items()} for row in data]
        self.header = list(self.data[0].keys()) if data else []
        self.max_width = max_width
        self.col_width = self._get_widths()
        self._table_str = self._make_table_str()

    @staticmethod
    def _get_string_width(val: str):
        w = 0
        for v in val:
            if u'\u4e00' <= v <= u'\u9fff' or v in '【】（）—…￥！·、？。，《》：；‘“':
                w += 2
            else:
                w += 1
        return w

    def _get_widths(self):
        """获取列宽度，列宽度为整列数据中的最大数据宽度"""

        col_width = [self._get_string_width(key) for key in self.header]
        for row in self.data:
            for i, key in enumerate(self.header):
                value = row.get(key, '')
                width = min(self._get_string_width(value), self.max_width)
                col_width[i] = max(col_width[i], width)
        return col_width

    def _make_table_str(self):
        def format_str(val, width):
            length = self._get_string_width(val)
            left = (width - length) // 2
            right = (width - length) - left
            return f'{" " * left}{val}{" " * right}'

        header = ' | '.join(format_str(key, w) for w, key in zip(self.col_width, self.header))
        rows = [' | '.join(format_str(row.get(key, ""), w) for w, key in zip(self.col_width, self.header)) for row in
                self.data]
        return '\n'.join([header, '=' * len(header)] + rows)

    def __str__(self):
        return self._table_str

    __repr__ = __str__

    def show(self, message=''):
        logger.info(message + '\n' + str(self.__str__()))


if __name__ == '__main__':
    from my_tools.color import Color
    table = ConsoleTable([{'name': Color.red("Tom"), 'b': 2}, {'name': Color.blue("Lucy"), 'b': 4}])
    table.show()
