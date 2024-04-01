# 概要

英語の音節数を計算するツールです。  
nltkのcmudict(カーネギーメロン大学が作成した発音辞書)をベースとして、非収録語にもある程度対応できるアルゴリズムを採用しています。  

# セットアップ
```
pip install count-syllable
```

# アンインストール
```
pip uninstall count-syllable nltk
```

# 使用方法
```
from count_syllable import count_syllable

data = count_syllable("anyone")

print(data)
```

# アルゴリズム

前方単語ブロック、後方単語ブロック、中間単語ブロックに分けて考える  

(1)単語がcmudictに存在するか参照しあればその音節数を前方単語ブロックの音節数とする、なければ後方文字を一文字削減して再度参照し、2文字以下になるまで繰り返す
(2)2文字以下になった場合は、母音の数を計算し、前方単語ブロックの音節数とする
(3)前方単語ブロックを除いた単語がcmudictに存在するか参照しあればその音節数を後方単語ブロックの音節数とする、なければ前方文字を一文字削減して再度参照し、2文字以下になるまで繰り返す
(4)2文字以下になった場合は、母音の数を計算し、後方単語ブロックの音節数とする
(5)前方単語ブロック、後方単語ブロックを除いた単語について、母音の数を計算し、中間単語ブロックの音節数とする
(6)2文字以下になった単語をまとめて、二重母音の数を計算する
(7)前方単語ブロック、後方単語ブロック、中間単語ブロックの音節数を加算し、二重母音の数を減算して、単語の音節数を求める

# 関連ツール、関連サイト

## Sylco: https://github.com/eaydin/sylco
独自アルゴリズムで英語の音節数を計算するツール。
ライセンスが非記載のため、利用用途は限られるが、アルゴリズムは参考になる。
  
## How Many Syllables: https://www.howmanysyllables.com
5つの手法を用いて英語の音節数を計算するサイト。  
詳細な使用アルゴリズムは不明だが、多くの英単語に対応している。  
  
# 論文

論文化、または、学会発表を予定してます。  


# ライセンス
- count-syllable
	- Python Software Foundation License
	- Copyright (C) 2024 Shinya Akagi
- nltk
	- Apache License 2.0
	- Copyright (C) 2001-2023 NLTK Project
- cmudict
	- BSD License
	- Copyright (C) 1998 Carnegie Mellon University
  
