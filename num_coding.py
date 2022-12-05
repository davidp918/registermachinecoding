def enc_pair(x, y):
    # Encode <<x, y>>
    return (2 ** x * (2 * y + 1))


def dec_pair(code):
    # Decode <<x, y>>
    x = 0
    y = 0

    while code % 2 == 0:
        code = code // 2
        x += 1
    y = (code - 1) / 2

    return(x, y)


def enc_pair_alt(x, y):
    # Encode <x, y>
    return (2 ** x * (2 * y + 1) - 1)


def dec_pair_alt(code):
    # Decode <x, y>
    return dec_pair(code + 1)


def enc_list(l):
    if l == []:
        return 0
    else:
        return enc_pair(l[0], enc_list(l[1:]))


def dec_list(code):
    res = []

    while code != 0:
        (item, tail) = dec_pair(code)
        code = tail
        res.append(item)

    return res


def dec_instr(code):
    res = []

    if code == 0:
        return res

    (i, j) = dec_pair(code)

    if i % 2 == 0:
        res.append(i // 2)
        res.append(j)

    else:
        # res.append((i - 1) // 2)
        res.append(i)
        (k, l) = dec_pair_alt(j)
        res.append(k)
        res.append(l)

    return res


def enc_instr(instr):
    # Representations:
    # HALT = []
    # Ri + -> Rj = [i, j]
    # Ri - -> Rj, Rk = [i, j, k]
    if len(instr) == 0:
        return 0
    elif len(instr) == 2:
        return enc_pair(2 * instr[0], instr[1])

    goto = enc_pair_alt(instr[1], instr[2])
    return enc_pair(2 * instr[0] + 1, goto)


def enc_rm(machine):
    # Encode register machine instruction by instruction
    res = []
    for instr in machine:
        res.append(enc_instr(instr))

    return enc_list(res)


def dec_rm(code):
    res = []
    instrs = dec_list(code)

    for instr in instrs:
        res.append(dec_instr(instr))

    return res


def print_rm(rm):
    for i, instr in enumerate(rm):
        if len(instr) == 1:
            print(f"L{i}: HALT")
        elif len(instr) == 2:
            print(f"L{i}: R" + str(instr[0]) + "+ -> L" + str(instr[1]))
        else:
            print(f"L{i}: R" + str(instr[0]) + "- -> L" + str(instr[1])
                  + ", L" + str(instr[2]))


p1 = (0, 0)
p2 = (1, 2)

r1 = enc_pair(*p1)
r2 = enc_pair_alt(*p2)

print(r1)
print(r2)

d1 = dec_list(2 ** 94 * 16395)
print(d1)

print(dec_pair(8197))

print(enc_list([94, 0, 1, 10]))

print_rm([[1, 3, 1], [0], [0, 0], [1, 0, 1]])
