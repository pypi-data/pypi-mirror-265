import numpy as np
import numpy.random as rgt
from scipy.stats import norm
from scipy.special import logsumexp
from scipy.optimize import minimize
import warnings


###############################################################################
###########################    Helper Functions    ############################
###############################################################################
def mad(x):
    ''' Median absolute deviation '''
    return 1.4826 * np.median(np.abs(x - np.median(x)))


def boot_weight(weight):
    ''' Bootstrap (random) weights generator '''
    boot = {'Multinomial': lambda n :
            np.random.multinomial(n, pvals=np.ones(n)/n), 
            'Exponential': lambda n : np.random.exponential(size=n), 
            'Rademacher': lambda n : 2*np.random.binomial(1, 1/2, n), 
            'Gaussian': lambda n : np.random.normal(1, 1, n), 
            'Uniform': lambda n : np.random.uniform(0, 2, n), 
            'Folded-normal': lambda n :
            abs(np.random.normal(size=n)) * np.sqrt(.5 * np.pi)
            }
    return boot[weight]


def asymHuber_grad(x, tau, c):
    ''' Gradient of the asymmetric Huber loss '''
    pos = x > 0
    tmp = np.minimum(abs(x), c)
    tmp[pos] *= tau
    tmp[~pos] *= tau - 1
    return tmp


def smooth_check(x, tau=0.5, h=0.5, kernel='Laplacian', w=np.array([])):
    ''' Smoothed (weighted) check loss '''
    if kernel == 'Laplacian':
        loss = lambda x: np.where(x >= 0, tau*x, (tau-1)*x) \
                         + (h/2) * np.exp(-abs(x)/h)
    elif kernel == 'Gaussian':
        loss = lambda x: (tau - norm.cdf(-x/h)) * x \
                              + (h/2) * np.sqrt(2 / np.pi) \
                                * np.exp(-(x/h) ** 2 / 2)
    elif kernel == 'Logistic':
        loss = lambda x: tau * x + h * np.log(1 + np.exp(-x/h))
    elif kernel == 'Uniform':
        loss = lambda x: (tau - .5) * x \
                         + h * (.25 * (x/h)**2 + .25) * (abs(x) < h) \
                         + .5 * abs(x) * (abs(x) >= h)
    elif kernel == 'Epanechnikov':  
        loss = lambda x: (tau - .5) * x + .5 * h * (.75 * (x/h) ** 2 \
                         - .125 * (x/h) ** 4 + .375) * (abs(x) < h) \
                         + .5 * abs(x) * (abs(x) >= h)
    if not w.any(): 
        return np.mean(loss(x))
    else:
        return np.mean(loss(x) * w)


def conquer_weight(x, tau, kernel="Laplacian", w=np.array([])):
    ''' Gradient weights for the (weighted) smoothed check loss '''
    if kernel=='Laplacian':
        Ker = lambda x : 0.5 + 0.5 * np.sign(x) * (1 - np.exp(-abs(x)))
    elif kernel=='Gaussian':
        Ker = lambda x : norm.cdf(x)
    elif kernel=='Logistic':
        Ker = lambda x : 1 / (1 + np.exp(-x))
    elif kernel=='Uniform':
        Ker = lambda x : np.where(x > 1, 1, 0) \
                         + np.where(abs(x) <= 1, 0.5 * (1 + x), 0)
    elif kernel=='Epanechnikov':
        Ker = lambda x : 0.25 * (2 + 3 * x / 5 ** 0.5 \
                         - (x / 5 ** 0.5)**3 ) * (abs(x) <= 5 ** 0.5) \
                         + (x > 5 ** 0.5)                      
    if not w.any():
        return (Ker(x) - tau) 
    else:
        return w * (Ker(x) - tau)


def find_root(f, tmin, tmax, tol=1e-5):
    while tmax - tmin > tol:
        tau = (tmin + tmax) / 2
        if f(tau) > 0:
            tmin = tau
        else: 
            tmax = tau
    return tau


