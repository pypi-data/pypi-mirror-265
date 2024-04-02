__all__ = [
    "parse_and_aggregate_benchmark_report",
    "plot_compression_ratio_performance_instructions",
    "plot_compression_ratio_performance_throughput",
    "plot_absolute_compression_error",
    "plot_absolute_relative_compression_error",
    "plot_compression_goodness_uniformity",
    "plot_compression_goodness_preserved_pca",
    "plot_compression_goodness_bit_information",
    "plot_dataset_variable_compressor_card",
    "plot_performance_comparison_instructions",
    "plot_performance_comparison_throughput",
    "plot_absolute_compression_error_comparison",
    "plot_absolute_relative_compression_error_comparison",
    "plot_compression_goodness_uniformity_comparison",
    "plot_compression_goodness_preserved_pca_comparison",
    "plot_compression_goodness_bitinformation_comparison",
    "plot_cross_dataset_compressor_default_derivative_comparison",
]

from collections import defaultdict as _defaultdict
from collections import namedtuple as _namedtuple
from pathlib import Path as _Path

import matplotlib as _  # noqa: F401
import matplotlib.ticker as _mtick
import numpy as _np
import proplot as _plt

ResultKey = _namedtuple(
    "ResultKey",
    ["dataset", "variable", "variable_long", "units", "compressor"],
)
CompressorPerformance = _namedtuple(
    "CompressorPerformance",
    ["compression_ratio", "instructions", "throughput"],
)
CompressorGoodness = _namedtuple(
    "CompressorGoodness",
    [
        "uniformity",
        "preserved_pca",
        "bit_information",
        "error_abs",
        "error_rel_abs",
    ],
)
CompressorResult = _namedtuple(
    "CompressorResult",
    ["label", "ticks", "performance", "goodness_per_derivative"],
)

ConfidenceDistributionDtype = _np.dtype(
    [
        ("p2_5", _np.float64),
        ("p15_9", _np.float64),
        ("p50", _np.float64),
        ("p84_1", _np.float64),
        ("p97_5", _np.float64),
    ]
)


def _tokenize_compressor(compressor: dict) -> list[str]:
    tokens = [compressor["name"], ": "]

    for i, codec in enumerate(compressor["codecs"]):
        if i > 0:
            tokens.append(", ")
        tokens.append(codec["import_path"].split(".")[-1])
        tokens.append("(")

        for j, (parameter, value) in enumerate(codec["parameters"].items()):
            if j > 0:
                tokens.append(", ")
            tokens.append(parameter)
            tokens.append("=")
            tokens.append(str(value["value"]))

        tokens.append(")")

    return tokens


def _simplify_tokens(tokens: list[list[str]]) -> tuple[str, list[list[str]]]:
    common = []
    variables = [[] for _ in tokens]  # noqa: F811
    variable = 0

    for tokens in zip(*tokens):
        first = tokens[0]
        if all(x == first for x in tokens):
            common.append(first)
        else:
            variable += 1
            common.append(f"#{variable}")

            for t, v in zip(tokens, variables):
                v.append(t)

    return "".join(common), variables


def _prettify_derivative(variable: str, derivatives: list) -> str:
    pretty = variable

    for derivative in derivatives:
        if derivative.get("differentiate", None) is not None:
            pretty += f" ∂{derivative['differentiate']}"
        elif derivative.get("integrate", None) is not None:
            pretty += f" ∫{derivative['integrate']}"

    return pretty


