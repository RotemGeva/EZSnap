import sys
import time
import keyboard
import pyscreeze as py
import os
import configparser
import logging
import pyautogui
from win10toast import ToastNotifier
from Configuration import Configuration

# Add to --copy-metadata=win10toast
# In win10toast __init__.py - on_destroy function changed to "return 0" instead of "return None"

def create_log():
    logging.basicConfig(filemode='w', filename='EZSnap.log',
                        format='%(asctime)s.%(msecs)03d %(levelname)-8s %('
                               'funcName)-32s'
                               '%(message)s', datefmt='%d-%m-%Y %H:%M:%S',
                        level=logging.INFO)
    logging.info('Log initialized.')


def check_keys(keys):
    """
    Checks if key combination for was pressed.
    :param keys: Given keys combination.
    :return: Return true if keys were pressed.
    """
    for key in keys:
        if not keyboard.is_pressed(key):
            return False
    logging.info("Combination key function was activated.")
    return True


def is_released(keys):
    """
    Checks if key combination for screenshots was released.
    :param keys: The key combination that supposed to be released.
    :return: Return true if keys were released.
    """
    for key in keys:
        if not keyboard.is_pressed(key):
            return True
    logging.info("Combination key release function was activated.")
    return False


def read_configuration_file() -> dict:
    try:
        config = configparser.ConfigParser()
        script_dir = os.getcwd()
        logging.info(f"Reading configuration file from: {os.path.join(script_dir, 'configuration.ini')}.")
        config.read(os.path.join(script_dir, 'configuration.ini'))
        configuration_dict = {section: dict(config.items(section)) for section in config.sections()}
        return configuration_dict
    except Exception as err:
        logging.error(f"Error during reading configuration file. {err}")
        raise Exception()


def parse_configuration_file(configuration_info: dict) -> Configuration:
    try:
        logging.info(f"Parsing information of configuration file: {configuration_info}.")
        location_info = configuration_info.get('Location')
        names_info = configuration_info.get('Names')
        numbering_info = configuration_info.get('Numbering')
        timeout_info = configuration_info.get('Timeout')
        timeout = int(timeout_info.get('timetoselfterminate')) * 60
        configuration = Configuration(location_info, names_info, numbering_info, timeout)
        return configuration
    except Exception as err:
        logging.error(f"Failed to retrieve all information from configuration file. {err}")
        raise Exception()


def start_snipping(configuration, last_action_time, index_counter, restart_numbering='ON'):
    """
    Handles all snipping process.
    :param configuration: Contains all configuration details.
    :param last_action_time: Last time the user activated the app.
    :param index_counter: Image number in current directory.
    :param restart_numbering: Restarts numbering of images in folder when previous folder does not exist.
    """
    keys_to_snip = ["ctrl", "alt", "z"]
    keys_to_close = ["ctrl", "alt", "s"]
    keys_to_check = ["ctrl", "alt", "x"]
    logging.info(f"Start snipping; Closing keys: {keys_to_close}; Snipping keys: {keys_to_snip}, "
                 f"restart numbering: {restart_numbering}.")
    toaster = ToastNotifier()
    while True:
        start_time_loop = time.time()
        try:
            if time.time() - last_action_time >= configuration.timeout:
                logging.info("Time cap was reached.")
                toaster.show_toast("Closing EZSnap!", "Bye!", duration=4, icon_path=configuration.icon_path)
                sys.exit()
            time.sleep(0.001)
            if check_keys(keys_to_close):
                logging.info("Detected closing combination. Closing EZSnap...")
                toaster.show_toast("Closing EZSnap!", "Bye!", duration=4, icon_path=configuration.icon_path)
                sys.exit()
            if not os.path.exists(configuration.folder_path):
                logging.info("Target folder was changed, creating a new folder in path..")
                os.makedirs(configuration.folder_path)
                if restart_numbering == 'ON':
                    index_counter = 1
            if check_keys(keys_to_snip):
                last_action_time = time.time()
                logging.info("Recorded last action time.")
                logging.info(f"Detected snapshots combination. Creating screenshot...")
                screenshot = py.screenshot()
                screenshot.save(configuration.folder_path + "\\" + configuration.img_name + str(index_counter) + ".png")
                msg = configuration.img_name + str(index_counter) + " was saved"
                toaster.show_toast("Saved!", msg, duration=2, icon_path=configuration.icon_path)
                index_counter += 1
            if check_keys(keys_to_check):
                last_action_time = time.time()
                logging.info("Detected still here combination. Presenting message still here.")
                toaster.show_toast("Still Here!", "EZSnap is still working in background",
                                   duration=3, icon_path=configuration.icon_path)
                while time.time() - start_time_loop < 0.5:
                    logging.info("Keys up")
                    pyautogui.keyUp('ctrl')
                    pyautogui.keyUp('alt')
                    pyautogui.keyUp('z')

        except Exception as err:
            logging.error(f"Failed to take a screenshot, {err}")
            raise Exception()


# Main
create_log()

config_info = read_configuration_file()
configuration = parse_configuration_file(config_info)
last_action_time, index_counter = configuration.start_application
match configuration.numbering.get("restartimgnumber"):
    case 'ON':
        start_snipping(configuration, last_action_time, index_counter)
    case 'OFF':
        start_snipping(configuration, last_action_time, index_counter, 'OFF')


