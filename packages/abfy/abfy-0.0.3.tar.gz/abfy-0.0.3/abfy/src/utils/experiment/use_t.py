from scipy.stats import t


def adjust_result_using_t(est, se, n, p, alpha=0.05):
    """
    Based on model output treatment effect and standard error,
    compute p-value and confidence interval by using t-distribution with df_resid = n - p

    :param est: estimated treatment effect from model
    :param se: estimated standard error from model
    :param n: effective number of units, if cluster exists should be number of clusters
    :param p: number of regressors including intercept
    :param alpha: threshold by default 0.05
    :return: p_value, ci_left, ci_right
    """
    t_stats = est / se
    df_resid = max(n - p, 1)
    ci_radius = t.ppf(1 - alpha / 2, df_resid) * se
    p_value = (1 - t.cdf(abs(t_stats), df_resid)) * 2
    ci_left = est - ci_radius
    ci_right = est + ci_radius
    return p_value, ci_left, ci_right
