import unittest
import os
os.environ['SAPHIRA_URL'] = 'http://localhost:8081'
import requests
import saphira

class BatteryCapacityTest(unittest.TestCase):
    def test_electric_range(self):
        energy_density = 250  # Wh/kg
        minimum_range = int(saphira.get_param('83092519-da63-4882-a899-297e3e62b65d.json', 'BattRef-0001'))  # kilometers
        print(minimum_range)
        efficiency_factor = 0.9  # Efficiency factor to account for losses
        
        # Assuming battery weight in kilograms
        battery_weight = minimum_range / (energy_density * efficiency_factor)
        
        # Calculate the minimum required battery capacity in kWh
        min_battery_capacity_kWh = minimum_range * energy_density / 1000
        
        # Assert the minimum battery capacity supports the required range
        self.assertGreaterEqual(battery_weight, 0, "Battery weight cannot be negative")
        self.assertTrue(min_battery_capacity_kWh > 0, "Minimum battery capacity must be positive")
        self.assertTrue(battery_weight < 500, "Battery weight should be reasonable (< 500 kg)")
        self.assertTrue(min_battery_capacity_kWh >= 225, "Minimum battery capacity should support at least 675 km range, is " + str(min_battery_capacity_kWh))
        self.assertTrue(min_battery_capacity_kWh <= 250, "Minimum battery capacity should not exceed required energy density")

if __name__ == '__main__':
    try:
        unittest.main()
        requests.post('http://localhost:8081/update_status', {'key': 'BattRef-0001', 'status': 'Validated'})
    except:
        resp = requests.post('http://localhost:8081/update_status', json={'key': 'BattRef-0001', 'status': 'Unvalidated'})
        print(resp.text)