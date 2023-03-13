from engine.engine import engine
import time

if __name__ == "__main__":
    e = engine("template/simulation.json")
    e.start_simulation()
    time.sleep(15)
    e.stop_simulation()
    print("fine")
