# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 13:15:02 2018

@author: Home
"""

from __future__ import print_function
import json
from watson_developer_cloud import AssistantV1
#from watson_developer_cloud.assistant_v1 import RuntimeIntent

#import csv
#import logging

# Parameters ####################################
param_workspace_limit = 5

# Functions #####################################

# Class Wat: handles the watson api and returns the response in a simple form
    
class Wat():
    def __init__(self, username, password, workspace_id = None):
        self.assistant = AssistantV1(
                    username= username,
                    password= password,
                    version='2017-04-21')
        self.workspace_name = None
        self.workspace_id = None
        if workspace_id:
            self.set_workspace_by_id(workspace_id)
    
    def set_workspace_by_id(self,workspace_id):
        wlist = self.list_workspace()
        if workspace_id in wlist:
            self.workspace_id = workspace_id
            self.workspace_name = wlist[workspace_id]
            return True
        else:
            # The assistance does not have an workspace with that id
            return False

    def get_workspace_id_from_name(self,name, wlist = None):
        if not wlist:
            wlist = self.list_workspace()
        workspace_id = None
        for key, value in wlist.items():
            if value == name:
                workspace_id = key
                break
        return workspace_id
        
    def set_workspace_by_name(self, name):
        '''Set the workspace to the FIRST one with the given name!'''
        res = self.get_workspace_id_from_name(name)
        if res:
            self.workspace_id = res
            self.workspace_name = name
            return True
        else:
            # The assistance does not have an workspace with that id
            return False
    
    def delete_workspace(self,name):
        workspace_id = self.get_workspace_id_from_name(name)
        if workspace_id:
            self.assistant.delete_workspace(
                    workspace_id = workspace_id
                )
            return True, 'Workspace %s deleted' % name
        else:
            return False, 'Workspace %s not found' % name
            
    def create_workspace(self,name):
        wlist = self.list_workspace()
        workspace_id = self.get_workspace_id_from_name(name, wlist)
        if workspace_id:
            return False, 'Workspace %s exits' % name
        else:
            # Do not create workspace if reached the limit
            if len(wlist) == param_workspace_limit:
                return False, 'Maximum number of workspaces reached:%d' % param_workspace_limit
            self.assistant.create_workspace(name= name,description='Sciencer workspace')
            
            self.workspace_id = self.get_workspace_id_from_name(name)
            self.workspace_name = name
            return True, 'Workspace %s created' % name
    
    def check_intent_existance(self, label, expected):
        '''If 'expected' == True then the error is when the intent does not exist
        The code must check both the 'label' and 'label_no' intents
        '''
        def is_error(label, expected, list):
            result = True
            return_str = ''
            if label in l and not expected:
                return_str += 'Error: intent %s already exists' % label + '\n'
                result = False
            elif label not in l and expected:
                return_str += 'Error: intent %s does not exist' % label + '\n'
                result = False
            return result, return_str
        
        l = self.list_intent()
        result, return_str = is_error(label, expected, l)
        result_no, return_str_no = is_error(label + '_no', expected, l)
        return result and result_no, return_str + return_str_no
        
        
    def create_question(self, label, ans, wrong):
        ''' Create indents corresponding to a questions. For each questions there are two 
        associated intents: foo (containing examples) and foo_no (containing conter examples)
        
        Returns True if the intents where successfully created.
        In case of error the second parameter is the error message
        '''
        res, return_str = self.check_intent_existance(label, False)
        if not res:
            return res, return_str
        self.add_intent(label, 'string', ans)
        self.add_intent(label +'_no', 'string', wrong)
        return True, return_str
    
    def identify(self, label, answer, workspace_id = None):
        '''Clasisfies the answer according to the watson workspace
        Gets workspace_id as an optional parameter'''
        if not workspace_id:
            workspace_id = self.workspace_id
        response = self.assistant.message(workspace_id= workspace_id,
            input={'text': answer}, alternate_intents = True)   
        #print(json.dumps(response, indent = 2))
        return [[elem['intent'], elem['confidence']] for elem in response['intents'] 
                if elem['intent'] in [label, label + '_no']]
    
    def list_workspace(self):
        '''Returns the dictionary of available workspaces in the form id:name'''
        response = self.assistant.list_workspaces()
        #print(json.dumps(response, indent=2))
        res = {x['workspace_id']:x['name'] for x in response['workspaces']}
        return res
        
    def list_intent(self):
        response = self.assistant.list_intents(self.workspace_id)
        res = {x['intent'] for x in response['intents']}
        return res
        
    def get_intent(self, label):
        '''Return False and error message if the intents do not exist
        Return the dictionary describign the intent if it exist
        '''
        valid, message = self.check_intent_existance(label, True)
        if not valid:
            return False, message
        response = self.assistant.get_intent(workspace_id= self.workspace_id, intent= label, export=True)
        res = {}
        res['description'] = response['description']
        res['examples'] = [elem['text'] for elem in response['examples']]
        #Get couterexamples from the '_o' intent:
        response = self.assistant.get_intent(workspace_id= self.workspace_id, intent= label + '_no', export=True)
        res['counterexamples'] = [elem['text'] for elem in response['examples']]
        return True, res
            
    def add_intent(self, Q_name, description, q1Examples):
        ''' Add an intent in watson workspace'''
        examples = [{'text': line} for line in q1Examples]
        response = self.assistant.create_intent(workspace_id= self.workspace_id,
            intent= Q_name, description= description, examples= examples)
        #print(json.dumps(response, indent=2))
        return response

    def delete_intent(self, label):
        '''Delete intent 'text' if it exists in workspace'''
        res, return_str = self.check_intent_existance(label, True)
        if not res:
            return res, return_str
        return_str += 'Delete ' + label + '\n'
        self.assistant.delete_intent(workspace_id=self.workspace_id, intent = label)
        self.assistant.delete_intent(workspace_id=self.workspace_id, intent = label + '_no')
        return True, return_str

    def update_intent(self, label, answers):
        examples = [{'text': line} for line in answers]
        response = self.assistant.update_intent(workspace_id=self.workspace_id,
            intent= label, new_examples = examples, description = 'string')
        #print(json.dumps(response, indent=2))
        return json.dumps(response, indent=2) + '\n'
        
    def update_question(self, label, ans, wrong):
        res, return_str = self.check_intent_existance(label, True)
        if not res:
            return res, return_str
        return_str += self.update_intent(label, ans)
        return_str += self.update_intent(label+'_no', wrong)
        return True, return_str
    

        