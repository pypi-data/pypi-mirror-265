import os
import logging
from copy import deepcopy
from helper_files.utils import exception_handler, Run_Mode, OutputGenerator, read_input_file
from helper_files.ragaas_constants import Default_Output_Values 

class Inputloader:
    def __init__(self, conf):
        self.conf = conf

    def load_input_data(self, run_mode, base_path):
        # if run_mode == Run_Mode.Synthetic_Generation_And_Evaluation:
        #     # II. read input file
        #     # get the filename
        #     input_filepath = os.path.join(base_path, 'gensynthetic', 'src', 'synthetic_data_filenames.txt')
        #     with open(input_filepath, 'r') as f:
        #         filename = f.read()
        #     file_path = os.path.join(self.conf['output']['synthetic_data_output_dir'], filename)
        #     df = read_input_file(os.path.abspath(file_path))

        # if run_mode == Run_Mode.Evaluation_public:
        #     input_filepath = os.path.join(base_path, 'dataset', 'public_dataset_ouput_filenames.txt')
        #     with open(input_filepath, 'r') as f:
        #         filename = f.read()
        #     file_path = os.path.join(self.conf['output']['public_data_output_dir'], filename)
        #     df = read_input_file(os.path.abspath(file_path))

        if run_mode == Run_Mode.Evaluation_Golden:
            input_path = self.conf['input']['golden_data_input_dir']
            df = read_input_file(os.path.abspath(input_path))
        return df

    @exception_handler()
    def execute(self, run_mode, base_path):
        # run validation on input file
        logging.info("--------RAGAAS EVALUATION: Running Input loader pipeline on output file--------")
        df = self.load_input_data(run_mode, base_path)
        logging.info("--------RAGAAS EVALUATION: Input loader pipeline run complete--------")
        return df


class Preprocessor:
    def __init__(self, conf):
        self.conf = conf

    def validate_input_file(self, df):

        if (df is not None) and (len(df) > 1):
            golden_dataset_dict= self.conf['golden_dataset']
            golden_dataset_dict.pop('use')
            golden_dataset_columns = golden_dataset_dict.values()
            # check if required columns for evaluation are available in the input dataframe
            req_cols = [col for col in golden_dataset_columns if col != '']
            # we dont need to validate 'user_rating', as it might not present in golden dataset 
            req_cols.remove(self.conf['golden_dataset']['user_rating'])
            missing_cols = []
            _ = [missing_cols.append(col) for col in req_cols if col not in df.columns]
            logging.info(f"________missing_cols in input: {missing_cols}________")
            if missing_cols:
                logging.info('________missing columns found________')
                logging.info(f"________Input file validation: FAILED : {missing_cols} not present in the input file________")
                return
            logging.info(f"________Input file validation: OKAY : Required column are present in the input file________")   
            
        return df

    def clean_input_file(self, df):
        if (df is not None) and (len(df) > 1):
            # fill na values with ""
            df.fillna('', inplace=True)
        return df

    @exception_handler()
    def execute(self, df):
        logging.info("------------------RAGAAS Evaluation: Running Model Preprocessing Pipeline------------------")
        # run validation on input file
        logging.info("________RAGAAS Evaluation: Preprocessing- Running input validation on input file________")
        df = self.validate_input_file(df)

        if (df is None) or (len(df) < 1):
            return

        # Perform the cleaning on the input file
        logging.info("________RAGAAS Evaluation: Preprocessing- Performing cleaning on input file________")
        df = self.clean_input_file(df)

        logging.info("------------------Evaluation: Model Preprocessing Pipeline Run Completed------------------")
        return df


class Postprocessor:
    def __init__(self, conf):
        self.conf = conf

    def postprocess_ouput_file(self, df):
        # replace all '-1' with '#NA'
        df.replace(to_replace=[Default_Output_Values.Not_Applicable, Default_Output_Values.Not_Available], value=['#NA', 'Not Available'], inplace=True)

        return df

    @exception_handler()
    def execute(self, df):
        # run validation on input file
        logging.info("---------RAGAAS Evaluation: Postprocessing Output: Running post processing pipeline on output file---------")
        df = self.postprocess_ouput_file(df)
        logging.info("---------RAGAAS Evaluation: Postprocessing Output: Post processing pipeline run complete---------")
        return df


class OutputFileGenerator:
    def __init__(self, conf):
        self.conf = conf

    def save_output(self, df_eval, run_mode, base_path):
        # if run_mode == Run_Mode.Synthetic_Generation_And_Evaluation:
        #     OutputGenerator.generate_output(self.conf['output']['synthetic_data_output_dir'], df_eval)
        # if run_mode == Run_Mode.Evaluation_public:
        #     OutputGenerator.generate_output(self.conf['output']['public_data_output_dir'], df_eval)
        if run_mode == Run_Mode.Evaluation_Golden:
            OutputGenerator.generate_output(self.conf['output']['golden_data_output_dir'], df_eval)
        return


    @exception_handler()
    def execute(self, df_eval, run_mode, base_path):
        # run validation on input file
        logging.info("---------RAGAAS Evaluation : Running Output File Generation Pipeline---------")
        _ = self.save_output(df_eval, run_mode, base_path)
        logging.info("---------RAGAAS Evaluation : Output File Generation Pipeline Completed---------")
        return