###############################################################################
################## Convolution Smoothed Quantile Regression ###################
###############################################################################
class low_dim():
    '''
        Convolution Smoothed Quantile Regression (conquer)

    Methods:
        bw() : bandwidth selection.
        als() : asymmetric least squares or Huber regression.
        fit() : fit conquer via the GD-BB algorithm.
        bfgs_fit() : fit conquer via the BFGS algorithm.
        bw_path() : solution path of conquer at a sequence of bandwidths.
        norm_ci() : normal calibrated confidence intervals.
        mb() : multiplier bootstrap estimates.
        mb_ci() : multiplier bootstrap confidence intervals.
        Huber() : Huber regression via BFGS.
        adaHuber() : adaptive Huber regression.

    Attributes:
        kernels : built-in smoothing kernels.
        weights : built-in random weight distributions.
        params : internal statistical and optimization parameters.
    '''
    kernels = ["Laplacian", "Gaussian", "Logistic", "Uniform", "Epanechnikov"]
    weights = ["Exponential", "Multinomial", "Rademacher",
               "Gaussian", "Uniform", "Folded-normal"]
    params = {'max_iter': 1e3, 'max_lr': 50, 'tol': 1e-6, 
              'warm_start': True, 'nboot': 200, 'min_bandwidth': 1e-4}

    def __init__(self, X, Y, intercept=True, options=dict()):
        '''
        Args:
            X: n by p matrix of covariates; each row is an observation vector.
            Y: an ndarray of response variables.
            intercept: logical flag for adding an intercept to the model.
            options: a dictionary of internal statistical and optimization parameters.
                max_iter: maximum numder of iterations in the GD-BB algorithm; 
                          default is 500.
                max_lr: maximum step size/learning rate. 
                        If set to False, there is no contraint on the maximum step size.
                tol: the iteration will stop when max{|g_j|: j = 1, ..., p} <= tol
                     where g_j is the j-th component of the (smoothed) gradient; 
                     default is 1e-4.
                warm_start: logical flag for using a robust expectile 
                            regression estimate as an initial value.
                nboot: number of bootstrap samples for inference.
                min_bandwidth: minimum bandwidth value; default is 1e-4.
        '''
        self.n = X.shape[0]
        if X.shape[1] >= self.n: 
            raise ValueError("covariate dimension exceeds sample size")
        self.Y = Y.reshape(self.n)
        self.mX, self.sdX = np.mean(X, axis=0), np.std(X, axis=0)
        self.itcp = intercept

        if intercept:
            self.X = np.c_[np.ones(self.n), X[:]]
            self.X1 = np.c_[np.ones(self.n), 
                            (X[:] - self.mX)/self.sdX]
        else:
            self.X, self.X1 = X[:], X[:]/self.sdX

        self.params.update(options)


    def bandwidth(self, tau):
        n, p = self.X.shape
        h0 = min((p + np.log(n))/n, 0.5)**0.4
        return max(self.params['min_bandwidth'], 
                   h0 * (tau-tau**2)**0.5)


    def als(self, tau=0.5, robust=5,
            standardize=True, adjust=True, scale=False):
        '''
            Asymmetric Least Squares/Huber Regression
        '''
        X = self.X1 if standardize else self.X
        asym = lambda x : 2 * np.where(x < 0, (1-tau) * x, tau * x)

        beta = np.zeros(X.shape[1])
        if self.itcp: beta[0] = np.quantile(self.Y, tau)
        res = self.Y - beta[0]

        c, c0 = robust, robust * mad(asym(self.Y))
        if scale:
            ares = asym(res)
            c = robust * max(mad(ares), 0.1 * c0)
        grad0 = X.T.dot(-asymHuber_grad(res, tau, c)) / self.n
        diff_beta = -grad0
        beta += diff_beta
        res, t = self.Y - X.dot(beta), 0

        while t < self.params['max_iter'] and max(abs(grad0)) > self.params['tol']:
            if scale: 
                ares = asym(res)
                c = robust * max(mad(ares), 0.1 * c0)
            grad1 = X.T.dot(-asymHuber_grad(res, tau, c)) / self.n
            diff_grad = grad1 - grad0
            r0, r1 = diff_beta.dot(diff_beta), diff_grad.dot(diff_grad)
            if r1 == 0: lr = 1
            else:
                r01 = diff_grad.dot(diff_beta)
                lr = min(logsumexp(abs(r01/r1)), logsumexp(abs(r0/r01)))
            if self.params['max_lr']: lr = min(lr, self.params['max_lr'])
            grad0, diff_beta = grad1, -lr*grad1
            beta += diff_beta
            res = self.Y - X.dot(beta)
            t += 1
        
        if standardize and adjust:
            beta[self.itcp:] = beta[self.itcp:]/self.sdX
            if self.itcp: beta[0] -= self.mX.dot(beta[1:])

        return {'beta': beta, 'res': res, 'niter': t, 'robust': c}


    def fit(self, tau=0.5, h=None, kernel="Laplacian",
            beta0=np.array([]), res=np.array([]), weight=np.array([]), 
            standardize=True, adjust=True):
        '''
            Convolution Smoothed Quantile Regression

        Args:
            tau: quantile level between 0 and 1; default is 0.5.
            h: bandwidth; the default value is computed by self.bandwidth(tau).
            kernel: a character string representing one of the 
                    built-in smoothing kernels; default is "Laplacian".
            beta0: initial estimate; default is np.array([]).
            res: an ndarray of fitted residuals; default is np.array([]).
            weight: an ndarray of observation weights; default is np.array([]).
            standardize: logical flag for x variable standardization 
                         prior to fitting the model; default is TRUE.
            adjust: logical flag for returning coefficients on the original scale.

        Returns:
            'beta': conquer estimate.
            'res': an ndarray of fitted residuals.
            'niter': number of iterations.
            'bw': bandwidth.
            'lr_seq': a sequence of learning rates determined by the BB method.
            'lval_seq': a sequence of (smoothed check) loss values at the iterations.
        '''
        bw = self.bandwidth(tau) if h is None else h 
        n, p = self.X.shape

        if kernel not in self.kernels:
            raise ValueError("kernel must be either Laplacian, Gaussian, Logistic, Uniform or Epanechnikov")

        X = self.X1 if standardize else self.X

        if len(beta0) == 0:
            if self.params['warm_start']:
                model = self.als(tau=tau, standardize=standardize, adjust=False)
                beta0, res = model['beta'], model['res']
            else:
                beta0 = rgt.randn(p) / p**0.5
                res = self.Y - X.dot(beta0)
        elif len(beta0) == p: 
            res = self.Y - X.dot(beta0)
        else:
            raise ValueError("dimension of beta0 must match parameter dimension")
        
        lr_seq, lval_seq = [], []
        grad0 = X.T.dot(conquer_weight(-res/bw, tau, kernel, weight)) / n
        diff_beta = -grad0
        beta = beta0 + diff_beta
        res, t = self.Y - X.dot(beta), 0
        lval_seq.append(smooth_check(res, tau, bw, kernel, weight))
        
        while t < self.params['max_iter'] \
            and max(abs(diff_beta)) > self.params['tol']:
            grad1 = X.T.dot(conquer_weight(-res/bw, tau, kernel, weight)) / n
            diff_grad = grad1 - grad0
            r0, r1 = diff_beta.dot(diff_beta), diff_grad.dot(diff_grad)
            if r1 == 0: lr = 1
            else:
                r01 = diff_grad.dot(diff_beta)
                lr = min(logsumexp(abs(r01/r1)), logsumexp(abs(r0/r01)))

            if self.params['max_lr']: lr = min(lr, self.params['max_lr'])
            lr_seq.append(lr)
            grad0, diff_beta = grad1, -lr*grad1
            beta += diff_beta
            res = self.Y - X.dot(beta)
            lval_seq.append(smooth_check(res, tau, bw, kernel, weight))
            t += 1
        
        if standardize and adjust:
            beta[self.itcp:] = beta[self.itcp:]/self.sdX
            if self.itcp: beta[0] -= self.mX.dot(beta[1:])

        return {'beta': beta, 'bw': bw, 'niter': t,
                'lval_seq': np.array(lval_seq),
                'lr_seq': np.array(lr_seq), 'res': res}


    def bfgs_fit(self, tau=0.5, h=None, kernel="Laplacian",
                 beta0=np.array([]), tol=None, options=None):
        '''
            Convolution Smoothed Quantile Regression via BFGS
        
        Args:
            tau : quantile level between 0 and 1; default is 0.5.
            h : bandwidth/smoothing parameter; the default value is 
                computed by self.bandwidth(tau).
            kernel : a character string representing one of the built-in 
                     smoothing kernels; default is "Laplacian".
            beta0 : initial estimate; default is np.array([]).
            tol : tolerance for termination.
            options : a dictionary of solver options. Default is 
                      options={'gtol': 1e-05, 'norm': inf, 'maxiter': None,
                               'disp': False, 'return_all': False}
                      gtol : gradient norm must be less than gtol(float) 
                             before successful termination.
                      norm : order of norm (Inf is max, -Inf is min).
                      maxiter : maximum number of iterations to perform.
                      disp : set to True to print convergence messages.
                      return_all : set to True to return a list of the 
                                   best solution at each of the iterations.
        
        Returns:
            'beta' : conquer estimate (computed by the BFGS algorithm).
            'res' : a vector of fitted residuals.
            'bw' : bandwidth/smoothing parameter.
            'niter' : number of iterations.
            'loss_val' : value of the smoothed quantile loss at the output.
            'grad_val' : value of the gradient (of the smoothed loss) at the output.
            'message' : description of the cause of the termination.
        '''
        y, X = self.Y, self.X
        if h is None:
            h = self.bandwidth(tau)
        if h <= 0:
            raise ValueError('the bandwidth h must be strictly positive')
        if len(beta0) == 0:
            beta0 = np.zeros(X.shape[1])

        fun = lambda beta : smooth_check(y - X.dot(beta), tau, h, kernel)
        grad = lambda beta : \
            X.T.dot(conquer_weight((X.dot(beta)-y)/h, tau, kernel)) / self.n

        model = minimize(fun, beta0, method='BFGS', 
                         jac=grad, tol=tol, options=options)
        return {'beta': model['x'], 'bw': h,
                'res': y - X.dot(model['x']),
                'niter': model['nit'],
                'loss_val': model['fun'],
                'grad_val': model['jac'],
                'message': model['message']}


    def bw_path(self, tau=0.5, h_seq=np.array([]), L=20, kernel="Laplacian", 
                standardize=True, adjust=True):
        '''
            Solution Path of Conquer at a Sequence of Bandwidths

        Args:
            tau : quantile level; default is 0.5.
            h_seq : a sequence of bandwidths.
            L : number of bandwdiths; default is 20.
            kernel : a character string representing one of the built-in
                     smoothing kernels; default is "Laplacian".
            standardize : logical flag for x variable standardization.
            adjust : logical flag for returning coefficients 
                     on the original scale.

        Returns:
            'beta_seq' : a sequence of conquer estimates.
            'res_seq' : a sequence of residual vectors.
            'bw_seq' : a sequence of bandwidths in descending order.
        '''

        n, p = self.X.shape
        if not np.array(h_seq).any():
            h_seq = np.linspace(0.01, min((p + np.log(n))/n, 0.5)**0.4, num=L)

        X = self.X1 if standardize else self.X
        h_seq, L = np.sort(h_seq)[::-1], len(h_seq)
        beta_seq = np.empty(shape=(X.shape[1], L))
        res_seq = np.empty(shape=(n, L))
        model = self.fit(tau, h_seq[0], kernel, 
                         standardize=standardize, adjust=False)
        beta_seq[:,0], res_seq[:,0] = model['beta'], model['res']

        for l in range(1,L):      
            model = self.fit(tau, h_seq[l], kernel, 
                             model['beta'], model['res'],
                             standardize=standardize, adjust=False)
            beta_seq[:,l], res_seq[:,l] = model['beta'], model['res']
    
        if standardize and adjust:
            beta_seq[self.itcp:,] = beta_seq[self.itcp:,]/self.sdX[:,None]
            if self.itcp:
                beta_seq[0,:] -= self.mX.dot(beta_seq[1:,])

        return {'beta_seq': beta_seq, 'res_seq': res_seq, 'bw_seq': h_seq}

        
    def norm_ci(self, tau=0.5, h=None, kernel="Laplacian", 
                method=None, alpha=0.05, standardize=True):
        '''
            Normal Calibrated Confidence Intervals
        
        Args:
            tau : quantile level; default is 0.5.
            h : bandwidth. The default is computed by self.bandwidth(tau).
            kernel : a character string representing one of the built-in 
                     smoothing kernels; default is "Laplacian".
            method : a character string representing the method for 
                     computing the estimate; default is None.
            alpha : miscoverage level for each CI; default is 0.05.
            standardize : logical flag for x variable standardization 
                          prior to fitting the model; default is TRUE.

        Returns:
            'beta' : conquer estimate.
            'normal_ci' : numpy array. Normal CIs based on estimated 
                          asymptotic covariance matrix.
        '''
        if h is None: h = self.bandwidth(tau)
        X = self.X
        if method=='BFGS':
            model = self.bfgs_fit(tau, h, kernel)
        else:
            model = self.fit(tau, h, kernel, standardize=standardize)
        h = model['bw']
        hess_weight = norm.pdf(model['res']/h)
        grad_weight = ( norm.cdf(-model['res']/h) - tau)**2
        hat_V = (X.T * grad_weight).dot(X)/self.n
        inv_J = np.linalg.inv((X.T * hess_weight).dot(X)/(self.n * h))
        ACov = inv_J.dot(hat_V).dot(inv_J)
        rad = norm.ppf(1-0.5*alpha)*np.sqrt( np.diag(ACov) / self.n )        
        ci = np.c_[model['beta'] - rad, model['beta'] + rad]

        return {'beta': model['beta'], 'normal_ci': ci}


    def mb(self, tau=0.5, h=None, kernel="Laplacian", 
           weight="Exponential", standardize=True):
        '''
            Multiplier Bootstrap Estimates

        Args:
            tau : quantile level; default is 0.5.
            h : bandwidth. The default is computed by self.bandwidth(tau).
            kernel : a character string representing one of the built-in 
                     smoothing kernels; default is "Laplacian".
            weight : a character string representing weight distribution;
                     default is "Exponential".
            standardize : logical flag for x variable standardization 
                          prior to fitting the model; default is TRUE.

        Returns:
            'mb_beta' : numpy array. 
                        1st column: conquer estimate; 
                        2nd to last: bootstrap estimates.
        '''

        if h is None: h = self.bandwidth(tau)
        
        if weight not in self.weights:
            raise ValueError("weight distribution must be either Exponential,\
                             Rademacher, Multinomial, Gaussian,\
                             Uniform or Folded-normal")
           
        mdl = self.fit(tau, h, kernel, standardize=standardize, adjust=False)
        mb_beta = np.zeros([len(mdl['beta']), self.params['nboot']+1])
        mb_beta[:,0], res = np.copy(mdl['beta']), np.copy(mdl['res'])

        for b in range(self.params['nboot']):
            mdl = self.fit(tau, h, kernel, beta0=mb_beta[:,0],
                           res=res, weight=boot_weight(weight)(self.n),
                           standardize=standardize)
            mb_beta[:,b+1] = mdl['beta']

        if standardize:
            mb_beta[self.itcp:,0] = mb_beta[self.itcp:,0]/self.sdX
            if self.itcp: mb_beta[0,0] -= self.mX.dot(mb_beta[1:,0])

        ## delete NaN bootstrap estimates (when using Gaussian weights)
        mb_beta = mb_beta[:,~np.isnan(mb_beta).any(axis=0)]

        return mb_beta


    def mb_ci(self, tau=0.5, h=None, kernel="Laplacian", 
              weight="Exponential", alpha=0.05, standardize=True):
        '''
            Multiplier Bootstrap Confidence Intervals

        Arguments
        ---------
        tau : quantile level; default is 0.5.
        h : bandwidth. The default is computed by self.bandwidth(tau).
        kernel : a character string representing one of the built-in 
                 smoothing kernels; default is "Laplacian".
        weight : a character string representing weight distribution;
                 default is "Exponential".
        alpha : miscoverage level for each CI; default is 0.05.
        standardize : logical flag for x variable standardization 
                      prior to fitting the model; default is TRUE.

        Returns
        -------
        'boot_beta' : numpy array. 
                      1st column: conquer estimate; 
                      2nd to last: bootstrap estimates.
        'percentile_ci' : numpy array. Percentile bootstrap CI.
        'pivotal_ci' : numpy array. Pivotal bootstrap CI.
        'normal_ci' : numpy array. Normal-based CI using bootstrap variance estimates.
        '''
        if h==None: h = self.bandwidth(tau)
        
        mb_beta = self.mb(tau, h, kernel, weight, standardize)
        if weight in self.weights[:4]:
            adj = 1
        elif weight == 'Uniform':
            adj = np.sqrt(1/3)
        elif weight == 'Folded-normal':
            adj = np.sqrt(0.5*np.pi - 1)

        percentile_ci = np.c_[np.quantile(mb_beta[:,1:], 0.5*alpha, axis=1),\
                              np.quantile(mb_beta[:,1:], 1-0.5*alpha, axis=1)]
        pivotal_ci = np.c_[(1+1/adj)*mb_beta[:,0] - percentile_ci[:,1]/adj,\
                           (1+1/adj)*mb_beta[:,0] - percentile_ci[:,0]/adj] 

        radi = norm.ppf(1-0.5*alpha)*np.std(mb_beta[:,1:], axis=1)/adj
        normal_ci = np.c_[mb_beta[:,0] - radi, mb_beta[:,0] + radi]

        return {'boot_beta': mb_beta, 
                'percentile_ci': percentile_ci,
                'pivotal_ci': pivotal_ci,
                'normal_ci': normal_ci}


    def Huber(self, c=1, beta0=np.array([]), tol=1e-6, options=None):
        '''
            Huber Regression via BFGS

        Args:
            c : robustness parameter; default is 1.
            beta0 : initial estimate; default is np.array([]).
            tol : tolerance for termination.
            options : a dictionary of solver options. Default is 
                      {'gtol': 1e-05, 'norm': inf, 'maxiter': None, 
                       'disp': False, 'return_all': False}
        '''

        y, X = self.Y, self.X

        huber_loss = lambda u : \
            np.where(abs(u)<=c, 0.5 * u**2, c * abs(u) - 0.5 * c**2)
        huber_score = lambda u : np.where(abs(u)<=c, u, np.sign(u)*c)

        beta0 = np.zeros(X.shape[1]) if len(beta0) == 0 else beta0

        fun = lambda beta : np.mean(huber_loss(y - X@beta))
        grad = lambda beta : X.T.dot(huber_score(X@beta - y))/X.shape[0]
        model = minimize(fun, beta0, method='BFGS', jac=grad, tol=tol, options=options)

        return {'beta': model['x'], 'robust': c,
                'res': y - X.dot(model['x']),
                'niter': model['nit'],
                'loss_val': model['fun'],
                'grad_val': model['jac'],
                'message': model['message']}


    def adaHuber(self, dev_prob=None, max_iter=100):
        '''
            Adaptive Huber Regression

        Args:
            dev_prob : exception probability value between; 
                       default is 1/sample_size.
            max_iter : maximum number of iterations; default is 100.
        '''
        if dev_prob is None:
            dev_prob = 1 / self.n
        beta_hat = np.linalg.solve(self.X.T.dot(self.X), self.X.T.dot(self.Y))

        rel, err, t = (self.X.shape[1] + np.log(1 / dev_prob)) / self.n, 1, 0
        while err > self.params['tol'] and t < max_iter:
            res = self.Y - self.X.dot(beta_hat)
            f = lambda c: np.mean(np.minimum((res / c) ** 2, 1)) - rel
            robust = find_root(f, np.min(np.abs(res)) \
                               + self.params['tol'], np.sqrt(res @ res))
            model = self.Huber(c=robust)
            # self.als(robust=robust, scale=False)
            err = np.max(np.abs(model['beta'] - beta_hat))
            beta_hat = model['beta']
            t += 1

        return {'beta': beta_hat, 'niter': t,
                'robust': robust, 'res': res}



###############################################################################
###########################    Helper Functions    ############################
###############################################################################
def soft_thresh(x, c):
    tmp = abs(x) - c
    return np.sign(x)*np.where(tmp<=0, 0, tmp)


