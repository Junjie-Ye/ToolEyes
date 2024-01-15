import re
import os
import sys
import argparse
from util.gpt_request import *
import json
import traceback
import tqdm
from transformers import AutoTokenizer
import gpt3_tokenizer
from gpt3_tokenizer import count_tokens
import re

def process_action_pair(action_input):
    key_pattern = re.compile("[\'][^,\"]*[\'][:]",re.DOTALL)
    #value_pattern = re.compile(":[\s\n]*[\"\'][^\"]*[\"\']",re.DOTALL)
    value_pattern = re.compile(":[\s\n]*[\'\"][^}]*",re.DOTALL)
    k = [key.replace(':', '').strip() for key in key_pattern.findall(action_input)]
    v = [value.split(':', 1)[1].strip() for value in value_pattern.findall(action_input)]
    action_input_dict = {}
    while len(v) < len(k):
        v.append('')
    for key,value in zip(k,v):
        #if len(value)>0:
        action_input_dict[key[1:-1]] = value[1:-1]
        #else:
        #    action_input_dict[key[1:-1]] = 'Sorry, I can\'t answer in correct format.'
    return action_input_dict


def process_message(message):
    thought_pattern = re.compile(".*?Action:",re.DOTALL)
    action_pattern = re.compile("Action:.*?Input",re.DOTALL)
    action_input_pattern = re.compile("Action Input:.*", re.DOTALL)
    thought_content = re.sub("Thought[\s]*:","",re.sub("Action.:*",'',thought_pattern.search(message).group())).strip().strip('\n')
    action_content = re.sub("Action[\s]*:","",re.sub("Action Input",'',action_pattern.search(message).group())).strip()
    action_input_content = re.sub("Action Input[\s]*:","",action_input_pattern.search(message).group()).strip().strip('\n')
    return [thought_content,action_content,action_input_content],thought_content+'\n'+action_content+'\n'+action_input_content

def eval_action_thought_matching(sample,use_demon=False):
    if use_demon:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].split('You should reply in the format of the examples.')[0].strip()
    else:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].strip()
    action_thought_doc_pair = []
    for conv in sample['conversations']:
        if conv['from'] == 'assistant':
            message_seg,_ = process_message(conv['value'])
            thought = message_seg[0]
            tool = message_seg[1]
            sys_prompt = '''As a professional assessment expert, your task is to objectively evaluate the quality of the provided data based on the given guidelines. 

When presented with a tool document, a THOUGHT, and a tool from the tool document, please ascertain the correlation between the specified tool and the given THOUGHT based on the guidelines below:

    1. If the THOUGHT is empty, assign a score of 5 immediately.

    2. If the THOUGHT is not empty, determine if the chosen tool is more pertinent to the planning in the THOUGHT compared to other tools in the tool document based on the tool documentation description. The more relevant the tool, the higher the score.

Please provide your assessment in the following format:"""
    Scoring Reason: <Provide a reason for your score, referencing the given criteria>.

    Evaluation Score: <Assign a score between 1 and 10>.
"""
    '''
            user_input= f'''
Tool Document:
{document}

THOUGHT:"""
{thought}
"""

Tool:"""
{tool}
"""

Assessment:'''
            prompt_gpt4 = [{'role':'system','content':sys_prompt},{'role':'user','content':user_input}]
            action_thought_doc_pair.append(prompt_gpt4)
    return action_thought_doc_pair

def eval_thought_quality(sample,use_demon=False):
    if use_demon:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].split('You should reply in the format of the examples.')[0].strip()
    else:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].replace('Begin!','').strip()
    query = sample['conversations'][1]['value'].replace('Begin!', '').strip()
    thought_chain = ''
    turn_cnt = 1
    for i in range(len(sample['conversations'])):
        if sample['conversations'][i]['from'] == 'assistant':
            message_seg,_ = process_message(sample['conversations'][i]['value'])
            thought_chain += f'Turn {turn_cnt}:\n'+message_seg[0].strip(' ').strip('\n')+'\n\n'
            #thought_chain += f'Turn {turn_cnt}:\n\n'+message_seg[0]
            turn_cnt += 1
    thought_chain = thought_chain.strip()
    sys_prompt = '''As a professional assessment expert, your task is to objectively evaluate the quality of the provided data based on the given guidelines.

When given a tool document, a user query and a thought chain that addresses the query, please rate the quality of the thought chain based on the following criteria:

1. The presence or absence of grammatical errors in the thought chain. The fewer the errors, the higher the score.

2. The logical consistency of the thought chain. The fewer logical inconsistencies, the higher the score.

3. The timeliness of detection and correction of any logical inconsistencies in the thought chain. The more timely the correction, the higher the score.

Please provide your assessment in the following format:"""
Scoring Reason: <Provide a reason for your score, referencing the given criteria>.

Evaluation Score: <Assign a score between 1 and 10>.
"""
'''
    user_input= f'''
Tool Document:
{document}

User Query:"""
{query}
"""

Thought Chain:"""
{thought_chain}
"""

Assessment:'''
    prompt_gpt4 = [{'role':'system','content':sys_prompt},{'role':'user','content':user_input}]
    return prompt_gpt4
