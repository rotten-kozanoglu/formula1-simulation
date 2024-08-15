import random
import statistics
import matplotlib.pyplot as plt
import json
import os
# test
class Track:
    def __init__(self, name, length, laps):
        self.name = name
        self.length = float(length.replace(" km", ""))
        self.laps = laps

class Driver:
    def __init__(self, name, team, morale, car_performance):
        self.name = name
        self.team = team
        self.morale = morale
        self.car_performance = car_performance
        self.best_lap_time = float('inf')
        self.driver_of_the_day_count = 0
        self.laps_led = 0
            
    def get_team_logo(self):
        team_logos = {
            "Mercedes": "Mercedes.png",
            "Red Bull": "Red_Bull.png",
            "Ferrari": "Ferrari.png",
            "McLaren": "McLaren.png",
            "Alpine": "Alpine.png",
            "Aston Martin": "Aston_Martin.png",
            "Williams": "Williams.png",
            "Haas": "Haas.png",
            "Alfa Romeo": "Alfa_Romeo.png",
            "AlphaTauri": "AlphaTauri.png",
        }
        return team_logos.get(self.team, "Williams.png")

class RaceSimulator:
    def __init__(self, tracks, drivers):
        self.tracks = tracks
        self.drivers = drivers

    def simulate_practice(self, track):
        results = []

        for driver in self.drivers:  
            base_lap_time = (track.length / 206) * 3600  

            morale_factor = driver.morale / 10.0
            car_performance_factor = driver.car_performance / 10.0
            adjusted_lap_time = base_lap_time * (1 + (1 - morale_factor * car_performance_factor))

            lap_time = random.gauss(adjusted_lap_time, 1.5)

            results.append({
                "driver": driver,  # Use the Driver instance instead of a dictionary
                "lap_time": lap_time
            })

        results.sort(key=lambda x: x["lap_time"])

        print(f"Practice Session Results ({track.length} km track) ({track.name}):")
        print(f"  {'Driver':<25} {'Lap Time'}")
        print(f"{'-' * 45}")

        for result in results:
            lap_time = round(result['lap_time'], 3)
            minutes, seconds = divmod(lap_time, 60)
            lap_time_str = f"{int(minutes):02d}:{seconds:06.3f}"

            print(f"  {result['driver_name']:<25} {lap_time_str}")

        lap_times = [result['lap_time'] for result in results]
        mean_lap_time = statistics.mean(lap_times)
        std_lap_time = statistics.stdev(lap_times)

        print(f"{'-' * 45}")
        print(f"Mean lap time: {mean_lap_time:.3f} seconds")
        print(f"Standard deviation: {std_lap_time:.3f} seconds")

        driver_names = [result['driver_name'] for result in results]
        driver_names.reverse()
        lap_times.reverse()

        plt.figure(figsize=(10, 6))
        plt.barh(driver_names, lap_times, color='blue')
        plt.xlabel('Lap time (seconds)')
        plt.title(f'Practice Session Results ({track.length} km track) - Track: {track.name}')

        for i, lap_time in enumerate(lap_times):
            plt.text(lap_time, i, f'{lap_time:.3f}', va='center', fontsize=10, color='black')

        plt.grid(axis='x', linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.savefig('practice_results.png')


    def simulate_qualifying(self, track):
        results = []

        for driver in self.drivers:
            base_lap_time = (track.length / 206) * 3600

            morale_factor = driver.morale / 10.0
            car_performance_factor = driver.car_performance / 10.0
            adjusted_lap_time = base_lap_time * (1 + (1 - morale_factor * car_performance_factor))

            lap_time = random.gauss(adjusted_lap_time, 1.0)

            results.append({
                "driver": driver,  # Use the Driver instance instead of a dictionary
                "lap_time": lap_time
            })

        results.sort(key=lambda x: x["lap_time"])

        print(f"Qualifying Session Results ({track.length} km track) ({track.name}):")
        print(f"  {'Driver':<25} {'Lap Time'}")
        print(f"{'-' * 45}")

        for result in results:
            lap_time = round(result['lap_time'], 3)
            minutes, seconds = divmod(lap_time, 60)
            lap_time_str = f"{int(minutes):02d}:{seconds:06.3f}"

            print(f"  {result['driver'].name:<25} {lap_time_str}")

        driver_names = [result['driver'].name for result in results]
        driver_names.reverse()
        lap_times = [result['lap_time'] for result in results]
        lap_times.reverse()

        plt.figure(figsize=(10, 6))
        plt.barh(driver_names, lap_times, color='green')
        plt.xlabel('Lap time (seconds)')
        plt.title(f'Qualifying Session Results ({track.length} km track) - Track: {track.name}')

        for i, lap_time in enumerate(lap_times):
            plt.text(lap_time, i, f'{lap_time:.3f}', va='center', fontsize=10, color='black')

        plt.grid(axis='x', linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.savefig('qualifying_results.png')

        return results

    def simulate_race(self, track, laps):
        race_results = []
        driver_info = {driver.name: {"best_lap_time": float('inf'), "driver_of_the_day_count": 0, "laps_led": 0} for driver in self.drivers}
        starting_grid = sorted(self.simulate_qualifying(track), key=lambda x: x['lap_time'])

        driver_positions = {driver.name: [] for driver in self.drivers}

        for lap in range(1, laps + 1):
            lap_times = []

            for driver_result in starting_grid:
                driver_instance = driver_result["driver"]
                driver_name = driver_instance.name
                tire_deg_factor = random.uniform(0.98, 1.02)
                fuel_load_factor = 1 - (lap / laps) * 0.04
                base_lap_time = (track.length / 206) * 3600 * tire_deg_factor * fuel_load_factor

                morale_factor = driver_instance.morale / 10.0
                car_performance_factor = driver_instance.car_performance / 10.0

                adjusted_lap_time = base_lap_time * (1 + (1 - morale_factor * car_performance_factor))
                lap_time = random.gauss(adjusted_lap_time, 1.0)

                lap_times.append({
                    "driver": driver_instance,
                    "lap_time": lap_time
                })

                if lap_time < driver_info[driver_name]["best_lap_time"]:
                    driver_info[driver_name]["best_lap_time"] = lap_time

                driver_positions[driver_name].append(driver_instance)

                if driver_positions[driver_name][-1] == driver_instance:
                    driver_info[driver_name]["laps_led"] += 1

            lap_times.sort(key=lambda x: x['lap_time'])

            print(f"Lap {lap}/{laps}")
            print(f"{'Driver':<25} {'Lap Time'}")
            print(f"{'-' * 45}")

            for result in lap_times:
                lap_time = round(result['lap_time'], 3)
                minutes, seconds = divmod(lap_time, 60)
                lap_time_str = f"{int(minutes):02d}:{seconds:06.3f}"

                print(f"{result['driver'].name:<25} {lap_time_str}")


            race_results.append(lap_times)

        race_winner = min(driver_info, key=lambda driver: driver_info[driver]["best_lap_time"])
        best_lap_times = [driver_info[driver]["best_lap_time"] for driver in driver_info]
        worst_lap_time = max(driver_info, key=lambda driver: driver_info[driver]["best_lap_time"])
        driver_of_the_day = [driver for driver in driver_info if driver_info[driver]["best_lap_time"] == min(best_lap_times)]

        print(f"{'-' * 45}")
        print(f"Race Winner: {race_winner}")
        print(f"Driver of the Day: {', '.join(driver_of_the_day)}")

        fastest = max(driver_info, key=lambda driver: driver_info[driver]["laps_led"])
        slowest = worst_lap_time

        print(f"Fastest Driver: {fastest}")
        print(f"Slowest Driver: {slowest}")

        return race_results

    def save_race_data(self, race_data, file_path):
        static_folder = os.path.join(os.path.dirname(__file__), 'static')
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        with open(file_path, 'w') as json_file:
            json.dump(race_data, json_file, indent=4)

        self.save_practice_results_plot(os.path.join(static_folder, 'practice_results.png'))
        self.save_qualifying_results_plot(os.path.join(static_folder, 'qualifying_results.png'))

