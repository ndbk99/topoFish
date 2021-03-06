% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/drawRadius.R
\name{drawRadius}
\alias{drawRadius}
\title{drawRadius}
\usage{
drawRadius(x, y, rsize, ...)
}
\arguments{
\item{x, y}{coordinates of points in longitude latitude}

\item{rsize}{size of radius in km}

\item{...}{arguments to pass to \code{\link{polygon}}}
}
\value{
invisibly returns NULL
}
\description{
Draw a radius around a point, or points
}
\details{
from http://stackoverflow.com/a/34187454/2343633
}
\examples{
x <- -140:-170
y <- 15:45
plot(x, y)
drawRadius(x, y, 100)

}