def concave_weight(x, penalty="SCAD", a=None):
    if penalty == "SCAD":
        if a is None:
            a = 3.7
        tmp = 1 - (abs(x) - 1) / (a - 1)
        tmp = np.where(tmp <= 0, 0, tmp)
        return np.where(tmp > 1, 1, tmp)
    elif penalty == "MCP":
        if a is None:
            a = 3
        tmp = 1 - abs(x) / a 
        return np.where(tmp <= 0, 0, tmp)
    elif penalty == "CappedL1":
        if a is None:
            a = 3
        return abs(x) <= a / 2
        

def als_loss(x, tau, c):
    out = 0.5 * (abs(x) <= c) * x**2 \
        + (c * abs(x) - 0.5 * c ** 2) * (abs(x) > c)
    return np.mean(abs(tau - (x<0)) * out)


def sparse_proj(x, s):
    return np.where(abs(x) < np.sort(abs(x))[-s], 0, x)


def sparse_supp(x, s):
    y = abs(x)
    return y >= np.sort(y)[-s]


###############################################################################
################### Penalized Smoothed Quantile Regression ####################
###############################################################################
class high_dim(low_dim):
    '''
        Penalized Convolution Smoothed Quantile Regression via ILAMM
        (iterative local adaptive majorize-minimization)
    '''
    weights = ['Multinomial', 'Exponential', 'Rademacher']
    penalties = ["L1", "SCAD", "MCP", "CapppedL1"]
    params = {'phi': 0.1, 'gamma': 1.25, 'max_iter': 1e3, 'tol': 1e-8, 
              'iter_warning': True, 'warm_start': True, 'max_lr': 50,
              'irw_tol': 1e-5, 'nsim': 200, 'nboot': 200, 
              'min_bandwidth': 1e-4}

    def __init__(self, X, Y, intercept=True, options={}):

        '''
        Args:
            X: n by p matrix of covariates; each row is an observation vector.
            Y: an ndarray of response variables.
            intercept: logical flag for adding an intercept to the model.
            options: a dictionary of internal statistical and optimization parameters.
                phi: initial quadratic coefficient parameter in the ILAMM algorithm; 
                     default is 0.1.
                gamma: adaptive search parameter that is larger than 1; default is 1.25.
                max_iter: maximum numder of iterations in the ILAMM algorithm; default is 1e3.
                tol: the ILAMM iteration terminates when |beta^{k+1} - beta^k|_max <= tol; 
                     default is 1e-8.
                iter_warning: logical flag for warning when the maximum number 
                              of iterations is achieved for the l1-penalized fit.
                warm_start: logical flag for using a penalized robust expectile regression 
                            estimate as an initial value.
                irw_tol: tolerance parameter for stopping iteratively reweighted L1-penalization; 
                         default is 1e-5.
                nsim: number of simulations for computing a data-driven lambda; default is 200.
                nboot: number of bootstrap samples for post-selection inference; default is 200.
        '''
        self.n, self.p = X.shape
        self.Y = Y.reshape(self.n)
        self.mX, self.sdX = np.mean(X, axis=0), np.std(X, axis=0)
        self.itcp = intercept
        if intercept:
            self.X = np.c_[np.ones(self.n), X[:]]
            self.X1 = np.c_[np.ones(self.n), (X[:] - self.mX)/self.sdX]
        else:
            self.X, self.X1 = X[:], X[:]/self.sdX

        self.params.update(options)


    def bandwidth(self, tau):
        h0 = (np.log(self.p) / self.n) ** 0.25
        return max(self.params['min_bandwidth'], 
                   h0 * (tau-tau**2) ** 0.5)


    def self_tuning(self, tau=0.5, standardize=True):
        '''
            A Simulation-based Approach for Choosing the Penalty Level
        
        Refs:
            l1-Penalized quantile regression in high-dimensinoal sparse models
            by Alexandre Belloni and Victor Chernozhukov
            The Annals of Statistics 39(1): 82--130, 2011

        Args:
            tau: quantile level; default is 0.5.
            standardize: logical flag for x variable standardization
                         prior to fitting the model; default is TRUE.
        
        Returns:
            lambda_sim: an ndarray of simulated lambda values.
        '''

        X = self.X1 if standardize else self.X
        lambda_sim = \
            np.array([max(abs(X.T@(tau - (rgt.uniform(0,1,self.n) <= tau))))
                      for b in range(self.params['nsim'])])
        return lambda_sim/self.n


    def l1_als(self, tau=0.5, Lambda=np.array([]), robust=5,
               beta0=np.array([]), res=np.array([]),
               standardize=True, adjust=True):
        '''
            L1-Penalized Asymmetric (Robust) Least Squares Regression
        ''' 
        if not np.array(Lambda).any(): 
            Lambda = np.quantile(self.self_tuning(tau, standardize), 0.9)

        X = self.X1 if standardize else self.X
        if len(beta0) == 0:
            beta0 = np.zeros(X.shape[1])
            if self.itcp: beta0[0] = np.quantile(self.Y, tau)
            res = self.Y - beta0[0]

        phi, dev, count = self.params['phi'], 1, 0
        while dev > self.params['tol'] \
            and count < self.params['max_iter']:
            c = robust * min(mad(res), np.std(res))
            if c == 0 or np.log(c) < -10:
                c = robust
            grad0 = X.T.dot(-asymHuber_grad(res, tau, c))
            loss_eval0 = als_loss(res, tau, c)
            beta1 = beta0 - grad0/phi
            beta1[self.itcp:] = soft_thresh(beta1[self.itcp:], Lambda/phi)
            diff_beta = beta1 - beta0
            r0 = diff_beta.dot(diff_beta)
            res = self.Y - X.dot(beta1)
            loss_proxy = loss_eval0 + diff_beta.dot(grad0) + 0.5*phi*r0
            loss_eval1 = als_loss(res, tau, c)
            
            while loss_proxy < loss_eval1:
                phi *= self.params['gamma']
                beta1 = beta0 - grad0/phi
                beta1[self.itcp:] = soft_thresh(beta1[self.itcp:], Lambda/phi)
                diff_beta = beta1 - beta0
                r0 = diff_beta.dot(diff_beta)
                res = self.Y - X.dot(beta1)
                loss_proxy = loss_eval0 + diff_beta.dot(grad0) + 0.5*phi*r0
                loss_eval1 = als_loss(res, tau, c)
                
            dev = max(abs(diff_beta))
            beta0, phi = beta1, self.params['phi']
            count += 1

        if standardize and adjust:
            beta0[self.itcp:] = beta0[self.itcp:]/self.sdX
            if self.itcp: beta0[0] -= self.mX.dot(beta0[1:])

        return {'beta': beta0, 'res': res, 'niter': count, 'lambda': Lambda}

        
    def l1(self, tau=0.5, Lambda=np.array([]), 
           h=None, kernel="Laplacian",
           beta0=np.array([]), res=np.array([]), 
           standardize=True, adjust=True, weight=np.array([])):
        '''
            L1-Penalized Convolution Smoothed Quantile Regression (l1-conquer)

        Args:
            tau : quantile level; default is 0.5.
            Lambda : regularization parameter. This should be either a scalar, or 
                     a vector of length equal to the column dimension of X. If unspecified, 
                     it will be computed by self.self_tuning().
            h : bandwidth/smoothing parameter; the default value is computed by self.bandwidth().
            kernel : a character string representing one of the built-in smoothing kernels; 
                     default is "Laplacian".
            beta0 : initial estimate. If unspecified, it will be set as a vector of zeros.
            res : residual vector of the initial estimate.
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            adjust : logical flag for returning coefficients on the original scale.
            weight : an ndarray of observation weights; default is np.array([]) (empty).
        
        Returns:
            'beta' : an ndarray of estimated coefficients.
            'res' : an ndarray of fitted residuals.
            'niter' : number of iterations.
            'lambda' : lambda value.
            'bw' : bandwidth.
        '''

        X = self.X1 if standardize else self.X
        if not np.array(Lambda).any():
            Lambda = 0.75*np.quantile(self.self_tuning(tau,standardize), 0.9)
        if h is None: h = self.bandwidth(tau)
        
        if len(beta0) == 0:
            if self.params['warm_start']:
                init = self.l1_als(tau, Lambda, 
                                   standardize=standardize, adjust=False)
                beta0, res = init['beta'], init['res']
            else:
                beta0 = np.zeros(X.shape[1])
                if self.itcp: beta0[0] = np.quantile(self.Y, tau)
                res = self.Y - beta0[0]
        elif len(beta0) == X.shape[1]:
            res = self.Y - X.dot(beta0)
        else:
            raise ValueError("dimension of beta0 must match parameter dimension")
        
        phi, r0, t = self.params['phi'], 1, 0 
        while r0 > self.params['tol'] and t < self.params['max_iter']:
            grad0 = X.T@(conquer_weight(-res/h, tau, kernel, weight)/self.n)
            loss_eval0 = smooth_check(res, tau, h, kernel, weight)
            beta1 = beta0 - grad0/phi
            beta1[self.itcp:] = soft_thresh(beta1[self.itcp:], Lambda/phi)
            diff_beta = beta1 - beta0
            r0 = diff_beta.dot(diff_beta)          
            res = self.Y - X@(beta1)
            loss_proxy = loss_eval0 + diff_beta.dot(grad0) + 0.5*phi*r0
            loss_eval1 = smooth_check(res, tau, h, kernel, weight)
            
            while loss_proxy < loss_eval1:
                phi *= self.params['gamma']
                beta1 = beta0 - grad0/phi
                beta1[self.itcp:] = soft_thresh(beta1[self.itcp:], Lambda/phi)
                diff_beta = beta1 - beta0
                r0 = diff_beta.dot(diff_beta)
                res = self.Y - X@(beta1)
                loss_proxy = loss_eval0 + diff_beta.dot(grad0) + 0.5*phi*r0
                loss_eval1 = smooth_check(res, tau, h, kernel, weight)

            beta0, phi = beta1, self.params['phi']
            t += 1

        if t == self.params['max_iter'] and self.params['iter_warning']: 
            warnings.warn("Maximum number of iterations achieved when applying l1() with Lambda={} and tau={}".format(Lambda, tau))

        if standardize and adjust:
            beta1[self.itcp:] = beta1[self.itcp:]/self.sdX
            if self.itcp: beta1[0] -= self.mX.dot(beta1[1:])
            
        return {'beta': beta1, 'res': res, 
                'niter': t, 'lambda': Lambda, 'bw': h}


    def irw(self, tau=0.5, Lambda=np.array([]),
            h=None, kernel="Laplacian",
            beta0=np.array([]), res=np.array([]), 
            penalty="SCAD", a=3.7, nstep=3, 
            standardize=True, adjust=True, weight=np.array([])):
        '''
            Iteratively Reweighted L1-Penalized Conquer (irw-l1-conquer)
        
        Args:
            tau : quantile level; default is 0.5.
            Lambda : regularization parameter. This should be either a scalar, or 
                     a vector of length equal to the column dimension of X. If unspecified, 
                     it will be computed by self.self_tuning().
            h : bandwidth/smoothing parameter; 
                default value is computed by self.bandwidth().
            kernel : a character string representing one of the built-in smoothing kernels;
                     default is "Laplacian".
            beta0 : initial estimator. If unspecified, it will be set as zero.
            res : residual vector of the initial estiamtor.
            penalty : a character string representing one of the built-in concave penalties;
                      default is "SCAD".
            a : the constant (>2) in the concave penality; default is 3.7.
            nstep : number of iterations/steps of the IRW algorithm; default is 3.
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            adjust : logical flag for returning coefficients on the original scale.
            weight : an ndarray of observation weights; default is np.array([]) (empty).

        Returns:
            'beta' : an ndarray of estimated coefficients.
            'res' : an ndarray of fitted residuals.
            'nstep' : number of reweighted penalization steps.
            'lambda' : lambda value.
            'niter' : total number of iterations.
            'nit_seq' : a sequence of numbers of iterations.
        '''

        if not Lambda.any():
            Lambda = 0.75*np.quantile(self.self_tuning(tau,standardize), 0.9)
        if h is None: h = self.bandwidth(tau)
        
        if len(beta0) == 0:
            model = self.l1(tau, Lambda, h, kernel, standardize=standardize,
                            adjust=False, weight=weight)
        else:
            model = self.l1(tau, Lambda, h, kernel, beta0, res, standardize, 
                            adjust=False, weight=weight)

        nit_seq = []
        beta0, res = model['beta'], model['res']
        nit_seq.append(model['niter'])
        if penalty == 'L1': nstep = 0

        lam = Lambda * np.ones(len(self.mX))
        pos = lam > 0
        rw_lam = np.zeros(len(self.mX))

        dev, step = 1, 1
        while dev > self.params['irw_tol'] and step <= nstep:
            rw_lam[pos] = lam[pos] * \
                          concave_weight(beta0[self.itcp:][pos]/lam[pos], 
                                         penalty, a)
            model = self.l1(tau, rw_lam, h, kernel, beta0, res,
                            standardize, adjust=False, weight=weight)
            dev = max(abs(model['beta']-beta0))
            beta0, res = model['beta'], model['res']
            nit_seq.append(model['niter'])
            step += 1
        
        if standardize and adjust:
            beta0[self.itcp:] = beta0[self.itcp:]/self.sdX
            if self.itcp: beta0[0] -= self.mX.dot(beta0[1:])
        nit_seq = np.array(nit_seq)
            
        return {'beta': beta0, 'res': res, 'nstep': step, 'lambda': Lambda,
                'niter': np.sum(nit_seq), 'nit_seq': nit_seq}


    def irw_als(self, tau=0.5, Lambda=np.array([]), robust=3,
                penalty="SCAD", a=3.7, nstep=3,
                standardize=True, adjust=True):
        '''
            Iteratively Reweighted L1-Penalized Asymmetric Least Squares 
            (irw-l1-als)
        '''
        if not Lambda.any():
            Lambda = np.quantile(self.self_tuning(tau,standardize), 0.9)
        
        model = self.l1_als(tau, Lambda, robust, 
                            standardize=standardize, adjust=False)
        beta0, res = model['beta'], model['res']

        lam = Lambda * np.ones(len(self.mX))
        pos = lam > 0
        rw_lam = np.zeros(len(self.mX))        

        dev, step = 1, 1
        while dev > self.params['irw_tol'] and step <= nstep:
            rw_lam[pos] = lam[pos] * \
                          concave_weight(beta0[self.itcp:][pos]/lam[pos], 
                                         penalty, a)
            model = self.l1_als(tau, rw_lam, robust, \
                                   beta0, res, standardize, adjust=False)
            dev = max(abs(model['beta']-beta0))
            beta0, res = model['beta'], model['res']
            step += 1
        
        if standardize and adjust:
            beta0[self.itcp:] = beta0[self.itcp:]/self.sdX
            if self.itcp: beta0[0] -= self.mX.dot(beta0[1:])
            
        return {'beta': beta0, 'res': res, 'nstep': step, 'lambda': Lambda}
    

    def l1_path(self, tau, 
                lambda_seq=np.array([]), nlambda=50, order="descend",
                h=None, kernel="Laplacian", 
                standardize=True, adjust=True):
        '''
            Solution Path of L1-Penalized Conquer

        Args:
            tau : quantile level (float between 0 and 1).
            lambda_seq : an ndarray of lambda values.
            nlambda : number of lambda values (int).
            order : a character string indicating the order of lambda values 
                    along which the solution path is obtained; default is 'descend'.
            h : bandwidth/smoothing parameter (float).
            kernel : a character string representing one of the built-in smoothing kernels;
                     default is "Laplacian".
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            adjust : logical flag for returning coefficients on the original scale.

        Returns:
            'beta_seq' : a sequence of l1-conquer estimates; 
                         each column corresponds to an estiamte for a lambda value.
            'res_seq' : a sequence of residual vectors. 
            'size_seq' : a sequence of numbers of selected variables. 
            'lambda_seq' : a sequence of lambda values in ascending/descending order.
            'nit_seq' : a sequence of numbers of iterations.
            'bw' : bandwidth.
        '''

        if h is None: h = self.bandwidth(tau)

        if len(lambda_seq) == 0:
            lam_max = max(self.self_tuning(tau, standardize))
            lambda_seq = np.linspace(0.25*lam_max, lam_max, num=nlambda)
 
        if order == 'ascend':
            lambda_seq = np.sort(lambda_seq)
        elif order == 'descend':
            lambda_seq = np.sort(lambda_seq)[::-1]

        nit_seq = []
        beta_seq = np.zeros(shape=(self.X.shape[1], len(lambda_seq)))
        res_seq = np.zeros(shape=(self.n, len(lambda_seq)))
        model = self.l1(tau, lambda_seq[0], h, kernel, 
                        standardize=standardize, adjust=False)
        beta_seq[:,0], res_seq[:,0] = model['beta'], model['res']
        nit_seq.append(model['niter'])

        for l in range(1, len(lambda_seq)):
            model = self.l1(tau, lambda_seq[l], h, kernel, beta_seq[:,l-1],
                            res_seq[:,l-1], standardize, adjust=False)
            beta_seq[:,l], res_seq[:,l] = model['beta'], model['res']
            nit_seq.append(model['niter'])

        if standardize and adjust:
            beta_seq[self.itcp:,] = beta_seq[self.itcp:,]/self.sdX[:,None]
            if self.itcp: beta_seq[0,:] -= self.mX.dot(beta_seq[1:,])

        return {'beta_seq': beta_seq, 
                'res_seq': res_seq,
                'size_seq': np.sum(beta_seq[self.itcp:,:] != 0, axis=0),
                'lambda_seq': lambda_seq, \
                'nit_seq': np.array(nit_seq), 'bw': h}


    def irw_path(self, tau, 
                 lambda_seq=np.array([]), nlambda=50, order="descend",
                 h=None, kernel="Laplacian",
                 penalty="SCAD", a=3.7, nstep=3, 
                 standardize=True, adjust=True):
        '''
            Solution Path of Iteratively Reweighted L1-Conquer

        Args: 
            tau : quantile level (float between 0 and 1).
            lambda_seq : an ndarray of lambda values (int).
            nlambda : number of lambda values.
            order : a character string indicating the order of lambda values
                    along which the solution path is obtained; default is 'descend'.
            h : bandwidth/smoothing parameter (float).
            kernel : a character string representing one of the built-in smoothing kernels;
                     default is "Laplacian".
            penalty : a character string representing one of the built-in concave penalties;
                      default is "SCAD".
            a : the constant (>2) in the concave penality; default is 3.7.
            nstep : number of iterations/steps of the IRW algorithm; default is 3.
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            adjust : logical flag for returning coefficients on the original scale.

        Returns:
            'beta_seq' : a sequence of irw-l1-conquer estimates;
                         each column corresponds to an estiamte for a lambda value.
            'res_seq' : a sequence of residual vectors. 
            'size_seq' : a sequence of numbers of selected variables. 
            'lambda_seq' : a sequence of lambda values in ascending/descending order.
            'nit_seq' : a sequence of numbers of iterations.
            'bw' : bandwidth.
        '''

        if h is None: h = self.bandwidth(tau)

        if len(lambda_seq) == 0:
            lam_max = max(self.self_tuning(tau, standardize))
            lambda_seq = np.linspace(0.5*lam_max, lam_max, num=nlambda)
        
        if order == 'ascend':
            lambda_seq = np.sort(lambda_seq)
        elif order == 'descend':
            lambda_seq = np.sort(lambda_seq)[::-1]

        beta_seq = np.zeros(shape=(self.X.shape[1], len(lambda_seq)))
        res_seq = np.zeros(shape=(self.n, len(lambda_seq)))
        nit_seq = []
        model = self.irw(tau, lambda_seq[0], h, kernel,
                         penalty=penalty, a=a, nstep=nstep,
                         standardize=standardize, adjust=False)
        beta_seq[:,0], res_seq[:,0] = model['beta'], model['res']
        nit_seq.append(model['niter'])

        for l in range(1, len(lambda_seq)):
            model = self.irw(tau, lambda_seq[l], h, kernel,
                             beta_seq[:,l-1], res_seq[:,l-1],
                             penalty, a, nstep, standardize, adjust=False)
            beta_seq[:,l], res_seq[:,l] = model['beta'], model['res']
            nit_seq.append(model['niter'])

        if standardize and adjust:
            beta_seq[self.itcp:,] /= self.sdX[:,None]
            if self.itcp: beta_seq[0,:] -= self.mX.dot(beta_seq[1:,])
    
        return {'beta_seq': beta_seq, 
                'res_seq': res_seq,
                'size_seq': np.sum(beta_seq[self.itcp:,:] != 0, axis=0),
                'lambda_seq': lambda_seq,
                'nit_seq': np.array(nit_seq), 'bw': h}


    def bic(self, tau=0.5, 
            lambda_seq=np.array([]), nlambda=100, order='descend',
            h=None, kernel="Laplacian", max_size=False, Cn=None,
            penalty="SCAD", a=3.7, nstep=3, 
            standardize=True, adjust=True):
        '''
            Model Selection via Bayesian Information Criterion
        
        Refs:
            Model selection via Bayesian information criterion 
            for quantile regression models (2014)
            by Eun Ryung Lee, Hohsuk Noh and Byeong U. Park
            Journal of the American Statistical Association 109(505): 216--229.

        Args:
            max_size : an upper bound on the selected model size; default is FALSE (no restriction).
            Cn : a positive constant in the modified BIC; default is log(log n).

        Returns:
            'bic_beta' : estimated coefficient vector for the BIC-selected model.
            'bic_res' : residual vector for the BIC-selected model.
            'bic_size' : size of the BIC-selected model.
            'bic_lambda' : lambda value that corresponds to the BIC-selected model.
            'beta_seq' : a sequence of penalized conquer estimates; 
                         each column corresponds to an estiamte for a lambda value.
            'size_seq' : a vector of estimated model sizes corresponding to lambda_seq.
            'lambda_seq' : a vector of lambda values.
            'bic' : a vector of BIC values corresponding to lambda_seq.
            'bw' : bandwidth.
        '''  

        if not lambda_seq.any():
            lam_max = max(self.self_tuning(tau=tau, standardize=standardize))
            lambda_seq = np.linspace(0.25 * lam_max, lam_max, num=nlambda)
        else:
            nlambda = len(lambda_seq)

        if Cn is None: Cn = max(2, np.log(np.log(self.n)))

        if penalty not in self.penalties: 
            raise ValueError("penalty must be either L1, SCAD, MCP or CapppedL1")

        check_sum = lambda x : np.sum(np.where(x >= 0, tau * x, (tau - 1) * x))

        if penalty == "L1":
            model_all = self.l1_path(tau, lambda_seq, nlambda, order,
                                     h, kernel, standardize, adjust)
        else:
            model_all = self.irw_path(tau, lambda_seq, nlambda, order,
                                      h, kernel, penalty, a, nstep, 
                                      standardize, adjust)

        BIC = np.array([np.log(check_sum(model_all['res_seq'][:,l])) 
                        for l in range(nlambda)])
        BIC += model_all['size_seq'] * np.log(self.p) * Cn / self.n
        if not max_size:
            bic_select = np.argmin(BIC)
        else:
            bic_select = np.where(BIC==min(BIC[model_all['size_seq'] 
                                               <= max_size]))[0][0]

        return {'bic_beta': model_all['beta_seq'][:,bic_select],
                'bic_res':  model_all['res_seq'][:,bic_select],
                'bic_size': model_all['size_seq'][bic_select],
                'bic_lambda': model_all['lambda_seq'][bic_select],
                'beta_seq': model_all['beta_seq'],
                'size_seq': model_all['size_seq'],
                'lambda_seq': model_all['lambda_seq'],
                'bic': BIC,
                'bw': model_all['bw']}


    def boot_select(self, tau=0.5, Lambda=None, 
                    h=None, kernel="Laplacian",
                    weight="Multinomial", penalty="SCAD", a=3.7, nstep=3,
                    standardize=True, parallel=False, ncore=None):
        '''
            Model Selection via Bootstrap 

        Args:   
            tau : quantile level; default is 0.5.
            Lambda : regularization parameter (float);
                     if unspecified, it will be computed by self.self_tuning().
            h : smoothing parameter/bandwidth. The default is computed by self.bandwidth().
            kernel : a character string representing one of the built-in smoothing kernels;
                     default is "Laplacian".
            weight : a character string representing the random weight distribution;
                     default is "Multinomial".
            penalty : a character string representing one of the built-in concave penalties;
                      default is "SCAD".
            a : the constant (>2) in the concave penality; default is 3.7.
            nstep : number of iterations/steps of the IRW algorithm; default is 3.
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            parallel : logical flag to implement bootstrap using parallel computing;
                       default is FALSE.
            ncore : number of cores used for parallel computing.
        
        Returns:
            'boot_beta' : numpy array. 
                          1st column: penalized conquer estimate; 
                          2nd to last: bootstrap estimates.
            
            'majority_vote' : selected model by majority vote.

            'intersection' : selected model by intersecting.
        '''

        if Lambda is None: 
            Lambda = 0.75*np.quantile(self.self_tuning(tau, standardize), 0.9)
        if h is None: h = self.bandwidth(tau) 
        if weight not in self.weights[:3]:
            raise ValueError("weight distribution must be either Exponential, Rademacher or Multinomial")

        model = self.irw(tau, Lambda, h, kernel, 
                         penalty=penalty, a=a, nstep=nstep,
                         standardize=standardize, adjust=False)
        mb_beta = np.zeros(shape=(self.p+self.itcp, self.params['nboot']+1))
        mb_beta[:,0] = model['beta']
        if standardize:
            mb_beta[self.itcp:,0] = mb_beta[self.itcp:,0]/self.sdX
            if self.itcp: mb_beta[0,0] -= self.mX.dot(mb_beta[1:,0])

        if parallel:
            import multiprocessing
            max_ncore = multiprocessing.cpu_count()
            if ncore is None: ncore = max_ncore
            if ncore > max_ncore: raise ValueError("number of cores exceeds the limit")

        def bootstrap(b):
            boot_fit = self.irw(tau, Lambda, h, kernel,
                                beta0=model['beta'], res=model['res'],
                                penalty=penalty, a=a, nstep=nstep,
                                standardize=standardize,
                                weight=boot_weight(weight)(self.n))
            return boot_fit['beta']

        if not parallel:
            for b in range(self.params['nboot']): 
                mb_beta[:,b+1] = bootstrap(b)
        else:
            from joblib import Parallel, delayed
            boot_results \
                = Parallel(n_jobs=ncore)(delayed(bootstrap)(b)
                                         for b in range(self.params['nboot']))
            mb_beta[:,1:] = np.array(boot_results).T
        
        ## delete NaN bootstrap estimates (when using Gaussian weights)
        mb_beta = mb_beta[:,~np.isnan(mb_beta).any(axis=0)]
        
        ## Method 1: Majority vote among all bootstrap models
        selection_rate = np.mean(mb_beta[self.itcp:,1:]!=0, axis=1)
        model1 = np.where(selection_rate>0.5)[0]
        
        ## Method 2: Intersection of all bootstrap models
        model2 = np.arange(self.p)
        for b in range(len(mb_beta[0,1:])):
            boot_model = np.where(mb_beta[self.itcp:,b+1] != 0)[0]
            model2 = np.intersect1d(model2, boot_model)

        return {'boot_beta': mb_beta, \
                'majority_vote': model1, \
                'intersection': model2}


    def boot_inference(self, tau=0.5, Lambda=None, 
                       h=None, kernel="Laplacian",
                       weight="Multinomial", alpha=0.05, 
                       penalty="SCAD", a=3.7, nstep=3,
                       standardize=True, parallel=False, ncore=None):
        '''
            Post-Selection-Inference via Bootstrap

        Returns:
            'boot_beta' : numpy array. 
                          1st column: penalized conquer estimate; 
                          2nd to last: bootstrap estimates.
            
            'majority_vote' : selected model by majority vote.

            'intersection' : selected model by intersecting.

            'percentile_ci' : numpy array. Percentile bootstrap CI.

            'pivotal_ci' : numpy array. Pivotal bootstrap CI.

            'normal_ci' : numpy array. Normal-based CI using bootstrap variance estimates.
        '''

        mb_model = self.boot_select(tau, Lambda, h, kernel, weight,
                                    penalty, a, nstep, standardize,
                                    parallel, ncore)
        
        percentile_ci = np.zeros([self.p + self.itcp, 2])
        pivotal_ci = np.zeros([self.p + self.itcp, 2])
        normal_ci = np.zeros([self.p + self.itcp, 2])

        # post-selection bootstrap inference
        X_select = self.X[:, mb_model['majority_vote']+self.itcp]
        fit = low_dim(X_select, self.Y, self.itcp)\
              .mb_ci(tau, kernel=kernel, weight=weight,
                     alpha=alpha, standardize=standardize)

        percentile_ci[mb_model['majority_vote']+self.itcp,:] \
            = fit['percentile_ci'][self.itcp:,:]
        pivotal_ci[mb_model['majority_vote']+self.itcp,:] \
            = fit['pivotal_ci'][self.itcp:,:]
        normal_ci[mb_model['majority_vote']+self.itcp,:] \
            = fit['normal_ci'][self.itcp:,:]

        if self.itcp: 
            percentile_ci[0,:] = fit['percentile_ci'][0,:]
            pivotal_ci[0,:] = fit['pivotal_ci'][0,:]
            normal_ci[0,:] = fit['normal_ci'][0,:]

        return {'boot_beta': mb_model['boot_beta'],
                'percentile_ci': percentile_ci,
                'pivotal_ci': pivotal_ci,
                'normal_ci': normal_ci,
                'majority_vote': mb_model['majority_vote'],
                'intersection': mb_model['intersection']}


    def l0(self, tau=0.5, h=None, kernel='Laplacian', 
           sparsity=5, exp_size=5, beta0=np.array([]),
           standardize=True, adjust=True,
           tol=1e-5, max_iter=1e3):
        '''
            L0-Penalized Conquer via Two-Step Iterative Hard-Thresholding

        Refs:
            On iterative hard thresholding methods for high-dimensional M-estimation
            by Prateek Jain, Ambuj Tewari and Purushottam Kar
            Advances in Neural Information Processing Systems 27, 2014

        Args:
            tau : quantile level between 0 and 1 (float); default is 0.5.
            h : smoothing/bandwidth parameter (float).
            kernel : a character string representing one of the built-in smoothing kernels;
                     default is "Laplacian".
            sparsity : sparsity level (int, >=1); default is 5.
            exp_size : expansion size (int, >=1); default is 5.
            beta0 : initial estimate.
            standardize : logical flag for x variable standardization prior to fitting the model;

        Returns:
            'beta' : an ndarray of estimated coefficients.
            'select' : indices of non-zero estimated coefficients (intercept excluded).
            'bw' : bandwidth.
            'niter' : number of IHT iterations.
        '''

        X, Y, itcp = self.X, self.Y, self.itcp

        if h is None: 
            h0 = min((sparsity + np.log(self.n))/self.n, 0.5) ** 0.4
            h = max(0.01, h0 * (tau-tau**2) ** 0.5)
        if len(beta0) == 0: beta0 = np.zeros(X.shape[1])
        
        t, dev = 0, 1
        while t < max_iter and dev > tol:
            grad0 = X.T@(conquer_weight((X@beta0 - Y)/h, tau, kernel)/self.n)
            supp0 = sparse_supp(grad0[itcp:], exp_size) + (beta0[itcp:] != 0)
            beta1 = np.zeros(X.shape[1])
            out0 = low_dim(X[:,itcp:][:,supp0], Y, intercept=itcp) \
                   .fit(tau=tau, h=h, standardize=standardize, adjust=adjust)
            beta1[itcp:][supp0] = out0['beta'][itcp:]
            if itcp: beta1[0] = out0['beta'][0]
            beta1[itcp:] = sparse_proj(beta1[itcp:], sparsity)
            supp1 = beta1[itcp:] != 0
            out1 = low_dim(X[:,itcp:][:,supp1], Y, intercept=itcp) \
                   .fit(tau=tau, h=h, standardize=standardize, adjust=adjust)
            beta1[itcp:][supp1] = out1['beta'][itcp:]
            if itcp: beta1[0] = out1['beta'][0]
            dev = max(abs(beta1 - beta0))
            beta0 = beta1[:]
            t += 1

        return {'beta': beta0, 
                'select': np.where(beta0[itcp:] != 0)[0],
                'bw': h,
                'niter': t}


    def l0_path(self, tau, h=None, kernel='Laplacian', 
                sparsity_seq=np.array([]), order='ascend',
                sparsity_max=20, exp_size=5, 
                standardize=True, adjust=True,
                tol=1e-5, max_iter=1e3):
        '''
            Solution Path of L0-Penalized Conquer

        Args:
            tau : quantile level between 0 and 1 (float).
            h : smoothing/bandwidth parameter (float).
            kernel : a character string representing one of the built-in smoothing kernels;
                     default is "Laplacian".
            sparsity_seq : a sequence of sparsity levels (int, >=1).
            order : a character string indicating the order of sparsity levels 
                    along which the solution path is obtained; default is 'ascend'.
            sparsity_max : maximum sparsity level (int, >=1).
            exp_size : expansion size (int, >=1); default is 5.
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            adjust : logical flag for returning coefficients on the original scale.
            tol : tolerance for convergence.
            max_iter : maximum number of iterations.

        Returns:
            'beta_seq' : a sequence of l0-conquer estimates;
                         each column corresponds to an estiamte for a sparsity level.
            'size_seq' : a sequence of numbers of selected variables.
            'bw_seq' : a sequence of bandwidths.
            'nit_seq' : a sequence of numbers of iterations.
        '''
        if len(sparsity_seq) == 0:
            sparsity_seq = np.array(range(1, sparsity_max+1))
            
        if order=='ascend':
            sparsity_seq = np.sort(sparsity_seq)
        elif order=='descend':
            sparsity_seq = np.sort(sparsity_seq)[::-1]
        L = len(sparsity_seq)

        if h is None: 
            h0 = np.minimum((sparsity_seq + np.log(self.n))/self.n, 0.5)
            h = np.maximum(0.01, h0 ** 0.4 * (tau-tau**2) ** 0.5)
        else:
            h = h * np.ones(L)

        beta_seq, nit_seq = np.zeros((self.X.shape[1], L+1)), []
        for k in range(L):
            model = self.l0(tau, h[k], kernel,
                            sparsity_seq[k], exp_size, beta_seq[:,k-1],
                            standardize, adjust, tol, max_iter)
            beta_seq[:,k] = model['beta']
            nit_seq.append(model['niter'])

        return {'beta_seq': beta_seq[:,:L],  
                'size_seq': np.sum(beta_seq[self.itcp:,:L] != 0, axis=0),
                'bw_seq': h,
                'nit_seq': np.array(nit_seq)}



