export CUDA_VISIBLE_DEVICES=4
export PYTHONPATH=./

python /workspace/ToolEyes/Code/Inference/inference_pipeline.py \
    --backbone_model tool \
    --model_path /mnt/data/models/pretrain_models/Llama-2/hf/Llama-2-7b-chat-hf \
    --max_observation_length 1024 \
    --method tool \
    --input_query_file /workspace/ToolEyes/Test_Data/scenario_data_processed.json \
    --output_answer_file ./test_result.jsonl \
    --max_turn 8