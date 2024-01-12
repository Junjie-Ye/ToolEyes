import sys
import argparse
from inference import pipeline_runner
import os


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_query_file', type=str,
                        default="",
                        required=True, help='input path')
    parser.add_argument('--output_answer_file', type=str,
                        default="./test.jsonl", required=False, help='output path')
    parser.add_argument('--model_path', type=str,
                        default="",
                        required=True, help='')
    parser.add_argument('--backbone_model', type=str, default="tool",
                        required=False)
    parser.add_argument("--lora", action="store_true",
                        help="Load lora model or not.")
    parser.add_argument('--lora_path', type=str,
                        default="your_lora_path if lora", required=False, help='')
    parser.add_argument('--max_observation_length', type=int,
                        default=1024, required=False, help='maximum observation length')
    parser.add_argument('--max_source_sequence_length', type=int, default=4096,
                        required=False, help='original maximum model sequence length')
    parser.add_argument('--max_sequence_length', type=int, default=8192,
                        required=False, help='maximum model sequence length')
    parser.add_argument('--method', type=str, default="tool", choices=["tool", "general"], required=False,
                        help='method for answer generation: tool, general')
    parser.add_argument('--max_turn', type=int,
                        default=8, required=False),
    parser.add_argument('--history_sample', type=int,
                        default=1, required=False),
    parser.add_argument('--api_key', type=str,
                        default=None, required=False)
    parser.add_argument('--orgnization', type=str,
                        default=None, required=False)
    parser.add_argument('--url', type=str,
                        default=None, required=False)
    parser.add_argument('--mode', type=str,
                        default=None, required=False)
    parser.add_argument('--openai_model', type=str,
                        default=None, required=False)
    parser.add_argument('--proxy', type=str,
                        default="127.0.0.1:7890", required=False)

    args = parser.parse_args()

    os.environ['http_proxy'] = args.proxy
    os.environ['https_proxy'] = args.proxy

    pipeline_runner = pipeline_runner(args)
    pipeline_runner.run()
