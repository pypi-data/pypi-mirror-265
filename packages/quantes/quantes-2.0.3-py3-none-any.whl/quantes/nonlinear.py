import numpy as np

from scipy.optimize import minimize
from scipy.stats import norm
from scipy.sparse import csc_matrix
from sklearn.metrics import pairwise_kernels as PK
from sklearn.kernel_ridge import KernelRidge as KR

from qpsolvers import Problem, solve_problem


###############################################################################
########################## Kernel Ridge Regression ############################
###############################################################################
class KRR:
    '''
    Kernel Ridge Regression
    
    Methods:
        __init__(): Initialize the KRR object
        qt(): Fit (smoothed) quantile kernel ridge regression
        es(): Fit (robust) expected shortfall kernel ridge regression
        qt_seq(): Fit a sequence of quantile kernel ridge regressions
        qt_predict(): Compute predicted quantile at test data
        es_predict(): Compute predicted expected shortfall at test data
        qt_loss(): Check or smoothed check loss
        qt_grad(): Compute the (sub)gradient of the (smoothed) check loss
        bw(): Compute the bandwidth (smoothing parameter)
        genK(): Generate the kernel matrix for test data

    Attributes:
        params (dict): a dictionary of kernel parameters;
            gamma (float), default is 1;
            coef0 (float), default is 1;
            degree (int), default is 3.
            rbf : exp(-gamma*||x-y||_2^2)
            polynomial : (gamma*<x,y> + coef0)^degree
            laplacian : exp(-gamma*||x-y||_1)
    '''
    params = {'gamma': 1, 'coef0': 1, 'degree': 3}


    def __init__(self, X, Y, normalization=None, 
                 kernel='rbf', kernel_params=dict(),
                 smooth_method='convolution', 
                 min_bandwidth=1e-4, n_jobs=None):
        ''' 
        Initialize the KRR object

        Args:
            X (ndarray): n by p matrix of covariates;
                         n is the sample size, p is the number of covariates.
            Y (ndarray): response/target variable.
            normalization (str): method for normalizing covariates;
                                 should be one of [None, 'MinMax', 'Z-score'].
            kernel (str): type of kernel function; 
                          choose one from ['rbf', 'polynomial', 'laplacian'].
            kernel_params (dict): a dictionary of user-specified kernel parameters; 
                                  default is in the class attribute.
            smooth_method (str): method for smoothing the check loss;
                                 choose one from ['convolution', 'moreau'].
            min_bandwidth (float): minimum value of the bandwidth; default is 1e-4.
            n_jobs (int): the number of parallel jobs to run; default is None.

        Attributes:
            n (int) : number of observations
            Y (ndarray) : target variable
            nm (str) : method for normalizing covariates
            kernel (str) : type of kernel function
            params (dict) : a dictionary of kernel parameters
            X0 (ndarray) : normalized covariates
            xmin (ndarray) : minimum values of the original covariates
            xmax (ndarray) : maximum values of the original covariates
            xm (ndarray) : mean values of the original covariates
            xsd (ndarray) : standard deviations of the original covariates
            K (ndarray) : n by n kernel matrix
        '''

        self.n = X.shape[0]
        self.Y = Y.reshape(self.n)
        self.nm = normalization
        self.kernel = kernel
        self.params.update(kernel_params)

        if normalization is None:
            self.X0 = X[:]
        elif normalization == 'MinMax':
            self.xmin = np.min(X, axis=0)
            self.xmax = np.max(X, axis=0)
            self.X0 = (X[:] - self.xmin)/(self.xmax - self.xmin)
        elif normalization == 'Z-score':
            self.xm, self.xsd = np.mean(X, axis=0), np.std(X, axis=0)
            self.X0 = (X[:] - self.xm)/self.xsd
        
        self.min_bandwidth = min_bandwidth
        self.n_jobs = n_jobs
        self.smooth_method = smooth_method

        # compute the kernel matrix
        self.K = PK(self.X0, metric=kernel, filter_params=True,
                    n_jobs=self.n_jobs, **self.params)


    def genK(self, x):
        ''' Generate the kernel matrix for test data '''
        if np.ndim(x) == 1:
            x = x.reshape(1, -1)
        if self.nm == 'MinMax':
            x = (x - self.xmin)/(self.xmax - self.xmin)
        elif self.nm == 'Z-score':
            x = (x - self.xm)/self.xsd
        
        # return an n * m matrix, m is test data size
        return PK(self.X0, x, metric=self.kernel, 
                  filter_params=True, n_jobs=self.n_jobs, 
                  **self.params)


    def qt_loss(self, x, h=0):
        '''
        Check or smoothed check loss
        '''
        tau = self.tau
        if h == 0:
            out = np.where(x > 0, tau * x, (tau - 1) * x)
        elif self.smooth_method == 'convolution':
            out = (tau - norm.cdf(-x/h)) * x \
                  + (h/2) * np.sqrt(2/np.pi) * np.exp(-(x/h) ** 2 /2)
        elif self.smooth_method == 'moreau':
            out = np.where(x > tau*h, tau*x - tau**2 * h/2, 
                           np.where(x < (tau - 1)*h, 
                                    (tau - 1)*x - (tau - 1)**2 * h/2, 
                                    x**2/(2*h)))
        return np.sum(out)


    def qt_grad(self, x, h=0):
        '''
        Gradient/subgradient of the (smoothed) check loss
        '''
        if h == 0:
            return np.where(x >= 0, self.tau, self.tau - 1)
        elif self.smooth_method == 'convolution':
            return self.tau - norm.cdf(-x / h)
        elif self.smooth_method == 'moreau':
            return np.where(x > self.tau * h, self.tau, 
                            np.where(x < (self.tau - 1) * h, 
                                     self.tau - 1, x/h))


    def bw(self, exponent=1/3):
        '''
        Compute the bandwidth (smoothing parameter)

        Args: 
            exponent (float): the exponent in the formula; default is 1/3.
        '''
        krr = KR(alpha = 1, kernel=self.kernel,
                 gamma = self.params['gamma'],
                 degree = self.params['degree'],
                 coef0 = self.params['coef0'])
        krr.fit(self.X0, self.Y)
        krr_res = self.Y - krr.predict(self.X0)
        return max(self.min_bandwidth, 
                   np.std(krr_res)/self.n ** exponent)


    def qt(self, tau=0.5, alpha_q=1, 
           init=None, intercept=True, 
           smooth=False, h=0., method='L-BFGS-B', 
           solver='clarabel', tol=1e-7, options=None):
        '''
        Fit (smoothed) quantile kernel ridge regression

        Args:
            tau (float): quantile level between 0 and 1; default is 0.5.
            alpha_q (float): regularization parameter; default is 1.
            init (ndarray): initial values for optimization; default is None.
            intercept (bool): whether to include intercept term; 
                              default is True.
            smooth (bool): a logical flag for using smoothed check loss; 
                           default is FALSE.
            h (float): bandwidth for smoothing; default is 0.
            method (str): type of solver if smoothing (h>0) is used;
                          choose one from ['BFGS', 'L-BFGS-B'].
            solver (str): type of QP solver if check loss is used; 
                          default is 'clarabel'.
            tol (float): tolerance for termination; default is 1e-7.
            options (dict): a dictionary of solver options; default is None.
        
        Attributes:
            qt_sol (OptimizeResult): solution of the optimization problem
            qt_beta (ndarray): quantile KRR coefficients
            qt_fit (ndarray): fitted quantiles (in-sample)
        '''
        self.alpha_q, self.tau, self.itcp_q = alpha_q, tau, intercept
        if smooth and h == 0: 
            h = self.bw()
        n, self.h = self.n, h

        # compute smoothed quantile KRR estimator with bandwidth h
        if self.h > 0: 
            if intercept:
                x0 = init if init is not None else np.zeros(n + 1)
                x0[0] = np.quantile(self.Y, tau)
                res = lambda x: self.Y - x[0] - self.K @ x[1:]
                func = lambda x: self.qt_loss(res(x),h) + \
                                 (alpha_q/2) * np.dot(x[1:], self.K @ x[1:])
                grad = lambda x: np.insert(-self.K @ self.qt_grad(res(x),h) 
                                           + alpha_q*self.K @ x[1:], 
                                           0, np.sum(-self.qt_grad(res(x),h)))
                self.qt_sol = minimize(func, x0, method=method, 
                                       jac=grad, tol=tol, options=options)
                self.qt_beta = self.qt_sol.x
                self.qt_fit = self.qt_beta[0] + self.K @ self.qt_beta[1:]
            else:
                x0 = init if init is not None else np.zeros(n)
                res = lambda x: self.Y - self.K @ x
                func = lambda x: self.qt_loss(res(x), h) \
                                 + (alpha_q/2) * np.dot(x, self.K @ x)
                grad = lambda x: -self.K @ self.qt_grad(res(x), h) \
                                 + alpha_q * self.K @ x
                self.qt_sol = minimize(func, x0=x0, method=method, 
                                       jac=grad, tol=tol, options=options)
                self.qt_beta = self.qt_sol.x
                self.qt_fit = self.K @ self.qt_beta
        else: 
            # fit quantile KRR by solving a quadratic program
            C = 1 / alpha_q
            lb = C * (tau - 1)
            ub = C * tau
            prob = Problem(P=csc_matrix(self.K), q=-self.Y, G=None, h=None, 
                           A=csc_matrix(np.ones(n)), b=np.array([0.]), 
                           lb=lb * np.ones(n), ub=ub * np.ones(n))
            self.qt_sol = solve_problem(prob, solver=solver)
            self.itcp_q = True
            self.qt_fit = self.K @ self.qt_sol.x
            b = np.quantile(self.Y - self.qt_fit, tau)
            self.qt_beta = np.insert(self.qt_sol.x, 0, b)
            self.qt_fit += b


    def qt_seq(self, tau=0.5, alphaseq=np.array([0.1]), 
               intercept=True, smooth=False, h=0., 
               method='L-BFGS-B', solver='clarabel', 
               tol=1e-7, options=None):
        '''
        Fit a sequence of (smoothed) quantile kernel ridge regressions
        '''
        alphaseq = np.sort(alphaseq)[::-1]
        args = [intercept, smooth, h, method, solver, tol, options]

        x0 = None
        x, fit = [], []
        for alpha_q in alphaseq:
            self.qt(tau, alpha_q, x0, *args)
            x.append(self.qt_beta)
            fit.append(self.qt_fit)
            x0 = self.qt_beta

        self.qt_beta = np.array(x).T
        self.qt_fit = np.array(fit).T
        self.alpha_q = alphaseq


    def qt_predict(self, x): 
        '''
        Compute predicted quantile at new input x
        
        Args:
            x (ndarray): new input.
        '''
        return self.itcp_q*self.qt_beta[0] + \
               self.qt_beta[self.itcp_q:] @ self.genK(x)


    def es(self, tau=0.5, alpha_q=1, alpha_e=1, 
           init=None, intercept=True, 
           qt_fit=None, smooth=False, h=0., 
           method='L-BFGS-B', solver='clarabel',
           robust=False, c=None, 
           qt_tol=1e-7, es_tol=1e-7, options=None):
        """ 
        Fit (robust) expected shortfall kernel ridge regression
        
        Args:
            tau (float): quantile level between 0 and 1; default is 0.5.
            alpha_t, alpha_e (float): regularization parameters; default is 1.
            init (ndarray): initial values for optimization; default is None.
            intercept (bool): whether to include intercept term; 
                              default is True.
            qt_fit (ndarray): fitted quantiles from the first step; 
                              default is None.
            smooth (bool): a logical flag for using smoothed check loss; 
                           default is FALSE.
            h (float): bandwidth for smoothing; default is 0.
            method (str): type of solver if smoothing (h>0) is used;
                          choose one from ['BFGS', 'L-BFGS-B'].
            solver (str): type of QP solver if check loss is used; 
                          default is 'clarabel'.
            robust (bool): whether to use the Huber loss in the second step; 
                           default is False.
            c (float): positive tuning parameter for the Huber estimator; 
                       default is None.
            qt_tol (float): tolerance for termination in qt-KRR; 
                            default is 1e-7.
            es_tol (float): tolerance for termination in es-KRR; 
                            default is 1e-7.
            options (dict): a dictionary of solver options; default is None.
    
        Attributes:
            es_sol (OptimizeResult): solution of the optimization problem
            es_beta (ndarray): expected shortfall KRR coefficients
            es_fit (ndarray): fitted expected shortfalls (in-sample)
        """
        if qt_fit is None:
            self.qt(tau, alpha_q, None, intercept, smooth, h, 
                    method, solver, qt_tol, options)
            qt_fit = self.qt_fit
        elif len(qt_fit) != self.n:
            raise ValueError("Length of qt_fit should be equal to \
                              the number of observations.")
        
        self.alpha_e, self.tau, self.itcp = alpha_e, tau, intercept
        n = self.n
        
        qt_nres = np.minimum(self.Y - qt_fit, 0)
        if robust == True and c is None:
            c = np.std(qt_nres) * (n/np.log(n))**(1/3) / tau
        self.c = c
        # surrogate response
        Z = qt_nres/tau + qt_fit
        if intercept:
            x0 = init if init is not None else np.zeros(n + 1)
            x0[0] = np.mean(Z)
            res = lambda x: Z - x[0] - self.K @ x[1:]
            func = lambda x: huber_loss(res(x), c) + \
                             (alpha_e/2) * np.dot(x[1:], self.K @ x[1:])
            grad = lambda x: np.insert(-self.K @ huber_grad(res(x), c)
                                       + alpha_e * self.K @ x[1:],
                                       0, -np.sum(huber_grad(res(x), c)))
            self.es_sol = minimize(func, x0, method=method, 
                                   jac=grad, tol=es_tol, options=options)
            self.es_beta = self.es_sol.x
            self.es_fit = self.es_beta[0] + self.K @ self.es_beta[1:]
        else:
            x0 = init if init is not None else np.zeros(n)
            res = lambda x: Z - self.K @ x
            func = lambda x: huber_loss(res(x), c) \
                             + (alpha_e/2) * np.dot(x, self.K @ x)
            grad = lambda x: -self.K @ huber_grad(res(x), c)  \
                             + alpha_e * self.K @ x
            self.es_sol = minimize(func, x0=x0, method=method, 
                                   jac=grad, tol=es_tol, options=options)
            self.es_beta = self.es_sol.x
            self.es_fit = self.K @ self.es_beta
        self.es_residual = Z - self.es_fit
        self.es_model = None


    def lses(self, tau=0.5, 
             alpha_q=1, alpha_e=1,
             smooth=False, h=0., 
             method='L-BFGS-B', solver='clarabel',
             qt_tol=1e-7, options=None):
        
        self.alpha_e, self.tau, self.itcp = alpha_e, tau, True
        self.qt(tau, alpha_q, None, True,
                smooth, h, method, solver, qt_tol, options) 
        n = self.n
        Z = np.minimum(self.Y - self.qt_fit, 0)/tau + self.qt_fit
        if self.kernel == 'polynomial':
            self.params['gamma'] = None
        self.es_model = KR(alpha = alpha_e, kernel=self.kernel, 
                           gamma = self.params['gamma'],
                           degree = self.params['degree'],
                           coef0 = self.params['coef0'])
        self.es_model.fit(self.X0, Z)
        self.es_fit = self.es_model.predict(self.X0)
        self.es_residual = Z - self.es_fit
        self.es_beta = None


    def es_predict(self, x): 
        '''
        Compute predicted expected shortfall at new input x
        
        Args:
            x (ndarray): new input.
        '''

        if self.es_beta is not None:
            return self.itcp*self.es_beta[0] \
                   + self.es_beta[self.itcp:] @ self.genK(x)
        elif self.es_model is not None:
            if self.nm == 'MinMax':
                x = (x - self.xmin)/(self.xmax - self.xmin)
            elif self.nm == 'Z-score':
                x = (x - self.xm)/self.xsd
            return self.es_model.predict(x)


    def bahadur(self, x):
        '''
        Compute Bahadur representation of the expected shortfall estimator
        '''
        if np.ndim(x) == 1:
            x = x.reshape(1, -1)
        if self.nm == 'MinMax':
            x = (x - self.xmin)/(self.xmax - self.xmin)
        elif self.nm == 'Z-score':
            x = (x - self.xm)/self.xsd
        
        A = self.K/self.n + self.alpha_e * np.eye(self.n)
        return np.linalg.solve(A, self.genK(x)) \
               * self.es_residual.reshape(-1,1)


