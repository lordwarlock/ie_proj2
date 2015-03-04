import glob
import re
from nltk.tree import Tree
class SentLine(object):
    def __init__(self,line):
        self.tree = Tree.fromstring(line)
class PosLine(object):
    def __init__(self,line):
        token_poses = line.split()
        self.tokens = []
        for token_pos in token_poses:
            match = re.match('(.*)_(.*)',token_pos)
            self.tokens.append((match.group(1),match.group(2)))

    def __str__(self):
        return str(self.tokens)

class BuildCorpus(object):
    def __init__(self):
        self.postagged_data = dict()
        self.sentence_data = dict()
        self.corpus = None
        self.build_postagged_data()
        #self.build_sentence_data()

    def build_postagged_data(self,directory='./postagged-files'):
        pos_files = glob.glob(directory+'/*.pos')
        regex=re.compile(r'.*[/|\\](.*?)\.head\.coref\.raw\.pos')
        for pos_file in pos_files:
            with open(pos_file,'r') as f_pos:
                match = regex.match(pos_file)
                data_name = match.group(1)
                lines = []
                for line in f_pos:
                    if (line == '\n'): continue
                    lines.append(PosLine(line))
                self.postagged_data[data_name] = lines

    def build_sentence_data(self,directory='./nopos'):
        sentence_files = glob.glob(directory+'/*.txt')
        for sentence_file in sentence_files:
            with open(sentence_file,'r') as f_sent:
                match = re.match('.*/(.*?)\.head\.coref\.raw\.txt',sentence_file)
                data_name = match.group(1)
                lines = []
                for line in f_sent:
                    lines.append(SentLine(line))
                self.sentence_data[data_name] = lines
if __name__ == '__main__':
    bc = BuildCorpus()
    #print bc.postagged_data.values()[0][15].tokens[23:24]