##############################################################################
##### Use Cross-Validation to Choose the Regularization Parameter Lambda #####
##############################################################################
class cv_lambda():
    '''
        Cross-Validated Penalized Quantile Regression 
    '''
    penalties = ["L1", "SCAD", "MCP"]
    params = {'phi': 0.1, 'gamma': 1.25, 'warm_start': True, 
              'max_iter': 1e3, 'max_lr': 50,
              'tol': 1e-6, 'irw_tol': 1e-5, 'nsim': 200}
    methods = ['conquer', 'admm']


    def __init__(self, X, Y, intercept=True, options={}):
        self.n, self.p = X.shape
        self.X, self.Y = X, Y.reshape(self.n)
        self.itcp = intercept
        self.params.update(options)


    def divide_sample(self, nfolds=5):
        '''
            Divide the Sample into V=nfolds Folds
        '''
        idx, folds = np.arange(self.n), []
        for v in range(nfolds):
            folds.append(idx[v::nfolds])
        return idx, folds


    def fit(self, tau=0.5, h=None, kernel="Laplacian", 
            lambda_seq=np.array([]), nlambda=40, order='descend',
            nfolds=5, penalty="SCAD", a=3.7, nstep=3,
            method='conquer', standardize=True, adjust=True,
            sigma=0.01, eta=None, smoothed_criterion=False):

        if method not in self.methods: 
            raise ValueError("method must be either conquer or admm")
        if penalty not in self.penalties: 
            raise ValueError("penalty must be either L1, SCAD or MCP")

        init = high_dim(self.X, self.Y, self.itcp, self.params)
        if h is None: h = init.bandwidth(tau)
        itcp = self.itcp

        if not lambda_seq.any():
            lam_max = max(init.self_tuning(tau, standardize))
            lambda_seq = np.linspace(0.25*lam_max, lam_max, num=nlambda)

        else:
            nlambda = len(lambda_seq)
        
        # empirical check loss
        check = lambda x : np.mean(np.where(x >= 0, tau * x, (tau - 1)*x))   
        idx, folds = self.divide_sample(nfolds)
        val_err = np.zeros((nfolds, nlambda))
        for v in range(nfolds):
            X_train = self.X[np.setdiff1d(idx,folds[v]),:] 
            Y_train = self.Y[np.setdiff1d(idx,folds[v])]
            X_val, Y_val = self.X[folds[v],:], self.Y[folds[v]]

            if method == 'conquer':
                train = high_dim(X_train, Y_train, itcp, self.params)
            elif method == 'admm':
                train = pADMM(X_train, Y_train, itcp)

            if penalty == "L1":
                if method == 'conquer':
                    model = train.l1_path(tau, lambda_seq, nlambda, order,
                                          h, kernel, standardize, adjust)
                elif method == 'admm':
                    model = train.l1_path(tau, lambda_seq, nlambda, order, 
                                          sigma=sigma, eta=eta)
            else:
                if method == 'conquer':
                    model = train.irw_path(tau, lambda_seq, nlambda, order,
                                           h, kernel, penalty, a, nstep, 
                                           standardize, adjust)
                elif method == 'admm':
                    model = train.irw_path(tau, lambda_seq, nlambda, order,
                                           sigma=sigma, eta=eta,
                                           penalty=penalty, a=a, nstep=nstep)
            
            if not smoothed_criterion:
                val_err[v,:] \
                    = np.array([check(Y_val - model['beta_seq'][0,l]*itcp 
                                      - X_val@(model['beta_seq'][itcp:,l]))
                                      for l in range(nlambda)])
            else:
                val_err[v,:] \
                    = np.array([smooth_check(Y_val - model['beta_seq'][0,l]*itcp
                                             - X_val@(model['beta_seq'][itcp:,l]),
                                             tau, h, kernel)
                                             for l in range(nlambda)])

        
        cv_err = np.mean(val_err, axis=0)
        cv_min = min(cv_err)
        lambda_min = model['lambda_seq'][np.argmin(cv_err)]

        if penalty == "L1":
            if method == 'conquer':
                cv_model = init.l1(tau, lambda_min, h, kernel,
                                   standardize=standardize, adjust=adjust)
            elif method == 'admm':
                init = pADMM(self.X, self.Y, itcp)
                cv_model = init.l1(tau, lambda_min, sigma=sigma, eta=eta)
        else:
            if method == 'conquer':
                cv_model = init.irw(tau, lambda_min, h, kernel,
                                    penalty=penalty, a=a, nstep=nstep,
                                    standardize=standardize, adjust=adjust)
            elif method == 'admm':
                init = pADMM(self.X, self.Y, itcp)
                cv_model = init.irw(tau, lambda_min, sigma=sigma, eta=eta,
                                    penalty=penalty, a=a, nstep=nstep)

        return {'cv_beta': cv_model['beta'],
                'cv_res': cv_model['res'],
                'lambda_min': lambda_min,
                'lambda_seq': model['lambda_seq'],
                'min_cv_err': cv_min,
                'cv_err': cv_err}


