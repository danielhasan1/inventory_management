# Warehouse CLI Tool
## Overview
This is a simple command-line tool to manage warehouse locations and inventories. It supports registering/unregistering locations, incrementing/decrementing items, transferring items between locations, and observing inventories.

The tool persists state in an SQLite database file so multiple CLI instances can safely operate concurrently.

## Design Decisions
### Data Storage
**SQLite** was chosen as the persistence layer because it is lightweight, requires no setup, and supports safe concurrent access.

* Schema:

  * locations(id VARCHAR PRIMARY KEY, name VARCHAR UNIQUE, status INTEGER)

  * inventory(id VARCHAR  PRIMARY KEY, location_id VARCHAR, item_id VARCHAR, quantity INTEGER)

### Data Structures

* Dataclasses (Location, Inventory) represent domain entities in Python.

* Repositories handle database queries (separating persistence from business logic).

* Services implement business rules (e.g., preventing deregistration if inventory exists).

* Factory pattern is used to expose service instances cleanly.

### Input/Output
* Commands are read from stdin, one per line.

* Responses are written to stdout, in the format described in the assignment.

* Error messages are prefixed with ERR: and success with OK.

### Concurrency Handling
* SQLite’s built-in locking ensures consistency when multiple CLI instances access the same file.

* Each command commits immediately after success, so state is always durable.

### External Dependencies

* No external dependencies were used; only the Python standard library (sqlite3, uuid, dataclasses).

* This keeps the project lightweight and easy to run anywhere.

## Running the Tool
```commandline
python cli.py
```

Then Enter commands like

```commandline
LOCATION REGISTER LA
INVENTORY INCREMENT LA IA 5
INVENTORY OBSERVE LA
```


## Notes

In real-world systems, an ORM (like SQLAlchemy) would normally be used for maintainability, but here raw sqlite3 is sufficient for simplicity.

The layered design (models → repositories → services → CLI) is deliberate to show scalability without overcomplicating the solution.