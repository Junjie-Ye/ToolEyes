from util.utils import *
import jsonlines
import json
import argparse
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from util.process_utils import *
import copy
def get_all_data(infer_res_path):
    root_path =  os.getcwd()
    root_path = os.path.join(root_path,infer_res_path)
    data_path = root_path
    path = infer_res_path
    data_list = []
    if 'wo_demo' not in path and 'tuned' not in path and ('vicuna' in path or 'text_davinci' in path or 'Llama2chat' in path):
        use_demon = True
    else:
        use_demon = False
    infer_res_data = json.load(open(data_path,'r'))
    #infer_res_data = jsonlines.open(data_path)
    sample_res = []
    for data in infer_res_data:
        res = get_all_res(data,use_demon=use_demon)
        sample_res.append(res)
        res['id'] = data['id']
        res['path'] = data['path']
        data_list.append(res)
    return data_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file_path', type=str,
                        default="test_input.json",
                        required=True, help='input data path')
    parser.add_argument('--eval_output_path', type=str,
                        default="Code/Evaluation/evaluation_results", required=False, help='output path of evaluation result')
    parser.add_argument('--gpt4_key', type=str,
                        required=True,default='', help='Your openai key')
    parser.add_argument('--radar_fig_output_path', type=str,
                        default="Code/Evaluation/evaluation_results/radar_fig", required=False, help='output path of radar figures')
    parser.add_argument('--result_tab_output_path', type=str,
                        default="Code/Evaluation/evaluation_results/result_tab",
                        required=False, help='output path of model performance statistics')
    parser.add_argument('--result_stat_required', type=str,
                    default=True,
                    required=False, help='')
    parser.add_argument('--radar_fig_required', type=str,
                    default=True,
                    required=False, help='')

    args = parser.parse_args()
    model_name = args.input_file_path.split('/')[-1].split('.json')[0]
    eval_data_path = args.input_file_path
    print('Formatting inference data')
    data = get_all_data(eval_data_path)
    
    print('Evaluating inference data')
    all_model_eval_res = model_eval(data,model_name,args)
    print('Evaluation is over')

    # categorizing data
    tool_category = {
        'TG':['Advice','Faker','Joke','Random','Translation'],
        'RS':['Calendar','News','Paper','Search','Trend','Weather'],
        'DU':['Comparison','NLP','Predict','Validation','Word'],
        'PL':['Entertainment','Food','Health','Job','Location','Music','Product','Travel'],
        'AM':['Calculator','Execute','File','Mail','URL','Zapier'],
        'IR':['Animal','Anti_Malware','Art','Competition','Database','Entity','IP','Social','Vehicle'],
        'FT':['Finance','Stock']
    }

    stats_scenario = {}
    stats_detailed = {}
    stats_scen_diff = {}
    scen_data_detailed = {}

    model_data = all_model_eval_res
    app_data_id_dict = {
    'TG':[],
    'RS':[],
    'DU':[],
    'PL':[],
    'AM':[],
    'IR':[],
    'FT':[]
    }
    for data in json.load(open(args.input_file_path,'r')):
        data_scen= data['scenario']
        if data['id'] not in app_data_id_dict[data_scen]:
            app_data_id_dict[data_scen].append(data['id'])
    stats_all = []
    stats_scenario = {}
    stats_detailed = {}

    print('Analysing evalution results')
    stats_scenario ,stats_detailed, scen_data_detailed = aggregated_data(model_data, copy.deepcopy(app_data_id_dict), args, model_name)

    if args.radar_fig_required:
        # plot radar fig for different scen
        for scen in tool_category.keys():
            plot_radar_single_scen(scen_data_detailed, scen, model_name, args)
        
    if args.result_stat_required:
        #all scenarios tab
        import pandas as pd
        df = pd.DataFrame([stats_detailed])
        df.to_excel(f'{args.result_tab_output_path}/{model_name}_all_scen_summary.xlsx')

        #overall score of different scenarios tab
        import pandas as pd
        df = pd.DataFrame([stats_scenario])
        df.to_excel(f'{args.result_tab_output_path}/{model_name}_diff_scen_summary.xlsx')
    print('Analysing over')