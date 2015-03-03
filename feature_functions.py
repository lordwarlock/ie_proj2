import re

def get_feature_functions():
    return [distance,definite,demonstrative,str_match,sub_str,pro_str_match,ne_match,pronoun_1,pronoun_2,capital_i_j]


#pronons = ['i', ]

def distance(coref,corpus):
    return coref.second.sent-coref.first.sent

def definite(coref,corpus):
    return coref.second.word.lower().startswith('the_')


def demonstrative(coref,corpus):
    return coref.second.word.lower() in ['this', 'that', 'those', 'these']

def str_match(coref,corpus):
    return coref.first.word == coref.second.word



def sub_str(structure,corpus):
    if structure.first.word in structure.second.word:
        return True
    elif structure.second.word in structure.first.word:
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

def pronoun_2(structure,corpus):
    document = structure.document
    first = structure.first
    second = structure.second
    return corpus.postagged_data[document][second.sent].tokens[second.start:second.end][0][1]=='PRP'

def capital_i_j(structure,corpus):
    result = 2
    if (structure.first.word == structure.first.word.lower()):
        result -= 1
    if (structure.second.word == structure.second.word.lower()):
        result -= 1
    return result

