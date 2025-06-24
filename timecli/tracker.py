from datetime import datetime

from dateutil import parser

from timecli.storage import load_sessions, save_sessions

SESSIONS_PATH = "data/sessions.json"


def start_task(project, tags):
    sessions = load_sessions()
    if any(s.get("end") is None for s in sessions):
        print("⚠️ There is a task running, please stop it first.")
        return

    frame = {
        "project": project,
        "tags": tags,
        "start": datetime.now().isoformat(),
        "end": None,
    }
    sessions.append(frame)
    save_sessions(sessions)
    print(f"🚀 Task '{project}' started!")


def stop_task():
    sessions = load_sessions()
    for s in reversed(sessions):
        if s.get("end") is None:
            s["end"] = datetime.now().isoformat()
            save_sessions(sessions)
            print(f"⏹️ Task '{s['project']}' stopped.")
            return
    print("⚠️ No task is running.")


def status_task():
    sessions = load_sessions()
    for s in reversed(sessions):
        if s.get("end") is None:
            start_time = parser.isoparse(s["start"])
            now = datetime.now()
            duration = now - start_time
            minutes = int(duration.total_seconds() // 60)
            seconds = int(duration.total_seconds() % 60)
            print(f"🟢 Task on: {s['project']}")
            print(f"⏱️ Running for: {minutes} min {seconds} sec")
            return
    print("⚪ No task is running.")


def resume_task():
    sessions = load_sessions()
    last = None
    for s in reversed(sessions):
        if s.get("end") is not None:
            last = s
            break

    if not last:
        print("⚠️ No previous task to resume.")
        return

    new_frame = {
        "project": last["project"],
        "tags": last["tags"],
        "start": datetime.now().isoformat(),
        "end": None,
    }
    sessions.append(new_frame)
    save_sessions(sessions)
    print(f"🔁 Task '{last['project']}' resumed.")
