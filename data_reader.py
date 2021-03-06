from nltk import ParentedTree

class DataSet(object):
    """description of class"""
    def __init__(self,file,haslabel=True):
        self.haslabel=haslabel
        self.dict={}
        self.data=[]
        with open(file) as f:
            for line in f:
                values=line.split()
                docname=values[0]
                list=self.dict.get(docname,[])
                coref=Coref(values,haslabel)
                list.append(coref)
                self.data.append(coref)



class Coref(object):
    def __init__(self,list,haslabel):
        
        if haslabel:
            self.label = list[-1]
            list=list[:-1]
        else:
            self.label=None
        self.document=list[0][:-11]
        self.first = Markable()
        self.second = Markable()
        self.first.sent, self.first.start, self.first.end, self.first.ne, self.first.word = list[1:6]
        self.second.sent, self.second.start, self.second.end, self.second.ne, self.second.word = list[6:]
        self.first.start = int(self.first.start)
        self.second.start = int(self.second.start)
        self.first.end = int(self.first.end)
        self.second.end = int(self.second.end)
        self.first.sent = int(self.first.sent)
        self.second.sent = int(self.second.sent)

class Markable(object):
    pass


class Document(object):

    def __init__(self,fparsed,fpos):
        self.sents=[]
        self.trees=[]
        with open(fparsed,'r') as f1:
            with open(fpos,'r') as f2:
                poslines=filter(lambda x:x.strip() != '', f2.readlines())
                lines=f1.readlines()
                for line,pos in zip(lines,poslines):
                    #positer=iter(pos.split())
                    #tup=None

                    #def read_node(str):
                    #    try:
                    #        if tup==None:
                    #            tup=positer.next().split('_')
                    #        if tup[0]==str:
                    #            tup=None
                    #            return tuple(tup)
                    #        print str
                    #        print tup
                    #        return tup
                    #    except StopIteration:
                    #        return str
                        
                    tree=ParentedTree.fromstring(line,read_leaf=read_node)
                    self.sents.append(tree)

class Corpus(object):
    def __init__(self,folder):
        pass



    


if __name__ == '__main__':
    doc=Document(r"D:\Projects\ie_proj2\nopos\APW20001001.2021.0521.head.coref.raw.txt",r"D:\Projects\ie_proj2\postagged-files\APW20001001.2021.0521.head.coref.raw.pos")
    pass
