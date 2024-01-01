# ToolEyes

## ToolEyes: Fine-Grained Evaluation for Tool Learning Capabilities of Large Language Models in Real-world Scenarios

> Data for paper "ToolEyes: Fine-Grained Evaluation for Tool Learning Capabilities of Large Language Models in Real-world Scenarios"

Junjie Ye

jjye23@m.fudan.edu.cn

Jan. 01, 2024

## Requirement
- Run the command to install the packages required.
    ```bash
    pip install -r requirements.txt
    ```

## Data
The tool lobrary and test data are released, which can be found in `ToolEyes/Tool_Library` and `/ToolEyes/Test_Data`, respectively. Below is the statistics of the data:

| **Scenario**      | **TG** | **DU** | **RS** | **PL** | **IR** | **AM** | **FT** | **Total** |
|-------------------|--------|--------|--------|--------|--------|--------|--------|-----------|
| **# Cat**         | 5      | 5      | 6      | 8      | 9      | 6      | 2      | 41        |
| **# Subcat**      | 6      | 5      | 14     | 30     | 19     | 7      | 14     | 95        |
| **# Tool**        | 27     | 26     | 75     | 164    | 150    | 164    | 96     | 568       |
| **# Query**       | 58     | 49     | 56     | 70     | 54     | 45     | 50     | 382       |