##############################################################################
###### Use Validation Set to Choose the Regularization Parameter Lambda ######
##############################################################################
class validate_lambda(cv_lambda):
    '''
        Train Penalized Conquer on a Validation Set
    '''
    penalties = ["L1", "SCAD", "MCP"]
    

    def __init__(self, X_train, Y_train, X_val, Y_val, 
                 intercept=True, options={}):
        self.n, self.p = X_train.shape
        self.X_train, self.Y_train = X_train, Y_train.reshape(self.n)
        self.X_val, self.Y_val = X_val, Y_val.reshape(len(Y_val))
        self.itcp = intercept
        self.params.update(options)


    def train(self, tau=0.5, h=None, kernel="Laplacian", 
              lambda_seq=np.array([]), nlambda=20, order='descend', 
              penalty="SCAD", a=3.7, nstep=3, standardize=True):
        '''
        Args:
            tau : quantile level between 0 and 1 (float).
            h : smoothing/bandwidth parameter (float).
            kernel : a character string representing one of the built-in smoothing kernels;
                     default is "Laplacian".
            lambda_seq : an ndarray of lambda values (int).
            nlambda : number of lambda values.
            order : a character string indicating the order of lambda values
                    along which the solution path is obtained; default is 'descend'.
            penalty : a character string representing one of the built-in concave penalties;
                      default is "SCAD".
            a : the constant (>2) in the concave penality; default is 3.7.
            nstep : number of iterations/steps of the IRW algorithm; default is 3.
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
        
        Returns:
            'val_beta' : an ndarray of regression estimates. 
            'val_res' : an ndarray of fitted residuals.
            'model_size' : a sequence of selected model sizes.
            'lambda_min' : the value of lambda that gives minimum validation error.
            'lambda_seq' : a sequence of lambdas in descending order. 
            'val_min' : minimum validation error.
            'val_seq' : a sequence of validation errors.
        '''
  
        train = high_dim(self.X_train, self.Y_train,
                         intercept=self.itcp, options=self.params)
        if not lambda_seq.any():
            lam_max = max(train.self_tuning(tau, standardize))
            lambda_seq = np.linspace(0.25*lam_max, lam_max, num=nlambda)
        else:
            nlambda = len(lambda_seq)
            
        if h is None: h = train.bandwidth(tau)

        if penalty not in self.penalties:
            raise ValueError("penalty must be either L1, SCAD or MCP")
        elif penalty == "L1":
            model = train.l1_path(tau, lambda_seq, nlambda, order,
                                  h, kernel, standardize)
        else:
            model = train.irw_path(tau, lambda_seq, nlambda, order,
                                   h, kernel, penalty, a, nstep, standardize)
        
        # empirical check loss
        loss = lambda x : np.mean(np.where(x >= 0, tau * x, (tau - 1)*x))   
        val_err = \
                np.array([loss(self.Y_val - model['beta_seq'][0,l]*self.itcp 
                               - self.X_val@(model['beta_seq'][self.itcp:,l]))
                               for l in range(nlambda)])
        val_min = min(val_err)
        l_min = np.where(val_err==val_min)[0][0]

        return {'val_beta': model['beta_seq'][:,l_min],
                'val_res': model['res_seq'][:,l_min],
                'val_size': model['size_seq'][l_min],
                'lambda_min': model['lambda_seq'][l_min],
                'lambda_seq': model['lambda_seq'],
                'min_val_err': val_min, 'val_err': val_err}




