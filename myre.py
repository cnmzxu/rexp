#myre.py
class __compiledre(object):
    def __init__(self, NFA):
        self.transtable, self.START_STATE, self.STOP_STATES, self.STATES = NFA
    def search(self, string, start = 0, end = None):
        ans = list()
        if end == None:
            end = len(string)
        matchx = start
        while True:
            if matchx == end:
                break
            nowstates = set([self.START_STATE])
            tmatchy = matchx
            matchy = matchx
            while True:
                if len(nowstates & self.STOP_STATES) > 0:
                    matchy = tmatchy
                if tmatchy == end:
                    break
                newstate = set()
                for state in nowstates:
                    newstate |= self.transtable[state].get(string[tmatchy], set())
                if len(newstate) == 0:
                    break
                nowstates = newstate
                tmatchy = tmatchy + 1
            if matchy != matchx:
                ans.append((matchx, matchy))
                matchx = matchy
                continue
            matchx += 1
        return ans

def _pattern2e_NFA(pattern):
    transtable = [dict()]
    startstate = 0
    statenum = 1
    i = 0
    while True:
        _i = i + 1
        if _i != len(pattern) and pattern[_i] == '*':
            transtable[statenum - 1][None] = transtable[statenum - 1].get(None, set([])) | set([statenum - 1])
            transtable[statenum - 1][pattern[i]] = transtable[statenum - 1].get(pattern[i], set([])) | set([statenum - 1])
            i = _i + 1
        else:
            transtable[statenum - 1][pattern[i]] = transtable[statenum - 1].get(pattern[i],set([])) | set([statenum])
            statenum = statenum + 1
            transtable.append(dict())
            i = i + 1
        if i == len(pattern):
            break
    return (transtable, startstate, statenum - 1, range(statenum))

def _e_NFA2NFA(e_NFA):
    table, s, e, states = e_NFA
    e_closure = [None] * (max(states) + 1)
    transtable = [None] * (max(states) + 1)

    for state in states:
        stack = [state]
        e_closure[state] = [state]
        transtable[state] = dict()
        while(len(stack) > 0):
            x = stack.pop()
            for y in table[x].get(None, []):
                if y not in e_closure[state]:
                    e_closure[state].append(y)
                    stack.append(y)
        for x in e_closure[state]:
            for y in table[x]:
                if y != None:
                    transtable[state][y] = transtable[state].get(y, set()) | table[x][y]

    if e in e_closure[s]:
        stopstates = set([s, e])
    else:
        stopstates = set([e])

    return (transtable, s, stopstates, set(states))

def recompile(pattern):
    NFA = _e_NFA2NFA(_pattern2e_NFA(pattern))
    print(NFA)
    return __compiledre(NFA)

