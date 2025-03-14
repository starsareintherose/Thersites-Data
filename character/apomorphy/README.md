# Parsimony character optimization

## Wincladtree

This use the tnt compitable tree file and the character matrix file to optimize the characters on the tree. The output is a svg file with the optimized characters.

This only can get ambiguous optimization with homoplasy scores.

```bash
bash run.sh
```

## Winclada

`File` -> `Open File` -> select the tnt 

`File` -> `Open Tree file` -> Open the tree file

`View` -> `Tree style` -> `Rectangular`

`HashMarks` -> `Show characters` + `Number hashmarks (Characters)` + `Number hashmarks (States)`

`Optimization` -> `Uambig` to get ambiguous optimization, `Fast optimization` to get ACCTRAN optimization, `Slow optimization` to get DELTRAN optimization

`File` -> `Create tree metafile` -> save the emf files

You can convert emf files with inkscape using the bash script `convert.sh` in the `winclada` folder.

