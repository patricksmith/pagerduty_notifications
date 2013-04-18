pagerduty_notifications
=======================

A script to send email to individuals about to go on PagerDuty rotation. Uses the (PagerDuty API)[http://developer.pagerduty.com/] to find users that will be on call next Monday and send them an email.

Why?
----

While PagerDuty is great for notifying you of problems, it won't notify you when you're on call. I wrote this script after I had unknowningly been on call for a couple days so that next time I'd be prepared.

How?
----

This script will connect to the PagerDuty API to find applicable schedules that you want to send emails about. The users that are on call the next Monday (from whenever the script is run) for each schedule will be sent an email.

Monday is the day our schedules change users, but you can update the script use a different offset, if you wish.

I currently have this running as a cronjob once a week to notify developers a couple days before they're on call.

How Do I Use It?
----------------

To run the script, simply run `python pagerduty_notifications.py`. You'll need to have the python package `requests` (>1.0) installed.

You'll want to update the constants at the top of the code file to point to your company's PagerDuty API (`BASE_URL`), the correct auth token (`AUTH_TOKEN`), the schedules to be alerted on (`SCHEDULES`), and some details about the mail being sent (`SMPT_HOST`, `FROM_ADDRESS`).

A note on the `SCHEDULES`: this should be a list of strings that match the names of the schedules you want to notify on or strings that appear at the beginning of the name of the schedules. So, if you have two schedules "Developer Primary" and "Developer Secondary", you can set `SCHEDULES` to either `["Developer Primary", "Developer Secondary"]` or simply `["Developer"]`.
