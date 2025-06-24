from datetime import datetime

from timecli.storage import load_sessions


def show_log():
    sessions = load_sessions()
    for s in sessions:
        end = s["end"] or "In progress"
        print(
            f"- {s['project']} | Início: {s['start']} | Fim: {end} | Tags: {s['tags']}"
        )


def generate_report():
    sessions = load_sessions()
    report = {}
    for s in sessions:
        if not s.get("end"):
            continue
        start = datetime.fromisoformat(s["start"])
        end = datetime.fromisoformat(s["end"])
        duration = (end - start).total_seconds() / 60
        project = s["project"]
        report[project] = report.get(project, 0) + duration

    print("📊 Report about your time:")
    for proj, total in report.items():
        print(f"- {proj}: {total:.1f} minutes")
