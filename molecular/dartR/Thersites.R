library(dartR)
library(logging)
##Log file
basicConfig()
addHandler(writeToFile, file = "Rfile.log")

##Import Data
gl = gl.read.dart("Report_DFigu25-10193_SNP_1.csv", ind.metafile = "meta.ind.csv") # Be careful about the lastmetric !!! somewhat careful to topskip
save(gl, file = "Thersites.Rdata")
gl
##SNP filtering on read depth
read.depth = gl.report.rdepth(gl)
read.depth
gl1 = gl.filter.rdepth(gl, lower = 5, upper = 30)
gl1
##SNP filtering on average repeatability
gl2 = gl.filter.reproducibility(gl1, threshold = 1)
gl2
##SNP filtering on call rate (loci and individuals)
gl3_a = gl.filter.callrate(gl2, method = "loc", threshold = 0.80, mono.rm = TRUE, recalc = TRUE, recursive = TRUE)
gl3_a
gl3_b = gl.filter.callrate(gl3_a, method = "ind", threshold = 0.50, mono.rm = TRUE, recalc = TRUE, recursive = TRUE)
gl3_b
##SNP filtering on MAF
gl4 = gl.filter.maf(gl3_b, threshold = 0.01)
gl4
##SNP filtering on potential linkage
gl5 = gl.filter.secondaries(gl4, method = "random")
gl5
##PCoA
pcoa = gl.pcoa(gl5)
gl.pcoa.plot(pcoa, gl5, xaxis = 1, yaxis = 2, interactive = FALSE)
gl.pcoa.plot(pcoa, gl5, xaxis = 1, yaxis = 3, interactive = FALSE)

pcoa$scores

library(ggplot2)

# change pcoa$scores to data.frame
pcoa_scores = as.data.frame(pcoa$scores)
pcoa_scores$id = rownames(pcoa_scores)

# read csv to get pop
meta = read.csv("meta.ind.csv", header = TRUE, stringsAsFactors = FALSE)

# merge data
pcoa_data = merge(pcoa_scores, meta, by = "id")

# custom color
custom_colors = c("darlingtoni" = "#75ff66",
                   "mitchellae" = "#48b9ff",
                   "novaehollandiae" = "#ff888a",
                   "richmondiana" = "#ede100",
                   "sp_Coolah" = "#b3b3b3",
                   "sp_MtKaputar" = "#0057b7")

# plot
ggplot(pcoa_data, aes(x = PC1, y = PC2, color = pop)) +
  geom_point(size = 3) +
  scale_color_manual(values = custom_colors) +
  labs(x = "PC1", y = "PC2", title = "PCoA") +
  theme_classic()

gl2fasta(
  x = gl5,
  outfile = "gl_output.fasta",
  outpath = ".",
  verbose = 2
)

gl2bpp(
  x = gl5,
  outfile = "bpp.txt",
  method = 2,
  imap = "Imap.txt",
  outpath = ".",
  verbose = 2
)

gl2snapp(
  x = gl5,
  outfile = "snapp.nex",
  outpath = ".",
  verbose = 2
)

quit()
