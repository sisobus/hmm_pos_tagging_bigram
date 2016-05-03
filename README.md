# hmm_pos_tagging_bigram
- 서강대학교 자연어처리 HW#3 hmm pos tagging 제작

## file info
- train.txt : 확률 계산을 위한 데이터 파일
    - P(word|pos), P(pos_i,pos_i-1), P(pos)를 구할 수 있다.
- input.txt : 품사 태깅할 문자열 
- result.txt : input.txt 의 문자열을 어절별로 형태소 분석한 결과파일

## execute
```
    $ python a.py
```
