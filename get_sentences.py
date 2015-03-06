import glob
import re
class GetSentences(object):
    def __init__(self,in_dir,extension,out_dir):
        self.in_dir = in_dir
        self.extension = extension
        self.dir_list = glob.glob(in_dir+'/*.'+extension)
        #print self.dir_list
        self.out_dir = out_dir
        for directory in self.dir_list:
            self.process_each_file(directory,self.out_dir)
            #break
    def exclude_POStag(self,line):
        result = re.sub('_.*? ',' ',line[:-1])
        result = re.sub('\(','[',result)
        result = re.sub('\)',']',result)
        return result

    def process_each_file(self,dir_in,dir_out):
        in_match = re.match('.*/(.*?)\.'+self.extension,dir_in)
        filename = in_match.group(1)
        file_out = dir_out+ '/' + filename + '.txt'
        with open(dir_in,'r') as f_in:
            with open(file_out,'w') as f_out:
                for line in f_in:
                    if line == '\n': continue
                    f_out.write(self.exclude_POStag(line) + '\n')
                    #break

if __name__ == '__main__':
    gs = GetSentences('./project2/data/postagged-files','pos','./raw-b-1/')