# TODO: move implementation to Rust
def parse_and_aggregate_benchmark_report(
    report: dict,
) -> dict[ResultKey, CompressorResult]:
    results = _defaultdict(
        lambda: CompressorResult(
            label="",
            ticks=[],
            performance=CompressorPerformance(
                compression_ratio=[],
                instructions=[],
                throughput=[],
            ),
            goodness_per_derivative=_defaultdict(
                lambda: CompressorGoodness(
                    uniformity=[],
                    preserved_pca=[],
                    bit_information=[],
                    error_abs=[],
                    error_rel_abs=[],
                )
            ),
        )
    )

    for result in report["results"]:
        dataset = _Path(result["dataset"]).name
        variable = result["variable"]["name"]
        variable_long = result["variable"]["long_name"]
        units = result["variable"]["units"]["verbose"]["expression"]["latex"]
        compressor = result["compressor"]["name"]

        output = result["result"].get("Ok", None)
        if output is None:
            continue
        stats = output["stats"]

        key = ResultKey(dataset, variable, variable_long, units, compressor)
        res = results[key]

        compressor = result["compressor"]

        res.ticks.append(_tokenize_compressor(compressor))

        res.performance.compression_ratio.append(
            tuple(
                stats["compression_ratio"]["mean"][p]["ratio"]
                for p in ("p2_5", "p15_9", "p50", "p84_1", "p97_5")
            )
        )
        res.performance.instructions.append(
            tuple(
                stats["instructions"]["mean"][p]["ratio"]
                for p in ("p2_5", "p15_9", "p50", "p84_1", "p97_5")
            )
        )
        res.performance.throughput.append(
            tuple(
                stats["throughput"]["mean"][p]["throughput"]
                for p in ("p2_5", "p15_9", "p50", "p84_1", "p97_5")
            )
        )

        for derivative, goodness in zip(
            [[]] + result["variable"]["derivatives"], stats["goodness"]
        ):
            derivative = _prettify_derivative(variable, derivative)
            res_goodness = res.goodness_per_derivative[derivative]

            res_goodness.uniformity.append(
                tuple(
                    goodness["uniformity"]["mean"][p]["uniformity"]
                    for p in ("p2_5", "p15_9", "p50", "p84_1", "p97_5")
                )
            )
            res_goodness.preserved_pca.append(
                tuple(
                    goodness["preserved_pca"]["mean"][p][
                        "abs_correlation_sum_fraction"
                    ]
                    for p in ("p2_5", "p15_9", "p50", "p84_1", "p97_5")
                )
            )
            res_goodness.bit_information.append(
                tuple(
                    goodness["bit_information"]["mean"][p][
                        "information_content_ratio"
                    ]
                    for p in ("p2_5", "p15_9", "p50", "p84_1", "p97_5")
                )
            )
            res_goodness.error_abs.append(
                tuple(
                    goodness["error_abs"]["mean"][p]["error"]
                    for p in ("p2_5", "p15_9", "p50", "p84_1", "p97_5")
                )
            )
            res_goodness.error_rel_abs.append(
                tuple(
                    goodness["error_rel_abs"]["mean"][p]["error"]
                    for p in ("p2_5", "p15_9", "p50", "p84_1", "p97_5")
                )
            )

    def try_parse_arg_into_number(a: str) -> int | float | str:
        try:
            return int(a)
        except ValueError:
            pass

        try:
            return float(a)
        except ValueError:
            pass

        return a

    new_results = dict()

    for key in sorted(
        results.keys(), key=lambda key: (key.variable, key.compressor)
    ):
        result = results[key]

        label, ticks = _simplify_tokens(result.ticks)

        tick_sortable = _np.empty(len(ticks), dtype=object)
        tick_sortable[:] = [
            tuple(try_parse_arg_into_number(a) for a in tick) for tick in ticks
        ]
        indices = _np.argsort(tick_sortable)

        new_results[key] = CompressorResult(
            label=label,
            ticks=_np.array([", ".join(tick) for tick in ticks])[indices],
            performance=CompressorPerformance(
                compression_ratio=_np.array(
                    result.performance.compression_ratio,
                    dtype=ConfidenceDistributionDtype,
                )[indices],
                instructions=_np.array(
                    result.performance.instructions,
                    dtype=ConfidenceDistributionDtype,
                )[indices],
                throughput=_np.array(
                    result.performance.throughput,
                    dtype=ConfidenceDistributionDtype,
                )[indices],
            ),
            goodness_per_derivative={
                derivative: CompressorGoodness(
                    uniformity=_np.array(
                        goodness.uniformity, dtype=ConfidenceDistributionDtype
                    )[indices],
                    preserved_pca=_np.array(
                        goodness.preserved_pca,
                        dtype=ConfidenceDistributionDtype,
                    )[indices],
                    bit_information=_np.array(
                        goodness.bit_information,
                        dtype=ConfidenceDistributionDtype,
                    )[indices],
                    error_abs=_np.array(
                        goodness.error_abs, dtype=ConfidenceDistributionDtype
                    )[indices],
                    error_rel_abs=_np.array(
                        goodness.error_rel_abs,
                        dtype=ConfidenceDistributionDtype,
                    )[indices],
                )
                for (
                    derivative,
                    goodness,
                ) in result.goodness_per_derivative.items()
            },
        )

    return new_results


