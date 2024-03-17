library(dplyr)

# KIDPAN_DATA.DAT
kidpan_data = read.table(
  "C:/Users/brand/Desktop/STAR_Delimited/Delimited Text File 202312/Kidney_ Pancreas_ Kidney-Pancreas/KIDPAN_DATA.DAT",
  header=FALSE, sep="\t"
)
colnames = read.table(
  "C:/Users/brand/Desktop/STAR_Delimited/Analysis/KIDPAN_DATA_colnames.csv",
  header=TRUE, sep=","
)
colnames(kidpan_data) <- colnames$LABEL