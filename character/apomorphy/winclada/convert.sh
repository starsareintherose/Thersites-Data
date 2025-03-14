for file in *.emf; do
    inkscape "$file" --export-filename="${file%.emf}.svg"
done

