def erase_tag(filename,outname):
    f_out = open(outname,'w')
    with open(filename,'r') as f_in:
        for line in f_in:
            if (line[0] == 'y'): f_out.write(line[4:])
            else : f_out.write(line[3:])
    f_out.close()

if __name__ == '__main__':
    erase_tag('coref-testset.gold.fv.txt','test-raw.txt')