###############################################################################
###########################    Helper Functions    ############################
###############################################################################
def prox_map(x, tau, alpha):
    return x - np.maximum((tau - 1)/alpha, np.minimum(x, tau/alpha))


###############################################################################
###################    proximal ADMM for Penalized QR    ######################
###############################################################################
class pADMM(high_dim):
    '''
        pADMM: proximal ADMM algorithm for solving 
               weighted L1-penalized quantile regression

    Refs:
        ADMM for high-dimensional sparse penalized quantile regression
        by Yuwen Gu, Jun Fan, Lingchen Kong, Shiqian Ma and Hui Zou
        Technometrics 60(3): 319--331, 2018
    '''
    opt = {'gamma': 1, 'max_iter': 5e3, 'tol': 1e-5, 'nsim': 200}

    def __init__(self, X, Y, intercept=True, options={}):
        '''
        Args:
            X : n by p matrix of covariates; each row is an observation vector.
            Y : n-dimensional vector of response variables.
            intercept : logical flag for adding an intercept to the model.
            options : a dictionary of internal optimization parameters.
                gamma : constant step length for the theta-step; default is 1.
                max_iter : maximum numder of iterations; default is 5e3.
                tol : tolerance level in the ADMM convergence criterion; default is 1e-5.
                nsim : number of simulations for computing a data-driven lambda; 
                       default is 200.
        '''

        self.n = len(Y)
        self.Y = Y.reshape(self.n)
        self.itcp = intercept
        self.X = np.c_[np.ones(self.n), X] if intercept else X
        self.params.update(options)


    def _eta(self):
        return np.linalg.svd(self.X, compute_uv=0).max()**2


    def l1(self, tau=0.5, Lambda=0.1, beta=np.array([]), 
           res=np.array([]), sigma=0.01, eta=None):
        '''
            Weighted L1-Penalized Quantile Regression
        
        Args:
            tau : quantile level (between 0 and 1); default is 0.5.
            Lambda : regularization parameter. This should be either a scalar, or
                     a vector of length equal to the column dimension of X.
            beta : initial estimator of slope coefficients;
                   if unspecified, it will be set as zero.
            res : residual vector of the initial estiamtor.
            sigma : augmentation parameter; default is 0.01.
            eta :  a positive parameter;
                   if unspecifed, it will be set as the largest eigenvalue of X'X.
        
        Returns:
            'beta' : an ndarray of estimated coefficients.
            'res' : an ndarray of fitted residuals.
            'lambda' : regularization parameter.
        '''

        n, dim = self.n, self.X.shape[1]
        if not beta.any(): 
            beta, res = np.zeros(dim), self.Y
        z, theta = res, np.ones(n)/n
        if eta is None: eta = self._eta()

        if self.itcp:
            Lambda = np.insert(Lambda * np.ones(dim-1), 0, 0)

        k, dev = 0, 1
        while dev > self.params['tol'] and k < self.params['max_iter']:
            beta_new = soft_thresh(beta+self.X.T@(theta/sigma + res - z)/eta,
                                   Lambda / sigma / eta)
            res = self.Y - self.X@(beta_new)
            z = prox_map(res + theta/sigma, tau, n * sigma)
            theta = theta - self.params['gamma'] * sigma * (z - res)
            dev = max(abs(beta_new - beta))
            beta = beta_new
            k += 1

        return {'beta': beta, 
                'res': res,
                'niter': k, 
                'theta': theta,
                'lambda': Lambda}


    def l1_path(self, tau=0.5, lambda_seq=np.array([]), nlambda=50,
                order="descend", sigma=0.1, eta=None):
        '''
            Solution Path of L1-Penalized Quantile Regression

        Args:
            tau : quantile level (between 0 and 1); default is 0.5.
            lambda_seq : an ndarray of lambda values (regularization parameters).
            nlambda : number of lambda values.
            order : a character string indicating the order of lambda values along
                    which the solution path is obtained; default is 'descend'.
            sigma : augmentation parameter; default is 0.01.
            eta :  a positive parameter;
                   if unspecifed, it will be set as the largest eigenvalue of X'X.

        Returns:
            'beta_seq' : a sequence of l1 estimates.
            'res_seq' : a sequence of residual vectors.
            'size_seq' : a sequence of numbers of selected variables.
            'lambda_seq' : a sequence of lambda values in ascending/descending order.
        '''
 
        if len(lambda_seq) == 0:
            lam_max = max(self.self_tuning(tau, standardize=False))
            lambda_seq = np.linspace(0.25*lam_max, lam_max, num=nlambda)
        
        if order == 'ascend':
            lambda_seq = np.sort(lambda_seq)
        elif order == 'descend':
            lambda_seq = np.sort(lambda_seq)[::-1]
        nlambda = len(lambda_seq)
        
        if eta is None: eta = self._eta()

        beta_seq = np.zeros(shape=(self.X.shape[1], nlambda))
        res_seq = np.zeros(shape=(self.n, nlambda))
        niter_seq = np.ones(nlambda)
        model = self.l1(tau, lambda_seq[0], sigma=sigma, eta=eta)
        beta_seq[:,0], res_seq[:,0] = model['beta'], model['res']
        niter_seq[0] = model['niter']
        
        for l in range(1, nlambda):
            model = self.l1(tau, lambda_seq[l], beta_seq[:,l-1], 
                            res_seq[:,l-1], sigma=sigma, eta=eta)
            beta_seq[:,l], res_seq[:,l] = model['beta'], model['res']
            niter_seq[l] = model['niter']

        return {'beta_seq': beta_seq, 
                'res_seq': res_seq,
                'size_seq': np.sum(beta_seq[self.itcp:,:] != 0, axis=0),
                'lambda_seq': lambda_seq,
                'niter_seq': niter_seq}


    def irw(self, tau=0.5, Lambda=0.1, beta=np.array([]), res=np.array([]), 
            sigma=0.01, eta=None, penalty="SCAD", a=3.7, nstep=3):
        '''
            Iteratively Reweighted L1-Penalized Quantile Regression

        Arguments
        ---------
        tau : quantile level (between 0 and 1); default is 0.5.

        Lambda : regularization parameter. This should be either a scalar, or
                 a vector of length equal to the column dimension of X.

        beta : initial estimate of slope coefficients. 
               If unspecified, it will be set as zero.

        res : residual vector of the initial estiamtor.

        sigma : augmentation parameter; default is 0.01.

        eta :  a positive parameter; 
               if unspecifed, it will be set as the largest eigenvalue of X'X.

        penalty : a character string representing one of the built-in concave penalties; 
                  default is "SCAD".
        
        a : the constant (>2) in the concave penality; default is 3.7.
        
        nstep : number of iterations/steps of the IRW algorithm; default is 3.

        Returns
        -------
        'beta' : an ndarray of estimated coefficients.
        
        'res' : an ndarray of fitted residuals.

        'lambda' : regularization parameter.
        '''
        if not beta.any():
            model = self.l1(tau, Lambda, sigma=sigma, eta=eta)
        else:
            res = self.Y - self.X.dot(beta)
            model = self.l1(tau, Lambda, beta, res, sigma, eta)
        beta, res = model['beta'], model['res']
        lam = np.ones(self.X.shape[1] - self.itcp) * Lambda
        pos = lam > 0
        rw_lam = np.zeros(self.X.shape[1] - self.itcp)

        if eta is None: eta = self._eta()

        err, t = 1, 1
        while err > self.params['tol'] and t <= nstep:
            rw_lam[pos] = lam[pos] \
                          * concave_weight(beta[self.itcp:][pos]/lam[pos],
                                           penalty, a)
            model = self.l1(tau, rw_lam, beta, res, sigma=sigma, eta=eta)
            err = max(abs(model['beta']-beta))
            beta, res = model['beta'], model['res']
            t += 1
            
        return {'beta': beta, 
                'res': res, 
                'nstep': t, 
                'lambda': lam}


    def irw_path(self, tau=0.5, lambda_seq=np.array([]), nlambda=50, 
                 order="descend", sigma=0.1, eta=None, 
                 penalty="SCAD", a=3.7, nstep=3):
        '''
            Solution Path of IRW-L1-Penalized Quantile Regression

        Returns:
            'beta_seq' : a sequence of irw estimates.
            'res_seq' : a sequence of residual vectors.
            'size_seq' : a sequence of numbers of selected variables.
            'lambda_seq' : a sequence of lambda values in ascending/descending order.
        '''

        if order == 'ascend':
            lambda_seq = np.sort(lambda_seq)
        elif order == 'descend':
            lambda_seq = np.sort(lambda_seq)[::-1]
        nlambda = len(lambda_seq)

        if eta is None: eta = self._eta()

        beta_seq = np.zeros(shape=(self.X.shape[1], nlambda))
        res_seq = np.zeros(shape=(self.n, nlambda))
        model = self.irw(tau, lambda_seq[0], sigma=sigma, eta=eta, 
                         penalty=penalty, a=a, nstep=nstep)
        beta_seq[:,0], res_seq[:,0] = model['beta'], model['res']

        for l in range(1, nlambda):
            model = self.irw(tau, lambda_seq[l], beta_seq[:,l-1], 
                             res_seq[:,l-1], sigma, eta, penalty, a, nstep)
            beta_seq[:,l], res_seq[:,l] = model['beta'], model['res']

        return {'beta_seq': beta_seq,
                'res_seq': res_seq,
                'size_seq': np.sum(beta_seq[self.itcp:,:] != 0, axis=0),
                'lambda_seq': lambda_seq}



