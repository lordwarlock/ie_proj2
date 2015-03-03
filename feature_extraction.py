from feature_functions import get_feature_functions
from data_reader import *
from build_corpus import BuildCorpus
#from gender_detector import gender_detector


class FeatureExtraction(object):
    def __init__(self,corpus=None):
        self.corpus = corpus
        self.feat = []
        self.data= None
        self.weka_attr = []
    def extract(self,dataset):
        ffunc_list = get_feature_functions()
        for index,line in enumerate(dataset.data):
            if line==None:
                self.feat.append(None)
            else:
                featuredict={ffunc.__name__:str(ffunc(line,self.corpus)) for ffunc in ffunc_list}
                if dataset.haslabel:
                    featuredict['label']=line.label
                self.feat.append(featuredict)

    def mallet_output(self,line):
        label=None
        list=[]
        for key,value in line.iteritems():
            if key=='label':
                label=value
                continue
            list.append(key + '=' + str(value))
        return ('' if label==None else label + ' ') +  ' '.join(list)

    def output_feat(self,filename,linefunc):
        with open(filename,'w') as output_file:
            for line in self.feat:
                
                output_file.write(linefunc(line) + '\n')

    def weka_output(self,line):
        label = None
        result = ''
        for key,value in line.iteritems():
            if key == 'label':
                label = value
                continue
            if key not in self.weka_attr: self.weka_attr.append(key)
            result += str(value) + ', '
        return result + label
"""
@RELATION coref_train

@ATTRIBUTE distance	numeric
@ATTRIBUTE both_pronoun	{0,1,2}
@ATTRIBUTE demonstrative	{True,False}
@ATTRIBUTE definite	{True,False}
@ATTRIBUTE sub_str	{True,False}
@ATTRIBUTE ne_match	{True,False}
@ATTRIBUTE str_match	{True,False}
@ATTRIBUTE capital_i_j	{0,1,2}
@ATTRIBUTE prp_str_match	{True,False}
@ATTRIBUTE pronoun_2	{True,False}
@ATTRIBUTE pronoun_1	{True,False}
@ATTRIBUTE class 	{yes, no}

@DATA
"""
if __name__=='__main__':
    f_ex=FeatureExtraction(BuildCorpus())
    f_ex.extract(DataSet(r"./project2/data/coref-trainset.gold"))
    f_ex.output_feat(r"coref-trainset.gold.fv.txt",f_ex.mallet_output)
    f_ex.output_feat(r"weka-trainset.arff",f_ex.weka_output)
    print f_ex.weka_attr
    f_ex=FeatureExtraction(BuildCorpus())
    f_ex.extract(DataSet(r"./project2/data/coref-testset.gold"))
    f_ex.output_feat(r"coref-testset.gold.fv.txt",f_ex.mallet_output)
    f_ex.output_feat(r"weka-testset.arff",f_ex.weka_output)
