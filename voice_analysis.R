# Set the default CRAN mirror
# options(repos = c(CRAN = "https://cloud.r-project.org/"))

# Install and load necessary packages
# install.packages(c('tuneR', 'seewave'))
library(tuneR)
library(seewave)


# Function for acoustic feature extraction
specan3 <- function(file_path) {
  # Check if the file exists
  if (!file.exists(file_path)) {
    stop("File not found.")
  }
  
  # Read the wave file
  r <- readWave(file_path)
  
  # Frequency bandpass
  bp <- c(0, 22)
  
  # Window length
  wl <- 2048
  
  # Threshold for fundamental frequency
  threshold <- 5
  
  # Frequency spectrum analysis
  songspec <- spec(r, f = r@samp.rate, plot = FALSE)
  analysis <- specprop(songspec, f = r@samp.rate, flim = c(0, 280/1000), plot = FALSE)
  
  # Save parameters
  meanfreq <- analysis$mean/1000
  sd <- analysis$sd/1000
  median <- analysis$median/1000
  Q25 <- analysis$Q25/1000
  Q75 <- analysis$Q75/1000
  IQR <- analysis$IQR/1000
  skew <- analysis$skewness
  kurt <- analysis$kurtosis
  sp.ent <- analysis$sh
  sfm <- analysis$sfm
  mode <- analysis$mode/1000
  centroid <- analysis$cent/1000
  
  # Fundamental frequency parameters
  ff <- fund(r, f = r@samp.rate, ovlp = 50, threshold = threshold, 
             fmax = 280, ylim=c(0, 280/1000), plot = FALSE, wl = wl)[, 2]
  meanfun <- mean(ff, na.rm = TRUE)
  minfun <- min(ff, na.rm = TRUE)
  maxfun <- max(ff, na.rm = TRUE)
  
  # Dominant frequency parameters
  y <- dfreq(r, f = r@samp.rate, ovlp = 50, wl = wl, plot = FALSE)
  meandom <- mean(y, na.rm = TRUE)
  mindom <- min(y, na.rm = TRUE)
  maxdom <- max(y, na.rm = TRUE)
  dfrange <- maxdom - mindom
  
  # Modulation index calculation
  changes <- vector()
  for (j in which(!is.na(y))){
    change <- abs(y[j] - y[j + 1])
    changes <- append(changes, change)
  }
  modindx <- ifelse(mindom == maxdom, 0, mean(changes, na.rm = TRUE) / dfrange)
  
  # Save results
  results <- c(meanfreq, sd, median, Q25, Q75, IQR, skew, kurt, sp.ent, 
               sfm, mode, centroid, meanfun, minfun, maxfun, 
               meandom, mindom, maxdom, dfrange, modindx)
  
  # Return results
  return(results)
}

file_path <- commandArgs(trailingOnly = TRUE)[1]
features <- specan3(file_path)
print(features)