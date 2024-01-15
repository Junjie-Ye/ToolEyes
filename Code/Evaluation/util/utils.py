import re
import jsonlines
import numpy as np
import copy
import os
os.sys.path.append('ToolEyes/Code/Evaluation/util')
from util.gpt_request import *
from util.process_utils import *
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
model_map = {
    'LLaMA-2-chat':'LLaMA-2-chat-7B',
    'llama_chat_13b':'LLaMA-2-chat-13B',
    'llama_chat_70b':'LLaMA-2-chat-70B',
    'Vicuna-1.5':'Vicuna-1.5-7B',
    'vicuna13b':'Vicuna-1.5-13B',
    'ToolLLaMA v1':'ToolLLaMA-2-7B-v1',
    'ToolLLaMA v2':'ToolLLaMA-2-7B-v2',
    'Text-davinci-003':'Text-davinvi-003',
    'GPT-3.5-turbo':'GPT-3.5-turbo',
    'GPT-4':'GPT-4'
}

tool_category = {
    'TG':['Advice','Faker','Joke','Random','Translation'],
    'RS':['Calendar','News','Paper','Search','Trend','Weather'],
    'DU':['Comparison','NLP','Predict','Validation','Word'],
    'PL':['Entertainment','Food','Health','Job','Location','Music','Product','Travel'],
    'AM':['Calculator','Execute','File','Mail','URL','Zapier'],
    'IR':['Animal','Anti_Malware','Art','Competition','Database','Entity','IP','Social','Vehicle'],
    'FT':['Finance','Stock']
}

def structuring_data(single_eval_data,raw_data,scenario,valid_TS):

    key_map = {
        'FA':'IF','IC':'IU','BP':'BP','TS':'TS','AO':'AO',
        'IC_memory':'thought_foucus',
        'BP_quality':'thought_quality',
        'BP_validity':'thought_validity',
        'valid_TS_mean':'action_thought_match',
        'Ans_quality':'relavance'
    }

    score_structure = {
        'FA':{
            'rule':['IF'],
            'GPT4':[]
        },
        'IC':{
            'rule':[],
            'GPT4':['IC_memory']
        },
        'TS':{
            'rule':['tool_reality'],
            'GPT4':['valid_TS_mean']
        },
        'BP':{
            'rule':[],
            'GPT4':['BP_validity','BP_quality']
        },
        'AO':{
            'rule':['Ans_pass'],
            'GPT4':['Ans_quality']
        }
    }

    '''
    Structure of output:
    {
        'id':
        'scenario':
        'first level score':{
            'score for criteria':,
            'score composition':
                [
                    {
                    'second level score':
                    'scoring reason':(If evaluated by GPT4)
                    },
                    ...
                ]
        }
    }
    '''

    output_data = {}
    output_data['id'] = raw_data['id']
    output_data['scenario'] = scenario
    output_data['Overall score'] = single_eval_data['overall_score']
    for k in score_structure.keys():
        output_data[k] = {'score for criteria':single_eval_data[key_map[k]],'score composition':[]}
        for rule_score in score_structure[k]['rule']:
            if k == 'FA':
                output_data[k]['score composition'].append({'FA':{'score for criteria':single_eval_data[rule_score],'provided by':'rule'}})
            else:
                output_data[k]['score composition'].append({rule_score:{'score for criteria':single_eval_data[rule_score],'provided by':'rule'}})
        for gpt4_score in score_structure[k]['GPT4']:
            if gpt4_score != 'valid_TS_mean':
                output_data[k]['score composition'].append({gpt4_score:{'score for criteria':single_eval_data[gpt4_score],'reason':raw_data[key_map[gpt4_score]]['reason'],'provided by':'LLM'}})
            else:
                #If no valid TS, then the reason for TS will be empty
                output_data[k]['score composition'].append({gpt4_score:{'score for criteria':single_eval_data[gpt4_score],'reason':valid_TS,'provided by':'LLM'}})
    return output_data





