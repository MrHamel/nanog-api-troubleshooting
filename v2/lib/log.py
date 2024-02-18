from datetime import datetime
import logging
import os

class Log:
    log_full_name = None
    logger = None
    
    @staticmethod
    def start(script_function, output_dir):
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
            
        print(f"\nIf log entries are present, the file will be saved under: {output_dir}\n")

        script_time_stamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        log_filename      = f"{output_dir}/{script_function}_log_{script_time_stamp}.log"
        logger            = logging.getLogger(script_function)
        
        # create file handler which logs even debug messages
        fh = logging.FileHandler(log_filename)
        fh.setLevel(logging.WARNING)

        # create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)-15s %(levelname)-8s %(message)s")
        fh.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        
        Log.log_full_name = log_filename
        Log.logger        = logger
        
    @staticmethod
    def get():
        if Log.logger:
            return Log.logger
        else:
            Log.start("generic_program", "/tmp")
            return Log.logger

    @staticmethod
    def end():
        if os.stat(Log.log_full_name).st_size == 0:
            print(f"\nLog file was empty, removing file: {Log.log_full_name}")
            os.remove(Log.log_full_name)
        else:
            print(f"\nScript has log entries, find log here: {Log.log_full_name}")