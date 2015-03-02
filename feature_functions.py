import re

def get_feature_functions():
    return [distance,definite,demonstrative,str_match,sub_str]


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
    Postag_first = corpus.postagged_data[document][first.sent][first.start:first.end]
    Postag_second = corpus.postagged_data[document][second.sent][second.start:second.end]
    if Postag_first.endswith('_PRP') and Postag_second.endswith('_PRP') and first.word == second.word:
        return True
    else:
        return False
