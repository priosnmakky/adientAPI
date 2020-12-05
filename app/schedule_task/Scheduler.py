from apscheduler.schedulers.background import BackgroundScheduler
from app.schedule_task.Jobs import files_management
def start_jobs():
    scheduler = BackgroundScheduler()
    
    #Set cron to runs every 20 min.
    cron_job = {'month': '*', 'day': '*', 'hour': '*', 'minute':'*/1'}
    
    #Add our task to scheduler.
    scheduler.add_job(files_management, 'cron', **cron_job)
#And finally start.    
    scheduler.start()