def huber_loss(u, c=None):
    ''' Huber loss '''
    if c is None:
        out = 0.5 * u ** 2
    else:
        out = np.where(abs(u)<=c, 0.5*u**2, c*abs(u) - 0.5*c**2)
    return np.sum(out)


def huber_grad(u, c=None):
    ''' Gradient of Huber loss '''
    if c is None:
        return u    
    else:
        return np.where(abs(u)<=c, u, c*np.sign(u))



###############################################################################
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.data.dataset import random_split
from torch.distributions.normal import Normal
import matplotlib.pyplot as plt
from enum import Enum


###############################################################################
######################### Neural Network Regression ###########################
###############################################################################
class ANN:
    '''
    Artificial Neural Network Regression
    '''
    optimizers = ["sgd", "adam"]
    activations = ["sigmoid", "tanh", "relu", "leakyrelu"]
    params = {'batch_size' : 64, 'val_pct' : .25, 'step_size': 10,
              'activation' : 'relu', 'depth': 4, 'width': 256,  
              'optimizer' : 'adam', 'lr': 1e-3, 'lr_decay': 1., 'n_epochs' : 200,
              'dropout_rate': 0.1, 'Lambda': .0, 'weight_decay': .0, 
              'momentum': 0.9, 'nesterov': True}


    def __init__(self, X, Y, normalization=None):
        '''
        Args:
            X (ndarry): n by p matrix of covariates; 
                        n is the sample size, p is the number of covariates.
            Y (ndarry): response/target variable.
            normalization (str): method for normalizing covariates;
                                 should be one of [None, 'MinMax', 'Z-score'].

        Attributes:
            Y (ndarray): response variable.
            X0 (ndarray): normalized covariates.
            n (int): sample size.
            nm (str): method for normalizing covariates.
        '''
        self.n = X.shape[0]
        self.Y = Y.reshape(self.n)
        self.nm = normalization

        if self.nm is None:
            self.X0 = X
        elif self.nm == 'MinMax':
            self.xmin = np.min(X, axis=0)
            self.xmax = np.max(X, axis=0)
            self.X0 = (X - self.xmin)/(self.xmax - self.xmin)
        elif self.nm == 'Z-score':
            self.xm, self.xsd = np.mean(X, axis=0), np.std(X, axis=0)
            self.X0 = (X - self.xm)/self.xsd


    def plot_losses(self):
        fig = plt.figure(figsize=(10, 4))
        plt.style.use('fivethirtyeight')
        plt.plot(self.results['losses'],
                 label='Training Loss', c='b')
        if self.params['val_pct'] > 0:
            plt.plot(self.results['val_losses'],
                     label='Validation Loss', c='r')
        plt.yscale('log')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.tight_layout()
        return fig


    def qt(self, tau=0.5, smooth=False, h=0., options=dict(),
           plot=False, device='cpu', min_bandwidth=1e-4):
        '''
        Fit (smoothed) quantile neural network regression

        Args: 
            tau (float): quantile level between 0 and 1; default is 0.5.
            smooth (boolean): a logical flag for using smoothed check loss; default is FALSE.
            h (float): bandwidth for smoothing; default is 0.
            options (dictionary): a dictionary of neural network and optimization parameters.
                batch_size (int): the number of training examples used in one iteration; 
                                  default is 64.
                val_pct (float): the proportion of the training data to use for validation;
                                   default is 0.25.
                step_size (int): the number of epochs of learning rate decay; default is 10.
                activation (string): activation function; default is the ReLU function.
                depth (int): the number of hidden layers; default is 4.
                width (int): the number of neurons for each layer; default is 256.
                optimizer (string): the optimization algorithm; default is the Adam optimizer.
                lr (float): , learning rate of SGD or Adam optimization; default is 1e-3.
                lr_decay (float): multiplicative factor by which the learning rate will be reduced;
                                  default is 0.95.
                n_epochs (int): the number of training epochs; default is 200.
                dropout_rate : proportion of the dropout; default is 0.1.
                Lambda (float): L_1-regularization parameter; default is 0.
                weight_decay (float): weight decay of L2 penalty; default is 0.
                momentum (float): momentum accerleration rate for SGD algorithm; 
                                  default is 0.9.
                nesterov (boolean): whether to use Nesterov gradient descent algorithm;
                                    default is TRUE.
            plot (boolean) : whether to plot loss values at iterations.
            device (string): device to run the model on; default is 'cpu'.
            min_bandwidth (float): minimum value of the bandwidth; default is 1e-4.
        '''
        self.params.update(options)
        self.device = device
        self.tau = tau
        if smooth and h == 0:
            h = max(min_bandwidth, 
                    (tau - tau**2)**0.5 / self.n ** (1/3))
        self.h = h if smooth else 0.   # bandwidth for smoothing
        self.results = self.trainer(self.X0, self.Y, 
                                    QuantLoss(tau, h), 
                                    device, 
                                    QuantLoss(tau, 0))
        if plot: self.fig = self.plot_losses()
        self.model = self.results['model']
        self.fit = self.results['fit']


    def es(self, tau=0.5, robust=False, c=None, 
           qt_fit=None, smooth=False, h=0., 
           options=dict(), plot=False, device='cpu'):
        '''
        Fit (robust) expected shortfall neural network regression
        '''
        self.params.update(options)
        self.device = device
        self.tau = tau
        if qt_fit is None:
            self.qt(tau=tau, smooth=smooth, h=h, plot=False, device=device)
            qt_fit = self.fit
        elif len(qt_fit) != self.n:
            raise ValueError("Length of qt_fit should be equal to \
                             the number of observations.")
        qt_nres = np.minimum(self.Y - qt_fit, 0)
        if robust == True and c is None:
            c = np.std(qt_nres) * (self.n / np.log(self.n))**(1/3) / tau
        self.c = c
        Z = qt_nres / tau + qt_fit    # surrogate response
        loss_fn = nn.MSELoss(reduction='mean') if not robust \
                    else nn.HuberLoss(reduction='mean', delta=c)
        self.results = self.trainer(self.X0, Z, loss_fn, device)
        if plot: self.fig = self.plot_losses()
        self.model = self.results['model']
        self.fit = self.results['fit']


    def mean(self, options=dict(), 
             robust=False, c=None, s=1.,
             plot=False, device='cpu'):
        ''' 
        Fit least squares neural network regression 
        or its robust version with Huber loss
        '''
        self.params.update(options)
        self.device = device
        if robust == True and c is None:
            ls_res = self.Y - self.results['fit']
            scale = s * np.std(ls_res) + (1 - s) * mad(ls_res)
            c = scale * (self.n / np.log(self.n))**(1/3)
        self.c = c
        loss_fn = nn.MSELoss(reduction='mean') if not robust \
                    else nn.HuberLoss(reduction='mean', delta=c)
        self.results = self.trainer(self.X0, self.Y, loss_fn, device)
        if plot: self.fig = self.plot_losses()
        self.model = self.results['model']
        self.fit = self.results['fit']


    def predict(self, X):
        ''' Compute predicted outcomes at new input X '''
        if self.nm == 'MinMax':
            X = (X - self.xmin)/(self.xmax - self.xmin)
        elif self.nm == 'Z-score':
            X = (X - self.xm)/self.xsd
        Xnew = torch.as_tensor(X, dtype=torch.float).to(self.device)
        return self.model.predict(Xnew)


    def trainer(self, x, y, loss_fn, device='cpu', val_fn=None):
        '''
        Train an MLP model with given loss function
        '''
        input_dim = x.shape[1]
        x_tensor = torch.as_tensor(x).float()
        y_tensor = torch.as_tensor(y).float()
        dataset = TensorDataset(x_tensor, y_tensor)
        n_total = len(dataset)
        n_val = int(self.params['val_pct'] * n_total)
        train_data, val_data = random_split(dataset, [n_total - n_val, n_val])

        train_loader = DataLoader(train_data, 
                                  batch_size=self.params['batch_size'], 
                                  shuffle=True, 
                                  drop_last=True)
        if self.params['val_pct'] > 0:
            val_loader = DataLoader(val_data, 
                                    batch_size=self.params['batch_size'], 
                                    shuffle=False)
        
        # initialize the model
        model = MLP(input_dim, options=self.params).to(device)
        
        # choose the optimizer
        if self.params['optimizer'] == "sgd":
            optimizer = optim.SGD(model.parameters(),
                                  lr=self.params['lr'],
                                  weight_decay=self.params['weight_decay'],
                                  nesterov=self.params['nesterov'],
                                  momentum=self.params['momentum'])
        elif self.params['optimizer'] == "adam":
            optimizer = optim.Adam(model.parameters(), 
                                   lr=self.params['lr'], 
                                   weight_decay=self.params['weight_decay'])
        else:
            raise Exception(self.params['optimizer'] 
                            + "is currently not available")

        if val_fn is None: val_fn = loss_fn
        train_step_fn = make_train_step_fn(model, loss_fn, optimizer)
        val_step_fn = make_val_step_fn(model, val_fn)
        scheduler = optim.lr_scheduler.StepLR(optimizer, 
                                              step_size=self.params['step_size'],
                                              gamma=self.params['lr_decay'])

        losses, val_losses, best_val_loss = [], [], 1e10
        for epoch in range(self.params['n_epochs']):
            loss = mini_batch(device, train_loader, train_step_fn)
            losses.append(loss)

            if self.params['val_pct'] > 0:
                with torch.no_grad():
                    val_loss = mini_batch(device, val_loader, val_step_fn)
                    val_losses.append(val_loss)
                # save the best model
                if val_losses[epoch] < best_val_loss:
                    best_val_loss = val_losses[epoch]
                    torch.save({'epoch': epoch+1,
                                'model_state_dict': model.state_dict(),
                                'best_val_loss': best_val_loss,
                                'val_losses': val_losses,
                                'losses': losses}, 'checkpoint.pth')
                # learning rate decay
                scheduler.step()
            else:
                torch.save({'epoch': epoch+1,
                            'model_state_dict': model.state_dict(),
                            'losses': losses}, 'checkpoint.pth')

        checkpoint = torch.load('checkpoint.pth')
        final_model = MLP(input_dim, options=self.params).to(device)
        final_model.load_state_dict(checkpoint['model_state_dict'])

        return {'model': final_model,
                'fit': final_model.predict(x_tensor.to(device)),
                'checkpoint': checkpoint,
                'losses': losses,
                'val_losses': val_losses,
                'total_epochs': epoch+1}


