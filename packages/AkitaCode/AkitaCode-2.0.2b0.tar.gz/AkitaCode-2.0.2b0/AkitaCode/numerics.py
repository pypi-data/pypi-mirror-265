def to_signed_format(n):
    """
    Aquesta funció converteix un enter negatiu a la seva representació en complement a dos.
    
    :param n: Enter que es vol convertir a complement a dos.
    :type n: int
    :return: Representació en binari signat en complement a dos o False si n no és un enter negatiu.
    :rtype: int (or False)
    """
    if type(n) == int:
        if n < 0:
            nstr = "{0:b}".format(n)
            aux = int(nstr[1:],2)
            exp = 0
            for e in list(range(0,64)):
                if (2**e) >= aux:
                    exp = e
                    break
            r = n + (2*(2**exp))
            return r
        else:
            return False
    else:
        False



def to_int_format(n):
    """
    Aquesta funció converteix un enter en format de complement a dos (utilitzat en la codificació de números negatius) 
    a un enter negatiu.

    :param n: Valor que es vol convertir a format de complement a dos.
    :type n: int
    :return: Valor resultant de la conversió o False si n no és un enter.
    :rtype: int (or False)
    """
    if type(n) == int:
        if n > 0:
            nstr = "{0:b}".format(n)
            newval = 0
            for i in list(range(len(nstr))):
                if i == 0:
                    newval -= 2**((len(nstr)-1)-i)*int(nstr[i])
                else:
                    newval += 2**((len(nstr)-1)-i)*int(nstr[i])
            
            return newval
            
        else:
            return False
    else:
        return False
    

def list_to_int(l:list):
    """
    Converteix una llista de enters compressos entre 0-255, en un enter.
    """
    return int.from_bytes(bytes(l))


def int_reverse(i:int):
    """
    Gira els bits lògics del
    """




if __name__ == "__main__":
    a = -12
    b = -5
    c = -27
    d = -1
    e = -129
    print(to_signed_format(a))
    print(to_signed_format(b))
    print(to_signed_format(c))
    print(to_signed_format(d))
    print(to_signed_format(e))
    a = 20
    b = 11
    c = 37
    d = 1
    e = 383
    print(to_int_format(a))
    print(to_int_format(b))
    print(to_int_format(c))
    print(to_int_format(d))
    print(to_int_format(e))