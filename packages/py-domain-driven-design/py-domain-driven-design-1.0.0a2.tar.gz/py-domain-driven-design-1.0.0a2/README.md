[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![First Principles Software](https://img.shields.io/badge/Powered_by-First_Principles_Software-blue)
[![Status](https://img.shields.io/badge/Status-Alpha-yellow)](https://github.com/runemalm/py-domain-driven-design)

> **Note:** This library is currently in alpha stage and is under active development. APIs and features may change before the final release.

## py-domain-driven-design

A domain driven design library for Python.

## Purpose

The purpose of `py-domain-driven-design` is to provide a comprehensive toolkit for Python developers to implement domain-driven design (DDD) in their applications. This library focuses on enabling the development of rich domain models that accurately reflect complex business requirements, facilitating better communication between developers and domain experts, and promoting a more maintainable and scalable codebase.

## Roadmap

Below is a list of planned features and enhancements for future releases of the `py-domain-driven-design` library.

- [x] **Repository Pattern**: Add support for the repository pattern to provide a standard way to access domain objects from a data source.
- [ ] **Aggregates**: Add support for defining and working with aggregates, including aggregate roots and associated objects.
- [ ] **Value Objects**: Implement support for defining value objects to represent immutable domain concepts.
- [ ] **Entities**: Add support for defining entities with distinct identities and lifecycles.
- [ ] **Domain Events**: Implement infrastructure for defining and handling domain events to capture important domain changes.
- [ ] **Integration Events**: Add support for defining and handling integration events for communication between different bounded contexts.
- [ ] **Domain Services**: Support for encapsulating domain logic in services outside of entities or value objects.
- [ ] **Infrastructure Services**: Support for services that provide technical capabilities like data persistence and messaging, supporting the application's infrastructure needs.
- [ ] **Listeners**: Implement listeners to react to domain and integration events, enabling reactive and decoupled systems.
- [ ] **Documentation**: Expand the documentation to cover new features and provide more comprehensive usage examples and best practices.

We welcome feedback and contributions to help shape the future of this library. If you have ideas or suggestions, please [create an issue](

## Python Compatibility

This library is compatible and tested with the following Python versions:

- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

[![Push on master](https://github.com/runemalm/py-domain-driven-design/actions/workflows/master.yml/badge.svg?branch=master)](https://github.com/runemalm/py-domain-driven-design/actions/workflows/master.yml)

## Installation:

```bash
$ pip install py-domain-driven-design
```

## Example:

Here's an example demonstrating the use of the repository pattern in the library:

```python
from typing import List
from ddd.infrastructure.repository.in_memory.in_memory_repository_base import InMemoryRepositoryBase
from carbusiness.domain.model.vehicle.ivehicle_repository import IVehicleRepository
from carbusiness.domain.model.vehicle.vehicle import Vehicle

class InMemoryVehicleRepository(InMemoryRepositoryBase[Vehicle], IVehicleRepository):
    def find_with_colors(self, colors: List[str]) -> List[Vehicle]:
        with self._lock:
            return [vehicle for vehicle in self._entities.values() if vehicle.color in colors]

# Creating a repository for Vehicle entities
vehicle_repository = InMemoryVehicleRepository()

# Adding some vehicles to the repository
vehicle_repository.save(Vehicle(id="1", color="red"))
vehicle_repository.save(Vehicle(id="2", color="blue"))
vehicle_repository.save(Vehicle(id="3", color="red"))

# Finding vehicles with the color red
red_vehicles = vehicle_repository.find_with_colors(["red"])
for vehicle in red_vehicles:
    print(f"Red Vehicle: ID {vehicle.id}, Color {vehicle.color}")
# Output:
# Red Vehicle: ID 1, Color red
# Red Vehicle: ID 3, Color red
```

For more examples, please refer to the [documentation](https://py-domain-driven-design.readthedocs.io/en/latest/).

## Documentation:

You can find the latest documentation at [readthedocs](https://py-domain-driven-design.readthedocs.io/en/latest/).

## License

`py-domain-driven-design` is released under the GPL 3 license. See [LICENSE](LICENSE) for more details.

## Source Code

You can find the source code for `py-domain-driven-design` on [GitHub](https://github.com/runemalm/py-domain-driven-design).

## Release Notes

### [1.0.0-alpha.2](https://github.com/runemalm/py-domain-driven-design/releases/tag/v1.0.0-alpha.2) (2024-04-02)

- New Feature: Introduced the repository pattern, providing a base for data access.
- Basic Documentation: An initial set of documentation is provided, focusing on the repository pattern.
- License: Released under the GPL 3 license.
- Compatibility: Ensured compatibility with Python versions 3.7 to 3.12.
