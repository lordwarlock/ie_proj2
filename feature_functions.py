import re
import inflect
import gender_detector as gd
def get_feature_functions():
    #return [hint_word_detection,hint_who_detection]
    return [distance,definite,demonstrative,str_match,sub_str,pro_str_match,ne_match,pronoun_1_v01,pronoun_2_v01,capital_i_j,both_pronoun,gender_agree,number_agree,alias,appositive,hint_word_detection,hint_who_detection]


#pronons = ['i', ]

def distance(coref,corpus):
    return coref.second.sent-coref.first.sent

def definite(coref,corpus):
    document = coref.document
    second = coref.second
    if coref.second.word.lower().startswith('the_'):
        return True
    if (second.start == 0): return False
    if (corpus.postagged_data[document][second.sent].tokens[second.start - 1][0].lower() == 'the'):
        return True
    return False

def demonstrative(coref,corpus):
    if coref.second.word.lower() in ['this', 'that', 'those', 'these']:
        return True
    document = coref.document
    second = coref.second
    if (second.start == 0): return False
    if (corpus.postagged_data[document][second.sent].tokens[second.start - 1][0].lower() in \
         ['this', 'that', 'those', 'these']):
        return True
    return False
    

def str_match(coref,corpus):
    return coref.first.word.lower() == coref.second.word.lower()



def sub_str(structure,corpus):
    if structure.first.word.lower() in structure.second.word.lower():
        return True
    elif structure.second.word.lower() in structure.first.word.lower():
        return True
    else:
        return False

def pro_str_match(structure,corpus):
    document = structure.document
    first = structure.first
    second = structure.second
    Postag_first = corpus.postagged_data[document][first.sent].tokens[first.start:first.end]
    Postag_second = corpus.postagged_data[document][second.sent].tokens[second.start:second.end]
    if Postag_first[0][1] == 'PRP' and Postag_second[0][1] == 'PRP' and first.word == second.word:
        #print first.word
        return True
    else:
        return False

def ne_match(structure,corpus):
    if (structure.first.ne == structure.second.ne):
        return True
    else:
        return False

def pronoun_1(structure,corpus):
    document = structure.document
    first = structure.first
    second = structure.second
    return corpus.postagged_data[document][first.sent].tokens[first.start:first.end][0][1]=='PRP'

def pronoun_1_v01(structure,corpus):
    document = structure.document
    first = structure.first
    second = structure.second
    tags = [ token_tuple[1] for token_tuple in\
        corpus.postagged_data[document][first.sent].tokens[first.start:first.end]]
    if ('PRP' in tags): return True
    else: return False

def pronoun_2(structure,corpus):
    document = structure.document
    first = structure.first
    second = structure.second
    return corpus.postagged_data[document][second.sent].tokens[second.start:second.end][0][1]=='PRP'

def pronoun_2_v01(structure,corpus):
    document = structure.document
    first = structure.first
    second = structure.second
    tags = [ token_tuple[1] for token_tuple in\
        corpus.postagged_data[document][second.sent].tokens[second.start:second.end]]
    if ('PRP' in tags): return True
    else: return False

def capital_i_j(structure,corpus):
    result = 2
    if (structure.first.word == structure.first.word.lower()):
        result -= 1
    if (structure.second.word == structure.second.word.lower()):
        result -= 1
    return result

def both_pronoun(structure,corpus):
    return pronoun_1(structure,corpus) + pronoun_2(structure,corpus)

def gender_agree(coref,corpus):
    g1=gender(coref.first.ne,coref.first.word,getslice(coref,corpus,1))
    g2=gender(coref.second.ne,coref.second.word,getslice(coref,corpus,2))
    if g1 == g2 and g1 != None:
        return True
    elif g1 == g2 and g1 == None:
        return None
    else:
        return False

def getslice(coref,corpus,num):
    markable= coref.first if num == 1 else coref.second
    return corpus.postagged_data[coref.document][markable.sent].tokens[markable.start:markable.end]

def number_agree(coref,corpus):
    n1 = number(coref.first.word,getslice(coref,corpus,1)) 
    n2 = number(coref.second.word,getslice(coref,corpus,2))
    #print n1,n2
    return n1 == n2

num_detect=inflect.engine()
def number(str,words):
    if len(words) == 1:
        pos = words[0][1][0]
        if pos=='N':
            return not num_detect.singular_noun(words[0][0]) == words[0][0]
        else:
            return num_detect.plural_adj(words[0][0]) == words[0][0]
    else:
        return num_detect.plural(str.replace('_',' ')) == str.replace('_',' ')
    

detector=gd.GenderDetector(unknown_value=None)
def gender(ne,str,words):
    if ne == 'PER':
        if str.lower() in ['his','him','he']:
            return 'male'
        elif str.lower() in ['hers','her','she']:
            return 'female'
        else:
            special_char_match = re.match('[a-zA-Z]+',words[0][0])
            if (special_char_match):
                if (special_char_match.group(0) != words[0][0]): return None
            else:
                return None
            guess = detector.guess(words[0][0])
            if guess == None and len(words) > 1:
                guess = detector.guess(words[-1][0])
        return guess
    else:
        return None

def alias(coref,corpus):
    w1=getslice(coref,corpus,1)
    w2=getslice(coref,corpus,2)
    w1=min(w1,w2,key=len)
    w2=max(w1,w2,key=len)
    if len(w1) == 1:
        acronym=''.join([w[0][0] for w in w2])
        if acronym == w1[0]:
            return True
    return False

def appositive(coref,corpus):
    if coref.first.sent == coref.second.sent:
        line=corpus.sentence_data[coref.document][coref.first.sent]
        node1=line.index[coref.first.start].parent()
        nodes = []
        while node1 != None and node1.label() != '' and node1.label()[0]=='N' :
            nodes.append(node1)
            node1 = node1.parent()
        node2 = line.index[coref.second.start].parent()
        while node2 != None and node2.label() != '' and node2.label()[0]=='N' :
            if node2 in nodes:
                return True
            node2 = node2.parent()
    return False

def hint_word_detection(coref,corpus,token_distance = 3,hint_words = ['is','are','was','were','be']):
    if(coref.first.sent != coref.second.sent): return False
    if ((coref.second.start - coref.first.start) > token_distance): return False
    between_word_list = []
    document = coref.document
    sentence = corpus.postagged_data[document][coref.first.sent].tokens
    for i in range(coref.first.start,coref.second.end):
        if (sentence[i][0] in hint_words):
            print coref.first.word,coref.first.end, coref.second.word,coref.second.start
            print sentence[coref.first.start:coref.second.end]
            return True

    return False
        
def hint_who_detection(coref,corpus):
    return hint_word_detection(coref,corpus,hint_words = ['who','which'],token_distance=5)
if __name__ == '__main__':
    from data_reader import *
    from feature_extraction import FeatureExtraction
    from build_corpus import BuildCorpus
    f_ex=FeatureExtraction(BuildCorpus())
    f_ex.test(DataSet(r"./project2/data/coref-trainset.gold"),appositive)
