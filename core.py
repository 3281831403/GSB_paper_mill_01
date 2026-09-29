"""造纸厂核心逻辑：浆料、抄纸机、白水回收和损耗。"""

import json


def new_game():
    return {
        "batches": {},
        "machine_load": 0,
        "machine_capacity": 2,
        "pulp": 100,
        "loss": 0,
        "batch_id": 0,
        "production": 0,
        "running": False,
        "whitewater_fault": False,
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    return json.loads(text)


def feed(state, batch_id, amount):
    if batch_id in state["batches"]:
        return False
    if state["machine_load"] >= state["machine_capacity"]:
        return False
    if state["pulp"] < amount:
        return False
    state["batches"][batch_id] = amount
    state["machine_load"] += amount
    state["pulp"] -= amount
    return True


def check_moisture(state, moisture):
    if moisture >= 40:
        return "wet"
    return "ok"


def cancel(state, batch_id):
    amount = state["batches"].get(batch_id)
    if amount is None:
        return False
    state["machine_load"] -= amount
    state["pulp"] += amount
    del state["batches"][batch_id]
    return True


def produce(state, amount):
    if state.get("whitewater_fault", False):
        return False
    state["production"] = state.get("production", 0) + amount
    return True


def break_event(state):
    state["loss"] += 10
    return state["loss"]


def start(state):
    if state["pulp"] <= 0:
        return False
    state["running"] = True
    return True


def main():
    print("造纸厂 - 命令: feed/moisture/cancel/produce/break/start/quit")
    state = new_game()
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        parts = raw.split()
        command = parts[0]
        try:
            if command == "feed":
                amount = int(parts[1])
                batch_id = state["batch_id"] + 1
                if feed(state, batch_id, amount):
                    state["batch_id"] = batch_id
                    print("fed batch %s amount %s" % (batch_id, amount))
                else:
                    print("feed rejected")
            elif command == "moisture":
                print(check_moisture(state, int(parts[1])))
            elif command == "cancel":
                print("cancelled" if cancel(state, int(parts[1])) else "cancel rejected")
            elif command == "produce":
                print("produced" if produce(state, int(parts[1])) else "produce rejected")
            elif command == "break":
                print("loss %s" % break_event(state))
            elif command == "start":
                print("started" if start(state) else "start rejected")
            else:
                print("unknown command")
        except (IndexError, ValueError):
            print("bad arguments")


if __name__ == "__main__":
    main()
