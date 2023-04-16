# AsymmetricError
Summarize a distribution of values considering the significant figures its spread.

This package allows you to calculate summary statistics (e.g., mean, standard deviation, confidence interval) for any distribution of values while also considering the number of significant figures of each tail of the distribution. 

For example, if you have a skewed distribution and you need to quote upper and lower uncertainties on the mean, it will determine the precision of the mean based on the *least* precise of the upper and lower spread. 

It is particularly useful when attempting to quote summary statistics and not wanting to inaccurately inflate the precision on the center value (mean or median) of the distribution.

This package relies on the sigfig library for rounding: https://pypi.org/project/sigfig/.