###############################################################################
###########################    Helper Functions    ############################
###############################################################################
def smooth_composite_check(x, alpha=np.array([]), tau=np.array([]), 
                           h=None, kernel='Laplacian', w=np.array([])):
    out = np.array([smooth_check(x - alpha[i], tau[i], h, kernel, w)
                    for i in range(len(tau))])
    return np.mean(out)


def composite_check_sum(x, tau, alpha):
    out = 0
    for i in range(0, len(tau)):
        out += np.sum(np.where(x - alpha[i] >= 0, 
                               tau[i] * (x - alpha[i]),
                               (tau[i] - 1) * (x - alpha[i])))
    return out / len(tau)
    

###############################################################################
############################ Penalized Composite QR ###########################
###############################################################################
class composite(high_dim):
    '''
        Penalized Composite Quantile Regression

    Refs:
        Sparse composite quantile regression in utrahigh dimensions 
        with tuning parameter calibration 
        by Yuwen Gu and Hui Zou
        IEEE Transactions on Information Theory 66(11): 7132-7154, 2020

        High-dimensional composite quantile regression: 
        optimal statistical guarantees and fast algorithms 
        by Haeseong Moon and Wen-Xin Zhou
        Electronic Journal of Statistics 17(2): 2067-2119, 2023
    '''
    params = {'phi': 0.1, 'gamma': 1.25, 'max_iter': 1e3, 'tol': 1e-5,
              'iter_warning': True, 'irw_tol': 1e-5, 'nsim': 200, 
              'min_bandwidth': 1e-4}

    def __init__(self, X, Y, options={}):
        self.n, self.p = X.shape
        self.X, self.Y = X, Y.reshape(self.n)
        self.mX, self.sdX = np.mean(X, axis=0), np.std(X, axis=0)
        self.X1 = (X - self.mX)/self.sdX
        self.params.update(options)


    def tau_grid(self, K=9):
        return np.linspace(1/(K+1), K/(K+1), K)
    

    def composite_weight(self, x, alpha=np.array([]), tau=np.array([]), 
                         h=None, kernel="Laplacian", w=np.array([])):
        out = conquer_weight((alpha[0] - x) / h, tau[0], kernel, w)
        for i in range(1, len(tau)):
            out = np.hstack((out, conquer_weight((alpha[i]-x)/h, tau[i], kernel, w)))
        return out / (len(tau) * self.n)


    def uniform_weights(self, tau=np.array([])):
        weight = (rgt.uniform(0, 1, self.n) <= tau[0]) - tau[0]
        for i in range(1, len(tau)):
            weight = np.hstack((weight, (rgt.uniform(0, 1, self.n) <= tau[i]) - tau[i]))
        return weight


    def lambda_tuning(self, XX, tau=np.array([])):
        lambda_sim = np.array([max(abs(XX.dot(self.uniform_weights(tau)))) \
                               for _ in range(self.params['nsim'])])
        return lambda_sim / (len(tau) * self.n)


    def l1(self, tau=np.array([]), K=9, Lambda=np.array([]),
           h=None, kernel="Laplacian", 
           alpha0=np.array([]), beta0=np.array([]), res=np.array([]), 
           standardize=True, adjust=True, weight=np.array([]), c=1.5):
        '''
           L1-Penalized Composite Quantile Regression via Convolution Smoothing
           (l1-composite-conquer)

        Args:
            tau : an ndarray of quantile levels (between 0 and 1);
                  default is {0.1, 0.2, ..., 0.9}.
            K : number of tau values; default = 9.
            Lambda : regularization parameter. This should be either a scalar, or
                     a vector of length equal to the column dimension of X. If unspecified,
                     it will be computed by lambda_tuning().
            h : bandwidth/smoothing parameter. The default is computed by self.bandwidth().
            kernel : a character string representing one of the built-in smoothing kernels; 
                     default is "Laplacian".
            beta0 : initial estimator of slope coefficients; 
                    if unspecified, it will be set to zero.
            alpha0 : initial estimator of intercept terms in CQR regression (alpha terms);
                     if unspecified, it will be set as zero.
            res : residual vector of the initial estiamtor.
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            adjust : logical flag for returning coefficients on the original scale.
            weight : an ndarray of observation weights; default is np.array([]) (empty).

        Returns:
            'alpha': an ndarray of estimated coefficients for intercept terms.
            'beta' : an ndarray of estimated coefficients for slope coefficients.
            'res' : an ndarray of fitted residuals.
            'niter' : number of iterations.
            'lambda' : lambda value.
            'bw' : bandwidth.
        '''

        if not np.array(tau).any(): 
            tau = self.tau_grid(K)
        K = len(tau)
        X = self.X1 if standardize else self.X
        XX = np.tile(X.T, K)

        if not np.array(Lambda).any():
            Lambda = c * np.quantile(self.lambda_tuning(XX, tau), 0.95)
        
        if h is None: h = self.bandwidth(np.mean(tau))

        if len(beta0)==0: beta0 = np.zeros(self.p)

        if len(alpha0)==0: alpha0 = np.zeros(K)

        res = self.Y - X.dot(beta0)

        alphaX = np.zeros((K, self.n * K))
        for i in range(0, K):
            for j in range(i * self.n, (i + 1) * self.n):
                alphaX[i, j] = 1

        phi, dev, count = self.params['phi'], 1, 0
        while dev > self.params['tol'] and count < self.params['max_iter']:

            gradalpha0 = alphaX.dot(self.composite_weight(res, alpha0, tau, h, kernel, w=weight))
            gradbeta0 = XX.dot(self.composite_weight(res, alpha0, tau, h, kernel, w=weight))
            loss_eval0 = smooth_composite_check(res, alpha0, tau, h, kernel, weight)
            alpha1 = alpha0 - gradalpha0 / phi
            beta1 = beta0 - gradbeta0 / phi
            beta1 = soft_thresh(beta1, Lambda / phi)
            diff_alpha = alpha1 - alpha0
            diff_beta = beta1 - beta0
            r0 = diff_beta.dot(diff_beta) + diff_alpha.dot(diff_alpha)
            res = self.Y - X.dot(beta1)
            loss_proxy = loss_eval0 + diff_beta.dot(gradbeta0) \
                         + diff_alpha.dot(gradalpha0) + 0.5 * phi * r0
            loss_eval1 = smooth_composite_check(res, alpha1, tau, h, kernel, weight)

            while loss_proxy < loss_eval1:
                phi *= self.params['gamma']
                alpha1 = alpha0 - gradalpha0 / phi
                beta1 = beta0 - gradbeta0 / phi
                beta1 = soft_thresh(beta1, Lambda / phi)
                diff_alpha = alpha1 - alpha0
                diff_beta = beta1 - beta0
                r0 = diff_beta.dot(diff_beta) + diff_alpha.dot(diff_alpha)
                res = self.Y - X.dot(beta1)
                loss_proxy = loss_eval0 + diff_beta.dot(gradbeta0) \
                             + diff_alpha.dot(gradalpha0) + 0.5 * phi * r0
                loss_eval1 = smooth_composite_check(res, alpha1, tau, h, kernel, weight)

            dev = max(abs(beta1 - beta0)) + max(abs(alpha1 - alpha0))
            alpha0, beta0, phi = np.copy(alpha1), np.copy(beta1), self.params['phi']
            count += 1

        if standardize and adjust:
            beta1 /= self.sdX

        return {'alpha': alpha1, 
                'beta': beta1, 
                'res': res,
                'niter': count, 
                'lambda': Lambda, 
                'bw': h}


    def irw(self, tau=np.array([]), K=9, Lambda=None, 
            h=None, kernel="Laplacian", 
            alpha0=np.array([]), beta0=np.array([]), res=np.array([]),
            penalty="SCAD", a=3.7, nstep=3, standardize=True, adjust=True, 
            weight=np.array([]), c=2):
        '''
            Iteratively Reweighted L1-Penalized Composite Conquer

        Args:
            tau : an ndarray of quantile levels (between 0 and 1);
                  default is {0.1, 0.2, ..., 0.9}.
            K : number of tau values; default = 9.
            Lambda : regularization parameter. This should be either a scalar, or
                     a vector of length equal to the column dimension of X. If unspecified,
                     it will be computed by lambda_tuning().
            h : bandwidth/smoothing parameter. The default is computed by self.bandwidth().
            kernel : a character string representing one of the built-in smoothing kernels; 
                     default is "Laplacian".
            beta0 : initial estimator of slope coefficients;
                    if unspecified, it will be set to zero.
            alpha0 : initial estimator of intercept terms in CQR regression (alpha terms);
                     if unspecified, it will be set as zero.
            res : residual vector of the initial estiamtor.
            penalty : a character string representing one of the built-in concave penalties; 
                      default is "SCAD".
            a : the constant (>2) in the concave penality; default is 3.7.
            nstep : number of iterations/steps of the IRW algorithm; default is 3.
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            adjust : logical flag for returning coefficients on the original scale.
            weight : an ndarray of observation weights; default is np.array([]) (empty).

        Returns:
            'alpha': an ndarray of estimated coefficients for intercept terms.
            'beta' : an ndarray of estimated coefficients for slope coefficients.
            'res' : an ndarray of fitted residuals.
            'niter' : number of iterations.
            'lambda' : lambda value.
            'bw' : bandwidth.
        '''

        if not np.array(tau).any(): tau = self.tau_grid(K)
        K = len(tau)
        X = self.X1 if standardize else self.X

        if Lambda is None:
            Lambda = c * np.quantile(self.lambda_tuning(np.tile(X.T, K), tau), 
                                     0.95)
        if h is None: h = self.bandwidth(np.mean(tau))

        if len(beta0) == 0:
            model = self.l1(tau, K, Lambda, h, kernel,
                            alpha0=np.zeros(K), beta0=np.zeros(self.p),
                            standardize=standardize, adjust=False, 
                            weight=weight)
        else:
            model = self.l1(tau, K, Lambda, h, kernel=kernel,
                            alpha0=alpha0, beta0=beta0, res=res,
                            standardize=standardize, adjust=False, 
                            weight=weight)
        alpha0, beta0, res = model['alpha'], model['beta'], model['res']
        nit = []
        nit.append(model['niter'])

        if penalty == 'L1': nstep == 0
        dev, step = 1, 1
        while dev > self.params['irw_tol'] and step <= nstep:
            rw_lambda = Lambda * concave_weight(beta0 / Lambda, penalty, a)
            model = self.l1(tau, K, rw_lambda, h, kernel, alpha0, beta0, res,
                            standardize, adjust=False, weight=weight)
            dev = max(abs(model['beta'] - beta0)) \
                  + max(abs(model['alpha'] - alpha0))
            alpha0, beta0, res = model['alpha'], model['beta'], model['res']
            step += 1
            nit.append(model['niter'])

        if standardize and adjust:
            beta0 /= self.sdX
        nit_seq = np.array(nit)

        return {'alpha': alpha0, 
                'beta': beta0, 
                'res': res,
                'h': h, 
                'lambda': Lambda,
                'nstep': step, 
                'niter': np.sum(nit_seq),
                'nit_seq': nit_seq}


    def l1_path(self, tau=np.array([]), K=9, 
                lambda_seq=np.array([]), nlambda=40, order="descend", 
                h=None, kernel="Laplacian", 
                standardize=True, adjust=True):
        '''
            Solution Path of L1-Penalized Composite Conquer

        Args:
            tau : an ndarray of quantile levels (between 0 and 1);
                  default is {0.1, 0.2, ..., 0.9}.
            K : number of tau values; default = 9.
            lambda_seq : an ndarray of lambda values (regularization parameters).
            nlambda : number of lambda values.
            order : a character string indicating the order of lambda values along
                    which the solution path is obtained; default is 'descend'.
            h : bandwidth/smoothing parameter. The default is computed by self.bandwidth().
            kernel : a character string representing one of the built-in smoothing kernels; 
                     default is "Laplacian".
            standardize : logical flag for x variable standardization prior to fitting the model;
                          default is TRUE.
            adjust : logical flag for returning coefficients on the original scale.
        
        Returns:
            'alpha_seq' : a sequence of l1-composite-conquer estimates for intercept terms.
            'beta_seq' : a sequence of l1-composite-conquer estimates for slope coefficients.
            'res_seq' : a sequence of residual vectors.
            'size_seq' : a sequence of numbers of selected variables.
            'lambda_seq' : a sequence of lambda values in ascending/descending order.
            'bw' : bandwidth.
        '''

        if not np.array(tau).any(): tau = self.tau_grid(K)
        K = len(tau)
        
        if not lambda_seq.any():
            X = self.X1 if standardize else self.X
            lambda_sim = self.lambda_tuning(np.tile(X.T, len(tau)), tau)
            lambda_seq = np.linspace(np.min(lambda_sim), 2*max(lambda_sim), 
                                     num=nlambda)
        
        if h is None: h = self.bandwidth(np.mean(tau))

        if order == 'ascend':
            lambda_seq = np.sort(lambda_seq)
        elif order == 'descend':
            lambda_seq = np.sort(lambda_seq)[::-1]

        nit_seq = []
        alpha_seq = np.zeros(shape=(len(tau), len(lambda_seq)))
        beta_seq = np.zeros(shape=(self.p, len(lambda_seq)))
        res_seq = np.zeros(shape=(self.n, len(lambda_seq)))
        model = self.l1(tau, K, lambda_seq[0], h, kernel,
                        standardize=standardize, adjust=False)
        alpha_seq[:,0], beta_seq[:,0], res_seq[:,0] \
            = model['alpha'], model['beta'], model['res']
        nit_seq.append(model['niter'])

        for l in range(1, len(lambda_seq)):
            model = self.l1(tau, K, lambda_seq[l], h, kernel,
                            alpha_seq[:, l-1], beta_seq[:, l-1],
                            res_seq[:, l - 1], standardize, adjust=False)
            beta_seq[:, l], res_seq[:, l] = model['beta'], model['res']
            nit_seq.append(model['niter'])

        if standardize and adjust:
            beta_seq[:, ] /= self.sdX[:, None]

        return {'alpha_seq': alpha_seq, 
                'beta_seq': beta_seq, 
                'res_seq': res_seq,
                'size_seq': np.sum(beta_seq != 0, axis=0),
                'lambda_seq': lambda_seq,
                'nit_seq': np.array(nit_seq), 
                'bw': h}


    def irw_path(self, tau=np.array([]), K=9,
                 lambda_seq=np.array([]), nlambda=40, order="descend",
                 h=None, kernel="Laplacian", 
                 penalty="SCAD", a=3.7, nstep=3,
                 standardize=True, adjust=True):
        '''
            Solution Path of Iteratively Reweighted L1-Penalized Composite Conquer
        '''
        if not np.array(tau).any(): tau = self.tau_grid(K)
        K = len(tau)
        
        if not lambda_seq.any():
            if standardize: X = self.X1
            else: X = self.X
            lambda_sim = self.lambda_tuning(np.tile(X.T, len(tau)), tau)
            lambda_seq = np.linspace(0.75*max(lambda_sim), 2*max(lambda_sim), 
                                     num=nlambda)
        
        if h is None: h = self.bandwidth(np.mean(tau))

        if order == 'ascend':
            lambda_seq = np.sort(lambda_seq)
        elif order == 'descend':
            lambda_seq = np.sort(lambda_seq)[::-1]

        if penalty == 'L1': nstep=0
        nit_seq = []
        alpha_seq = np.zeros(shape=(len(tau), len(lambda_seq)))
        beta_seq = np.zeros(shape=(self.p, len(lambda_seq)))
        res_seq = np.zeros(shape=(self.n, len(lambda_seq)))
        model = self.irw(tau, K, lambda_seq[0], h, kernel,
                         penalty=penalty, a=a, nstep=nstep,
                         standardize=standardize, adjust=False)
        alpha_seq[:,0], beta_seq[:,0], res_seq[:,0] \
            = model['alpha'], model['beta'], model['res']
        nit_seq.append(model['niter'])

        for l in range(1, len(lambda_seq)):
            model = self.irw(tau, K, lambda_seq[l], h, kernel,
                             alpha_seq[:, l-1], beta_seq[:, l-1], 
                             res_seq[:, l - 1],
                             penalty, a, nstep,
                             standardize, adjust=False)
            beta_seq[:, l], res_seq[:, l] = model['beta'], model['res']
            nit_seq.append(model['niter'])

        if standardize and adjust:
            beta_seq[:, ] /= self.sdX[:, None]

        return {'alpha_seq': alpha_seq, 
                'beta_seq': beta_seq,
                'res_seq': res_seq,
                'size_seq': np.sum(beta_seq != 0, axis=0),
                'lambda_seq': lambda_seq,
                'nit_seq': np.array(nit_seq),
                'bw': h}



