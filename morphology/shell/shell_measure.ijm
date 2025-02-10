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

