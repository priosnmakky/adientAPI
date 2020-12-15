from apscheduler.schedulers.background import BackgroundScheduler
from app.schedule_task.Jobs import files_management
from app.helper.config.ConfigsDatabase import ConfigsDatabase

def start_jobs():
    scheduler = BackgroundScheduler()
    
    #Set cron to runs every 20 min.
    cron_job = {'month': configsDatabase.configs.get("CRON_JOB_MONTH").data,
        'day': configsDatabase.configs.get("CRON_JOB_DAY").data,
        'hour': configsDatabase.configs.get("CRON_JOB_HOUR").data, 
        'minute':configsDatabase.configs.get("CRON_JOB_MINUTE").data}
    
    #Add our task to scheduler.
    scheduler.add_job(files_management, 'cron', **cron_job)
    #And finally start.    
    scheduler.start()