def query_with_gpt(prompt_gpt4,key=None):
    api_key = key
    os.environ['http_proxy'] = '127.0.0.1:7890'
    os.environ['https_proxy'] = '127.0.0.1:7890'
    result = make_request(api_key=api_key,model="gpt-4-1106-preview", messages=prompt_gpt4,
                            max_tokens=1024, temperature=0,top_p=0.5)
    return result

def process_message(message):
    thought_pattern = re.compile("Thought:.*?Action:", re.DOTALL)
    action_pattern = re.compile("Action:.*?Action Input:", re.DOTALL)
    action_input_pattern = re.compile("Action Input:.*", re.DOTALL)
    thought_content = thought_pattern.search(message).group().replace("Action:","").replace('Thought:', '').strip()
    action_content = action_pattern.search(message).group().replace('\\n', '').replace("Action:","").replace("Action Input:","").strip()
    action_input_content = action_input_pattern.search(message).group().replace('Action Input:','').strip()
    return [thought_content,action_content,action_input_content],thought_content+'\n'+action_content+'\n'+action_input_content
def reasoning_format_check(response):
    try:
        response_seg,_ = process_message(response)
        if len(response_seg[1])==0:
            return False
        return True
    except Exception as e:
        return False

def json_format_check(response):
    #return correctness of model's Action Input field.
    try:
        response_seg,_ = process_message(response)
        action_input = response_seg[2].replace('Action Input:','')
        try:
            eval(action_input)
            return True
        except Exception as e:
            return False
    except Exception as e:
        return False

def get_doc(sys_message):#return document of a subcategory according to system prompt
    doc = sys_message.split('Specifically, you have access of the following tools:')[-1].split('You should reply in the format of the examples.')[0].split('Let\'s Begin!')[0].strip()
    return eval(doc)

def action_hallucination_check(doc,params):#If the basic format of a response is correct, then check whether there is any action hallucination according to tool document.
    action_list = [func['name'] for func in doc]
    if params not in action_list:
        return False
    else:
        return True

def required_param_check(doc,action,params):# check whether is any required paramter missing. If not, return True.(passing the check) 
    for d in doc:
        if d['name'] == action:
            action_doc = d
            break
    missing_required_param_cnt = 0
    required_param_list = action_doc['required']
    for k in params.keys():
        if k in required_param_list:
            required_param_list.remove(k)
    missing_required_param_cnt = len(required_param_list)
    if len(action_doc['required'])>0:
        return False
    else:
        return True
def param_used_ratio(doc,action,params):
    for d in doc:
        if d['name'] == action:
            action_doc = d
            break
    valid_param_list = [p for p in action_doc['parameters']['properties'].keys()]
    total_param_num = len(valid_param_list)
    used_param_num = 0
    for k in params.keys():
        if k in valid_param_list:
            used_param_num += 1
    if total_param_num == 0:
        if used_param_num == 0:
            param_used_ratio = 1
        else:
            param_used_ratio = 0
    else:
        param_used_ratio = used_param_num/total_param_num
    return param_used_ratio

def get_task_infer_res(path,task_name):#path is the infer results of a certain model, task_id_list
    data_list = []
    datas = [d for d in jsonlines.open(path)]
    for data in datas:
        data_cat = data['path'].split('/')[-2]
        for k in tool_category.keys():
            if data_cat in tool_category[task_name]:
                data_list.append(data)
    return data_list

def param_hallucination_check(doc,action,params):# check the existence of each used param
    for d in doc:
        if d['name'] == action:
            action_doc = d
            break
    hallu_param_cnt = 0
    valid_param_list = [p for p in action_doc['parameters']['properties'].keys()]
    for k in params.keys():
        if k not in valid_param_list:
            hallu_param_cnt += 1
    return hallu_param_cnt