def plot_compression_ratio_performance_instructions(
    key: ResultKey, result: CompressorResult, ax=None
):
    show = ax is None
    if ax is None:
        fig, ax1 = _plt.subplots(figsize=(6, 4))
    else:
        fig, ax1 = ax.get_figure(), ax
    fig = fig
    ax2 = ax1.twinx()

    if show:
        ax1.set_title(
            f"Compression Ratio and Performance [universal]\n{key.variable}: "
            f"{key.variable_long}\n{key.dataset}"
        )
    else:
        ax1.set_title("Compression Ratio and Performance [universal]")

    ax1.fill_between(
        result.ticks,
        result.performance.compression_ratio["p15_9"],
        result.performance.compression_ratio["p84_1"],
        color="tab:blue",
        alpha=0.2,
    )
    ax2.fill_between(
        result.ticks,
        result.performance.instructions["p15_9"],
        result.performance.instructions["p84_1"],
        color="tab:orange",
        alpha=0.2,
    )

    ax1.plot(
        result.ticks, result.performance.compression_ratio["p50"], c="tab:blue"
    )
    ax2.plot(
        result.ticks, result.performance.instructions["p50"], c="tab:orange"
    )

    ax1.set_ylim(1.0, ax1.get_ylim()[1])
    ax2.set_ylim(0.0, ax2.get_ylim()[1])

    ax1.set_xlabel(result.label)
    ax1.set_xticks(_np.arange(len(result.ticks)))
    ax1.set_xticklabels(result.ticks, rotation=-45)
    ax1.set_ylabel("original size / compressed size")
    ax1.set_yscale("log")
    ax1.format(yformatter="log")
    ax2.set_ylabel("Compression-Decompression Instructions [#/B]")
    ax1.spines["left"].set_color("tab:blue")
    ax2.spines["left"].set_color("tab:blue")
    ax1.tick_params(axis="y", colors="tab:blue")
    ax1.spines["right"].set_color("tab:orange")
    ax2.spines["right"].set_color("tab:orange")
    ax2.tick_params(axis="y", colors="tab:orange")

    if show:
        _plt.show()


def plot_compression_ratio_performance_throughput(
    key: ResultKey, result: CompressorResult, ax=None
):
    show = ax is None
    if ax is None:
        fig, ax1 = _plt.subplots(figsize=(6, 4))
    else:
        fig, ax1 = ax.get_figure(), ax
    fig = fig
    ax2 = ax1.twinx()

    if show:
        ax1.set_title(
            f"Compression Ratio and Performance [measurement]\n{key.variable}:"
            f" {key.variable_long}\n{key.dataset}"
        )
    else:
        ax1.set_title("Compression Ratio and Performance [measurement]")

    ax1.fill_between(
        result.ticks,
        result.performance.compression_ratio["p15_9"],
        result.performance.compression_ratio["p84_1"],
        color="tab:blue",
        alpha=0.2,
    )
    ax2.fill_between(
        result.ticks,
        result.performance.throughput["p15_9"],
        result.performance.throughput["p84_1"],
        color="tab:orange",
        alpha=0.2,
    )

    ax1.plot(
        result.ticks, result.performance.compression_ratio["p50"], c="tab:blue"
    )
    ax2.plot(
        result.ticks, result.performance.throughput["p50"], c="tab:orange"
    )

    ax1.set_ylim(1.0, ax1.get_ylim()[1])
    ax2.set_ylim(0.0, ax2.get_ylim()[1])

    ax1.set_xlabel(result.label)
    ax1.set_xticks(_np.arange(len(result.ticks)))
    ax1.set_xticklabels(result.ticks, rotation=-45)
    ax1.set_ylabel("original size / compressed size")
    ax1.set_yscale("log")
    ax1.format(yformatter="log")
    ax2.set_ylabel("Compression-Decompression Throughput [B/s]")
    ax1.spines["left"].set_color("tab:blue")
    ax2.spines["left"].set_color("tab:blue")
    ax1.tick_params(axis="y", colors="tab:blue")
    ax1.spines["right"].set_color("tab:orange")
    ax2.spines["right"].set_color("tab:orange")
    ax2.tick_params(axis="y", colors="tab:orange")

    if show:
        _plt.show()


