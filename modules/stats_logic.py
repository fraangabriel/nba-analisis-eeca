import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

def ajustar_regresion_lineal(df, col_x, col_y):
    """Creacion del modelo de regresion lineal"""
    df_clean = df[[col_x, col_y]].dropna()
    formula = f"{col_y} ~ {col_x}"
    modelo = ols(formula, data=df_clean).fit()
    return modelo

def calcular_tabla_anova(modelo):
    """Genera la tabla ANOVA (SC, gl, CM, F)"""
    return sm.stats.anova_lm(modelo, typ=2)

def obtener_metricas_correlacion(df, col_x, col_y):
    """Calcula Pearson y Spearman """
    df_clean = df[[col_x, col_y]].dropna()
    x, y = df_clean[col_x], df_clean[col_y]
    n = len(df_clean)

    # Pearson y Contraste de significacion de rho
    r, p_pearson = stats.pearsonr(x, y)
    t_pearson = r * np.sqrt((n-2)/(1-r**2))

    # Spearman
    rho, p_spearman = stats.spearmanr(x, y)

    return {
        "r": r,
        "p_r": p_pearson,
        "t_r": t_pearson,
        "rho": rho,
        "p_rho": p_spearman,
        "n": n
    }
