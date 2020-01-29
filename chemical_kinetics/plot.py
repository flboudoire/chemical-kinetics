

import matplotlib.pyplot as plt
import numpy as np


def plot_c(ds, names = None):

    if names is None: names = ds.names

    df = ds.df_c
    df_std = ds.df_c_std
    df_fit = ds.df_c_fit

    plt.figure()
    lines = dict()
    for name in names:
        p = plt.errorbar(
            df["t"],
            df[name],
            yerr = df_std[name],
            linestyle = "none",
            marker = ".",
            label = name
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


def plot_ks(ds):

    params = ds.fit_result.params
    ks = np.array([params[key].value for key in params])
    ks_err = np.array([params[key].stderr for key in params])
    names = [key for key in params]

    undefined = [k < k_err for k, k_err in zip(ks, ks_err)]
    ks[undefined] = np.nan
    ks_err[undefined] = np.nan

    plt.figure()
    plt.plot(
        ks,
        np.arange(0, len(ks)),
        "|", color = "C0"
        )
    plt.errorbar(
        ks,
        np.arange(0, len(ks)),
        xerr=ks_err,
        linestyle = "none",
        color = "C0"
        )
    plt.gca().set_xscale("log")
    plt.gca().set_yticks(np.arange(0, len(ks)))
    plt.gca().set_yticklabels(names)
    plt.gca().invert_yaxis()
    for i, val in enumerate(ks):
        if not undefined[i]:
            plt.text(
                val,
                i-0.2,
                "%.1e"%val,
                va = "bottom",
                ha = "center",
                bbox=dict(
                    facecolor='white',
                    pad = 0,
                    edgecolor = "none",
                    alpha=1
                    )
                )
        else:
            plt.text(
                plt.gca().get_xlim()[0]*1.1,
                i,
                r"$\leftarrow$ undefined",
                va = "center",
                ha = "left"
                )