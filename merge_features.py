def merge_features(orgin_feats_filename,new_feats_filename,output_filename):
    out_file = open(output_filename,'w')
    org_file = open(orgin_feats_filename,'r')
    new_file = open(new_feats_filename,'r')
    flag = 1
    counter = 0
    for line in org_file:
        if (flag):
            if(line[:5] == '@DATA'):
                flag = 0
            out_file.write(line)
            continue
        new_feats = new_file.readline().split(',')
        new_feats = [feat.strip() for feat in new_feats]
        if (new_feats[0] == 'True' and new_feats[-1] == 'yes'): counter += 1
        str_new_feats = ','.join(new_feats)
        old_feats = line.split(',')
        str_old_feats = ','.join(old_feats[:-1])
        out_file.write(str_old_feats+', '+str_new_feats+'\n')
    print counter

if __name__ == '__main__':
    merge_features('./back-up-2/weka-trainset.arff','weka-trainset.arff','weka-trainset-new.arff')
    merge_features('./back-up-2/weka-testset.arff','weka-testset.arff','weka-testset-new.arff')