class Activation(Enum):
    ''' Activation functions '''
    relu = nn.ReLU()
    tanh = nn.Tanh()
    sigmoid = nn.Sigmoid()
    leakyrelu = nn.LeakyReLU()


class MLP(nn.Module):
    ''' Generate a multi-layer perceptron '''
    def __init__(self, input_size, options):
        super(MLP, self).__init__()

        activation = Activation[options.get('activation', 'relu')].value
        dropout = options.get('dropout_rate', 0)
        layers = [input_size] + [options['width']] * options['depth']
        
        nn_structure = []
        for i in range(len(layers) - 1):
            nn_structure.extend([
                nn.Linear(layers[i], layers[i + 1]),
                nn.Dropout(dropout) if dropout > 0 else nn.Identity(),
                activation
            ])
        nn_structure.append(nn.Linear(layers[-1], 1))

        self.fc_in = nn.Sequential(*nn_structure)

    def forward(self, x):
        return self.fc_in(x)

    def predict(self, X):
        with torch.no_grad():
            self.eval()
            yhat = self.forward(X)[:, 0]
        return yhat.cpu().numpy()
    

###############################################################################
###########################    Helper Functions    ############################
###############################################################################
def mad(x):
    ''' Median absolute deviation '''
    return 1.4826 * np.median(np.abs(x - np.median(x)))


