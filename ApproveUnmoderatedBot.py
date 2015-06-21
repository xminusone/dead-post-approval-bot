import praw
import datetime
import time

print('Dead Post Approval Bot - v1.0b')
print('Logging in to reddit account...')
r = praw.Reddit('Dead Post Approvals v1.0 - /u/YOURUSERNAME')
r.login('USERNAME', 'PASSWORD')
print('Success!')

# Print Current Timestamp, stolen from titlecheckbot
def printCurrentTime():
    currentSysTime = time.localtime()
    print(time.strftime('(%m/%d/%y: %H:%M:%S)', currentSysTime))

# Actual bot stuff
def queueCheckerBot():
    print('Starting cycle.')
    printCurrentTime()
    print('Updating current time...')
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    print('Grabbing unmoderated queue for /r/mod...')
    s = r.get_subreddit('mod')
    unmoderated = s.get_unmoderated(limit=1000) # Change this limit if you want to have it check less submissions for some reason
    print('Checking age of unmoderated submissions.')
    for submission in unmoderated:
        try:
            age = now - submission.created_utc
            if age < 86400:
                # Skips posts under 24hrs old
                print('Submission is less than 24hrs old, continuing.')
                continue
            if len(submission.mod_reports + submission.user_reports) > 0:
                # Skips posts that have reports
                print('Submission has reports, continuing.')
                continue
            print('Submission is 24hrs old, approving...')
            # Approves posts that are 24hrs old
            submission.approve()
            print('Done!')
        except:
            print('Error! Skipping submission.')
while True:
    try:
        queueCheckerBot()
        print('Cycle complete! Checked all submissions. Rechecking in 60min.')
        print('----------')
        time.sleep(3600)
    except:
        print('Error! Something broke. Retrying cycle.')
        pass
