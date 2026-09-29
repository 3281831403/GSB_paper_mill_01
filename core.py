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
    }


def save_state(state):
    return json.dumps(state, ensure_ascii=False)


def load_state(text):
    state = json.loads(text)
    return state


def feed(state, batch_id, amount):
    if batch_id in state["batches"]:
        return False
    if state["machine_load"] >= state["machine_capacity"]:
        return False
    if amount > state["pulp"]:
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
    if batch_id not in state["batches"]:
        return False
    amount = state["batches"].pop(batch_id)
    state["machine_load"] -= amount
    return True


def produce(state, amount):
    if state.get("whitewater_fault"):
        return False
    return True


def break_event(state):
    state["loss"] += 10
    return state["loss"]


def start(state):
    if state["pulp"] <= 0:
        return False
    return True


def main():
    print("造纸厂 - 命令: feed/moisture/cancel/produce/break/start/quit")
    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not raw or raw == "quit":
            break
        print("ok")


if __name__ == "__main__":
    main()