def Format_alignment_score(evaluation_res,stat_dict):
    conv_data = copy.deepcopy(evaluation_res['conversations'])
    format_correct_cnt = 0
    conv_cnt = 0
    format_err_cnt = 0
    assistant_response_cnt = 0
    failed_answer = 'I cannot handle the task.'
    assistant_response_cnt = 0
    evaluation_res['eval_score']['action_thought_match'] = [int(d) for d in evaluation_res['eval_score']['action_thought_match']]
    conv_cnt = 0
    for conv in conv_data:
        if conv['from'] == 'assistant':
            if reasoning_format_check(conv['value']) and not json_format_check(conv['value']):
                stat_dict['neat_json_err_cnt'] += 1
            if not reasoning_format_check(conv['value']) and json_format_check(conv['value']):
                stat_dict['neat_react_err_cnt'] += 1

            if conv['value'] == conv_data[-1]['value'] and failed_answer in conv['value'] and ('trying too many times' in conv['value'] == conv_data[-1]['value'] or 'During execution, an error occurs.' in conv['value'] == conv_data[-1]['value']) :
                stat_dict['Ans_pass'] = 0
                format_err_cnt += 1
                stat_dict['conv_force_terminated'] += 1
                assistant_response_cnt +=1
                continue
            elif conv['value'] == conv_data[-1]['value'] and reasoning_format_check(conv['value']):
                stat_dict['Ans_pass'] = 1
                format_correct_cnt += 1
                assistant_response_cnt += 1
                continue
            else:
                assistant_response_cnt += 1
                if not reasoning_format_check(conv['value']):
                    stat_dict['conv_react_err'] += 1
                else :
                    if not json_format_check(conv['value']):
                        stat_dict['conv_json_err'] += 1
            if reasoning_format_check(conv['value']) and json_format_check(conv['value']):
                # We will only take format correct and self-terminated data into consideration
                format_correct_cnt += 1
                conv_cnt += 1
            format_err_cnt += min((not json_format_check(conv['value']))+ (not reasoning_format_check(conv['value'])),1)
    if assistant_response_cnt==0:
        IF_score=0
    else:
        IF_score = format_correct_cnt/assistant_response_cnt
    stat_dict['format_err_cnt'] = format_err_cnt
    if assistant_response_cnt==0:
        stat_dict['neat_json_err_cnt'] = 0
        stat_dict['neat_react_err_cnt'] = 0
        stat_dict['format_err_cnt'] = 0
    else:
        stat_dict['neat_json_err_cnt'] /= assistant_response_cnt
        stat_dict['neat_react_err_cnt'] /= assistant_response_cnt
        stat_dict['format_err_cnt'] /= assistant_response_cnt
    stat_dict['IF'] = IF_score
    stat_dict['BP_validity'] = evaluation_res['eval_score']['thought_validity']/10
    stat_dict['BP_quality'] = evaluation_res['eval_score']['thought_quality']/10
    stat_dict['IC_memory'] = evaluation_res['eval_score']['thought_foucus']/10
    stat_dict['Ans_quality'] = evaluation_res['eval_score']['relavance']/10
    stat_dict['format_err_cnt'] = format_err_cnt
    return stat_dict, assistant_response_cnt


def Intent_comprehension_score(evaluation_res,stat_dict):
    stat_dict['IU'] = evaluation_res['eval_score']['thought_foucus']/10
    return stat_dict

def Behavior_planing_score(evaluation_res,stat_dict):
    stat_dict['BP'] = (evaluation_res['eval_score']['thought_validity']/10*evaluation_res['eval_score']['thought_quality']/10)
    return stat_dict


