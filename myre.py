#myre.py
class __compiledre(object):
    """
        a compiled regular expression engine.
    """
    def __init__(self, NFA):
        """
            init this expression engine with a DFA.
            a DFA includes:
                transtable: a list of dic, each dic is set->STATE
                START_STATE, STOP_STATE: a set
                STATES: a list of set
        """
        self.transtable, self.START_STATE, self.STOP_STATE = DFA


    def search(self, string, start = 0, end = None):
        """
            try to match the string between [start, end) with this regular expression.
        """
        ans = []
        if end == None:
            end = len(string)
        matchx = start
        while True:
            if matchx == end:
                break
            nowstate = self.START_STATE
            tmatchy = matchx
            matchy = matchx
            while True:
                if nowstate == self.STOP_STATE:
                    matchy = tmatchy
                if tmatchy == end:
                    break
                nowstate = self.transtable[state].get(string[tmatchy], None)
                if nowstate == None:
                    break
                tmatchy = tmatchy + 1
            if matchy != matchx:
                ans.append((matchx, matchy))
                matchx = matchy
                continue
            matchx += 1
        return ans

def _pattern2NFA(pattern):
    """
        change pattern into NFA = (transtable, star_tstate, stop_state).
        pattern: a regular expression. support: \, |, *, (, )
        NFA:
            transtable: a list of dic: char/None -> set(). a state can turn into states in set with inputting char
    """
    s, t = 0, len(pattern)
    transtable = []
    error = 0

    def __add_trans(source, index, dest):
        while source >= len(transtable):
            transtable.append({})
        s = transtable[source].get(index, None)
        if s == None:
            transtable[source][index] = set([dest])
        else:
            s.add(dest)

    def __pattern_change(pt, _s, _t, start):
        if _s == _t:
            return start

        #check '|'
        bracket_num = 0
        for i in range(_s, _t):
            if pt[i] == '(':
                bracket_num += 1
            elif pt[i] == ')':
                if bracket_num > 0:
                    bracket_num -= 1
                else:
                    error = 1
                    return start
            elif pt[i] == '|' and bracket_num == 0:
                t_stop_state1 = __pattern_change(pt, _s, i, start + 1)
                t_stop_state2 = __pattern_change(pt, i + 1, _t, t_stop_state1 + 1)
                __add_trans(start, None, start + 1)
                __add_trans(start, None, t_stop_state1 + 1)
                __add_trans(t_stop_state1, None, t_stop_state2 + 1)
                __add_trans(t_stop_state2, None, t_stop_state2 + 1)
                return t_stop_state2 + 1
        
        #check '()' and '*'
        if pt[_s] == '(':
            bracket_num = 0
            for i in range(_s, _t):
                if pt[i] == '(':
                    bracket_num += 1
                if pt[i] == ')':
                    if bracket_num > 1:
                        bracket_num -= 1
                    elif bracket_num == 0:
                        error = 1
                        return start
                    elif bracket_num == 1:
                        if i + 1 < _t and pt[i + 1] == '*':
                            t_stop_state = __pattern_change(pt, _s + 1, i, start + 1)
                            __add_trans(start, None, start + 1)
                            __add_trans(start, None, t_stop_state + 1)
                            __add_trans(t_stop_state, None, start + 1)
                            __add_trans(t_stop_state, None, t_stop_state + 1)
                            return __pattern_change(pt, i + 2, _t, t_stop_state + 1)
                        else:
                            t_stop_state =  __pattern_change(pt, _s + 1, i, start)
                            return __pattern_change(pt, i + 1, _t, t_stop_state)

        #check others anid '*'
        if pt[_s] == '\\':
            if _s + 1 < _t and pt[_s + 1] == '*':
                __add_trans(start, '*', start + 1)
                return __pattern_change(pt, _s + 2, _t, start + 1)
            else:
                error = 1
                return start
        else:
            if _s + 1 < _t and pt[_s + 1] == '*':
                __add_trans(start, None, start + 1)
                __add_trans(start, None, start + 3)
                __add_trans(start + 1, pt[_s], start + 2)
                __add_trans(start + 2, None, start + 3)
                __add_trans(start + 2, None, start + 1)
                return __pattern_change(pt, _s + 2, _t, start + 3)
            else:
                __add_trans(start, pt[_s], start + 1)
                return __pattern_change(pt, _s + 1, _t, start + 1)

    stop_state = __pattern_change(pattern, s, t, 0)

    transtable.append({})
    if error:
        return None
    else:
        return (transtable, 0, stop_state)

from collections import deque
def _NFA2DFA(NFA):
    """
    change NFA into DFA.
    DFA : (transtable, startstate, stopstates)

    """
    NFA_transtable, NFA_startstate, NFA_stopstate = NFA
    transtable = []
    states = []
    stopstates = set()
    ids = set([x for dic in NFA_transtable for x in dic if x])
    print(NFA_stopstate)
    print(ids)
    def __find_dest(s, index):
        dest = set()
        for x in s:
            dest.update(NFA_transtable[x].get(index, set()))
        return dest

    def __closure(s):
        visit_flag = [0] * (NFA_stopstate + 1)
        l = len(s)
        s = set(s)
        x = s
        while True:
            x = __find_dest(x, None)
            s.update(x)
            if l == len(s):
                break
            l = len(s)
        return s
    
    def __check_state(s):
        if s not in states:
            states.append(s)
        if NFA_stopstate in s and s not in stopstates:
            stopstates.add(states.index(s))

    def __add_trans(source, index, dest):
        x = states.index(source)
        while x >= len(transtable):
            transtable.append({})
        transtable[x][index] = states.index(dest)

    d = deque()
    startstate = __closure(set([NFA_startstate]))
    d.append(startstate)
    while True:
        if not len(d):
            break
        s = d.popleft()
        __check_state(s)
        for index in ids:
            dest = __closure(__find_dest(s, index))
            if dest not in states:
                d.append(dest)
                __check_state(dest)
                __add_trans(s, index, dest)
    print(states)
    print(states.index(startstate))
    print(stopstates)
    print("*****************************************")
    print(transtable)
    print("*****************************************")
    return transtable
        
"""def recompile(pattern):
    NFA = _e_NFA2NFA(_pattern2e_NFA(pattern))
    print(NFA)
    return __compiledre(NFA)"""

