#!/usr/bin/perl -w
$audio_dir = "/home/g/grad/zhihaozh/Documents/ie_proj2/raw-b/";
opendir(DIR,$audio_dir) || die "Cant open $audio_dir";
local(@filenames) = readdir(DIR);
closedir(DIR);

$output_dir = "/home/g/grad/zhihaozh/Documents/ie_proj2/nopos-b/"; #output directory
print "Input: $audio_dir Output: $output_dir\n";

for $file(@filenames){
    if($file=~/\.txt/){
        $wavfile = $audio_dir.$file;
        $outfile = $output_dir.$file;
        print "Processing $wavfile to $outfile\n";
        system("cat $wavfile | java -jar /home/g/grad/zhihaozh/Documents/ie_proj2/berkeleyparser/BerkeleyParser-1.7.jar -gr /home/g/grad/zhihaozh/Documents/ie_proj2/berkeleyparser/eng_sm6.gr > $outfile");
}}