class ncvxADMM():
    '''
        Nonconvex Penalized Quantile Regression via ADMM

    Refs:
        Convergence for nonconvex ADMM, with applications to CT imaging
        by Rina Foygel Barber and Emil Y. Sidky
        arXiv:2006.07278
    '''
    def __init__(self, X, Y, intercept=True):
        '''
        Args:
            X : n by p matrix of covariates; each row is an observation vector.
            Y : n-dimensional vector of response variables.
            intercept : logical flag for adding an intercept to the model.
        '''
        
        self.n = len(Y)
        self.Y = Y.reshape(self.n)
        self.itcp = intercept
        if intercept:
            self.X = np.c_[np.ones(self.n), X]
        else:
            self.X = X

    def loss(self, beta, tau=0.5, Lambda=0.1, c=1):
        return (np.maximum(self.Y - self.X.dot(beta), 0).sum()*tau \
                + np.maximum(self.X.dot(beta)-self.Y, 0).sum()*(1-tau)) / self.n \
                + Lambda * c * np.log(1 + np.abs(beta)/c).sum()

    def fit(self, tau=0.5, Lambda=0.1, c=1, 
            sig=0.0002, niter=5e3, tol=1e-5):
        '''
        Args:
            tau : quantile level; default is 0.5.
            Lambda : regularization parameter (float); default is 0.1.
            c : constant parameter in the penalty P_c(x) = c * log(1 + |x|/c); default = 1. 
                The penalty P_c(x) converges to |x| as c tends to infinity.
            sig : constant step length for the theta-step; default is 0.0002.
            niter : maximum numder of iterations; default is 5e3.
            tol : tolerance level in the ADMM convergence criterion; default is 1e-5.

        Returns:
            'beta' : penalized quantile regression estimate.
            'loss_val' : values of the penalized loss function at all iterates.
            'Lambda' : regularization parameter.
        '''

        gam = np.linalg.svd(self.X, compute_uv=0).max()**2
        loss_xt = np.zeros(np.int64(niter))
        loss_xtbar = np.zeros(np.int64(niter))
        beta_avg = np.zeros(self.X.shape[1])
        beta = np.zeros(self.X.shape[1])
        y = np.zeros(self.n)
        u = np.zeros(self.n)
        
        i, loss_diff = 0, 1e3
        while i < niter and loss_diff > tol:  
            beta = beta - self.X.T.dot(self.X.dot(beta))/gam + self.X.T.dot(y)/gam \
                   - self.X.T.dot(u)/sig/gam + Lambda * beta/(c+np.abs(beta))/sig/gam
            beta = np.sign(beta) * np.maximum(np.abs(beta)-Lambda/sig/gam, 0)
            y = self.X.dot(beta) + u/sig
            y = (y + tau/self.n/sig) * (y + tau/self.n/sig < self.Y) \
                + (y-(1-tau)/self.n/sig) * (y-(1-tau)/self.n/sig > self.Y) \
                + self.Y * (y + tau/self.n/sig >= self.Y) \
                    * (y - (1-tau)/self.n/sig <= self.Y)       
            u = u + sig * (self.X.dot(beta) - self.Y)
            beta_avg = beta_avg * (i/(i+1)) + beta * (1/(i+1))
            loss_xt[i] = self.loss(beta, tau, Lambda, c)
            loss_xtbar[i] = self.loss(beta_avg, tau, Lambda, c)
            if i >= 5:
                loss_diff = abs(loss_xt[i] - np.mean(loss_xt[i-5 : i]))
            i += 1

        return {'beta': beta, 
                'beta_avg': beta_avg, 
                'loss_val': loss_xt, 
                'Lambda': Lambda, 
                'niter': i}