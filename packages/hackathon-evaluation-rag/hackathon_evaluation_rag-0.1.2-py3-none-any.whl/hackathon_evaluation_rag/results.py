import os
import matplotlib.pyplot as plt
from hackathon_evaluation_rag.config import RESULTS


def plot_metrics_with_values(metrics_dict, title="RAG Metrics"):
    """
    Plots a bar chart for metrics contained in a dictionary and annotates the values on the bars.

    Args:
    metrics_dict (dict): A dictionary with metric names as keys and values as metric scores.
    title (str): The title of the plot.
    """
    names = list(metrics_dict.keys())
    values = list(metrics_dict.values())

    plt.figure(figsize=(15, 10))
    bars = plt.barh(names, values, color="skyblue")

    # Adding the values on top of the bars
    for bar in bars:
        width = bar.get_width()
        plt.text(
            width + 0.01,  # x-position
            bar.get_y() + bar.get_height() / 2,  # y-position
            f"{width:.4f}",  # value
            va="center",
        )

    plt.xlabel("Score")
    plt.title(title)
    plt.xlim(0, 1)
    plt.savefig(f"{RESULTS}/metrics.png")


def save_results(result):
    if not os.path.exists(f"{RESULTS}"):
        os.makedirs(f"{RESULTS}")

    df = result.to_pandas()

    df.to_csv(f"{RESULTS}/result.csv")
    print(f"---Results saved to `{RESULTS}/result.csv`---")

    plot_metrics_with_values(result)
