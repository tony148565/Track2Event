from core.pipeline import run_track2event

def main():
    result = run_track2event()
    print("stationary events:", len(result["stationary_events"]))

if __name__ == "__main__":
    main()