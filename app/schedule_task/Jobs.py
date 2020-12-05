import re
import os
from datetime import datetime,timedelta
from glob import glob
datetime_rex = re.compile("[0-9]{1}[0-9]{1}[-][0-9]{1}[0-9]{1}[-][0-9]{1}[0-9]{1}[0-9]{1}[0-9]{1}")
from django.conf import settings

def files_management():

    for root, dirs, files in os.walk(settings.MEDIA_ROOT):

        folder_list = root.split("\\")

        folder_str = folder_list[len(folder_list) - 1]

        if datetime_rex.match(folder_str) :

            day_str = folder_str[0:2]
            month_str = folder_str[3:5]
            year_str = folder_str[6:10]
            checked_datetime = datetime(int(year_str), int(month_str), int(day_str))

            during_datetime =  datetime.now()- checked_datetime

            if during_datetime.days > 1 :
                
                for filename in os.listdir(root):
                    file_path = os.path.join(root0, filename)
                    try:

                        if os.path.isfile(file_path) or os.path.islink(file_path):

                            os.unlink(file_path)

                        elif os.path.isdir(file_path):

                            shutil.rmtree(file_path)

                    except Exception as e:

                        print('Failed to delete %s. Reason: %s' % (file_path, e))

                # print(root)
            # print(month_str)
            # print(year_str)


        # print(root)
        # print(folder_str)
        # for folder in dirs :

        #     print(folder)

    # print('test')

    # file_list = [file for file in glob("media/*.")]

    # for file_str in file_list:


    #     print(file_str)
    
    # file_list = [file for file in glob("media/*.csv")]
    # print('test')

    # for file_str in file_list:

    #     date_str = file_str[-19:].split('.')[0]

    #     if datetime_rex.match(date_str) :

    #         year_str = date_str[0:4]
    #         month_str = date_str[4:6]
    #         day_str = date_str[6:8]
    #         hour_str = date_str[9:11]
    #         minute_str = date_str[11:13]
    #         checked_datetime = datetime(int(year_str), int(month_str), int(day_str), int(hour_str), int(minute_str))
    #         during_datetime =  datetime.now()- checked_datetime

    #         if during_datetime.days > 0 :

    #             if os.path.exists(file_str):
    #                 os.remove(file_str)
    #             else:
    #                 print("The file does not exist")
