import os
import sys
import pandas as pd 

from ...source.Logger import logging
from ...source.Exception import CustomException
from ...source.Utils import load_object


class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
class PredictPipeline:

    """"
    Yes if train a model then we also need to use it and predict the values out of it.
    This will predict our Target Variable using Trained best Model and give outcomes.

    """

    def __init__(self, problem_objective):
        self.Problem_Objective = problem_objective

    def predict(self, features):

        """
        Given Features in the Predict Funciton it take our test file and output the prediction.
        If classification then it will handle label encoding (from the pkl file) and reverse it to the orignal values.

        """

        try:
            model_path = os.path.join("artifact", "model.pkl")
            preprocessor_path = os.path.join('artifact', 'prerocessor.pkl')
        
            if self.Problem_Objective=="Classification":
                label_encoder_path = os.path.join('artifact','Targetlabel.pkl')
                label_encoder = load_object(file_path=label_encoder_path)
                logging.info("Here Target_label is also loaded succesfully")
            
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("Model Loaded Succesfully")
            logging.info("Preprocessing and model Loading is Successful")
            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            if self.Problem_Objective=="Classification":
                preds = preds.astype(int)
                preds = label_encoder.inverse_transform(preds)
                logging.info("Classification Done Succesfully and decoded the prediction to orignal Target Values")
            
            return preds

        except Exception as e:
            raise CustomException(e, sys)
        
class CustomData:

    """
    Our Program do not need to give Features and DF  hard coded into this,
    It will take care of all the Features .
    CustomData class is designed to dynamically handle features and convert them into a DataFrame,
    providing flexibility in working with different datasets.
    """


    def __init__(self,features_cols, **kwargs):
        try:
            self.Features_Cols = features_cols
            for feature in self.Features_Cols:
                # print(feature)
                setattr(self, feature, kwargs.get(feature, None))

        except Exception as e:
            raise CustomException(e, sys) 
    
    def get_data_as_data_frame(self):

        """ Here it will take our Custom data and convert it into Dataframe"""

        try:
            custom_data_input_dict = {}
            for feature in self.Features_Cols:
                feature_value = getattr(self,feature)
                #print("Fearture: ",feature,"Value: ",type(list(feature_value)))
                custom_data_input_dict[feature] = list(feature_value)
            logging.info("Features Loaded Succesfully")
            #print(custom_data_input_dict)
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
