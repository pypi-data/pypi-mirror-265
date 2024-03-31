from pureml_evaluate.policy.performance import Performance
from pureml_evaluate.policy.fairness import FairnessPolicy as Fairness
import numpy as np
from collections import defaultdict
from typing import Any
import json
from pureml.utils.logger import get_logger
logger = get_logger(name = 'pureml_policy.grade.py')

class Grader:
    list_of_performance_metrics:Any = [
    'accuracy',
    'precision',
    'recall' ,
    'f1',
    'confusionmatrix',
    'balancedaccuracyscore',
    'topkaccuracyscore' ,
    'logloss' ,
    'averageprecisionscore',
    'roc_auc' ,
    'brierscoreloss' ,
    'kolmogorovsmirnov' ,
    'wassersteindistance',
    'hellingerdistance' ,
    'linfinitydistance' ,
    'chisquaredstatistic',
    'cramersv',
    'populationstabilityindex' 
    ]
    metrics : list = []
    framework : dict   
    references : any
    predictions : any
    sensitive_features : any
    scores : dict = {}
    categories: dict = {}

    def __init__(self,references,predictions,sensitive_features,framework,metrics,**kwargs):
        self.references = references
        self.predictions = predictions
        self.sensitive_features  = sensitive_features
        self.framework = framework             #{'acccuracy' : 0.8}
        self.metrics = metrics       # ['accuracy']
        self.kwargs = kwargs


    def compute(self):
        all_metrics:Any = []
        
        
        operational_scores:Any = {} # To Store the values of metrics 
        fairness_scores:Any = {}


        for metric in self.metrics:
            #print(f"Line 59. grade.py: {metric}")
            if metric in self.list_of_performance_metrics:
                #print(f"Line 60. grade.py: {metric}")
                logger.info(f"Computing {metric} metric")
                performance = Performance()
                threshold_value = self.framework[metric]
                threshold = {metric : threshold_value}
                result = performance.compute(list_metrics = [metric],references = self.references,predictions = self.predictions,
                                             list_of_thresholds = threshold,prediction_scores = None,**self.kwargs)
                
                try:
                    #print(f"Line 69. grade.py result: {result}")
                    temp_scores  = {
                    f"{result['risk']}" : float(result['value'])
                    }
                    operational_scores.update(temp_scores)
                except Exception as e:
                    #print(f"Exception : {e}")
                    logger.error(f"Error in computing {metric} metric: {e}")
                    
            else:
                logger.info(f"Computing {metric} metric")
                fairness = Fairness()
                threshold_value = self.framework[metric]
                threshold = {metric : threshold_value}
                result = fairness.compute(list_metrics = [metric],references = self.references,predictions = self.predictions,
                                          list_of_thresholds = threshold,sensitive_features = self.sensitive_features,prediction_scores = None,**self.kwargs)
                try:
                    #print(f"Line 85. grade.py result: {result}")
                    temp_scores  = {
                        f"{result['risk']}" : float(result['value'])
                    }
                    fairness_scores.update(temp_scores)
                except Exception as e:
                    #print(f"Exception : {e}")
                    logger.error(f"Error in computing {metric} metric: {e}")
                    
        self.scores = {
                "operational_scores" : operational_scores,
                "fairness_scores" : fairness_scores,
            }
        
        #print(f"Line 119. grade.py: {self.scores}")
        return self.scores

