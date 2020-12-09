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
                    file_path = os.path.join(root, filename)
                    try:

                        if os.path.isfile(file_path) or os.path.islink(file_path):

                            os.unlink(file_path)

                        elif os.path.isdir(file_path):

                            shutil.rmtree(file_path)

                    except Exception as e:

                        print('Failed to delete %s. Reason: %s' % (file_path, e))
