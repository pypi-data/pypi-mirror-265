import logging
import sys, os
import warnings

warnings.filterwarnings('ignore')


def ragaas_evaluation(conf, df, run_mode = None):

    from dataprocessing.ragaas_processor import Preprocessor, Postprocessor
    from evaluation_model.ragaas_evaluator import Evaluator

    preprocessor = Preprocessor(conf)
    df = preprocessor.execute(df)

    if df is None:
        logging.info(f'RAGAAS Evaluation Pipeline Complete')
        print("RAGAAS Evaluation Pipeline Complete")
        return

    evaluator = Evaluator(conf)
    df_eval = evaluator.execute(df)

    if df_eval is None:
        logging.info(f'RAGAAS Evaluation Pipeline Complete')
        return

    postprocessor = Postprocessor(conf)
    df_eval = postprocessor.execute(df_eval)
    
    if df_eval is None:
        logging.info(f'RAGAAS Evaluation Pipeline Complete')
        return


    # saving the the output
    #TODO- we might have to update output path based on the conf
    OutputGenerator.generate_output(conf['output']['golden_data_output_dir'], df_eval)
    logging.info(f'RAGAAS Evaluation Pipeline Complete')



if __name__ == '__main__':
    # get the base path
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.extend([os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                    os.path.join(base_path, "evaluation", 'src'),
                    os.path.join(base_path, "gensynthetic", 'src')])
    from helper_files.utils import setup_logging, read_conf_file, read_input_file, StaticClass, OutputGenerator, Run_Mode, get_ragaas_run_mode
    setup_logging(logging.DEBUG)

    # I. read config file
    conf_path = os.path.join(base_path, 'config.yaml')
    logging.info("Reading the Config file")
    conf = read_conf_file(conf_path)
  

    # setup logging path
    StaticClass.path = os.path.join(conf['output']['logs_output_dir'], conf['logging']["file"])

    # TODO- get the clearity on how run is going to work based on config
    # III. Idnetify the mode of run (either to run generation + evaluation pipeline or evaluation pipeline alone)
    
    # run_mode = get_ragaas_run_mode(conf)
    # print("got the run mode")


    # TODO- we might have to modify input based on runtype
    # II. read input file
    input_path = conf['input']['golden_data_input_dir']
    df = read_input_file(os.path.abspath(input_path))


    # IV. run the ragaas pipeline based on run_mode
    ragaas_evaluation(conf, df, run_mode = 'Evaluation_Golden')



    
