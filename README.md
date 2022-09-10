# Text-Segmentation
![img](assets/ATS.png)
## Advanced Text Segmentation - ATS
![visitors](https://visitor-badge.glitch.me/badge?page_id=JiaDians.TextSegmentation&left_color=green&right_color=red)
![GitHub stars](https://badgen.net/github/stars/JiaDians/Text-Segmentation)

## Introduction
將**句子**或**文章**做斷詞處理，為 NLP 下游任務提供更有效率的處理。
## Usage
```
git clone https://github.com/JiaDians/Text-Segmentation.git
```
```python 
from text_segmentation import text_segment
in_str = '今年第11號颱風「軒嵐諾」，離開台灣後再次轉為強颱'
ts = TextSegment()
output = ts.get_segment_list(in_str)
print(output) # ['今年', '第', '11', '號', '颱風', '「', '軒嵐諾', '」', '，', '離開', '台灣', '後', '再次', '轉', '為', '強', '颱']
```
## Detail
此專案有加入新詞偵測 model，如需增加新詞辨識精確度，請在 data.txt 內提供新聞文章內容(單行)，目前資料量達到 **600多篇新聞**
## Demo
1. 早上好中國現在我有冰淇淋，我很喜歡冰淇淋<br>
2. 狼若回頭，必有緣由，不是報恩，就是報仇。<br>
3. 林佳龍將參與市長選舉<br>
4. 蔡英文是目前台灣總統<br>
5. 今年第11號颱風「軒嵐諾」，離開台灣後再次轉為強颱<br>

![img](assets/demo.png)

* old: 一般斷詞 <br>
* new: 附加新詞偵測斷詞 