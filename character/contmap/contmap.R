library(ape)
library(phytools)
library(readr)

# custom function to add a color bar to the left of the plot
add.left.color.bar <- function(cols, lims, digits = 3, lwd = 3) {
  usr <- par("usr")
  # get the axis limits
  offset <- (usr[2] - usr[1]) * 150
  xleft <- usr[1] - offset
  xright <- usr[1]
  
  # fix the y-axis limits
  y_range <- usr[4] - usr[3]
  ybottom <- usr[3] + y_range * 0.05  # up 5%
  ytop <- usr[4] - y_range * 0.05     # down 5%
  n <- length(cols)
  y_seq <- seq(ybottom, ytop, length.out = n + 1)
  
  # draw the color bar
  for (i in 1:n) {
    rect(xleft-0.3, y_seq[i], xright+0.3, y_seq[i+1], col = cols[i], border = NA)
  }
 #rect(xleft, ybottom, xright, ytop, border = "black", lwd = 1)
  
  # add the axis labels
  tick_values <- pretty(lims, n = 5)
  tick_positions <- ybottom + (tick_values - lims[1])/(diff(lims)) * (ytop - ybottom)
  axis(side = 2, at = tick_positions, labels = format(tick_values, digits = digits),
       las = 1, line = 2, tick = FALSE, cex.axis = 1.7, font = 7)
}

# get the command line arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 3) {
  stop("Usage: Rscript contmap.R <tree_file> <csv_file> <output_svg_file>")
}
tree_file   <- args[1]  # tree file
csv_file    <- args[2]  # CSV file which must include seq Width, Height, phallus, epiphallus1, epiphallus2, flagellum）
output_file <- args[3]  # svg output file

# read the tree and ladderize it
tree <- read.tree(tree_file)
tree <- ladderize(tree, right = TRUE)
tree$edge.length <- rep(1, length(tree$edge.length))

# read the data and convert to a data frame
data <- read_csv(csv_file, na = "?", show_col_types = FALSE)
data <- as.data.frame(data)
data$seq <- as.character(data$seq)

# check if the required columns are present
vars <- c("Width", "Height", "phallus", "epiphallus1", "epiphallus2", "flagellum")
vars <- vars[vars %in% colnames(data)]
# convert the variables to numeric and replace NA with the mean
for (v in vars) {
  data[[v]] <- as.numeric(data[[v]])
  if (any(is.na(data[[v]]))) {
    data[[v]][is.na(data[[v]])] <- mean(data[[v]], na.rm = TRUE)
  }
}

# create the continuous mapping for each variable
contmaps <- list()
for (v in vars) {
  trait <- data[[v]]
  names(trait) <- data$seq  # tip labels must match the tree
  contmaps[[v]] <- contMap(tree, trait, plot = FALSE)
  contmaps[[v]] <- setMap(contmaps[[v]], c('#68cff7', '#b9db89', '#ffe966', '#f5969f'))
}

# set up the plot
ncols <- 3
nrows <- ceiling(length(vars) / ncols)
# set up the plot
svg(filename = output_file, width = 24, height = 10 * nrows)
par(xpd = TRUE)  # allow plotting outside the plot region
par(mfrow = c(nrows, ncols), mar = c(20,12,8,4), oma = c(6,6,2,2)) # set the margin up left down right

# add the subletter labels
subletters <- LETTERS[1:length(vars)]

for (i in seq_along(vars)) {
  v <- vars[i]
  cm <- contmaps[[v]]
  
  # plot the continuous mapping
  plot(cm, fsize = 1.2, lwd = 10, legend = FALSE, outline=FALSE)
  
  # add the color bar
  add.left.color.bar(cm$cols, cm$lims, digits = 3, lwd = 3)
  
  # add the subletter label
  usr <- par("usr")
  line_offset <- (usr[4] - usr[3]) * 0.05
  text_y_pos <- usr[3] - line_offset
  mtext(paste0(subletters[i], ". Mapping for ", v), side = 1, line = text_y_pos,
      cex = 1.5, adj = 0.05)
}
dev.off()

