import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


BASE_DIR = "output"  
ANALYSIS_FILENAME = "analysis"
OUTPUT_FILE = "analysis_plot.png"

def read_numbers(path):
    nums = []
    with open(path, "r") as f:
        for line in f:
            nums.append(int(line))
    return nums


def main():
    plt.figure(figsize=(10, 6))

    for root, dirs, files in os.walk(BASE_DIR):
        if ANALYSIS_FILENAME in files:
            file_path = os.path.join(root, ANALYSIS_FILENAME)
            numbers = read_numbers(file_path)
            if not numbers:
                continue

            label = os.path.relpath(file_path, BASE_DIR)
            plt.plot(range(1, len(numbers) + 1), numbers, label=label)


    plt.title("Search space reduction across iterations")
    plt.xlabel("Iteration")
    plt.ylabel("Number of solutions left after adding blocking constraints")
    plt.tight_layout()
    plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    plt.savefig(OUTPUT_FILE)
    

    print(f"Plot saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
