import random
import statistics
import matplotlib.pyplot as plt
import json
import os

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
                "driver_name": driver.name,
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
                "driver_name": driver.name,
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

            print(f"  {result['driver_name']:<25} {lap_time_str}")

        driver_names = [result['driver_name'] for result in results]
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
                driver_name = driver_result["driver_name"]
                base_lap_time = (track.length / 206) * 3600

                driver_attributes = next((d for d in self.drivers if d.name == driver_name), None)
                if driver_attributes:
                    morale_factor = driver_attributes.morale / 10.0
                    car_performance_factor = driver_attributes.car_performance / 10.0

                    adjusted_lap_time = base_lap_time * (1 + (1 - morale_factor * car_performance_factor))
                    lap_time = random.gauss(adjusted_lap_time, 1.0)

                    lap_times.append({
                        "driver_name": driver_name,
                        "lap_time": lap_time
                    })

                    if lap_time < driver_info[driver_name]["best_lap_time"]:
                        driver_info[driver_name]["best_lap_time"] = lap_time

                    driver_positions[driver_name].append(driver_result["driver_name"])

                    if driver_positions[driver_name][-1] == driver_name:
                        driver_info[driver_name]["laps_led"] += 1

            lap_times.sort(key=lambda x: x['lap_time'])

            print(f"Lap {lap}/{laps}")
            print(f"{'Driver':<25} {'Lap Time'}")
            print(f"{'-' * 45}")

            for result in lap_times:
                lap_time = round(result['lap_time'], 3)
                minutes, seconds = divmod(lap_time, 60)
                lap_time_str = f"{int(minutes):02d}:{seconds:06.3f}"

                print(f"{result['driver_name']:<25} {lap_time_str}")

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
        with open(file_path, 'w') as json_file:
            json.dump(race_data, json_file, indent=4)



if __name__ == "__main__":
    tracks = [
        Track("Albert Park Circuit", "5.303 km", 58),
        Track("Baku City Circuit", "6.003 km", 51),
        Track("Buddh International Circuit", "5.125 km", 60),
        Track("Circuit de Barcelona-Catalunya", "4.675 km", 66),
        Track("Circuit de Monaco", "3.337 km", 78),
        Track("Circuit Gilles Villeneuve", "4.361 km", 70),
        Track("Circuit Paul Ricard", "5.842 km", 53),
        Track("Hockenheimring", "4.574 km", 67),
        Track("Hungaroring", "4.381 km", 70),
        Track("Istanbul Park Circuit", "5.338 km", 58),
        Track("Marina Bay Street Circuit", "5.063 km", 61),
        Track("Red Bull Ring", "4.318 km", 71),
        Track("Silverstone Circuit", "5.891 km", 52),
        Track("Sochi Autodrom", "5.848 km", 53),
        Track("Suzuka Circuit", "5.807 km", 53),
        Track("Yas Marina Circuit", "5.554 km", 58),
    ]

    drivers = [
        Driver("Lewis Hamilton", "Mercedes", 8.3, 9.4),
        Driver("George Russell", "Mercedes", 8.4, 9.1),
        Driver("Max Verstappen", "Red Bull Racing", 9.8, 9.8),
        Driver("Sergio Perez", "Red Bull Racing", 8.2, 9.5),
        Driver("Charles Leclerc", "Ferrari", 8.7, 8.6),
        Driver("Carlos Sainz", "Ferrari", 8.4, 8.4),
        Driver("Lando Norris", "McLaren", 8.9, 8.7),
        Driver("Oscar Piastri", "McLaren", 7.8, 8.1),
        Driver("Pierre Gasly", "Alpine", 8.1, 8.0),
        Driver("Esteban Ocon", "Alpine", 8.3, 7.9),
        Driver("Fernando Alonso", "Aston Martin", 8.6, 7.8),
        Driver("Lance Stroll", "Aston Martin", 7.9, 7.6),
        Driver("Alex Albon", "Williams", 8.0, 7.5),
        Driver("Logan Sargeant", "Williams", 7.5, 7.3),
        Driver("Kevin Magnussen", "Haas", 7.2, 7.1),
        Driver("Nico Hülkenberg", "Haas", 7.0, 6.9),
        Driver("Valtteri Bottas", "Alfa Romeo", 8.5, 7.7),
        Driver("Guanyu Zhou", "Alfa Romeo", 7.7, 7.4),
        Driver("Yuki Tsunoda", "AlphaTauri", 8.2, 8.2),
        Driver("Daniel Ricciardo", "AlphaTauri", 8.8, 8.5),        
    ]

    race_simulator = RaceSimulator(tracks, drivers)

    selected_track = random.choice(tracks)
    race_simulator.simulate_practice(selected_track)
    qualifying_results = race_simulator.simulate_qualifying(selected_track)
    race_results = race_simulator.simulate_race(selected_track, selected_track.laps)

    race_data = {
        "track": selected_track.name,
        "track_length": selected_track.length,
        "average_speed": 206,
        "qualifying_results": qualifying_results,
        "race_results": race_results
    }

    data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    json_file_path = os.path.join(data_folder, 'race_results.json')
    race_simulator.save_race_data(race_data, json_file_path)

    print("Yarış sonuçları JSON dosyası 'data' klasörü içine kaydedildi:", json_file_path)
