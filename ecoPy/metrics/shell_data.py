import os
import yaml
import subprocess
import pandas as pd

path = "./data/output/"
filename = "output_metrics.yaml"
datatype = ""

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

def writeToCsv(data, filename):
    df = pd.DataFrame({key: [value] for key, value in data.items()})
    if not os.path.exists(filename):
        df.to_csv(filename, index=False, encoding='utf-8')
    else:
        df.to_csv(filename, mode='a', index=False, header=False, encoding='utf-8')
    
    print(f"Data '{data['name']}' appended to '{filename}' successfully.")
    

def readYaml(path, filename, latents, datasets, object_type):
    typeFile = {
        "Integration Accuracy" : "integration_accuracy.csv"
    }
    file = os.path.join(path, filename)
    try:
        with open(file, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            config['name'] = latents
            config['object_type'] = object_type
            config['datasets'] = datasets
            writeToCsv(config, os.path.join(path, typeFile[object_type]))
    except FileNotFoundError:
        print("The file does not exist.")
    except yaml.YAMLError as e:
        print(f"Error in YAML file: {e}")

def readXlsx(path, filename):
    file = os.path.join(path, filename)
    df = pd.read_excel(file, engine='openpyxl')
    print(df)

if __name__ == "__main__":
    #runShell(path, "run_integration.sh")
    #readYaml(path, "output_metrics.yaml","temp", "temp", "Integration Accuracy")
    readXlsx(path, "Extended_Data_2_inteaccu.xlsx")