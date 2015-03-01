#!/usr/bin/perl -w
$audio_dir = "/home/g/grad/zhihaozh/Documents/ie_proj2/raw/";
opendir(DIR,$audio_dir) || die "Cant open $audio_dir";
local(@filenames) = readdir(DIR);
closedir(DIR);

$output_dir = "/home/g/grad/zhihaozh/Documents/ie_proj2/nopos/"; #output directory
print "Input: $audio_dir Output: $output_dir\n";

for $file(@filenames){
    if($file=~/\.txt/){
        $wavfile = $audio_dir.$file;
        $outfile = $output_dir.$file;
        print "Processing $wavfile to $outfile\n";
        system("bash /home/g/grad/zhihaozh/Documents/ie_proj2/bllip-parser-master/parse.sh $wavfile > $outfile");
}}

