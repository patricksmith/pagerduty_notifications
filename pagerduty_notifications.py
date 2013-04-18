from email.mime.text import MIMEText
import datetime
import requests
import smtplib

## Tailor the below constants to suit your environment
AUTH_TOKEN = 'REPLACE_ME'
"""Authorization token for the PagerDuty API."""
BASE_URL = 'REPLACE_ME'
"""Location of the PagerDuty API."""
SCHEDULES = [
    'Developer',
]
"""A list of schedules to send notifications for.

Can be the entire name of the schedule or a string that should appear at the
beginning of any applicable schedule's name.

"""
SMTP_HOST = 'localhost'
"""The host to connect to send mail."""
FROM_ADDRESS = 'REPLACE_ME@example.com'
"""The address mail will be sent from."""


HEADERS = {
    'Authorization': 'Token token={0}'.format(AUTH_TOKEN),
    'Content-type': 'application/json',
}


def is_developer_schedule(schedule):
    return schedule['name'].startswith('Developer')


def is_sysadmin_schedule(schedule):
    """Only consider Tier 1 sysadmins. Tiers 2 and 3 don't change."""
    return schedule['name'].startswith('Sysadmin Tier 1')


def is_schedule_relevant(schedule):
    """Tests whether a notification should be sent for `schedule`."""
    for applicable_schedule in SCHEDULES:
        if schedule['name'].startswith(applicable_schedule):
            return True
    return False


def schedules():
    """An iterable of applicable schedules."""
    all_schedules = requests.get(
        '{0}/schedules'.format(BASE_URL),
        headers=HEADERS,
    )
    for schedule in all_schedules.json()['schedules']:
        if is_schedule_relevant(schedule):
            yield schedule


def get_on_call(schedule_id, since):
    """Returns user oncall for `schedule_id` on day specified by `since`."""
    payload = {
        'since': since,
        'until': since + datetime.timedelta(days=1),
    }
    response = requests.get(
        '{0}/schedules/{1}/entries'.format(BASE_URL, schedule_id),
        headers=HEADERS,
        params=payload,
    )

    return response.json()['entries'][0]['user']


s = smtplib.SMTP(SMTP_HOST)
today = datetime.date.today()
offset = 7 - datetime.date.weekday(today)
since = today + datetime.timedelta(days=offset)
for schedule in schedules():
    user = get_on_call(schedule['id'], since)
    text = """Greetings {name},

This is a friendly reminder that you will be on call for {schedule} for the
week beginning {date}.

Enjoy!
""".format(name=user['name'], schedule=schedule['name'], date=since)
    msg = MIMEText(text)
    msg['Subject'] = "You're on call next week"
    me = FROM_ADDRESS
    you = user['email']
    msg['From'] = me
    msg['To'] = you
    s.sendmail(me, [you], msg.as_string())

s.quit()