def Tool_selection_score(evaluation_res,stat_dict):
    conv_data = copy.deepcopy(evaluation_res['conversations'])
    conv_cnt = 0
    assistant_response_cnt = 0
    failed_answer = 'I cannot handle the task.'
    evaluation_res['eval_score']['action_thought_match'] = [int(d) for d in evaluation_res['eval_score']['action_thought_match']]
    origin_TS_score = copy.deepcopy(evaluation_res['eval_score']['action_thought_match'])
    tool_hallu_cnt = 0
    param_hallu_cnt = 0
    format_correct_cnt = 0
    doc = get_doc(conv_data[0]['value'])
    valid_TS = []

    # While calculating TS score, we will omit turns that can not format output properly 
    for conv in conv_data:
        if conv['from'] == 'assistant':
            if conv['value'] == conv_data[-1]['value'] and failed_answer in conv['value'] and ('trying too many times' in conv['value'] == conv_data[-1]['value'] or 'During execution, an error occurs.' in conv['value'] == conv_data[-1]['value']) :
                assistant_response_cnt +=1
                continue
            elif conv['value'] == conv_data[-1]['value'] and reasoning_format_check(conv['value']):
                assistant_response_cnt += 1
                continue
            else:
                assistant_response_cnt += 1
            if reasoning_format_check(conv['value']) and json_format_check(conv['value']):
                # We will only take format correct and self-terminated data into consideration
                format_correct_cnt += 1
                response_seg,_ = process_message(conv['value'])
                action = response_seg[1]
                action_input = eval(response_seg[2])
                action_hallu = action_hallucination_check(doc,action)
                tool_hallu_cnt += (not action_hallu)
                valid_TS.append(evaluation_res['action_thought_match'][conv_cnt])
                if tool_hallu_cnt:
                    conv_cnt += 1
                else:
                    param_hallu= min((not required_param_check(doc,action,action_input))+(  param_hallucination_check(doc,action,action_input)),1)
                    param_hallu_cnt += param_hallu
                    conv_cnt += 1
            else:
                origin_TS_score[conv_cnt] = -1
                conv_cnt += 1
    if format_correct_cnt == 0:
        tool_reality = 0
    else:
        tool_reality = 1-(tool_hallu_cnt+param_hallu_cnt)/(format_correct_cnt)
    while -1 in origin_TS_score:
        origin_TS_score.remove(-1)
                
    if len(origin_TS_score) == 0:
        stat_dict['TS'] = 0
        stat_dict['valid_TS_mean'] = 0
    else:
        stat_dict['valid_TS_mean'] = np.mean(origin_TS_score)/10
        stat_dict['TS'] = tool_reality * np.mean(origin_TS_score)/10

    return stat_dict,valid_TS

def Answer_organization_score(evaluation_res,stat_dict):
    stat_dict['AO'] = evaluation_res['eval_score']['relavance']/10
    return stat_dict

def eval_single_data(data,model,scenario):
    eval_data = copy.deepcopy(data)
    conv_data = copy.deepcopy(data['conversations'])
    turn_cnt = 0
    #first_level_stat: IF TS LF SP AO overall
    #second_level_stat: format_err_cnt json_err_cnt neat_json_err_cnt neat_react_err_cnt action_mean_match tool_reality LF_quality LF_memory Ans_quality Ans_pass
    stat_dict = {'IF':0,'IU':0,'BP':1,'TS':0,'AO':0,'overall_score':0,
                 'format_err_cnt':0,'neat_json_err_cnt':0,'neat_react_err_cnt':0,'action_mean_match':0,'tool_reality':0,'BP_quality':0,'IC_memory':0,'Ans_quality':0,'Ans_pass':1,'conv_json_err':0,'conv_react_err':0,'valid_TS_mean':0,'conv_json_err_ratio':0,'conv_react_err_ratio':0,'conv_force_terminated':0}
    stat_dict, assistant_response_cnt = Format_alignment_score(eval_data,stat_dict)
    stat_dict = Intent_comprehension_score(eval_data,stat_dict)
    stat_dict = Behavior_planing_score(eval_data,stat_dict)
    stat_dict,valid_TS = Tool_selection_score(eval_data,stat_dict)
    stat_dict = Answer_organization_score(eval_data,stat_dict)


    first_level_stat = ['IF','TS','BP','IU','AO']
    for k in first_level_stat:
        stat_dict['overall_score'] += stat_dict[k]/5

    stat_dict['BP_validity'] = eval_data['eval_score']['thought_validity']/10
    stat_dict['BP_quality'] = eval_data['eval_score']['thought_quality']/10
    stat_dict['IC_memory'] = eval_data['eval_score']['thought_foucus']/10
    stat_dict['Ans_quality'] = eval_data['eval_score']['relavance']/10
    structured_data = structuring_data(stat_dict,data,scenario,valid_TS)
    turn_cnt = assistant_response_cnt

    return stat_dict,turn_cnt,structured_data


