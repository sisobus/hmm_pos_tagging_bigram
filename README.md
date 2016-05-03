# hmm_pos_tagging_bigram
- 서강대학교 자연어처리 HW#3 hmm pos tagging 제작

## file info
- train.txt : 확률 계산을 위한 데이터 파일
    - P(word|pos), P(pos_i,pos_i-1), P(pos)를 구할 수 있다.
- input.txt : 품사 태깅할 문자열 
- result.txt : input.txt 의 문자열을 어절별로 형태소 분석한 결과파일
- train_count.txt : train.txt 를 분석하여 count(word/pos), count(pos_i,pos_i-1), count(pos)가 저장되어 있다. 이 파일이 존재하지 않으면 a.py 를 실행했을 때 분석하는 시간이 약 5초정도 걸린다.
- a.py : 실행 파일
- output.txt : 이 파일에 결과를 출력한다.

## execute
```
    $ python a.py
```
