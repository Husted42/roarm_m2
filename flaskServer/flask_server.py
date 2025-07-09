from flask import Flask, jsonify
from flask_apscheduler import APScheduler
import datetime

import gmail_read_name
import roarm_movement

# Globals
global_latest_mail = None

app = Flask(__name__)

def activate_robot_arm(debug=True):
    '''
    This function checks if we have received a robot arm activation email.
    '''
    # Sting contatining the latest email subject
    global global_latest_mail

    # Variable for boolean logic 
    is_robot_mail = False
    is_new_mail = False
    is_first_load = False

    if debug:
        print("\n\n", datetime.datetime.now(), " - Activating robot arm...")
        print("Latest email subject:", global_latest_mail)

    # Check if string starts with "Robot arm - "
    if global_latest_mail is not None and global_latest_mail.lower().startswith("robot arm - "):
        is_robot_mail = True
    if global_latest_mail != gmail_read_name.read_gmail_header():
         is_new_mail = True
    if global_latest_mail is None:
        is_first_load = True

    if is_first_load:
        print("First load, no previous email found.")
        global_latest_mail = gmail_read_name.read_gmail_header()
        return False

    if is_robot_mail and is_new_mail and not is_first_load:        
        print("Variable has changed, activating robot arm...")
        global_latest_mail = gmail_read_name.read_gmail_header() 

        roarm_movement.main()

        return True
    else:
        return False


@app.route('/')
def home():
    return "Hello, world!"


@app.route('/get_latest_mail')
def get_latest_mail():
    """
    Returns the latest email subject line.
    """
    try:
        latest_mail = gmail_read_name.read_gmail_header()
        return jsonify({"latest_mail": latest_mail})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.add_job(
        func=activate_robot_arm,
        args=[False],
        trigger='interval',
        id='robot_check_job',
        seconds=3
    )
    scheduler.start()

    print("Starting Flask app and scheduler...")
    app.run()
