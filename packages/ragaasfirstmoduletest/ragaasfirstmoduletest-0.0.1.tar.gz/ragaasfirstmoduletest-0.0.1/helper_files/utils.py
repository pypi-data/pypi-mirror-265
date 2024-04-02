import yaml
import logging
import traceback
from logging.handlers import RotatingFileHandler
import pandas as pd
import os, sys
from datetime import datetime, timedelta
from helper_files.ragaas_constants import Run_Mode

class StaticClass:
    # to get log_path from config file, defined in main.py
    # Below path is default for log file to store
    path = "./rag_evaluation_errors.log"
    conf = None


def get_ragaas_run_mode(conf):
    # # A. generation + evaluation pipeline
    # if ((conf['synthetic_dataset']['create'] == True)) and ((conf['metrics']['create'] == True)):
    #     return Run_Mode.Synthetic_Generation_And_Evaluation
    # elif ((conf['synthetic_dataset']['create'] == True)) and ((conf['metrics']['create'] == False)):

    # # A. generation
    if (conf['synthetic_dataset']['create'] == True):
        return Run_Mode.Synthetic_Generation_only
    # B . run evaluation on public dataset
    elif (conf['public_dataset']['use'] == True):
        return Run_Mode.Evaluation_public
    # C. run evaluation on golden dataset
    elif (conf['golden_dataset']['use'] == True):
        return Run_Mode.Evaluation_Golden



def setup_logging(level, filename=None, filemode="a"):
    """
    Set up basic configuration for logging
    :param level: one of (logging.INFO, logging.DEBUG, logging.WARNING, logging.CRITICAL, logging.ERROR)
    :param filename (str): if specified, logging information to filename
    :param filemode (str): one of ["a", "w"]. If "a", log info will be appended to filename.
                            Else previous log will be deleted.
    :return:
    """
    #logging.getLogger().setLevel(level)
    if filename is not None:
        logging.basicConfig(format='[%(asctime)s] %(message)s',
                            datefmt='%Y-%m-%d %I:%M:%S %p',
                            level=level,
                            filename=filename,
                            filemode=filemode)
    else:
        logging.basicConfig(format='[%(asctime)s] %(message)s',
                            datefmt='%Y-%m-%d %I:%M:%S %p',
                            level=level)

# Exception handler Decorator
def exception_handler(*col_args):
    def inner(function):
        def wrapped_func(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                logging.exception(e, exc_info=True)
                trace = str(traceback.format_exc())
                log_path = StaticClass.path
                log_file_directory = os.path.dirname(log_path)
                os.makedirs(log_file_directory, exist_ok=True)
                ## write Traceback to log file
                with open(log_path, 'a+') as fp:
                    fp.write(f'{datetime.now()} ==> {trace} => {e} {col_args}\n')
        return wrapped_func
    return inner

def read_conf_file(conf_path):
    try:
        with open(conf_path, 'r') as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        #TODO - my be add logging here
        print(exc)
        return None
    return data


def read_input_file(filepath):
    file_type = filepath.split('.')[1]
    if file_type == 'csv':
        df = pd.read_csv(filepath)
    elif file_type == 'xlsx':
       
        print(filepath)
        df = pd.read_excel(filepath)
    elif file_type == 'xls':
        df = pd.read_excel(filepath)
    elif file_type == 'json':
        df = pd.read_json(filepath)
    else:
        logging.warning(f'unrecognized input file format: {file_type}')
    return df

class ExcelHandler():
    def load_data(self, file_path):
        pass

    @staticmethod
    def write_dataframe_to_excel(file_path, dataframe, index=False, encoding='UTF-8'):
        dataframe.to_excel(file_path, index=index)

class OutputGenerator:
    @exception_handler()
    def generate_output(path_out, df_eval, output_file_name="Ragaas_Evaluation_Results_df"):
        if (df_eval is None) or df_eval.empty:
            logging.info("No data found!")
            return
            
        os.makedirs(path_out, exist_ok=True)
        # Save the data in excel format to retain unicode characters
        full_file_path = os.path.join(path_out, output_file_name + '.xlsx')  # xls csv
        logging.info(f"________Saving the output: {full_file_path}________")
        ExcelHandler.write_dataframe_to_excel(full_file_path, df_eval)
        return



