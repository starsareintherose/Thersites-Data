for txt in $(ls *.txt)
do
    echo "Processing $txt"
    python parse_dfa.py $txt
done
