from signlanguage.interfaces.interfaces_model         import ITrace
import signlanguage.models.signmodel_class            as sm
import signlanguage.core.trainmodel_class             as tm
import signlanguage.core.executionmodel_class         as em
import signlanguage.interfaces.transfermodel_class    as ex
import signlanguage.utils.utils_class                 as utils
import numpy                             as np
import time
import asyncio

class StateTrace(ITrace):
    def __init__(self, label= "", state_value=-1, evaluationStandard=True):
        self._body_evaluation      = None
        self._body_classification  = []
        self._singTrace_evaluation = None
        self._label = label
        self._state_value = state_value
        self._validate = False
        self._evaluationStandard = evaluationStandard

    @property
    def label(self):
        return self._label
    
    @property
    def validate(self):
        return self._validate

    @property
    def body_classification(self):
        return self._body_classification

    @property
    def body_evaluation(self):
        return self._body_evaluation

    @body_evaluation.setter
    def body_evaluation(self, value):
        self._body_evaluation = value

    def return_result(self, result=False, confidence=0, msg="", review=False):
        return {
            "hand_value": f"{self._label}{self._state_value}",
            "evaluado": review,
            "rule_match": result,
            "message": msg,
            "confidence_results": confidence,
            "state_value": self._state_value
        }
    
    
    async def exec_model_async(self, data=None, executionModelmovement : em.ExecutionModelMovement =None, executionModelpool: em.ExecutionModelPool=None):
        try:
            if None in (data, executionModelmovement):
                return self.return_result(msg="Sin procesamiento de solicitud", confidence=0.0)
            
            tasks = []
            
            tasks.append(self._singTrace_evaluation.exec_model_async(data=data, executionModelpool=executionModelpool))
            tasks.append(executionModelmovement.evaluation_async(model_evaluation=self._body_evaluation, data=data))
            rst = await asyncio.gather(*tasks)
            
            res = rst[0]
            if res['rule_match'] == False:
                return self.return_result(result=res['rule_match'], confidence=res['confidence_results'], msg="Resultado obtenido exitosamente, no cumple con la directriz de mano", review=True)
            
            res = rst[1]
            if res is None:
                return self.return_result(msg="Resultados sin evaluar", confidence=0.0)
            
            result, confidence = utils.utils().evaluation_standard_body(data=res)
            return self.return_result(result=result, confidence=confidence, msg="Resultado obtenido exitosamente", review=True)        
        except Exception as e:
            print("Error Ocurrido [Model Exec - StateTrace], Mensaje: {0}".format(str(e)))
            return self.return_result(msg="Error Ocurrido [Model Exec - StateTrace], Mensaje: {0}".format(str(e)), review=True)

    def train_model(self, trainModelmovement: tm.TrainModelMovement=None, trainModelpool: tm.TrainModelPool=None, data=None, face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False):
        try:
            if None in (data, trainModelpool, trainModelmovement):
                raise ex.InvalidTrainModelException()
            
            print(f"------------------------------------------------------------------------------------")
            print(f"Label: {self._label} -  qty_data = {len(data)} -  state = {self._state_value}")
            start_time = time.time()
            print(f" signTrace training-----------------------------------------------------------------")
            
            self._singTrace_evaluation = sm.SignTrace(label=f"{self._label}{self._state_value}", face_relation=face_relation, body_relation=body_relation, hand_relation=hand_relation, hand_diff_relation=hand_diff_relation, evaluationStandard=self._evaluationStandard)
            self._singTrace_evaluation.train_model(trainModelpool=trainModelpool, data=data)
            
            if all(item is None for item in self._singTrace_evaluation.matrix_evaluation):#all(item is None for item in self._singTrace_evaluation.matrix_evaluation) or all(item is None for item in self._singTrace_evaluation.matrix_classification):
                raise ex.InvalidTrainModelException()
            
            print(f" Clustering model movement training------------------------------------------------")
            start_time_g = time.time()
            self._body_evaluation = trainModelmovement.Train_models(data=data)
            end_time_g = time.time()
            print(f"Ejecucion finalizada en {(end_time_g - start_time_g):.2f} segundos.")
            
            if self._body_evaluation is None:
                raise ex.InvalidTrainModelException(group_model=True, msg=f"it was not possible to create the evaluation model for the letter, label: {self._label}{self._state_value}")
            
            print(f" Verification model training------------------------------------------------------")
            result_message = "Insatisfactorio" if None in (self._body_evaluation) else "Satisfactorio"
            end_time = time.time()
            print(f"Label: {self._label}{self._state_value}, Resultado: {result_message}, Mensaje: El entrenamiento finalizo en {(end_time - start_time):.2f} segundos.")
            self._validate = not None in (self._body_evaluation)
                
  
        except Exception as e:
            self._body_evaluation = None
            self._singTrace_evaluation = None
            print(f"Label: {self._label}{self._state_value}, Resultado: Insatisfactorio, Mensaje: {e}")
        finally:
            print(f"------------------------------------------------------------------------------------")
