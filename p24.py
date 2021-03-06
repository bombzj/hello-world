import sys, re

def sortexp2(exp):
    parts = []
    part = "*"
    bracket = False
    for i in exp:
        if bracket:
            if i == ")":
                bracket = False
            part = part + i
        else:
            if i == '(':
                bracket = True
                part = part + i
            elif i == '*' or i == '/':
                parts.append(part)
                part = i
            else:
                part = part + i
    parts.append(part)
    for i in range(len(parts)):
        i2 = parts[i]
        if i2.find('(') != -1:
            parts[i] = i2[:2] + sortexp1(i2[2:-1]) + ')'
        elif i2 == '/1':
            parts[i] = '*1'
    parts.sort()
    parts[0] = parts[0][1:]
    return "".join(parts)


def sortexp1(exp):
    parts = []
    part = "+"
    bracket = False
    for i in exp:
        if bracket:
            if i == ")":
                bracket = False
            part = part + i
        else:
            if i == '(':
                bracket = True
                part = part + i
            elif i == '+' or i == '-':
                parts.append(part)
                part = i
            else:
                part = part + i
    parts.append(part)
    for i in range(len(parts)):
        i2 = parts[i]
        if i2.find('*') != -1 or i2.find('/') != -1:
            parts[i] = i2[:1] + sortexp2(i2[1:])
    parts.sort()
    parts[0] = parts[0][1:]
    return "".join(parts)

def prepare(numstr, lowpri=[False, False, False, False]):
    global calclist
    if len(numstr) == 1:
        calclist.append(numstr[0])
    else:
        numlen = len(numstr)
        for i in range(numlen - 1):
            for j in range(i + 1, numlen):
                numstr2 = numstr[:i] + numstr[i + 1:j] + numstr[j + 1:]
                lowpri2 = lowpri[:i] + lowpri[i + 1:j] + lowpri[j + 1:]
                ni = numstr[i]
                nj = numstr[j]
                prepare(numstr2 + [ni + "+" + nj], lowpri2 + [True])
                prepare(numstr2 + [ni + "-" + nj], lowpri2 + [True])
                prepare(numstr2 + [nj + "-" + ni], lowpri2 + [True])
                if lowpri[i]: ni = "(" + ni + ")"
                if lowpri[j]: nj = "(" + nj + ")"
                prepare(numstr2 + [ni + "*" + nj], lowpri2 + [False])
                prepare(numstr2 + [ni + "/" + nj], lowpri2 + [False])
                prepare(numstr2 + [nj + "/" + ni], lowpri2 + [False])


def test(a, b, c, d):
    global calclist2
    for i in calclist2:
        try:
            if eval(i) == 24:
                return True
        except ZeroDivisionError:
            pass
    return False


calclist = []
prepare(['a', 'b', 'c', 'd'])
uniq = set()
for i in calclist:
    uniq.add(sortexp1(i))
calclist2 = list(uniq)

while True:
    cin = input("input 4 number:")
    cins = cin.split(' ')
    num = []
    for i in cins:
        if i.isdigit():
            num.append(float(i))

    if len(num) != 4:
        print("need 4 numbers")
        sys.exit()
    a, b, c, d = num

    result = []
    for i in calclist2:
        try:
            if eval(i) == 24:
                r = i.replace('a', str(int(a))).replace('b', str(int(b))).replace('c', str(int(c))).replace('d', str(int(d)))
                result.append(sortexp1(r))
        except ZeroDivisionError:
            pass

    result = list(set(result))
    result.sort()

    for i in result:
        print(i)