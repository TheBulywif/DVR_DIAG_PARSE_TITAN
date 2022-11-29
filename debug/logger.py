import logging
import os


global logger
version = 'DVRLPv11.22.01'


def init_logger():
    try:
        logger = logging.getLogger('DVRLP Logger')
        logger.setLevel(logging.DEBUG)
        # CREATE FILE HANDLE
        fh = logging.FileHandler(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', version,
                                              'DVRLPLog.log'))
        fh.setLevel(logging.DEBUG)
        # CREATE CONSOLE OUTPUT HANDLER
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # CREATE FORMAT
        formatter = logging.Formatter('%(asctime)s: %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # ch.setFormatter(formatter)
        # ADD HANDLER
        logger.addHandler(fh)
        # logger.addHandler(ch)
        logger.debug("DIAGNOSTIC LOG INITIALIZED")
        return logger
    except NameError as e:
        logger.error(f"NameError: {e}")
        os.mkdir(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', version))
        init_logger()
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: {e}")
        os.mkdir(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', version))
        init_logger()
    except FileExistsError as e:
        logger.error(f"FileExistsError: {e}")


# START LOG
def start_log(logger):
    logger.info(f"---STARTING DIAGNOSTIC LOGGING---\n")


# END LOG
def end_log(logger):
    logger.info(f"---ENDING DIAGNOSTIC LOGGING---\n")


if __name__ == '__main__':
    log = init_logger()
    start_log(log)
    end_log(log)
