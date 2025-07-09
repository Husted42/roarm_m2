from flask import Flask, jsonify
from flask_apscheduler import APScheduler
import datetime

import gmail_read_name
import roarm_movement_test

# Globals
global_latest_mail = None

app = Flask(__name__)

def activate_robot_arm(debug=True):
    """
    This function checks if a robot arm activation email has been received.
    """
    global global_latest_mail

    try:
        current_mail = gmail_read_name.read_gmail_header()
    except Exception as e:
        if debug:
            print(f"[{datetime.datetime.now()}] Failed to read Gmail header: {e}")
        return False

    if debug:
        print(f"\n[{datetime.datetime.now()}] Checking for robot arm email...")
        print(f"Previous email: {global_latest_mail}")
        print(f"Current email: {current_mail}")

    if global_latest_mail is None:
        global_latest_mail = current_mail
        print("First run: stored initial email.")
        return False

    if current_mail != global_latest_mail and current_mail.lower().startswith("robot arm - "):
        print("New activation email detected. Triggering robot arm...")
        global_latest_mail = current_mail

        try:
            roarm_movement_test.main()
            print("Robot arm activated successfully.")
        except Exception as e:
            print(f"Error during robot arm activation: {e}")
            return False

        return True

    if debug:
        print("No activation required.")
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
