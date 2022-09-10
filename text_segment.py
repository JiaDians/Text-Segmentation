import re


class TextSegment:
    def __init__(self, common_char_prob=0.0028, dice_coef=0.7):
        self.common_char_prob = common_char_prob
        self.dice_coef = dice_coef

    # 斷詞
    def _segment(self, seg_str, search_dict, seg_max_len):
        if seg_str == '':
            return ''
        elif len(seg_str) == 1:
            return seg_str
        elif seg_str.isascii() and seg_str.isalnum():
            return seg_str
        elif seg_str[0:seg_max_len] in search_dict:
            return seg_str
        else:
            return self._segment(seg_str[:len(seg_str)-1], search_dict, seg_max_len)

    # 取出斷詞後的List
    def get_segment_list(self, input_str):
        output_list = []

        # 建立斷詞表
        file = 'dict_no_space.txt'
        seg_max_len = 30
        search_dict = dict()
        with open(file, 'r', encoding="utf-8") as head:
            for line in head:
                search_dict[line.strip()] = True

        # 初步斷詞
        pos = 0
        while pos < len(input_str):
            seg_str = self._segment(input_str[pos:], search_dict, seg_max_len)
            output_list.append(seg_str)
            pos += len(seg_str)
        print('old:', output_list)

        # 新詞偵測(凝聚力)
        # round 1
        new_output_list_1 = []
        index = 0
        while index < len(output_list):
            # print(output_list[index:index+2])
            # 確保三個空間
            if index + 2 < len(output_list):
                # 最左邊出現超常見字
                if self._check_very_common_char(output_list[index]):
                    new_output_list_1.append(output_list[index])
                    index += 1
                else:
                    if self._dice_coefficient(output_list[index:index+2]) >= self._dice_coefficient(output_list[index+1:index+3]) \
                            and self._dice_coefficient(output_list[index:index+2]) >= self.dice_coef:
                        new_output_list_1.append(
                            output_list[index] + output_list[index+1])
                        index += 2
                    elif self._dice_coefficient(output_list[index+1:index+3]) >= self.dice_coef:
                        new_output_list_1.append(output_list[index])
                        new_output_list_1.append(
                            output_list[index+1] + output_list[index+2])
                        index += 3
                    else:
                        new_output_list_1.append(output_list[index])
                        index += 1

            # 確保兩個空間
            elif index + 1 < len(output_list):
                # 左邊出現超常見字
                if self._check_very_common_char(output_list[index]):
                    new_output_list_1.append(output_list[index])
                    index += 1
                else:
                    if self._dice_coefficient(output_list[index:index+2]) >= self.dice_coef:
                        new_output_list_1.append(
                            output_list[index] + output_list[index+1])
                        index += 2
                    else:
                        new_output_list_1.append(output_list[index])
                        index += 1

            # 確保一個空間
            else:
                new_output_list_1.append(output_list[index])
                index += 1

        # round 2
        new_output_list_2 = []
        index = 0
        while index < len(new_output_list_1):
            # print(output_list[index:index+2])
            # 確保三個空間
            if index + 2 < len(new_output_list_1):
                # 最左邊出現超常見字
                if self._check_very_common_char(new_output_list_1[index]):
                    new_output_list_2.append(new_output_list_1[index])
                    index += 1
                else:
                    if self._dice_coefficient(new_output_list_1[index:index+2]) >= self._dice_coefficient(new_output_list_1[index+1:index+3]) \
                            and self._dice_coefficient(new_output_list_1[index:index+2]) >= self.dice_coef:
                        new_output_list_2.append(
                            new_output_list_1[index] + new_output_list_1[index+1])
                        index += 2
                    elif self._dice_coefficient(new_output_list_1[index:index+2]) < self._dice_coefficient(new_output_list_1[index+1:index+3]) and self._dice_coefficient(new_output_list_1[index+1:index+3]) >= self.dice_coef:
                        new_output_list_2.append(new_output_list_1[index])
                        new_output_list_2.append(
                            new_output_list_1[index+1] + new_output_list_1[index+2])
                        index += 3
                    else:
                        new_output_list_2.append(new_output_list_1[index])
                        index += 1

            # 確保兩個空間
            elif index + 1 < len(new_output_list_1):
                # 左邊出現超常見字
                if self._check_very_common_char(new_output_list_1[index]):
                    new_output_list_2.append(new_output_list_1[index])
                    index += 1
                else:
                    if self._dice_coefficient(new_output_list_1[index:index+2]) >= self.dice_coef:
                        new_output_list_2.append(
                            new_output_list_1[index] + new_output_list_1[index+1])
                        index += 2
                    else:
                        new_output_list_2.append(new_output_list_1[index])
                        index += 1

            # 確保一個空間
            else:
                new_output_list_2.append(new_output_list_1[index])
                index += 1

        return new_output_list_2

    # 字出現比例
    def _get_char_percent(self, ch):
        text = ""
        file = 'data.txt'
        with open(file, 'r', encoding='UTF-8') as fr:
            lines = fr.readlines()
            for line in lines:
                text += line
        return len([m.start() for m in re.finditer(ch, text)]) / len(text)

    # 詞內是否有常見字
    def _check_very_common_char(self, word):
        for c in word:
            if self._get_char_percent(c) >= self.common_char_prob:
                return True
        return False

    # 計算dice_coefficient
    def _dice_coefficient(self, text_list):
        file = 'data.txt'
        score_list = []

        with open(file, 'r', encoding='UTF-8') as fr:
            lines = fr.readlines()
            for line in lines:
                a = 2 * len([m.start()
                            for m in re.finditer(text_list[0] + text_list[1], line)])
                b = len([m.start() for m in re.finditer(text_list[0], line)]) + \
                    len([m.start()
                        for m in re.finditer(text_list[1], line)])
                if b == 0:
                    c = 0
                else:
                    c = a / b

                score_list.append(c)

        # print(text_list[0] + text_list[1], score_list)
        return max(score_list)


if __name__ == '__main__':
    ts = TextSegment()
    in_str = '早上好中國現在我有冰淇淋，我很喜歡冰淇淋'
    print('new:', ts.get_segment_list(in_str))
    print('--------------------------------------')
    in_str = '狼若回頭，必有緣由，不是報恩，就是報仇。'
    print('new:', ts.get_segment_list(in_str))
    print('--------------------------------------')
    in_str = '林佳龍將參與市長選舉'
    print('new:', ts.get_segment_list(in_str))
    print('--------------------------------------')
    in_str = '蔡英文是目前台灣總統'
    print('new:', ts.get_segment_list(in_str))
    print('--------------------------------------')
    in_str = '今年第11號颱風「軒嵐諾」，離開台灣後再次轉為強颱'
    print('new:', ts.get_segment_list(in_str))
