
def dectobin(d,nb=8):
    """Représentation d'un nombre entier en chaine binaire (nb: nombre de bits du mot)"""
    if d == 0:
        return "0".zfill(nb)
    if d<0:
        d += 1<<nb
    b=""
    while d != 0:
        d, r = divmod(d, 2)
        b = "01"[r] + b
    return b.zfill(nb)


a = 92    # 01011100
print(bool(int('00001000',2) & a))
print(dectobin((1<<(2-1))))
print(bool((2<<(4-1)) & a))

