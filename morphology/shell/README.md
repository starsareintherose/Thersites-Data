# Shell Morphology Analysis

## Shell Morphometrics

Landmark and semi-landmark were collected using tpsDig 2.32. Semi-landmarks were converted using tpsUtil 1.82. The data was analyzed in MorphoJ 1.08.02 using Procrustes Fit, Principle Compopnent Analysis (PCA) and Canonical Variate Analysis (CVA).

### tpsDig

The tps file was initially generated using the `gentps.sh`

Open file

`Input source` -> `File`

Collect landmarks

`Modes` -> `Digtize landmarks`

Collect semi-landmarks

`Modes` -> `Draw curves`

Save data

`File` -> `Save data as`

### tpsUtil

`Operation`: Select `Append tps Curve to landmarks`

`Input file`: Select the input tps file

`Output file`: Select the output tps file

Select `Create`

### MorphoJ

All the following steps are done in `Project Tree` panel.

`File` -> `Create New Project` -> `Dimensionality of the data`: select `2 dimensions`; `Object symmetry`: select `no`; `File type`: select `tps` -> `Create Dataset`

`File` -> `Create New Dataset` -> same as last step

`Preliminaries` -> Select a database -> `New Procrustes Fit` -> `Align by principal axes` -> `Perfrom Procrustes Fit`

`Preliminaries` -> `Extract new classifier from ID strings` -> `Name for new classifier`: spp; `First character`: 1; `Last character`: 3 -> `Execute`

`Comparison` -> `Canonical Variates Analysis` -> `Dataset`: select database name; `Data type`: select matrix name; `Classifier variables(s) to use for grouping`: select spp; select `Permutation tests`; `Number of literations` write `10000` -> `Execute`

`Preliminaries` -> Select a database -> `Average Observation By ..`

Run1: don't consider the within-group covariation
`Preliminaries` -> `Data types`: select `Procrustes coordinates` -> `Execute`
`Variation` -> `Principal Component Analysis` -> `Execute`

Run2: consider the within-group covariation
`Preliminaries` -> `Data types`: select `Procrustes coordinates` -> `Pooled within-group covariances`: select spp -> `Execute`
`Variation` -> `Principal Component Analysis` -> `Execute`

`File` -> `Save Project`

The following steps are done in `Graphics` panel.

Subpanel `PC/CV shape changes`
right click ->`Change the Type of Graph` -> `Transformation Grid`
right click -> `Choose PC/CV` -> select the PC/CV to visualize
right click -> `Exoport Graph to File` -> select the format and file name

Subpanel `PC/CV scores`
right click -> `Color the Data Points`
right click -> `Resize Data Points`
right click -> `Choose Principal/Canonical variate for the Horizontal/Vertical Axies`
right click -> `Exoport Graph to File` -> select the format and file name

## Shell measurement

Preparation was undertaken in Adobe PhotoShop 2024 with UNSW license or GIMP 2.10.38 with GMIC plugin 3.5.2. This step extracted the shell photo from the background, rotated it to a standard position, zoomed to 1000pixel = 1cm, and saved as png files.

The png files finally were converted to black background and white shell using imagemagick 7.1.1.43.

Measurements were taken using Fiji. Finally, the results were visualized in Python with matplotlib. The script `draw_shell_width_height.py` was used to draw the scatter plot.

### Preparation

```bash
mkdir -p output  # Create output directory if it doesn't exist
for img in *.png; do
    magick "$img" -alpha extract -negate "output/${img%.png}.jpg"
    magick "output/${img%.png}.jpg" -negate "output/${img%.png}.jpg"
done
```

### Fiji

`Plugins` -> `Macro` -> `Run` -> select the macro file `shell_measure.ijm`

```imagej
// Folder setting
inputDir = "/home/guoyi/Downloads/PhD/Thersites/TPS/outline_for/output/"; //input folder
outputFile = "/home/guoyi/Downloads/PhD/Thersites/TPS/outline_for/output/00results.csv"; // outputfolder

// create csv and input the header
File.append("Image,Width (pixels),Height (pixels),", outputFile);

// get all images
list = getFileList(inputDir);

for (i = 0; i < list.length; i++) {
    path = inputDir + list[i];
    if (endsWith(path.toLowerCase(), ".jpg")) { // the file must use jpg as file extension 
        open(path);
        
        // change photos to 8-bit format
        run("8-bit");

        // make the photo color binary
        setThreshold(200, 255);  // select the white region
        run("Make Binary");

        // measure
        width = getWidth(); // use getWidth to get width
        height = getHeight(); // use getHeight to get height

        // save results to csv
        File.append(list[i] + "," + width + "," + height + ",", outputFile);
        
        // close photo
        close(); 
    }
}
print("Batch processing complete. Results saved to " + outputFile);

```

## Measurement

```bash
for py in gen_violin_plot.py gen_distribution.py calculate.py draw_shell_width_height.py ; do
    python "$py"
done
```