def row_column_swap(data_dict):
    new_dict = {}
    for m in data_dict.keys():
        for s in data_dict[m].keys():
            
            if s not in new_dict.keys():
                new_dict[s] = {}
            new_dict[s][m] = data_dict[m][s]
    return new_dict

def aggregated_data(data_list,task_query,args,model=None):
    data_list = data_list
    stat_list = ['IF','IU','BP','TS','AO','overall_score',
            'format_err_cnt','neat_json_err_cnt','neat_react_err_cnt','action_mean_match','tool_reality','BP_validity','BP_quality','IC_memory','Ans_quality','Ans_pass','conv_json_err','conv_react_err','conv_force_terminated','valid_TS_mean']
    A_pass_list = []
    A_pass_dict = {}
    TS_none_zero_list = []
    TS_none_zero_dict = {}
    all_stat_list = []
    all_data_by_scenario = {}
    model_turn_cnt = []
    for k in tool_category.keys():
        all_data_by_scenario[k] = []
    # overall score of models in different scenarios
    stat_by_scenario = {}
    stat_by_scenario_detailed = {}
    # detailed score of models in all scenarios
    stat_detailed = {}
    for s in tool_category.keys():
        stat_by_scenario[s] = {}
        for stat in stat_list:
            stat_by_scenario[s][stat] = 0
    for m in stat_list:
        stat_detailed[m] = 0

    for scenario in task_query.keys():
        add_id = []
        queries = task_query[scenario]
        scenario_data = []
        for d in data_list:
            if d['id'] in queries and d['id'] not in add_id:
                scenario_data.append(d)
                add_id.append(d['id'])
        print(f'scenario:{scenario}')
        print(f'data cnt:{len(scenario_data)}')
        if len(scenario_data) == 0:
            continue
        task_query[scenario] = copy.deepcopy(add_id)
        for data in scenario_data:
            single_stat,turn_cnt,structured_data = eval_single_data(data,model,scenario)
            if single_stat['IF'] > 0:
                TS_none_zero_list.append(single_stat)
            if single_stat['Ans_pass'] != 0:
                A_pass_list.append(single_stat)
            model_turn_cnt.append(turn_cnt)
            all_stat_list.append(single_stat)
            all_data_by_scenario[scenario].append(single_stat['overall_score'])
            for stat in stat_list:
                stat_by_scenario[scenario][stat] += single_stat[stat]
            with open(os.path.join(os.getcwd(),args.eval_output_path+f'/jsonl/{model}_structured_data.jsonl'),'a',encoding='utf-8') as f:
                f.write(json.dumps(structured_data.copy(),ensure_ascii=False)+'\n')
        for stat in stat_list:
            if 'conv' in stat:
                continue
            stat_by_scenario[scenario][stat] /= len(scenario_data)
    data_cnt = 0
    for scenario in stat_by_scenario.keys():
        data_cnt += len(task_query[scenario])
        for stat in stat_list:
            if 'conv' in stat:
                stat_detailed[stat] += stat_by_scenario[scenario][stat]
                continue
            stat_detailed[stat] += stat_by_scenario[scenario][stat]*len(task_query[scenario])
        stat_by_scenario_detailed[scenario] = copy.deepcopy(stat_by_scenario[scenario])
        stat_by_scenario[scenario] = stat_by_scenario[scenario]['overall_score']

    for stat in stat_list:
        if 'conv' in stat:
            continue
        stat_detailed[stat] /= data_cnt
    for d in TS_none_zero_list:
        for k in d.keys():
            if k not in TS_none_zero_dict.keys():
                TS_none_zero_dict[k] = 0
            TS_none_zero_dict[k] += d[k]/len(TS_none_zero_list)
    TS_none_zero_dict['data num'] = len(TS_none_zero_list)
    for d in A_pass_list:
        for k in d.keys():
            if k not in A_pass_dict.keys():
                A_pass_dict[k] = 0
            A_pass_dict[k] += d[k]/len(A_pass_list)
    A_pass_dict['data num'] = len(A_pass_list)
        
    return stat_by_scenario,stat_detailed,stat_by_scenario_detailed


