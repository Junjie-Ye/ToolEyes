import os, json
import argparse


def process_infer_zero(src, trg, sys):
    with open(src, 'r', encoding='utf8') as f:
        target = []
        data = json.load(f)
        sample = {}
        for item in data:
            sample["id"] = f"Turn 1: {item['query']}"

            with open(os.path.join(item["path"], "config_gpt4.json"), 'r', encoding='utf8') as c:
                config = json.load(c)
            with open(sys, 'r', encoding='utf8') as s:
                value = s.read().replace('{Tool Document}', json.dumps(config))
            sample["conversations"] = [{"from": "system", "value": value},
                                       {"from": "user", "value": item["query"]}]
            sample["path"] = item["path"]
            sample["scenario"] = item["scenario"]

            target.append(sample.copy())
    
    with open(trg, 'w', encoding='utf8') as f:
        json.dump(target, f, ensure_ascii=False)


def process_infer_five(src, trg, sys, examples):
    with open(src, 'r', encoding='utf8') as f:
        target = []
        data = json.load(f)
        sample = {}
        for item in data:
            sample["id"] = f"Turn 1: {item['query']}"

            with open(os.path.join(item["path"], "config_gpt4.json"), 'r', encoding='utf8') as c:
                config = json.load(c)
            with open(sys, 'r', encoding='utf8') as s:
                value = s.read().replace('{Tool Document}', json.dumps(config))
            with open(examples, 'r', encoding='utf8') as e:
                value = value.replace('{examples}', e.read())
            sample["conversations"] = [{"from": "system", "value": value},
                                       {"from": "user", "value": item["query"]}]
            sample["path"] = item["path"]
            sample["scenario"] = item["scenario"]

            target.append(sample.copy())
    
    with open(trg, 'w', encoding='utf8') as f:
        json.dump(target, f, ensure_ascii=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src_path', required=True, type=str)
    parser.add_argument('--trg_path', required=True, type=str)
    parser.add_argument('--sys_path', required=True, type=str)
    parser.add_argument('--mode', required=True, type=str, choices=['zero', 'few'])
    parser.add_argument('--example_path', required=False, type=str)
    args = parser.parse_args()

    if args.mode == 'zero':
        process_infer_zero(args.src_path, args.trg_path, args.sys_path)
    elif args.mode == 'few':
        process_infer_five(args.src_path, args.trg_path, args.sys_path, args.example_path)
