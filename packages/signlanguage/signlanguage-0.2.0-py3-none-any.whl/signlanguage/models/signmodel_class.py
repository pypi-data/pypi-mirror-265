from signlanguage.interfaces.interfaces_model       import ITrace
import signlanguage.core.trainmodel_class           as tm
import signlanguage.core.executionmodel_class       as em
import signlanguage.interfaces.transfermodel_class  as ex
import signlanguage.utils.utils_class               as utils
import numpy                           as np
import time
import asyncio

#principal class execution
class SignTrace(ITrace):
    def __init__(self, label= "", face_relation=False, body_relation=False, hand_relation=False, hand_diff_relation=False, evaluationStandard=True):
        self._matrix_evaluation = []
        self._matrix_classification = []
        self._validate = False
        self._label = label
        self._hand_relation = hand_relation
        self._face_relation = face_relation
        self._hand_diff_relation = hand_diff_relation
        self._body_relation = body_relation
        self._evaluationStandard = evaluationStandard

    @property
    def label(self):
        return self._label
    
    @property
    def validate(self):
        return self._validate

    @property
    def matrix_classification(self):
        return self._matrix_classification

    @property
    def matrix_evaluation(self):
        return self._matrix_evaluation

    @matrix_evaluation.setter
    def matrix_evaluation(self, value):
        self._matrix_evaluation = value

    def return_result(self, result=False, confidence=0.0, msg="", review=False):
        return {
            "hand_value": self._label,
            "evaluado": review,
            "rule_match": result,
            "message": msg,
            "confidence_results": confidence
        }
    
    async def exec_model_async(self, executionModelpool: em.ExecutionModelPool, data=None):
        if data is None or executionModelpool is None:
            return self.return_result(msg="Sin procesamiento de solicitud", confidence=0)
            
        res = await executionModelpool.evaluation_async(
            model_evaluation=self._matrix_evaluation, 
            data=data, face_relation=self._face_relation, 
            body_relation=self._body_relation, 
            hand_relation=self._hand_relation, 
            hand_diff_relation=self._hand_diff_relation
        )
        if res is None:
            return self.return_result(result=False, confidence=0, msg="Resultado obtenido exitosamente - no cumple con los criterios", review=True)
        
        if all(element is None for element in res):
            return self.return_result(msg="Resultados sin evaluar", confidence=0)

        """if self.label == "N" or self.label == "M" or self.label == "P":
            print(self.label)
            print(res)"""
        
        result, confidence = utils.utils().evaluation_standard(data=res)
        return self.return_result(result=result, confidence=confidence, msg="Resultado obtenido exitosamente", review=True)         
    
        print("Error Ocurrido [Model Exec - SignTrace], Mensaje: {0}".format(str(e)))
        return self.return_result(msg="Error Ocurrido [Model Exec - SignTrace], Mensaje: {0}".format(str(e)), review=True)

    def train_model(self, trainModelpool: tm.TrainModelPool, data=None):
        try:
            if trainModelpool is None or data is None:
                raise ex.InvalidTrainModelException()
            
            print(f"------------------------------------------------------------------------------------")
            print(f"Label: {self._label}-  qty_data = {len(data)} -  face_relation={self._face_relation}, body_relation={self._body_relation}, hand_relation={self._hand_relation}, hand_diff_relation={self._hand_diff_relation}")
            start_time = time.time()

            print(f" Clustering model training----------------------------------------------------------")
            #group model
            start_time_g = time.time()
            self._matrix_evaluation = trainModelpool.Train_models(data=data, face_relation=self._face_relation, body_relation=self._body_relation, hand_relation=self._hand_relation, hand_diff_relation=self._hand_diff_relation)
            end_time_g = time.time()
            print(f"Ejecucion finalizada en {(end_time_g - start_time_g):.2f} segundos.")
            
            if self._matrix_evaluation is None:
                raise ex.InvalidTrainModelException(group_model=True, msg=f"it was not possible to create the evaluation model for the letter, label: {self._label}")
            
            print(f" Verification model training------------------------------------------------------")
            result_message = "Insatisfactorio" if all(element is None for element in self._matrix_evaluation) else "Satisfactorio"
            end_time = time.time()
            print(f"Label: {self._label}, Resultado: {result_message}, Mensaje: El entrenamiento finalizo en {(end_time - start_time):.2f} segundos.")
            self._validate = not all(element is None for element in self._matrix_evaluation)
            

        except Exception as e:
            self._matrix_classification = None
            self._matrix_evaluation = None
            print(f"Label: {self._label}, Resultado: Insatisfactorio, Mensaje: {e}")
        finally:
            print(f"------------------------------------------------------------------------------------")
