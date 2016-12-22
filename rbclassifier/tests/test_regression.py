import unittest

import rbclassifier.rbclassifier
from rbclassifier.rbclassifier import RelevanceBoundsRegressor
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import Lasso
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RandomizedLasso
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils import check_random_state
from sklearn.utils.testing import ignore_warnings
from sklearn.utils.testing import assert_greater, assert_equal, assert_true,assert_false
from numpy.testing import assert_array_almost_equal, assert_array_equal,assert_raises
import numpy as np
from sklearn.exceptions import FitFailedWarning
from sklearn.preprocessing import StandardScaler

class TestRegression(unittest.TestCase):
    def test_simpleRegression(self):

        generator = check_random_state(0)
        data = rbclassifier.genData.genRegressionData(n_samples=100, n_features=2, n_redundant=0,strRel=2,
                        n_repeated=0, random_state=generator)

        X_orig, y = data
        X_orig = StandardScaler().fit(X_orig).transform(X_orig)

        X = np.c_[X_orig, generator.normal(size=(len(X_orig), 6))]
        y = list(y)

        # Test using the score function
        rbc = RelevanceBoundsRegressor(random_state=generator, shadow_features=False)
        rbc.fit(X, y)

        assert_equal(len(rbc.allrel_prediction_), X.shape[1])
        assert_equal(len(rbc.interval_), X.shape[1])

        X_r = rbc.transform(X)
        print(rbc.interval_,rbc.allrel_prediction_)

        # All the noisy variable were filtered out
        assert_array_equal(X_r, X_orig)

        # All strongly relevant features have a lower bound > 0
        assert_true(np.all(rbc.interval_[0:2,0]>0))

    def test_genData(self):
        n = 100
        d = 10
        strRel = 2

        generator = check_random_state(1337)
        X,Y = rbclassifier.genData.genRegressionData(n_samples=n, n_features=d, n_redundant=0,strRel=strRel,
                        n_repeated=0, random_state=generator)

        assert_true(X.shape == (n,d))


        X,Y = rbclassifier.genData.genRegressionData(n_samples=n, n_features=d, n_redundant=2,strRel=strRel,
                        n_repeated=1, random_state=generator)

        assert_true(X.shape == (n,d))

        X,Y = rbclassifier.genData.genRegressionData(n_samples=n, n_features=d, n_redundant=2,strRel=0,
                        n_repeated=1, random_state=generator)

        assert_true(X.shape == (n,d))
if __name__ == '__main__':
    unittest.main()