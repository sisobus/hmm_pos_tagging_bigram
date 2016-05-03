#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
import re
import os

"""
: options   - dict, global
            > program option dictionary
"""
options = {
        'train_filename'        : 'train.txt',
        'result_filename'       : 'result.txt',
        'input_filename'        : 'input.txt',
        'output_filename'       : 'output.txt',
        'train_count_filename'  : 'train_count.txt',
        }

def get_train_set(filename):
    """
    : get_train_set - function
                    : read train file
    : parameter     - train_filename(str)
                    > 'train.txt'
    : return        - train_lines_list(list<str>)
                    >  ['기회가  기회/NNG+가/JKS','말  말/NNG',...]
    """
    with open(filename,'r') as fp:
        lines = fp.read().strip().split('\n')
    trains = []
    for line in lines:
        if len(line.strip()) == 0:
            continue
        trains.append(line)
    return trains

def split_by_position(s,pos):
    """
    : split_by_position - function
                        : split train_line by position
    : parameter         - s(str)
                        > 'A/SL++/SW+를/JKO'
                        - pos(list<int>) : index of '[A-Z]\+'s
                        > [4,9]
    : return            - ret(list<str>)
                        > ['A/SL','+/SW','를/JKO']
    """
    if len(pos) == 0:
        return [s]
    ret = [s[:pos[0]]]
    for i in xrange(1,len(pos)):
        ret.append(s[(pos[i-1]+1):pos[i]])
    ret.append(s[pos[-1]+1:])
    return ret

def split_train(train):
    """
    : split_train   - function
                    : split one train line by regex '[A-Z]\+'
    : parameter     - train(str)
                    > 'A/SL++/SW+를/JKO'
    : return        - split_by_position(list<str>) 
                    > ['A/SL','+/SW','를/JKO']
    """
    p = re.compile('[A-Z]\+')
    iterator = p.finditer(train)
    pos = [ (match.span()[0]+1) for match in iterator ]
    return split_by_position(train,pos)

def split_slash(s):
    """
    : split_slash   - function
                    : split string('word/pos') to tuple('word','pos') by slash
    : parameter     - s(str)
                    > 'A/SL'
    : return        - (s.split('/')[0],s.split('/')[1])(tuple<str,str>)
                    > ('A','SL')
    """
    if s[0] == '/':
        return ('/',s.split('/')[-1])
    t = s.split('/')
    return (t[0],t[1])

def get_train_count():
    """
    : get_train_count   - function
                        : get train('WORD/POS') count in options['train_filename']
                          if options['train_count_filename'] does not exists
                          (= if this program run first), read train file and calculate.
                          (get_train_set => split_train => words_with_pos[key]+=1)
                          else just read options['train_count_filename'] and load result
    : parameter         : None
    : return            : words_with_pos(dict)
                        > {'넘나들/VV': 20,'비빔밥/NNG': 5, ...}
    """
    words_with_pos = {}
    if os.path.exists(options['train_count_filename']):
        with open(options['train_count_filename']) as fp:
            lines = fp.read().strip().split('\n')
        for line in lines:
            word_with_pos,count = line.split()
            words_with_pos[word_with_pos] = count
    else:
        trains = get_train_set(options['train_filename'])
        for train in trains:
            cur = train.split()[1]
            words_with_pos_list = split_train(cur)
            for word_with_pos in words_with_pos_list:
                if not word_with_pos in words_with_pos:
                    words_with_pos[word_with_pos] = 0
                words_with_pos[word_with_pos] += 1
        with open(options['train_count_filename'],'w') as fp:
            for key in words_with_pos:
                fp.write(str(key)+' '+str(words_with_pos[key])+'\n')
    return words_with_pos

if __name__ == '__main__':
    get_train_count()