def plot_absolute_compression_error(
    key: ResultKey, result: CompressorResult, ax=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    if show:
        ax.set_title(
            f"Absolute Compression Error\n{key.variable}: {key.variable_long}"
            f"\n{key.dataset}"
        )
    else:
        ax.set_title("Absolute Compression Error")

    ymin = 1.0

    for derivative in result.goodness_per_derivative.keys():
        error_abs = result.goodness_per_derivative[derivative].error_abs

        ymin = min(
            ymin, _np.amin(error_abs["p15_9"][error_abs["p15_9"] > 0.0])
        )

        ax.fill_between(
            result.ticks, error_abs["p15_9"], error_abs["p84_1"], alpha=0.2
        )
        ax.plot(result.ticks, error_abs["p50"], label=derivative)

    ax.set_xlabel(result.label)
    ax.set_xticks(_np.arange(len(result.ticks)))
    ax.set_xticklabels(result.ticks, rotation=-45)
    ax.set_ylabel(
        rf"|{key.variable} - {key.variable}$_{{c}}$|   [{key.units}]"
    )
    ax.set_yscale("symlog", linthresh=ymin, linscale=1.0)
    ax.set_ylim(-ymin / 2, ax.get_ylim()[1] * 2)
    ax.format(yformatter="log")

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_absolute_relative_compression_error(
    key: ResultKey, result: CompressorResult, ax=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    if show:
        ax.set_title(
            f"abs(Relative) Compression Error\n{key.variable}: "
            f"{key.variable_long}\n{key.dataset}"
        )
    else:
        ax.set_title("abs(Relative) Compression Error")

    ymin = 1.0

    for derivative in result.goodness_per_derivative.keys():
        error_rel_abs = result.goodness_per_derivative[
            derivative
        ].error_rel_abs

        ymin = min(
            ymin,
            _np.amin(error_rel_abs["p15_9"][error_rel_abs["p15_9"] > 0.0]),
        )

        ax.fill_between(
            result.ticks,
            error_rel_abs["p15_9"],
            error_rel_abs["p84_1"],
            alpha=0.2,
        )
        ax.plot(result.ticks, error_rel_abs["p50"], label=derivative)

    ax.set_xlabel(result.label)
    ax.set_xticks(_np.arange(len(result.ticks)))
    ax.set_xticklabels(result.ticks, rotation=-45)
    ax.set_ylabel(
        rf"|{key.variable} - {key.variable}$_{{c}}$| / |{key.variable}|"
    )
    ax.set_yscale("symlog", linthresh=ymin, linscale=1.0)
    ax.set_ylim(-ymin / 2, ax.get_ylim()[1] * 2)
    ax.format(yformatter="log")

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_compression_goodness_uniformity(
    key: ResultKey, result: CompressorResult, ax=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig, ax = ax.get_figure(), ax

    if show:
        ax.set_title(
            f"Compression Uniformity Goodness\n{key.variable}: "
            f"{key.variable_long}\n{key.dataset}"
        )
    else:
        ax.set_title("Compression Uniformity Goodness")

    for derivative in result.goodness_per_derivative.keys():
        uniformity = result.goodness_per_derivative[derivative].uniformity

        ax.fill_between(
            result.ticks, uniformity["p15_9"], uniformity["p84_1"], alpha=0.2
        )
        p = ax.plot(result.ticks, uniformity["p50"], label=derivative)

        xlim = ax.get_xlim()

        max_x = _np.argmax(uniformity["p50"])
        ax.axvline(
            x=max_x,
            ymax=uniformity["p50"][max_x] / 1.1 + 0.05,
            c=p[0].get_color(),
            ls=":",
        )
        ax.axhline(
            y=uniformity["p50"][max_x],
            xmax=(max_x - xlim[0]) / (xlim[1] - xlim[0]),
            c=p[0].get_color(),
            ls=":",
        )
        ax.plot(
            max_x, uniformity["p50"][max_x], marker="x", color=p[0].get_color()
        )

    ax.set_xlabel(result.label)
    ax.set_xticks(_np.arange(len(result.ticks)))
    ax.set_xticklabels(result.ticks, rotation=-45)
    ax.set_ylabel("uniformity score")
    ax.set_ylim(-0.05, 1.05)
    ax.format(yformatter=_mtick.PercentFormatter(1.0))

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_compression_goodness_preserved_pca(
    key: ResultKey, result: CompressorResult, ax=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig, ax = ax.get_figure(), ax

    if show:
        ax.set_title(
            "Compression Preserved Principal Components Goodness\n"
            f"{key.variable}: {key.variable_long}\n{key.dataset}"
        )
    else:
        ax.set_title("Compression Preserved Principal Components Goodness")

    for derivative in result.goodness_per_derivative.keys():
        preserved_pca = result.goodness_per_derivative[
            derivative
        ].preserved_pca

        ax.fill_between(
            result.ticks,
            preserved_pca["p15_9"],
            preserved_pca["p84_1"],
            alpha=0.2,
        )
        ax.plot(result.ticks, preserved_pca["p50"], label=derivative)

    ax.set_xlabel(result.label)
    ax.set_xticks(_np.arange(len(result.ticks)))
    ax.set_xticklabels(result.ticks, rotation=-45)
    ax.set_ylabel("fraction of preserved PCs")
    ax.set_ylim(-0.05, 1.05)
    ax.format(yformatter=_mtick.PercentFormatter(1.0))

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_compression_goodness_bit_information(
    key: ResultKey, result: CompressorResult, ax=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig, ax = ax.get_figure(), ax

    if show:
        ax.set_title(
            f"Compression BitInformation Goodness\n{key.variable}: "
            f"{key.variable_long}\n{key.dataset}"
        )
    else:
        ax.set_title("Compression BitInformation Goodness")

    for derivative in result.goodness_per_derivative.keys():
        bit_information = result.goodness_per_derivative[
            derivative
        ].bit_information

        ax.fill_between(
            result.ticks,
            bit_information["p15_9"],
            bit_information["p84_1"],
            alpha=0.2,
        )
        ax.plot(result.ticks, bit_information["p50"], label=derivative)

    ax.set_xlabel(result.label)
    ax.set_xticks(_np.arange(len(result.ticks)))
    ax.set_xticklabels(result.ticks, rotation=-45)
    ax.set_ylabel("preserved information content")
    ax.set_ylim(-0.05, 1.05)
    ax.format(yformatter=_mtick.PercentFormatter(1.0))

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_dataset_variable_compressor_card(
    key: ResultKey, result: CompressorResult
):
    fig = _plt.figure(refaspect=2, refwidth=5, sharex=False, sharey=False)
    ax1, ax2, ax3, ax4, ax5, ax6, ax7 = fig.subplots(nrows=7, ncols=1)

    fig.format(
        suptitle=(
            f"{key.variable}: {key.variable_long}\n{key.dataset}\n\n"
            f"{result.label}"
        )
    )

    plot_compression_ratio_performance_instructions(key, result, ax=ax1)
    ax1.set_xlabel(None)

    plot_compression_ratio_performance_throughput(key, result, ax=ax2)
    ax2.set_xlabel(None)

    plot_absolute_compression_error(key, result, ax=ax3)
    ax3.set_xlabel(None)
    ax3.legend(loc="bottom")

    plot_absolute_relative_compression_error(key, result, ax=ax4)
    ax4.set_xlabel(None)
    ax4.legend(loc="bottom")

    plot_compression_goodness_uniformity(key, result, ax=ax5)
    ax5.set_xlabel(None)
    ax5.legend(loc="bottom")

    plot_compression_goodness_preserved_pca(key, result, ax=ax6)
    ax6.set_xlabel(None)
    ax6.legend(loc="bottom")

    plot_compression_goodness_bit_information(key, result, ax=ax7)
    ax7.set_xlabel(None)

    _plt.show()


def plot_performance_comparison_instructions(
    results: dict[ResultKey, CompressorResult], ax=None, cycle=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    ax.set_title("Compression Performance Comparison [universal]")

    for key, result in results.items():
        ax.plot(
            result.performance.instructions["p50"],
            result.performance.compression_ratio["p50"],
            label=f"{key.variable} x {key.compressor}",
            cycle=cycle,
        )

    ax.set_ylabel("original size / compressed size")
    ax.set_yscale("log")
    ax.format(yformatter="log")
    ax.set_xlabel("Compression-Decompression Instructions [#/B]")
    x_span = max(*ax.get_xlim()) - min(*ax.get_xlim())
    ax.set_xlim(
        max(*ax.get_xlim()) + x_span * 0.025,
        min(*ax.get_xlim()) - x_span * 0.025,
    )

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_performance_comparison_throughput(
    results: dict[ResultKey, CompressorResult], ax=None, cycle=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    ax.set_title("Compression Performance Comparison [measurement]")

    for key, result in results.items():
        ax.plot(
            result.performance.throughput["p50"],
            result.performance.compression_ratio["p50"],
            label=f"{key.variable} x {key.compressor}",
            cycle=cycle,
        )

    ax.set_ylabel("original size / compressed size")
    ax.set_yscale("log")
    ax.format(yformatter="log")
    ax.set_xlabel("Compression-Decompression Throughput [B/s]")
    x_span = max(*ax.get_xlim()) - min(*ax.get_xlim())
    ax.set_xlim(
        min(*ax.get_xlim()) - x_span * 0.025,
        max(*ax.get_xlim()) + x_span * 0.025,
    )

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_absolute_compression_error_comparison(
    results: dict[ResultKey, CompressorResult], ax=None, cycle=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    ax.set_title("Absolute Compression Error Comparison")

    ymin = 1.0

    for key, result in results.items():
        error_abs = result.goodness_per_derivative[key.variable].error_abs

        ymin = min(ymin, _np.amin(error_abs["p50"][error_abs["p50"] > 0.0]))

        ax.plot(
            error_abs["p50"],
            result.performance.compression_ratio["p50"],
            label=f"{key.variable} x {key.compressor}",
            cycle=cycle,
        )

    ax.set_ylabel("original size / compressed size")
    ax.set_yscale("log")
    ax.format(yformatter="log")
    ax.set_xlabel(r"|x - x$_{c}$|")
    ax.set_xscale("symlog", linthresh=ymin, linscale=1.0)
    ax.set_xlim(max(*ax.get_xlim()) * 2, -ymin / 2)
    ax.format(xformatter="log")

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_absolute_relative_compression_error_comparison(
    results: dict[ResultKey, CompressorResult], ax=None, cycle=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    ax.set_title("abs(Relative) Compression Error Comparison")

    ymin = 1.0

    for key, result in results.items():
        error_rel_abs = result.goodness_per_derivative[
            key.variable
        ].error_rel_abs

        ymin = min(
            ymin, _np.amin(error_rel_abs["p50"][error_rel_abs["p50"] > 0.0])
        )

        ax.plot(
            error_rel_abs["p50"],
            result.performance.compression_ratio["p50"],
            label=f"{key.variable} x {key.compressor}",
            cycle=cycle,
        )

    ax.set_ylabel("original size / compressed size")
    ax.set_yscale("log")
    ax.format(yformatter="log")
    ax.set_xlabel(r"|x - x$_{c}$| / |x|")
    ax.set_xscale("symlog", linthresh=ymin, linscale=1.0)
    ax.set_xlim(max(*ax.get_xlim()) * 2, -ymin / 2)
    ax.format(xformatter="log")

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_compression_goodness_uniformity_comparison(
    results: dict[ResultKey, CompressorResult], ax=None, cycle=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    ax.set_title("Compression Uniformity Goodness Comparison")

    for key, result in results.items():
        uniformity = result.goodness_per_derivative[key.variable].uniformity

        ax.plot(
            uniformity["p50"],
            result.performance.compression_ratio["p50"],
            label=f"{key.variable} x {key.compressor}",
            cycle=cycle,
        )

    ax.set_ylabel("original size / compressed size")
    ax.set_yscale("log")
    ax.format(yformatter="log")
    ax.set_xlabel("uniformity score")
    ax.set_xlim(-0.02, 1.02)
    ax.format(xformatter=_mtick.PercentFormatter(1.0))

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_compression_goodness_preserved_pca_comparison(
    results: dict[ResultKey, CompressorResult], ax=None, cycle=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    ax.set_title(
        "Compression Preserved Principal Components Goodness Comparison"
    )

    for key, result in results.items():
        preserved_pca = result.goodness_per_derivative[
            key.variable
        ].preserved_pca

        ax.plot(
            preserved_pca["p50"],
            result.performance.compression_ratio["p50"],
            label=f"{key.variable} x {key.compressor}",
            cycle=cycle,
        )

    ax.set_ylabel("original size / compressed size")
    ax.set_yscale("log")
    ax.format(yformatter="log")
    ax.set_xlabel("fraction of preserved PCs")
    ax.set_xlim(-0.02, 1.02)
    ax.format(xformatter=_mtick.PercentFormatter(1.0))

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_compression_goodness_bitinformation_comparison(
    results: dict[ResultKey, CompressorResult], ax=None, cycle=None
):
    show = ax is None
    if ax is None:
        fig, ax = _plt.subplots(figsize=(6, 4))
    else:
        fig = ax.get_figure()

    ax.set_title("Compression BitInformation Goodness Comparison")

    for key, result in results.items():
        bit_information = result.goodness_per_derivative[
            key.variable
        ].bit_information

        ax.plot(
            bit_information["p50"],
            result.performance.compression_ratio["p50"],
            label=f"{key.variable} x {key.compressor}",
            cycle=cycle,
        )

    ax.set_ylabel("original size / compressed size")
    ax.set_yscale("log")
    ax.format(yformatter="log")
    ax.set_xlabel("preserved information content")
    ax.set_xlim(-0.02, 1.02)
    ax.format(xformatter=_mtick.PercentFormatter(1.0))

    if show:
        fig.legend(loc="bottom")
        _plt.show()


def plot_cross_dataset_compressor_default_derivative_comparison(
    results: dict[ResultKey, CompressorResult], cycle=None
):
    fig = _plt.figure(refaspect=2, refwidth=5, sharex=False, sharey=False)
    ax1, ax2, ax3, ax4, ax5, ax6, ax7 = fig.subplots(nrows=7, ncols=1)

    fig.format(
        suptitle=(
            "Comparison of Compressors across Variables\n(top right is best)"
        )
    )

    plot_performance_comparison_instructions(results, ax=ax1, cycle=cycle)
    ax1.legend(loc="bottom")

    plot_performance_comparison_throughput(results, ax=ax2, cycle=cycle)
    ax2.legend(loc="bottom")

    plot_absolute_compression_error_comparison(results, ax=ax3, cycle=cycle)
    ax3.legend(loc="bottom")

    plot_absolute_relative_compression_error_comparison(
        results, ax=ax4, cycle=cycle
    )
    ax4.legend(loc="bottom")

    plot_compression_goodness_uniformity_comparison(
        results, ax=ax5, cycle=cycle
    )
    ax5.legend(loc="bottom")

    plot_compression_goodness_preserved_pca_comparison(
        results, ax=ax6, cycle=cycle
    )
    ax6.legend(loc="bottom")

    plot_compression_goodness_bitinformation_comparison(
        results, ax=ax7, cycle=cycle
    )

    _plt.show()
