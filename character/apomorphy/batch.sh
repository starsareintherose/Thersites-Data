for tre in $(ls 00tre/*.tre)
do
tnt run runwincladtree.run $tre,
done

cd 00tre
for tre in $(ls *.tre)
do
mv $tre.svg ../wincladtree
done
