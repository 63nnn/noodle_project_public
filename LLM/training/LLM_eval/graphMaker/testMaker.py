import matplotlib.pyplot as plt
import csv


def find_csv(target):
    csv_file_path = [
        f"{dir_data_source}{target}_A.csv",
        f"{dir_data_source}{target}_B.csv",
    ]
    return csv_file_path


# 範例資料


import matplotlib.pyplot as plt

dir_output = "./"


def graph_maker(bar_data, line_data, graph_name):
    plt.rcParams["font.family"] = "Times New Roman"

    # 創建圖表
    fig, ax1 = plt.subplots(figsize=(7, 9))  # 調整大小為水平圖表比例

    bar_colors = [(135 / 255, 206 / 255, 250 / 255)] * len(models)
    line_color = (0 / 255, 0 / 255, 0 / 255)

    # 繪製垂直長條圖
    ax1.bar(models, bar_data, color=bar_colors)
    ax1.set_ylabel("F1 score")  # 調整為 y 軸標籤
    ax1.set_title(graph_name)
    ax1.grid(axis="y", linestyle="--", alpha=0.7)

    # 顯示每個長條的數值
    for index, value in enumerate(bar_data):
        ax1.text(
            index, value, f"{value:.4}", ha="center", va="bottom"
        )  # 調整文字顯示位置

    # 創建第二個軸，繪製折線圖
    ax2 = ax1.twinx()  # 改用 twin x 軸，與垂直長條圖保持一致
    ax2.plot(
        models,
        line_data,
        color=line_color,
        marker="o",
        label="Line Plot",
        linestyle="-",
        linewidth=2,
    )
    ax2.set_ylabel("Performance Improvement(%)")

    # 調整佈局，防止重疊
    plt.tight_layout()

    # 保存圖表為圖片檔案
    output_filename = f"{dir_output}{graph_name}"
    plt.savefig(f"{output_filename}.png", format="png")

    # 顯示圖表
    plt.show()


models = ["Model A", "Model B", "Model C", "Model D"]
accuracy = [0.85, 0.78, 0.92, 0.88]
line_data = [0.9, 0.82, 0.95, 0.89]

graph_maker(accuracy, line_data, "test")
