# Title     : TODO
# Objective : TODO
# Created by: dimitrius
# Created on: 20.12.2019


lambda <- 0.001
x0 <- 15
x1 <- -9

y <- x0^2 + x1^2

for (i in 1:100) {
  x0 <- x0 - lambda * 2  * x0
  x1 <- x1 - lambda * 2  * x1

  y <- c(y, x0^2 + x1^2)
}
