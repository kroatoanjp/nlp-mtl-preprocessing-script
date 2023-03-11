from typing import Iterable
import string

# https://en.wikipedia.org/wiki/Katakana_(Unicode_block)
KATAKANA_CHARSET = {
'゠','ァ','ア','ィ','イ','ゥ','ウ','ェ','エ','ォ','オ','カ','ガ','キ','ギ','ク',
'グ','ケ','ゲ','コ','ゴ','サ','ザ','シ','ジ','ス','ズ','セ','ゼ','ソ','ゾ','タ',
'ダ','チ','ヂ','ッ','ツ','ヅ','テ','デ','ト','ド','ナ','ニ','ヌ','ネ','ノ','ハ',
'バ','パ','ヒ','ビ','ピ','フ','ブ','プ','ヘ','ベ','ペ','ホ','ボ','ポ','マ','ミ',
'ム','メ','モ','ャ','ヤ','ュ','ユ','ョ','ヨ','ラ','リ','ル','レ','ロ','ヮ','ワ',
'ヰ','ヱ','ヲ','ン','ヴ','ヵ','ヶ','ヷ','ヸ','ヹ','ヺ','・','ー','ヽ','ヾ'
}

# Punctuation unicode ranges:
# https://kairozu.github.io/updates/cleaning-jp-text
PUNCTUATION_CHARSET = {
'　','、','。','〃','〄','々','〆','〇','〈','〉','《','》','「','」','『','』',
'【','】','〒','〓','〔','〕','〖','〗','〘','〙','〚','〛','〜','〝','〞','〟',
'〠','〡','〢','〣','〤','〥','〦','〧','〨','〩','〪','〫','〬','〭','〮','〯',
'〰','〱','〲','〳','〴','〵','〶','〷','〸','〹','〺','〻','〼','〽','〾','〿',
'！','＂','＃','＄','％','＆','＇','（','）','＊','＋','，','－','．','／','：',
'；','＜','＝','＞','？','［','＼','］','＾','＿','｀','｛','｜','｝','～','｟',
'｠','｡','｢','｣','､','･','ー','※',' ',' ',' ',' ',
' ',' ',' ',' ',' ',' ',' ',
'​','‌','‍','‎','‏','‐','‑','‒','–','—',
'―','‖','‗','‘','’','‚','‛','“','”','„','‟','†','‡','•','‣','․','‥','…','‧',
' ',' ','‪','‫','‬','‭','‮',
' ','‰','‱','′','″','‴','‵','‶','‷','‸','‹','›','※','‼','‽','‾','‿',
'⁀','⁁','⁂','⁃','⁄','⁅','⁆','⁇','⁈','⁉','⁊','⁋','⁌','⁍','⁎','⁏','⁐','⁑','⁒',
'⁓','⁔','⁕','⁖','⁗','⁘','⁙','⁚','⁛','⁜','⁝','⁞',' ','⁠',
'⁦','⁧','⁨','⁩','«','»','×',"△","▼"
} | set(string.punctuation) # EN punctuation set

def is_katakana(val):
    return all([char in KATAKANA_CHARSET for char in val])

def sort_list_by_string_length(str_list:Iterable, reverse=False):
    len_tagged_str_list = [(len(word), word) for word in str_list]
    sorted_list = []
    for word_len, word in sorted(len_tagged_str_list, reverse=reverse):
        sorted_list.append(word)
    return sorted_list

def is_punctuation(val):
    return all([char in PUNCTUATION_CHARSET for char in val])