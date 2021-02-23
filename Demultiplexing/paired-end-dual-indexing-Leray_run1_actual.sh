# source ~/.bash_profile #if you want to use modules or need environment variables, source 
## All options and environment variables found on schedMD site: http://slurm.schedmd.com/sbatch.html
# export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

# source activate qiime2-2018.8



#! bin bash

# This script demultiplexes paired-end reads with dual indexes (one for forward and one for reverse reads).
# To use it, just create a tab separated file with one column containing the sample name, 
# one column with the forward and indexand one column with the reverse index.
# The program will loop through each fastq files (if more than one) and extract all reads that matches an index pair"""

###############################################
mkdir /Users/stephaniematthews/Documents/Chapter1/demultiplexed_data/Lerayrun1

Output="/Users/stephaniematthews/Documents/Chapter1/demultiplexed_data/Lerayrun1"
DATADIR="/Users/stephaniematthews/Documents/P1604/Allen/Sommer_020819-118427309/FASTQ_Generation_2019-02-11_11_16_49Z-160020829/leray"
 
for i in /Users/stephaniematthews/Documents/P1604/Allen/Sommer_020819-118427309/FASTQ_Generation_2019-02-11_11_16_49Z-160020829/leray/S*/S*_R1_001.fastq.gz
do
R1=$i;
R2=${R1//_R1_/_R2_};
SAMPLE=`basename ${R1%_L001_R1_001.fastq.gz};`
echo $SAMPLE
mkdir $Output/$SAMPLE
 
while read -r Sample_Name index index2; do
 
cutadapt -G $index2 -g $index -o $Output/$SAMPLE/$Sample_Name.trimmed.1.fastq.gz -p $Output/$SAMPLE/$Sample_Name.trimmed.2.fastq.gz $R1 $R2 -j 0 --no-indels --discard-untrimmed --overlap 6
done<~/Documents/P1604/Allen/leray_run1_6mer_demultiplex.txt > $Output/$SAMPLE/summary.txt
 
done 

###############################################
# This command will delete all fastq files except the 2 largest one for each sample
for dir in $Output/*
do
echo $dir
ls -S $dir/*.gz | tail -n +3 | xargs rm -rf
#./ > errors.txt
#rm errors.txt
done

###############################################
# This is to parse and create a trimmed summary
#Output="Results"
for i in $Output/*/summary.txt
do
New_summary=${i%.txt}.csv;
python /Users/stephaniematthews/Documents/P1604/Allen/cutadapt_parser.py -i $i -o $New_summary
done

###############################################
# This is for collecting the second row of each trimmed summary file into one table

for i in $Output/*/*.csv
do
sed -n '2p' $i
done > /Users/stephaniematthews/Documents/P1604/Allen/Overall_summary_leray_run1.csv
###############################################



