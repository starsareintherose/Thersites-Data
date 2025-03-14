
#for file in lm slm1 slm2 fl50
#do
#python nts2csv.py 00nts/$file.nts 00csv/$file.csv
#done

for file in lm slm1 slm2 fl50
do
python lm_nts.py 00csv/$file.csv 01nts/$file
#python lm_tps.py 00tps/$file.tps 01tps/$file
done
