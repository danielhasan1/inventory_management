# import argparse
import sys


from factory import WarehouseFactory



COMMANDS = {
    ("LOCATION", "REGISTER"): WarehouseFactory.get_location_service().register_location,
    ("LOCATION", "UNREGISTER"): WarehouseFactory.get_location_service().deregister_location,
    ("INVENTORY", "INCREMENT"): WarehouseFactory.get_inventory_service().increment_inventory,
    ("INVENTORY", "DECREMENT"): WarehouseFactory.get_inventory_service().decrement_inventory,
    ("INVENTORY", "TRANSFER"): WarehouseFactory.get_inventory_service().transfer_inventory,
    ("INVENTORY", "OBSERVE"): WarehouseFactory.get_inventory_service().observer_inventory,
}


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--db", default="warehouse.db", help="Path to database file")
    # args = parser.parse_args()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        tokens = line.split()
        handler = COMMANDS.get(tuple(tokens[:2]))
        if not handler:
            print("> UNKNOWN_COMMAND")
            continue
        result = handler(*tokens[2:])
        print(f"> {result}")


if __name__ == "__main__":
    main()