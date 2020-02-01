

import matplotlib.pyplot as plt
import numpy as np


def plot_c(ds, names = None):
    """ #TODO: comment function
    """
    if names is None: names = ds.names

    df = ds.df_c
    df_std = ds.df_c_std
    df_fit = ds.df_c_fit

    plt.figure()
    lines = dict()
    for name in names:
        style = dict(
            linestyle = "none",
            marker = ".",
            label = name
            )
        if np.all(np.isnan(df_std[name])):
            p = plt.plot(
                df["t"],
                df[name],
                **style
                )
        else:
            p = plt.errorbar(
                df["t"],
                df[name],
                yerr = df_std[name],
                **style
                )
        lines[name] = p[0]
    plt.xlabel(ds.t_label)
    plt.ylabel(ds.c_label)
    plt.legend()

    if df_fit is not None:
        for name in names:
            plt.plot(
                df_fit["t"],
                df_fit[name],
                color = lines[name].get_color()
                )

    plt.show()


def plot_q(ds):
    """ #TODO: comment function
    """
    df = ds.df_q
    df_std = ds.df_q_std
    df_fit = ds.df_q_fit

    plt.figure()
    plt.fill_between(
        df["t"],
        df["Q"] - df_std["Q"],
        df["Q"] + df_std["Q"],
        color = "C0", alpha = 0.3, lw = 0
        )
    plt.plot(df["t"], df["Q"], label = "data")
    plt.xlabel(ds.t_label)
    plt.ylabel(ds.q_label)

    if df_fit is not None:
        plt.plot(df_fit["t"], df_fit["Q"], "--", label = "fit")

    plt.legend()
    plt.show()