from abc import ABCMeta, abstractmethod
import cvxpy as cvx
import numpy as np


class BaseProblem(object):
    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None):
        # General data
        self.d = d
        self.n = n
        self.X = X
        # Dimension specific data
        self.di = di
        # Solver parameters
        self.kwargs = kwargs

        self.problem = None
        self._constraints = None
        self._objective = None

    def solve(self):
        self.problem = cvx.Problem(self._objective, self._constraints)
        
        self.problem.solve(**self.kwargs)

        return self


class BaseClassificationProblem(BaseProblem):
    """Base class for all common optimization problems."""

    __metaclass__ = ABCMeta

    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None, C=1, svmloss=1, L1=1):
        super().__init__(di=di, d=d, n=n, kwargs=kwargs, X=X, Y=Y)
        # Solver parameters
        self.kwargs = kwargs
        Y_array = np.array([Y, ] * 1).T

        # Solver Variables
        self.xp = cvx.Variable()  # x' , our opt. value
        self.omega = cvx.Variable(shape=(d,1))  # complete linear weight vector
        self.b = cvx.Variable()  # shift

        point_distances = cvx.multiply(Y_array, X * self.omega + self.b)
        loss = cvx.sum(cvx.pos(1 - point_distances))
        weight_norm = cvx.norm(self.omega, 1)

        self._constraints = [
            weight_norm <= L1,
            loss <= svmloss
        ]

class MinProblemClassification(BaseClassificationProblem):
    """Class for minimization."""

    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None, C=1, svmloss=1, L1=1):
        super().__init__(di=di, d=d, n=n, kwargs=kwargs, X=X, Y=Y, C=C, svmloss=svmloss, L1=L1)

        self._constraints.extend(
            [
                cvx.abs(self.omega[di]) <= self.xp
            ])

        self._objective = cvx.Minimize(self.xp)


class MaxProblem1(BaseClassificationProblem):
    """Class for maximization."""

    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None, C=1, svmloss=1, L1=1):
        super().__init__(di=di, d=d, n=n, kwargs=kwargs, X=X, Y=Y, C=C, svmloss=svmloss, L1=L1)

        self._constraints.extend([
            self.xp <= self.omega[self.di]
        ])

        self._objective = cvx.Maximize(self.xp)


class MaxProblem2(BaseClassificationProblem):
    """Class for maximization."""

    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None, C=1, svmloss=1, L1=1):
        super().__init__(di=di, d=d, n=n, kwargs=kwargs, X=X, Y=Y, C=C, svmloss=svmloss, L1=L1)

        self._constraints.extend([
            self.xp <= -(self.omega[self.di])
        ])

        self._objective = cvx.Maximize(self.xp)

'''
#############
            ##### REGRESSION
#############
'''

class BaseRegressionProblem(BaseProblem):

    __metaclass__ = ABCMeta

    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None, C=1,epsilon=0.1, svrloss=1, L1=1):
        super().__init__(di=di, d=d, n=n, kwargs=kwargs, X=X, Y=Y)

        # General data
        #self.Y = Y # other format then with classification
        self.Y = Y.reshape((-1,1))
        self.svrloss = svrloss
        self.epsilon = epsilon
        self.L1 = L1
        self.C = C

        # Solver parameters
        self.kwargs = kwargs
        # Solver Variables
        self.xp = cvx.Variable(shape=(d,1))  # x' , our opt. value
        self.omega = cvx.Variable(shape=(d,1))  # complete linear weight vector
        self.b = cvx.Variable()  # shift
        self.slack = cvx.Variable(shape=(n,1),nonneg=True)  # slack variables

        self._constraints = [
            cvx.norm(self.omega, 1) <= self.L1,
            cvx.sum(self.slack) <= self.svrloss,
            cvx.abs(self.Y - (self.X * self.omega + self.b )) <= self.epsilon + self.slack
        ]


class MinProblemRegression(BaseRegressionProblem):
    """Class for minimization."""

    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None, C=1,epsilon=0.1, svmloss=1, L1=1):
        super().__init__(di=di, d=d, n=n, kwargs=kwargs, X=X, Y=Y, C=C, epsilon=epsilon, svrloss=svmloss, L1=L1)

        self._constraints.extend(
            [
                cvx.abs(self.omega[self.di]) <= self.xp[self.di],
            ])

        self._objective = cvx.Minimize(self.xp[self.di])


class MaxProblem1Regression(BaseRegressionProblem):
    """Class for maximization."""

    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None, C=1,epsilon=0.1, svmloss=1, L1=1):
        super().__init__(di=di, d=d, n=n, kwargs=kwargs, X=X, Y=Y, C=C, epsilon=epsilon, svrloss=svmloss, L1=L1)

        self._constraints.extend([
            self.xp[self.di] <= self.omega[self.di]
        ])

        self._objective = cvx.Maximize(self.xp[self.di])



class MaxProblem2Regression(BaseRegressionProblem):
    """Class for maximization."""

    def __init__(self, di=0, d=0, n=0, kwargs=None, X=None, Y=None, C=1,epsilon=0.1, svmloss=1, L1=1):
        super().__init__(di=di, d=d, n=n, kwargs=kwargs, X=X, Y=Y, C=C, epsilon=epsilon, svrloss=svmloss, L1=L1)

        self._constraints.extend([
           self.xp[self.di] <= -(self.omega[self.di])
        ])

        self._objective = cvx.Maximize(self.xp[self.di])