def model_eval(model_data,model_name,args):
    root_path = os.path.join(os.getcwd(),args.eval_output_path)
    save_path = root_path+f'/tmp/{model_name}_res.jsonl'
    eval_res = []
    score_pattern = re.compile("Evaluation Score:[^\n]*",re.DOTALL)
    cnt = 0
    if os.path.exists(save_path):
        eval_res = [d for d in jsonlines.open(save_path)]
        datas = jsonlines.open(save_path)
        for d in datas:
            first_d = d
            break
        datas = jsonlines.open(save_path)
        if 'tag' in first_d.keys():
            evaled_data_id = [d['tag'] for d in datas]
        elif 'id' in first_d.keys():
            evaled_data_id = [d['id'] for d in datas]
    else:
        evaled_data_id = []
    for prompts in model_data:
        cnt += 1
        sample_eval_res = {}
        score_dict = {}
        if 'tag' in prompts.keys() and prompts['tag'] in evaled_data_id:
            continue
        elif 'id' in prompts.keys() and prompts['id'] in evaled_data_id:
            continue
        for k in prompts.keys():
            if 'match' in k:
                pair_match_res = []
                eval_score = []
                for pair in prompts[k]:
                    single_sample_eval_res = {}
                    res = query_with_gpt(pair,args.gpt4_key)['choices'][0]['message']['content']
                    try:
                        score = score_pattern.findall(res)[0]
                        score = int(re.search('(10|\d)',score_pattern.search(res).group()).group())
                    except Exception as e:
                        if 'N/A' in score or 'nan' in score.lower():
                            print('N/A occured')
                            score = 0
                        else:
                            print(res)
                            print(score_pattern.search(res).group())
                            print('this is error')
                            score = 0
                    single_sample_eval_res['reason'] = res
                    eval_score.append(score)
                    pair_match_res.append(single_sample_eval_res)
                score_dict[k] = eval_score
                sample_eval_res[k] = pair_match_res
            elif 'conv' in k or 'tag' in k or 'path' in k or ('id' in k and 'validity' not in k):
                sample_eval_res[k] = prompts[k]
            elif 'relavance' in k:
                single_sample_eval_res = {}
                res = query_with_gpt(prompts[k],args.gpt4_key)['choices'][0]['message']['content']
                try:
                    score = score_pattern.findall(res)[0]
                    score = int(re.search('(10|\d)',score_pattern.search(res).group()).group())
                except Exception as e:
                    if 'N/A' in score or 'nan' in score.lower():
                        print('N/A occured')
                        score = 0
                    else:
                        print(prompts[k])
                        print(res)
                        print(score_pattern.search(res).group())
                        print('this is error')
                        score = 0
                single_sample_eval_res['reason'] = res
                score_dict[k]= score
                sample_eval_res[k] = single_sample_eval_res
            else:
                single_sample_eval_res = {}
                res = query_with_gpt(prompts[k],args.gpt4_key)['choices'][0]['message']['content']
                try:
                    score = score_pattern.findall(res)[0]
                    score = int(re.search('(10|\d)',score_pattern.findall(res)[0]).group())
                except Exception as e:
                    if 'N/A' in score or 'nan' in score.lower():
                        print('N/A occured')
                        score = 0
                    else:
                        print(prompts[k])
                        print(res)
                        print(score_pattern.search(res).group())
                        print('this is error')
                single_sample_eval_res['reason'] = res
                score_dict[k]= score
                sample_eval_res[k] = single_sample_eval_res
            sample_eval_res['eval_score'] = score_dict
        eval_res.append(sample_eval_res)
        with open(save_path,'a',encoding='utf-8') as f:
            f.write(json.dumps(sample_eval_res.copy(),ensure_ascii=False)+'\n')
    return eval_res

