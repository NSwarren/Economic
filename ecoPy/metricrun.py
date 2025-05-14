import os
import pandas as pd
from pathlib import Path
from argparse import Namespace
import subprocess
import metrics.integration_accuracy as accuracy
import metrics.batch_effect_correction as correction
import metrics.biomarker as biomarker
import metrics.trajectory as trajectory


trajectory_dict = {
    "Chen-2019" : "OliI",
    "Ma-2020" : "Basal",
    "Yao-2021" : "NP",
    "Muto-2021" : "MES_FIB",
    "Multiome" : "HSPC"
}

def writeToCsv(data, filename):
    df = pd.DataFrame({key: [value] for key, value in data.items()})
    if not os.path.exists(filename):
        df.to_csv(filename, index=False, encoding='utf-8')
    else:
        df.to_csv(filename, mode='a', index=False, header=False, encoding='utf-8')
    
    print(f"Data '{data['name']}' appended to '{filename}' successfully.")
    
def accuracy_simulate(path, datasets, latents, output):
    datasetsPath = os.path.join(path, "datasets",datasets)
    #datasetss = os.listdir(datasetsPath)
    datasetsList = [os.path.join(datasetsPath, datasets + "-RNA_uni.h5ad"),
                    os.path.join(datasetsPath, datasets + "-ATAC_uni.h5ad")]
    latentsPath = os.path.join(path, "latents", latents)
    latentss = os.listdir(latentsPath)
    latentsList = [os.path.join(latentsPath, f) for f in latentss]

    outputPath = Path(os.path.join(path, "output/data", output))

    if len(datasetsList) == 0 or len(latentsList) == 0:
        return

    args = {
        "datasets": datasetsList,
        "latents": latentsList,
        "cell_type": "cell_type",
        "domain": "domain",
        "paired": "store_true",
        "output": outputPath
    }
    
    acc = accuracy.main(Namespace(**args))
    acc['name'] = latents
    acc['object_type'] = "Integration Accuracy"
    acc['datasets'] = datasets
    writeToCsv(acc, os.path.join(path, "output/data/integration_accuracy.csv"))

def batch_simulate(path, datasets, latents, output):
    datasetsPath = os.path.join(path, "datasets",datasets)
    datasetss = os.listdir(datasetsPath)
    datasetsList = [os.path.join(datasetsPath, f) for f in datasetss]
    latentsPath = os.path.join(path, "latents", latents)
    latentss = os.listdir(latentsPath)
    latentsList = [os.path.join(latentsPath, f) for f in latentss]

    outputPath = Path(os.path.join(path, "output/data", output))

    if len(datasetsList) == 0 or len(latentsList) == 0:
        return

    args = {
        "datasets": datasetsList,
        "latents": latentsList,
        "cell_type": "cell_type",
        "domain": "domain",
        "paired": False,
        "output": outputPath
    }

    corr = correction.main(Namespace(**args))
    corr['name'] = latents
    corr['object_type'] = "Batch Effect"
    corr['datasets'] = datasets
    writeToCsv(corr, os.path.join(path, "output/data/batch_correction.csv"))

def trajectory_simulate(path, datasets, latents, output):
    datasetsPath = os.path.join(path, "datasets",datasets)
    datasetss = os.listdir(datasetsPath)
    datasetsList = [os.path.join(datasetsPath, f) for f in datasetss]
    latentsPath = os.path.join(path, "latents", latents)
    latentss = os.listdir(latentsPath)
    latentsList = [os.path.join(latentsPath, f) for f in latentss]

    outputPath = Path(os.path.join(path, "output/data", output))
    combPath = Path(os.path.join(path, "output/data/trajectory_comb", "raw_combine_traj.h5ad"))

    if len(datasetsList) == 0 or len(latentsList) == 0:
        return
    
    args = {
        "datasets": datasetsList,
        "latents": latentsList,
        "root": trajectory_dict.get(datasets),
        "branch": "",
        "branch_name": "",
        "comb_data": "",
        "output": outputPath
    }
    eff = trajectory.main(Namespace(**args))
    eff['name'] = latents
    eff['object_type'] = "Trajectory"
    eff['datasets'] = datasets
    writeToCsv(eff, os.path.join(path, "output/data/trajectory.csv"))

def biomarker_simulate(path, biotype, datasets, latents,  output):
    datasetsPath = os.path.join(path, "datasets", datasets, datasets + "-RNA.h5ad")
    latentsPath = os.path.join(path, "embeddings", datasets)
    # latentss = os.listdir(latentsPath)
    # latentsList = [os.path.join(latentsPath, f) for f in latentss]
    outputPath = Path(os.path.join(path, "output/data", output))

    # methods = os.path.join(path, "embeddings")

    method = ["scVI", "GLUE", "LIGER", "TotalVI", "UnionCom", "scMoMaT", "MMD_MA", 
              "Deepmaps", "Cobolt", "scMDC", "bindsc", "Pamona", "PCA", "scJoint", 
              "seurat4", "seurat5", "iNMF", "MOFA", "Harmony", "UCE", "FM_scvi"]

    #method = [latents]
    # methodss = os.listdir(methods)
    # methodsList = [os.path.join(methods, f) for f in methodss]

    # if len(datasetsList) == 0 or len(latentsList) == 0:
    #     return
    
    args = {
        "datasets": [datasetsPath],
        "latent_dir": latentsPath,
        "methods": method,
        "mode": biotype,
        "cell_type": "cell_type",
        "domain": "domain",
        "paired": "",
        "output_dir": outputPath
    }
    cos = biomarker.main(Namespace(**args))
    cos['name'] = latents
    cos['object_type'] = "Biomarker DARs"

    if "rna" == biotype:
        cos['mode'] = "Biomarker"
    else:
        cos['mode'] = "Atac Level"
    cos['datasets'] = datasets
    writeToCsv(cos, os.path.join(path, "output/biomarker_dars.csv"))    

def runShell(path, name):
    datasetsPath = os.path.join(path, name)
    result = subprocess.run(
        [datasetsPath],  # 直接执行脚本（需有可执行权限）
        capture_output=True,  # 捕获标准输出和错误
        text=True,           # 以文本形式返回结果
        check=True           # 检查命令是否成功，失败时抛出异常
    )

    print("标准输出:", result.stdout)
    print("错误输出:", result.stderr)
    print("返回码:", result.returncode)


if __name__ == "__main__":
    path = "./data/"
    #runShell(path, "run_integration.sh")
    accuracy_simulate(path, "10x-Multiome-Pbmc10k-small", "scGPT", "output_metrics.yaml")
    #batch_simulate(path, "Multiome", "scGPT", "output_metrics.yaml")
    #trajectory_simulate(path, "Multiome", "scGPT", "output_metrics.yaml")
    #biomarker_simulate(path, "rna", "10x-Multiome-Pbmc10k-small", "scGPT", "output_metrics.yaml")