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
        'show_screen'           : True
        }

def get_train_set(filename):
    """
    : get_train_set - function
                    : read train file
    : parameter     - train_filename(str)
                    > 'train.txt'
    : return        - train_lines_list(list<str>)
                    >  ['기회가  기회/NNG+가/JKS','말  말/NNG',...]
    : dependency    - None
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
    : dependency        - None
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
    : dependency    - re, split_by_position 
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
    : dependency    - None
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
    : dependency        - split_train, split_slash
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
            pos_list = []
            """
            : WORD/POS count
            > count(WORD/POS)
            """
            for word_with_pos in words_with_pos_list:
                if not word_with_pos in words_with_pos:
                    words_with_pos[word_with_pos] = 0
                words_with_pos[word_with_pos] += 1
                pos_list.append(split_slash(word_with_pos)[1])
            """
            : bigram count and unigram count
            > count(JKO/NP) and count(JKO)
            """
            for i in xrange(len(pos_list)):
                if i == 0:
                    bigram_key = pos_list[i]+'/$'
                else:
                    bigram_key = pos_list[i]+'/'+pos_list[i-1]
                if not bigram_key in words_with_pos:
                    words_with_pos[bigram_key] = 0
                words_with_pos[bigram_key] += 1     # bigram count
                if not pos_list[i] in words_with_pos:
                    words_with_pos[pos_list[i]] = 0
                words_with_pos[pos_list[i]] += 1    # unigram count
        words_with_pos['$'] = len(trains)
        with open(options['train_count_filename'],'w') as fp:
            for key in words_with_pos:
                fp.write(str(key)+' '+str(words_with_pos[key])+'\n')
    return words_with_pos

def calculate_conditional_probability(count_dictionary,expr):
    """
    : calculate_conditional_probability - function
                                        : calculate probability given expression P(A|B)
                                        : P(A|B) = P(AB)/P(B)
                                        : P(A|B) = count(AB)/count(B)
    : parameter                         : count_dictionary(dict), expr(str)
                                        > {'넘나들/VV': 20,'JKO/NP':3931,'NP':47549,...}, 'JKO/NP'
    : return                            : probability(float)
                                        > 0.0826726114114
    : dependency                        - split_slash
    """
    (left,right) = split_slash(expr)
    if not right in count_dictionary:
        return 0.0001
    if count_dictionary[right] == 0:
        return 0.0001
    if not expr in count_dictionary:
        return 0.0001
    if count_dictionary[expr] == 0:
        return 0.0001
    return float(count_dictionary[expr])/float(count_dictionary[right])

def print_dictionary(d):
    """
    : print dictionary  - function
                        : test dictionary printer
    : parameter         - d(dict)
    : return            - None
    : dependency        - None
    """
    for key in d:
        print key, d[key]

def get_input_datas(filename):
    """
    : get_input_datas   - function
                        : read input file
    : parameter         - filename(str)
    : return            - ret(list<str>)
    : dependency    - None
    """
    with open(filename,'r') as fp:
        lines = fp.read().strip().split('\n')
    ret = []
    for line in lines:
        line.strip()
        if len(line) == 0:
            continue
        ret.append(line)
    return ret

def get_result_datas(filename):
    """
    : get_result_datas  - function
                        : read result file and create dict<list<str>>
    : parameter         : filename(str)
    : return            : ret(dict<list<str>>)
                        > {'안녕하세요':['안녕/NNG+하/NNG+세/NNB+요/EC','안녕/NNG+하/MAG+세/NNB+요/EC',..],...}
    : dependency        - get_input_datas
    """
    ret = {}
    lines = get_input_datas(filename)
    for line in lines:
        if not line.split('.')[0].strip().isdigit():
            key = line
            ret[key] = []
        else:
            ret[key].append(line.split()[1].strip())
    return ret

def calculate_observation_probability(count_dictionary,cur_morpheme):
    """
    : calculate_observation_probability - function
                                        : calculate current morpheme seq's observation probability
    : parameter                         : count_dictionary(dict), cur_morpheme(list<str>)
                                        > pass                  , ['안녕/NNG','하/XSV','세/EC','요/JX']
    : return                            : observation_probability(float)
                                        > P(안녕/NNG)*P(XSV/NNG)*P(하/XSV)*P(EC/XSV)*P(세/EC)*P(JX/EC)*P(요/JX)
    : dependency                        - calculate_conditional_probability, split_slash
    """
    observation_probability = calculate_conditional_probability(count_dictionary,cur_morpheme[0])
    for i in xrange(1,len(cur_morpheme)):
        previous_pos    = split_slash(cur_morpheme[i-1])[1]
        cur_pos         = split_slash(cur_morpheme[i])[1]
        observation_probability *= calculate_conditional_probability(count_dictionary,cur_pos+'/'+previous_pos)
        observation_probability *= calculate_conditional_probability(count_dictionary,cur_morpheme[i])
    return observation_probability

def hmm(count_dictionary,morpheme_dictionary,input_data):
    """
    : hmm           - function
                    : get highest probability morpheme sequence given input_data
                      using hmm and viterbi algorithm (bigram)
    : parameter     : count_dictionary(dict), morpheme_dictionary(dict<str,list<str>>), input_data(str)
                    > pass                  , pass                                    , '너를 사랑해!'
    : return        : ans(list<str>)
                    > ['너르/VA+ㄹ/ETM','사랑/NNG+하/VV+어/EF+!/SF']
    : dependency    - split_train, split_slash, calculate_conditional_probability, calculate_observation_probability
    """
    words = input_data.split()
    d = []  # dynamic programming table[word_length][that_word_morpheme_size]
    b = []  # backtracking table[word_length][that_word_morpheme_size]
    for word in words:
        d.append([ 0 for i in xrange(len(morpheme_dictionary[word])) ])
        b.append([ -1 for i in xrange(len(morpheme_dictionary[word])) ])

    """
    : viterbi(dp) algorithm 
    : a_st,ed  : transition_probability(st|ed)
    : b_s(o_1) : observation_probability(o_1)
    :
    : initializing state ( $ => ... )
    > for each state s form 1 to N do
    >   d[1,s]<-a_0,s * b_s(o_1)
    >   b[1,s]<-0
    """
    cur_morpheme_list = morpheme_dictionary[words[0]]
    for i in xrange(len(cur_morpheme_list)):
        cur_morpheme = split_train(cur_morpheme_list[i])
        first_pos = split_slash(cur_morpheme[0])[1]
        transition_probability  = calculate_conditional_probability(count_dictionary,first_pos+'/$')
        observation_probability = calculate_observation_probability(count_dictionary,cur_morpheme)
        d[0][i] = transition_probability*observation_probability
        b[0][i] = -1

    """
    : recursion step
    > for time step t from 1 to T-1 do
    >   for each state s from 1 to N do
    >       d[t,s]<-max_(1<=s'<=N)(d[t-1,s']*a_s',s*b_s(o_t)
    >       b[t,s]<-argmax_(1<=s'<=N)(viterbi[t-1,s']*a_s',s
    """
    for i in xrange(1,len(words)):
        cur_morpheme_list = morpheme_dictionary[words[i]]
        for j in xrange(len(cur_morpheme_list)):
            cur_morpheme = split_train(cur_morpheme_list[j])
            first_pos = split_slash(cur_morpheme[0])[1]
            observation_probability = calculate_observation_probability(count_dictionary,cur_morpheme)
            mx,idx = -1,-1
            for k in xrange(len(d[i-1])):
                previous_morpheme_list  = morpheme_dictionary[words[i-1]]
                previous_morpheme       = split_train(previous_morpheme_list[k])
                previous_pos            = split_slash(previous_morpheme[-1])[1]
                transition_probability = calculate_conditional_probability(\
                                            count_dictionary,first_pos+'/'+previous_pos)
                if d[i-1][k]*transition_probability*observation_probability > mx:
                    mx,idx = d[i-1][k]*transition_probability*observation_probability,k
            d[i][j] = mx
            b[i][j] = idx

    """
    : termination step
    > d[n-1,qF] <- max_(1<=s<=N)(d[n-1,s]*a_s,qF
    > b[n-1,qF] <- argmax_(1<=s<=N)(d[n-1,s]*a_s,qF
    """
    mx,idx = -1,-1
    for i in xrange(len(d[-1])):
        if d[-1][i] > mx:
            mx,idx = d[-1][i],i
    """
    : the backtrace path by following backpointers
      to states back in time from backpointer[n-1,qF]
    """
    ans = []
    for i in xrange(len(words)-1,-1,-1):
        ans = [morpheme_dictionary[words[i]][idx]]+ans
        idx = b[i][idx]
    return ans

if __name__ == '__main__':
    count_dictionary    = get_train_count()
    input_datas         = get_input_datas(options['input_filename'])
    morpheme_dictionary = get_result_datas(options['result_filename'])
    
    with open(options['output_filename'],'w') as fp:
        for input_data in input_datas:
            ans = hmm(count_dictionary,morpheme_dictionary,input_data)
            fp.write(input_data+'\n')
            for item in ans:
                fp.write(item+' ')
            fp.write('\n')
            """
            : if show_screen option is True, print screen
            """
            if options['show_screen']:
                print input_data
                for item in ans:
                    print item,
                print ''
