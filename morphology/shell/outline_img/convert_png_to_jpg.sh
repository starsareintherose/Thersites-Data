mkdir -p output  # Create output directory if it doesn't exist
for img in *.png; do
    magick "$img" -alpha extract -negate "output/${img%.png}.jpg"
    magick "output/${img%.png}.jpg" -negate "output/${img%.png}.jpg"
done
