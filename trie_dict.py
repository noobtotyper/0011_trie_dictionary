import marisa_trie

def rev(l):
    return [w[::-1] for w in l]

def imp_words():
    with open("de_50k.txt","r") as f:
        words=[word.split()[0] for word in f.readlines()]
        freqs=dict((b,str(a).zfill(5)) for a, b in (enumerate(words)))
        alph=sorted(words)
        hpla=sorted(rev(words))
        return words, freqs, alph, hpla

def imp_dict():
    with open("dict_de_en.txt","r") as f:
        words=[word.strip() for word in f.readlines()]
        return dict(zip(words[0::2],words[1::2]))

words,freqs,alph,hpla=imp_words()
dict_de_en=imp_dict()

pre=marisa_trie.Trie(alph)
su=marisa_trie.Trie(hpla)

prefix_mode=True # If true defaults to prefix search when the search string has no spaces.
translation=True # If true hows translation
frequencies=True # If true hows frequency count for the word
intersection_mode=True # If true ouputs words that match both prefix and suffix search. Otherwise union.
sort_by_freq=True # If true sorts by frequency instead of alphabetically
sort_reverse=True # If true shows most frequent words near the bottom

def query(x):
    #infix search
    if len(x)>1 and x[0]==" " and x[-1]==" ":
        keys=[key for key in alph if x[1:-1] in key]
    #suffix only
    elif x[0]==" ":
        x=x[1::] # remove space
        x=x[::-1] # input needs to be reversed because trie stores reversed strings
        keys=rev(su.keys(x)) # each word found in the trie is reversed, so reverse again
    #prefix only
    elif x[-1]==" ":
        x=x[:-1] # remove space
        keys=pre.keys(x)
    else:
        x=x.split() # any whitespace as separator
        #neither, return from default mode
        if len(x)==1:
            if prefix_mode:
                keys=pre.keys(x[0])
            else:
                x=x[::-1] # input needs to be reversed because trie stores reversed strings
                keys=rev(su.keys(x[0])) # each word found in the trie is reversed, so reverse again
        #both, then combine them
        else:
            k1=pre.keys(x[0])
            k2=rev(su.keys(x[1][::-1]))
            # Either intersection (both prefix and suffix match query)
            if intersection_mode:
                keys= list(set(k1) & set(k2))
            # Or union (either prefix or suffix match query)
            else:
                keys= list(set(k1) | set(k2))

    if keys==None:
        print("-")
    else:
        if sort_by_freq:
            keys.sort(key=lambda x:freqs[x], reverse=sort_reverse)
        else:
            keys.sort() # alphabetically
        # Format results
        results=[]
        for key in keys:
            result=""
            if frequencies:
                result+=freqs[key]
            result+="\t"
            result+=key.ljust(25) # To make columns
            if translation:
                result+=dict_de_en[key].ljust(30) 
            results.append(result)
        for r in results:
            print(r)


def print_help():
    print("Usage:\n\tPress ENTER without input to quit\n\tInput query text \"prefix[space]suffix\" + ENTER\n\tIf there is only one pre/suf-fix it uses flag -r\n\n(Edit code to change defaults)\n-h for help\n-c is pre/suf-fix combination (intersection vs union)\n-f to switch frequency on/off (number 0 to 49999 [ON])\n-r to reverse the searches (default mode prefix)\n-s to sort by frequencies on/off (default on)\n-S to sort in reverse order on/off (default on))\n-t to switch translation on or off (default on)")

print_help()
while x:=input():
    if x[0]=="-":
        if len(x)==1:
            pass
        elif x[1]=="h":
            print_help()
        elif x[1]=="c":
            intersection_mode=not intersection_mode
        elif x[1]=="f":
            frequencies=not frequencies
        elif x[1]=="r":
            prefix_mode=not prefix_mode
        elif x[1]=="s":
            sort_by_freq=not sort_by_freq
        elif x[1]=="S":
            sort_reverse=not sort_reverse
        elif x[1]=="t":
            translation=not translation
        print("\nIntersection (vs union): {}\nFrequencies: {}\nSort by frequencies: {}\nReverse sort on/off {}\nPrefix mode: {}\nTranslation: {}".format(intersection_mode,frequencies,sort_by_freq,sort_reverse,prefix_mode,translation))
    else:
        query(x)
    print("-------------------------------------------------------")

