library(geomorph)

# read landmarks from TPS files
lm   = readland.tps("lm.tps", specID = "ID")      # 7 landmarks
slm1 = readland.tps("slm1.tps", specID = "ID")    # 50 landmarks
slm2 = readland.tps("slm2.tps", specID = "ID")    # 50 landmarks

# extract specimen IDs from the landmarks
ids_lm   = dimnames(lm)[[3]]
ids_slm1 = dimnames(slm1)[[3]]
ids_slm2 = dimnames(slm2)[[3]]

# obtain common IDs across all landmark sets
common_ids = Reduce(intersect, list(ids_lm, ids_slm1, ids_slm2))

# sort common IDs to ensure consistent order
lm    = lm[,,common_ids]
slm1  = slm1[,,common_ids]
slm2  = slm2[,,common_ids]

# merge landmarks into a single array
n_specimens = length(common_ids)
n_landmarks = dim(lm)[1] + dim(slm1)[1] + dim(slm2)[1]
coords_combined = array(NA, dim = c(n_landmarks, 2, n_specimens),
                         dimnames = list(NULL, c("X", "Y"), common_ids))

for (i in seq_len(n_specimens)) {
  id = common_ids[i]
  coords_combined[,,i] = rbind(lm[,,id], slm1[,,id], slm2[,,id])
}

# check the dimensions of the combined coordinates
print(dim(coords_combined))  # should be (107, 2, n_specimens)

write.tps = function(land, file, ids = NULL){
  n = dim(land)[3]
  p = dim(land)[1]
  k = dim(land)[2]
  if (is.null(ids)) ids = paste0("ID", 1:n)
  
  con = file(file, "w")
  for (i in 1:n){
    writeLines(paste0("LM=", p), con)
    coords = land[,,i]
    writeLines(apply(coords, 1, paste, collapse = " "), con)
    writeLines(paste0("ID=", ids[i]), con)
  }
  close(con)
}

write.tps(coords_combined, "morpho_merged.tps", ids = common_ids)