def make_train_step_fn(model, loss_fn, optimizer):
    '''
    Builds function that performs a step in the training loop
    '''
    def perform_train_step_fn(x, y):
        model.train()
        yhat = model(x)
        loss = loss_fn(yhat, y.view_as(yhat))
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        return loss.item()
    return perform_train_step_fn


def make_val_step_fn(model, loss_fn):
    def perform_val_step_fn(x, y):
        model.eval()
        yhat = model(x)
        loss = loss_fn(yhat, y.view_as(yhat))
        return loss.item()
    return perform_val_step_fn


def mini_batch(device, data_loader, step_fn):
    mini_batch_losses = []
    for x_batch, y_batch in data_loader:
        x_batch = x_batch.to(device)
        y_batch = y_batch.to(device)
        mini_batch_loss = step_fn(x_batch, y_batch)
        mini_batch_losses.append(mini_batch_loss)
    return np.mean(mini_batch_losses)


def QuantLoss(tau=.5, h=.0):
    def loss(y_pred, y):
        z = y - y_pred
        if h == 0:
            return torch.max((tau - 1) * z, tau * z).mean()
        else:
            tmp = .5 * h * torch.sqrt(2/torch.tensor(np.pi))
            return torch.add((tau - Normal(0, 1).cdf(-z/h)) * z, 
                             tmp * torch.exp(-(z/h)**2/2)).mean()
    return loss