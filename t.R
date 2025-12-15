print(size)

vdi <- read.csv('C:/Users/bielm/Desktop/PE/PE_experiment_discs/resultat_VDI.csv')
vmdk <- read.csv('resultat_VMDK.csv')

dif <- vdi$time_seconds - vmdk$time_seconds

sd <- sd(dif)
l <- length(dif)
se <- sd / sqrt(l)

alpha <- 1 - 0.95
t <- qt(1-alpha/2, l - 1)
m <- mean(dif)
IC <- c(m - t * se, m + t * se)
