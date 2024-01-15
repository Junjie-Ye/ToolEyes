#!/bin/bash
python Code/Evaluation/eval_pipeline.py \
    --input_file_path  Code/Evaluation/inference_results/test.json\
    --eval_output_path Code/Evaluation/evaluation_results\
    --gpt4_key \
    --radar_fig_output_path Code/Evaluation/evaluation_results/radar_fig\
    --result_tab_output_path Code/Evaluation/evaluation_results/result_tab\