
import re

""" _____REGEX_____

    Symbols signification :
        - .     Le point correspond à n'importe quel caractère.
        - ^     Indique un commencement de segment mais signifie aussi "contraire de"
        - $     Fin de segment
        - [xy]  Une liste de segment possibble. Exemple [abc] équivaut à : a, b ou c
        - (x|y) Indique un choix multiple type (ps|ump) équivaut à "ps" OU "UMP" 
        - \d    le segment est composé uniquement de chiffre, ce qui équivaut à [0-9].
        - \D    le segment n'est pas composé de chiffre, ce qui équivaut à [^0-9].
        - \s    Un espace, ce qui équivaut à [ \t\n\r\f\v].
        - \S    Pas d'espace, ce qui équivaut à [^ \t\n\r\f\v].
        - \w    Présence alphanumérique, ce qui équivaut à [a-zA-Z0-9_].
        - \W    Pas de présence alphanumérique [^a-zA-Z0-9_].
        - \     Est un caractère d'échappement

    Occurence numbers:
        - A{2}     : on attend à ce que la lettre A (en majuscule) se répète 2 fois consécutives.
        - BA{1,9}  : on attend à ce que le segment BA se répète de 1 à 9 fois consécutives.
        - BRA{,10} : on attend à ce que le segment BRA ne soit pas présent du tout ou présent jusqu'à 10 fois consécutives.
        - VO{1,}   : on attend à ce que le segment VO soit présent au mois une fois.
    
    symbole	    Nb Caractères attendus  Exemple	    Cas possibles
    ?	        0 ou 1	                GR(.)?S	    GRS, GROS, GRIS, GRAS
    +	        1 ou plus	            GR(.)+S	    GROS, GRIS, GRAS
    *	        0, 1 ou plus	        GR(.)*S	    GRS,GROO,GRIIIS,GROlivierS
"""

splitted = "mdlfile -r --json --path 'C:/Programs/hello.json'".split(" ")
print(splitted)
for elem in splitted:
    if re.match("mdl([a-z])+", elem) != None:
        print("module: {}".format(elem))
    elif re.match("(-|-{2})+", elem) != None:
        print("command:", end=' ')
        if re.match("(-|-{2})+(j|json)", elem) != None:
            print("json: {}".format(elem))
        elif re.match("(-|-{2})+(p|path)", elem) != None:
            print("path: {}".format(elem))
            print("path: {}".format(splitted[splitted.index(elem)+1]))
        elif re.match("(-|-{2})+(r|read)", elem) != None:
            print("read: {}".format(elem))
        elif re.match("(-|-{2})+(w|write)", elem) != None:
            print("write: {}".format(elem))
        else:
            print("unknown command")
    elif re.match("(')+", elem) != None:
        print(elem)




