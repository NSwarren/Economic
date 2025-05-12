import os
from pathlib import Path
import metrics.integration_accuracy as accuracy
from argparse import Namespace

def list_files(inputPath):
    path = Path(inputPath)
    if not path.exists() or not path.is_dir():
        print(f"Invalid directory: {inputPath}")
        return []
    list = [os.path.join(inputPath, item.name) for item in path.iterdir() if item.is_file()]
    return list


def simulate_script_call(path, datasets, latents, output):
    datasetsPath = os.path.join(path, "datasets",datasets)
    datasetsList = list_files(datasetsPath)
    latentsPath = os.path.join(path, "latents", latents)
    latentsList = list_files(latentsPath)

    outputPath = os.path.join(path, "output", output)

    if len(datasetsList) == 0 or len(latentsList) == 0:
        return

    args = {
        "datasets": datasetsList,
        "latents": latentsList,
        # "cell_type": "cell_type",
        # "domain": "batch",
        # "paired": False,
        "output": outputPath
    }
    args_namespace = Namespace(**args)
    accuracy.main(args_namespace)


if __name__ == "__main__":
    path = "F:\workplace\Economic\data\\"

    simulate_script_call(path, "Multiome", "scGPT", "output_metrics.yaml")