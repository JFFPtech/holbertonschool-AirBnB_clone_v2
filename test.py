#!/usr/bin/python3
"""
Test storage functionality
"""
from models import storage
from models.state import State
from models.city import City

def test_storage():
    """
    Test storage functionality
    """
    # Create states
    state_1 = State(name="California")
    state_2 = State(name="Arizona")

    # Save states
    state_1.save()
    state_2.save()

    # Create cities associated with each state
    city_1_1 = City(state_id=state_1.id, name="Napa")
    city_1_2 = City(state_id=state_1.id, name="Sonoma")
    city_2_1 = City(state_id=state_2.id, name="Page")

    # Save cities
    city_1_1.save()
    city_1_2.save()
    city_2_1.save()

    # Close storage
    storage.close()

    # Reload storage
    storage.reload()

    # Retrieve all states
    all_states = storage.all(State)
    for state_id, state in all_states.items():
        print("State:", state.name)
        print("Cities:")
        for city in state.cities:
            print("\t", city.name)

if __name__ == "__main__":
    test_storage()
