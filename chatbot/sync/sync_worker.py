import json
import os

from .fetch_api_data import fetch_exam_schedule, fetch_assignments
from ..mcp_server.tools.create_calendar_event import create_calendar_event
from ..mcp_server.tools.update_event_by_title import update_event_by_title
from ..mcp_server.tools.delete_event_by_title import delete_event_by_title

DB_FILE = "chatbot/sync/sync_db.json"


def load_db():

    if not os.path.exists(DB_FILE):
        return {}

    try:
        with open(DB_FILE) as f:
            return json.load(f)
    except:
        return {}


def save_db(db):

    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)


def sync_exams():

    exams = fetch_exam_schedule()
    db = load_db()

    seen = set()

    for subject in exams:

        subject_name = subject["subject"]["name"]

        for exam_type, exam in subject["exams"].items():

            key = f"{subject_name}_{exam_type}"

            title = f"{subject_name} {exam_type}"

            start = exam["startTime"]
            end = exam["endTime"]

            seen.add(key)

            # -------- Create new event --------
            if key not in db:

                print("Creating event:", title)

                create_calendar_event(
                    {
                        "title": title,
                        "start_time": start,
                        "end_time": end
                    }
                )

                db[key] = {
                    "title": title,
                    "start": start,
                    "end": end
                }

            # -------- Update event --------
            else:

                if db[key]["start"] != start:

                    print("Updating event:", title)

                    update_event_by_title(
                        {
                            "title": title,
                            "start_time": start,
                            "end_time": end
                        }
                    )

                    db[key]["start"] = start
                    db[key]["end"] = end

    # -------- Delete removed events --------
    for key in list(db.keys()):

        if key not in seen:

            title = db[key]["title"]

            print("Deleting event:", title)

            delete_event_by_title(
                {
                    "title": title
                }
            )

            del db[key]

    save_db(db)


def sync_assignments():

    assignments = fetch_assignments()
    db = load_db()

    for a in assignments:

        key = f"assignment_{a['id']}"

        title = f"Assignment Due: {a['title']}"

        due = a["dueDate"]

        if key not in db:

            print("Creating assignment:", title)

            create_calendar_event(
                {
                    "title": title,
                    "start_time": due,
                    "end_time": due
                }
            )

            db[key] = {
                "title": title,
                "start": due,
                "end": due
            }

    save_db(db)


def run_sync():

    print("Running academic sync...")

    sync_exams()
    sync_assignments()

    print("Sync finished.")