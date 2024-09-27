import logging
import os
import time
from winotify import Notification
from win10toast import ToastNotifier


class Configuration:
    def __init__(self, location_info, names_info, numbering_info, timeout_info):
        self._folder_name = None
        self._folder_path = None
        self._img_name = None
        self._location = location_info
        self._naming = names_info
        self._numbering = numbering_info
        self._timeout = timeout_info
        self._icon_path = os.path.join(os.getcwd(), 'EZSnap.ico')
        if not os.path.exists(self._icon_path):
            logging.error(f"EZSnap.ico does not exist in: {self._icon_path}.")
            raise Exception()
        self.configuring_folder_name()
        self.configuring_folder_location()
        self.create_folder()
        self.configure_image_name()

    @property
    def icon_path(self):
        return self._icon_path

    @property
    def timeout(self):
        return self._timeout

    @property
    def folder_path(self):
        return self._folder_path

    @property
    def img_name(self):
        return self._img_name

    @property
    def numbering(self):
        return self._numbering

    def configuring_folder_name(self):
        """
        Updating app variables with folder name and image name info.
        """
        try:
            logging.info(f"Configuring folder name according to: {self._naming}...")
            if self._naming.get('usedefaultfoldername') == 'ON':
                self._folder_name = "EZSnap_Images"
                logging.info(f"Using default folder name: {self._folder_name}")
            else:
                self._folder_name = self._naming.get('foldername')
                logging.info(f"Using modified folder name: {self._folder_name}")
        except Exception as err:
            logging.error(f"Failed configure folder name. {err}")
            raise Exception()

    def configuring_folder_location(self):
        """
        Updating app variables with folder location info and creating target folder.
        """
        logging.info(f"Configuring folder path according to: {self._location}.")
        if self._location.get('usedefaultfolder') == 'ON':
            self._folder_path = os.path.join(os.getcwd(), self._folder_name)
            logging.info(f"Using default folder path:{self._folder_path}")
        else:
            logging.info("Verifying modified folder location exists...")
            if not os.path.exists(self._location.get('path')):
                logging.error(f"Target folder path: {self._location.get('path')} does not exist.")
                raise Exception()
            self._folder_path = os.path.join(self._location.get('path'), self._folder_name)
            logging.info(f"Modified folder path exists, using this folder path: {self._folder_path}.")
            self.create_folder()

    def create_folder(self):
        """
        Creates a folder to contain all snapshots.
        """
        logging.info(f"Checking if folder exists: {self._folder_path}...")
        if not os.path.exists(self._folder_path):
            logging.info("Folder does not exist. Creating new...")
            os.makedirs(self._folder_path)
        else:
            logging.info("Folder already exists. Using existed folder.")

    def configure_image_name(self):
        """
        Updating app variables with image name info.
        """
        try:
            logging.info("Configuring image name...")
            if self._naming.get('usedefaultimagename') == 'ON':
                self._img_name = "Img"
                logging.info(f"Using default image name: {self._img_name}")
            else:
                self._img_name = self._naming.get('imagename')
                logging.info(f"Using modified image name: {self._img_name}")
        except Exception as err:
            logging.error(f"Failed configure image name. {err}")
            raise Exception()

    @property
    def start_application(self):
        """
        Starts application.
        :return: Returns latest image numbering and current action time.
        """
        index_counter = self.get_latest_image_index(self._folder_path, self._img_name)
        last_action_time = time.time()
        # toast = Notification(app_id="EZSnap",
        #                      title="Ready!",
        #                      msg="Use Ctrl+Alt+Z to start snipping",
        #                      icon=self._icon_path)
        # toast.show()
        toaster = ToastNotifier()
        toaster.show_toast("Ready!", "Use Ctrl+Alt+Z to start snipping", duration=3, icon_path=self._icon_path)
        logging.info("EZSnap is ready.")
        return last_action_time, index_counter

    @staticmethod
    def get_latest_image_index(directory, img_name):
        """
        Gets the last image numbering from a given folder.
        :param directory: The directory that contains the images.
        :param img_name: Image title.
        :return: Returns the index of the last image.
        """
        logging.info(f"Finding latest index of images with name: {img_name}, in directory: {directory}")
        largest_number = 0
        for filename in os.listdir(directory):
            if filename.startswith(img_name):
                try:
                    number = int(filename.split(img_name)[1].split(".")[0])
                    if number > largest_number:
                        largest_number = number
                except ValueError:
                    pass  # Ignore files with invalid numbers
        logging.info(f"Latest image number in: {directory} is: {largest_number}")
        return largest_number + 1
