# Flagellum Shape Examination

## ImageJ2/FIJI

### Install

```
# pacman -S fiji
```

### Plugin

 - `Help` -> `Update ..`, when a windwos bottom shows that `Manage Update Sites`, search `IJPB-plugins`, click the box and then click `Apply` or you can use `# pacman -S fiji-plugin-morpholibj`
 
 - `Plugins` -> `Install ..`, select [width_profile_tools](https://raw.githubusercontent.com/MontpellierRessourcesImagerie/imagej_macros_and_scripts/master/volker/toolsets/width_profile_tools/width_profile_tools.ijm)

 - Select `>>`, click `width_profile_tools`

 - select the cloud with down arrow button named `Install or Update Tool`, select `v1.28` or higher version.

### Voronoi-Distance measurement

 - `File` -> `Open`

 - `Image` -> `Type` -> `8-bit`

 - `Image` -> `Adjust` -> `Threads`, select `Apply`

 - `Process` -> `Binary` -> `Make Binary`

 - `Polygon selections` or `Rectangle` tools to select the bottom of top of flagellum, the end of flagellum should be at the top of image than the end of flagellum. Once finished the selection, use `Ctrl+b`. 

 - When you finished selecting both sides, you should type `Ctrl+Shift+a`

 - Click the v button named `Voronoi (f6) Tool`

 - Save measurement data as individual csv file

## Resample points

 - use `resample_point.py` to resample the points generated by FIJI

 - The aim for this python script is to transfer the data to 100 points, this can be changed in script by changing `target_length=100`

My example script is 

```
#!/bin/bash

## Generate converted data
for csv in $(ls **/*.csv)
do
    python resample_point.py $csv
done


## Create the output directory
mkdir -p 00convert
mkdir -p 00convert/100

## transfer the converted csv to the aim folder
mv **/*_converted.csv 00convert/100
```

## Filtering data

Typically, an intact flagellum will undergo some obvious shape changes due to folding and the insect needle's inability to fully unfold it. These shape changes can be considered noisy, therefore, we could just pick a series of very tip points.

The following the step I used to create them

```
#!/bin/bash

## change folder
cd 00convert

## create directory
mkdir -p 50
mkdir -p 70

# use head command to get them
cd 100
for csv in $(ls *.csv)
do
    head -n 71 $csv > ../70/$csv
    head -n 51 $csv > ../50/$csv
done

```

## Draw lines

 - Use `darw_lines.py` to create the svg file under `00convert/[100,70,50]` folder


## Landmark-based Analysis

Same with shell readme MorphoJ part

### Convert csv to tps file

```
#!/bin/bash
python csv_to_tps.py 100 points100.tps
```

Following is normal MorphoJ analysis