def eval_thought_foucus(sample,use_demon=False):
    if use_demon:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].split('You should reply in the format of the examples.')[0].strip()
    else:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].replace('Begin!','').strip()
    query = sample['conversations'][1]['value'].replace('Begin!', '').strip()
    thought_chain = ''
    turn_cnt = 1
    for i in range(len(sample['conversations'])):
        if sample['conversations'][i]['from'] == 'user' and i != 1:
            thought_chain += 'User request:'+'\n' +sample['conversations'][i]['value'].strip()+'\n\n'
        if sample['conversations'][i]['from'] == 'assistant':
            message_seg,_ = process_message(sample['conversations'][i]['value'])
            thought_chain += f'Turn {turn_cnt}:\n'+message_seg[0].strip('\n').strip('\t').strip().strip('\n')+'\n\n'
            turn_cnt += 1
    thought_chain = thought_chain.strip()
    sys_prompt = '''As a professional assessment expert, your task is to objectively evaluate the quality of the provided data based on the given guidelines.

When given a tool document, a user query, and a thought chain that addresses the query, please rate the quality of the thought chain based on the following criteria:

1. The extent to which the thought chain consistently focuses on resolving the user query. The more relevant it is to the user query, the higher the score.

2. The ability of the thought chain to adapt promptly when the user provides new information or makes new requests. The higher the alignment with the new information and requests, the higher the score. If there is no new information or requests, please ignore the criteria.

Please provide your assessment in the following format:"""
Scoring Reason: <Provide a reason for your score, referencing the given criteria>.

Evaluation Score: <Assign a score between 1 and 10>.
"""
'''
    user_input= f'''
Tool Document:
{document}

User Query:"""
{query}
"""

Thought Chain:"""
{thought_chain}
"""

Assessment:'''
    prompt_gpt4 = [{'role':'system','content':sys_prompt},{'role':'user','content':user_input}]
    return prompt_gpt4
def eval_thought_validity(sample,use_demon=False):
    if use_demon:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].split('You should reply in the format of the examples.')[0].strip()
    else:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].replace('Begin!','').strip()
    query = sample['conversations'][1]['value'].replace('Begin!', '').strip()
    thought_chain = ''
    turn_cnt = 1
    for i in range(len(sample['conversations'])):
        if sample['conversations'][i]['from'] == 'assistant':
            message_seg,_ = process_message(sample['conversations'][i]['value'])
            thought_chain += f'Turn {turn_cnt}:\n'+message_seg[0].strip(' ').strip('\t').strip().strip('\n')+'\n\n'
            turn_cnt += 1
    thought_chain = thought_chain.strip()
    sys_prompt = '''As a professional assessment expert, your task is to objectively evaluate the quality of the provided data based on the given guidelines.

When given a tool document, a user query, and a thought chain that addresses the query, please rate the quality of the thought chain based on the following criteria:

1. Each step should succinctly summarize relevant information from the previous step; the more comprehensive the summary, the higher the score.

2. Each step should timely plan for the next one; the more detailed the next step, the higher the score.

3. Each step should be distinct from the previous one and contribute to resolving the user's query; the less repetition, the higher the score.

Please provide your assessment in the following format:"""
Scoring Reason: <Provide a reason for your score, referencing the given criteria>.

Evaluation Score: <Assign a score between 1 and 10>.
"""
'''
    user_input = f'''
Tool Document:
{document}

User Query:"""
{query}
"""

Thought Chain:"""
{thought_chain}
"""

Assessment:
'''
    prompt_gpt4 = [{'role':'system','content':sys_prompt},{'role':'user','content':user_input}]
    return prompt_gpt4

def eval_relavance(sample,use_demon=False):
    if use_demon:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].split('You should reply in the format of the examples.')[0].strip()
    else:
        document = sample['conversations'][0]['value'].split('Specifically, you have access of the following tools:')[-1].replace('Let\'s Begin!','').strip()
    query = sample['conversations'][1]['value'].replace('Begin!', '').strip()
    origin_message = sample['conversations'][-1]['value']
    message_seg,_ = process_message(sample['conversations'][-1]['value'].replace('\\\\', '\\').replace('{\n', '{').replace('\n}', '}'))
    try:
        response = eval(message_seg[2].replace('\\n\\', '\\'))['answer']
    except Exception as e:
        response = str(process_action_pair(message_seg[2].replace('\\\\', '\\')))
        res = process_action_pair(message_seg[2].replace('\\n\\', '\\').replace('{\n', '{').replace('\n}', '}'))
        (e)
        (sample)
    sys_prompt = '''As a professional assessment expert, your task is to objectively evaluate the quality of the provided data based on the given guidelines. 

When presented with a tool documentation, a user's initial query and a corresponding response, please rate the response's effectiveness in meeting the user's needs using the following criteria:

1. Assess whether the response directly addresses the user's original question. The more on-point the response is, the higher it should be scored.
2. Determine if the response includes any inaccurate information. Unless you have exact information, you need to assume that the information in the response is correct. A response with minimal inaccuracies should receive a higher score.
3. Consider if the response offer suggestions that could help resolve the user's query? The more beneficial the guidance, the higher the score should be. Disregard this criterion if the user's question has been fully answered by the response.

Please provide your assessment in the following format:"""
Scoring Reason: <Provide a reason for your score, referencing the given criteria>.

Evaluation Score: <Assign a score between 1 and 10>.
"""
'''
    user_input= f'''
Tool Document:
{document}
    
User Query:"""
{query}
"""

Corresponding Response:"""
{response}
"""

Assessment:'''
    prompt_gpt4 = [{'role':'system','content':sys_prompt},{'role':'user','content':user_input}]
    return prompt_gpt4

def get_all_res(sample,use_demon=False):
    e_r = eval_relavance(sample,use_demon)
    e_a = eval_action_thought_matching(sample,use_demon)#list of list
    e_q = eval_thought_quality(sample,use_demon)
    e_f = eval_thought_foucus(sample,use_demon)
    e_v = eval_thought_validity(sample,use_demon)
    return {'relavance':e_r,'action_thought_match':e_a,'thought_quality':e_q,'thought_foucus':e_f,'thought_validity':e_v,'conversations':sample['conversations']}