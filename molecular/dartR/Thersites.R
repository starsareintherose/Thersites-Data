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


gl2fasta(
  x = gl5,
  outfile = "gl_output.fasta",
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
