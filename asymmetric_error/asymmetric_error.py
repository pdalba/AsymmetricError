import numpy as np
import sigfig as sf

def asymmetric_error(distribution, sigfig=2, center='mean',
                     spread='stddev', ci=None, printOut=True,
                     LaTeX=False):
    """
        Summarize a distribution of values considering the significant
        figures its spread. If the distribution is asymmetric such that 
        the upper and lower spread have different significant figures,
        the value will only be reported to the amount of digits 
        consistent with the less precise spread. 

        Inputs
        ------
    
            distribution: array-like
                List or array containing the discrete values that comprise
                the distriubtion.

            sigfig: int
                Number of significant figures to report in the final value
                and spread. Must be >= 1. Default=2. 

            center: str
                Measure of the center of the distribution. Must be one of
                ['mean', 'median']. Default='mean'.

            spread: str
                Measure of the spread of the distribution. Must be one of
                ['stddev', 'CI'], representing the standard deviation and
                confidence interval. If 'CI' is passed, then the ci argument
                must also be given. Default='stddev'

            ci: tuple-like
                Tuple or list containin the lower and upper confidence
                intervals to report in percent. Must be passed if the
                spread argument is 'CI'. Intervals must be in the range
                [0, 100].

            printOut: bool 
                Flag to print the final value and spread to the command line
                instead of returning them. Default=True.

            LaTeX: bool
                Flag to print the final value and spread with LaTeX formatting.
                Ignored unless the printOut argument is True. Default=False.

        Outputs
        -------

            val, spread, [spread2]

            val: float
                The center value of the distribution. Only returned if the
                printOut argument is False.

            spread, [spread2]: float
                The values describing the spread of the distribution. Only
                returned if the printOut argument is False.
    """

    # Evaluate the args
    res = eval_args(distribution, sigfig, center, spread, ci,
                    printOut, LaTeX)
    distribution, sigfig, center, spread, ci, printOut, LaTeX = res

    # Calcuate center and spread of distribution
    if center.lower() == 'mean':
        val = np.mean(distribution)
    else:
        val = np.median(distribution)

    if spread == 'stddev':
        err = [np.std(distribution)] * 2
    else:
        p = np.percentile(distribution, ci)
        # Lower error listed first
        err = [np.abs(val - i) for i in p]

    # Round err to sigfig
    err = [sf.round(str(i), sigfigs=sigfig) for i in err]
    
    #Round the value to whichever error is more precise
    if len(err[0]) >= len(err[1]):
        val = sf.round(str(val), uncertainty=err[0], cutoff=99)
    else:    
        val = sf.round(str(val), uncertainty=err[1], cutoff=99)
    val = val.split(' ')[0]
    
    # Print formatted text to command line
    if printOut:
        if err[0] == err[1]:
            if LaTeX:
                return ' $' + val + '\pm' + err[0] + '$'
            else:
                return '{} +/- {}'.format(val, err[0])
        else:
            if LaTeX:
                return ' $' + val + '^{+' + err[1] + '}_{-' + err[0] + '}$'
            else:
                return '{} +{}/-{}'.format(val, err[1], err[0])
    #Otherwise, return floats
    else:
        return float(val), float(err[0]), float(err[1])        

def eval_args(distribution, sigfig, center, spread, ci,
              printOut, LaTeX):
    """
        Check for consistency and errors among the arguments
    """
    try:
        distribution = np.array(distribution)
    except:
        raise TypeError('Did not recognize distribution arg as ' \
                         'array-like object')
    sigfig = int(sigfig)
    if sigfig < 1:
        raise ValueError('Sigfig ({}) cannot be less than 1.'.format(sigfig))

    if center.lower() not in ['mean', 'median']:
        raise ValueError('Center metric ({}) not understood.'.format(center))

    if spread.lower() not in ['ci', 'stddev']:
        raise ValueError('Spread metric ({}) not understood.'.format(spread))

    if spread.lower() == 'ci' and ci is None:
        raise ValueError('Confidence intervals not provided.')
    elif spread.lower() == 'ci':
        if ci[0] < 0:
            ci[0] = 0.
        if ci[1] > 100:
            ci[1] = 100.
        if ci[0] >= ci[1]:
            raise ValueError('Lower CI value must be listed first.')

    return distribution, sigfig, center, spread, ci, printOut, LaTeX