def get_all_data(infer_res_path):
    root_path = infer_res_path
    data_path = root_path
    path = infer_res_path
    data_list = []
    if 'wo_demo' not in path and 'tuned' not in path and ('vicuna' in path or 'text_davinci' in path or 'Llama2chat' in path):
        use_demon = True
    else:
        use_demon = False
    infer_res_data = jsonlines.open(data_path)
    sample_res = []
    for data in infer_res_data:
        res = get_all_res(data,use_demon=use_demon)
        sample_res.append(res)
        res['id'] = data['id']
        res['path'] = data['path']
        data_list.append(res)
    return data_list

# Function to plot radar chart for a group with thicker border and custom legend handles
def plot_radar(ax, group, group_label, data,model, y_ticks=100, color_scheme=None, line_width=3):
    handles = []  # To store legend handles
    indicators = ['Format\nAlignment','Intent\nComprehension', 'Behavior\nPlanning', 'Tool\nSelection', 'Answer\nOrganization']
    for i in group:
        values = data
        values = np.concatenate((values, [values[0]]))  # Close the loop
        color = color_scheme[i % len(color_scheme)]

        # Fill the area between radar lines
        ax.fill_between(np.radians(np.linspace(0, 360, len(indicators) + 1)), 0, values, alpha=0.3, color=color)

        # Set a thicker border for the radar chart lines
        line, = ax.plot(np.radians(np.linspace(0, 360, len(indicators) + 1)), values, color=color, linewidth=line_width)

        # Store the legend handle for the line
        handles.append(Rectangle((0, 0), 1, 1, color=line.get_color(), linewidth=line_width, label=model))

    ax.set_title(group_label, fontsize=18)
    ax.set_theta_zero_location('N')
    ax.set_xticks(np.radians(np.linspace(0, 360, len(indicators)+1)))
    ax.set_xticklabels(indicators + [indicators[0],], fontsize=18)
    ax.set_yticks(np.linspace(0, y_ticks, 6))
    ax.set_yticklabels(np.linspace(0, y_ticks, 6), fontsize=15, rotation=180)
    ax.set_thetagrids(np.degrees(np.radians(np.linspace(0, 360, len(indicators)+1))), labels=indicators+[indicators[0],])
    ax.spines['polar'].set_visible(False)

    return handles

def plot_radar_single_scen(scen_data_detailed, scen,model_name, args):
    tmp_list = []
    crit_list = ['IF','IU','BP','TS','AO']
    for c in crit_list:
        tmp_list.append(scen_data_detailed[scen][c]*100)
    n_detailed_data = tmp_list

    # 模型名称
    # 数据
    data = np.array(n_detailed_data)

    # 分组
    group1 = [0]  # 最后三个为一组

    # 指标
    indicators = ['Format\nAlignment','Intent\nComprehension', 'Behavior\nPlanning', 'Tool\nSelection', 'Answer\nOrganization']

    # Matplotlib内置的颜色
    group_colors = ['lightskyblue', 'deepskyblue', 'darkblue']  # 天蓝色系

    # 创建子图和绘制雷达图
    fig, axs = plt.subplots(1, 1, figsize=(7, 8.5), subplot_kw=dict(polar=True))

    # Merging legend handles from all groups
    legend_handles = plot_radar(axs, group1, group_label='',  color_scheme=group_colors,data=data,model=model_name)

    # Adjusting legend position, enlarging font, and aligning with the ends of the entire figure
    fig.legend(handles=legend_handles, loc='upper center', bbox_to_anchor=(0.5, 0.95), ncol=1, frameon=True, fontsize=15)

    plt.tight_layout()
    plt.savefig(os.getcwd()+f'/{args.radar_fig_output_path}/{scen}_capability.pdf', format='pdf', bbox_inches='tight')
