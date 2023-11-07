import random
import statistics
import matplotlib.pyplot as plt
import json 
import os

tracks_2022 = [
    {"name": "Albert Park Circuit", "length": "5.303 km", "laps": 58},
    {"name": "Baku City Circuit", "length": "6.003 km", "laps": 51},
    {"name": "Buddh International Circuit", "length": "5.125 km", "laps": 60},
    {"name": "Circuit de Barcelona-Catalunya", "length": "4.675 km", "laps": 66},
    {"name": "Circuit de Monaco", "length": "3.337 km", "laps": 78},
    {"name": "Circuit Gilles Villeneuve", "length": "4.361 km", "laps": 70},
    {"name": "Circuit Paul Ricard", "length": "5.842 km", "laps": 53},
    {"name": "Hockenheimring", "length": "4.574 km", "laps": 67},
    {"name": "Hungaroring", "length": "4.381 km", "laps": 70},
    {"name": "Istanbul Park Circuit", "length": "5.338 km", "laps": 58},
    {"name": "Marina Bay Street Circuit", "length": "5.063 km", "laps": 61},
    {"name": "Red Bull Ring", "length": "4.318 km", "laps": 71},
    {"name": "Silverstone Circuit", "length": "5.891 km", "laps": 52},
    {"name": "Sochi Autodrom", "length": "5.848 km", "laps": 53},
    {"name": "Suzuka Circuit", "length": "5.807 km", "laps": 53},
    {"name": "Yas Marina Circuit", "length": "5.554 km", "laps": 58}
]


driver_roster = [
    {"name": "Lewis Hamilton", "team": "Mercedes", "morale": 8.3, "car_performance": 9.4}, # Mercedes-AMG F1 W14 E PERFORMANCE has a high performance rating[^1^][2]
    {"name": "George Russell", "team": "Mercedes", "morale": 8.4, "car_performance": 9.1}, # slightly lower than Hamilton due to less experience
    {"name": "Max Verstappen", "team": "Red Bull Racing", "morale": 9.8, "car_performance": 9.8}, # Red Bull Racing has the best car performance in 2023 according to some sources[^2^][3] [^3^][4]
    {"name": "Sergio Perez", "team": "Red Bull Racing", "morale": 8.2, "car_performance": 9.5}, # slightly lower than Verstappen due to less consistency
    {"name": "Charles Leclerc", "team": "Ferrari", "morale": 8.7, "car_performance": 8.6}, # Ferrari has improved its car performance from 2022 but still lags behind Mercedes and Red Bull[^3^][4]
    {"name": "Carlos Sainz", "team": "Ferrari", "morale": 8.4, "car_performance": 8.4}, # slightly lower than Leclerc due to less familiarity with the car
    {"name": "Lando Norris", "team": "McLaren", "morale": 8.9, "car_performance": 8.7}, # McLaren has a competitive car performance but not as strong as the top two teams[^3^][4]
    {"name": "Oscar Piastri", "team": "McLaren", "morale": 7.8, "car_performance": 8.1}, # slightly lower than Norris due to less experience
    {"name": "Pierre Gasly", "team": "Alpine", "morale": 8.1, "car_performance": 8.0}, # Alpine has a decent car performance but not as good as McLaren[^3^][4]
    {"name": "Esteban Ocon", "team": "Alpine", "morale": 8.3, "car_performance": 7.9}, # slightly lower than Gasly due to less consistency
    {"name": "Fernando Alonso", "team": "Aston Martin", "morale": 8.6, "car_performance": 7.8}, # Aston Martin has a mediocre car performance and struggles to keep up with the midfield[^3^][4]
    {"name": "Lance Stroll", "team": "Aston Martin", "morale": 7.9, "car_performance": 7.6}, # slightly lower than Alonso due to less skill
    {"name": "Alex Albon", "team": "Williams", "morale": 8.0, "car_performance": 7.5}, # Williams has a poor car performance and is often at the back of the grid[^3^][4]
    {"name": "Logan Sargeant", "team": "Williams", "morale": 7.5, "car_performance": 7.3}, # slightly lower than Albon due to less experience
    {"name": "Kevin Magnussen", "team": "Haas", "morale": 7.2, "car_performance": 7.1}, # Haas has the worst car performance in 2023 and is rarely competitive[^3^][4]
    {"name": "Nico Hülkenberg", "team": "Haas", "morale": 7.0, "car_performance": 6.9}, # slightly lower than Magnussen due to less familiarity with the car
    {"name": "Valtteri Bottas", "team": "Alfa Romeo", "morale": 8.5, "car_performance": 7.7}, # Alfa Romeo has a slightly better car performance than Williams and Haas but still lags behind the rest[^3^][4]
    {"name": "Guanyu Zhou", "team": "Alfa Romeo", "morale": 7.7, "car_performance": 7.4}, # slightly lower than Bottas due to less experience
    {"name": "Yuki Tsunoda", "team": "AlphaTauri", "morale": 8.2, "car_performance": 8.2}, # AlphaTauri has a good car performance and can challenge the top teams on some occasions[^3^][4]
    {"name": "Daniel Ricciardo", "team": "AlphaTauri", "morale": 8.8, "car_performance": 8.5}, # slightly higher than Tsunoda due to more experience and skill
]





def track():
    track = tracks_2022.pop(random.randrange(len(tracks_2022)))
    return track

def race_day():
    return "Sunday"

def practice_day():
    return "Friday"

def qualifying_day():
    return "Saturday"


def simulate_practice(track_length, average_speed):
    results = []

    for driver in driver_roster:
        base_lap_time = (track_length / average_speed) * 3600  

        morale_factor = driver["morale"] / 10.0  
        car_performance_factor = driver["car_performance"] / 10.0
        adjusted_lap_time = base_lap_time * (1 + (1 - morale_factor * car_performance_factor))

        lap_time = random.gauss(adjusted_lap_time, 1.5) 

        results.append({
            "driver_name": driver["name"],
            "lap_time": lap_time
        })

    results.sort(key=lambda x: x["lap_time"])


    print(f"Practice Session Results ({track_length} km track) ({selected_track['name']}):")
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
    plt.title(f'Practice Session Results ({track_length} km track) - Track: {selected_track["name"]}')

    for i, lap_time in enumerate(lap_times):
     plt.text(lap_time, i, f'{lap_time:.3f}', va='center', fontsize=10, color='black')

    plt.grid(axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('practice_results.png')


selected_track = track()
track_length = float(selected_track["length"].replace(" km", ""))
average_speed = 206
simulate_practice(track_length, average_speed)

def simulate_quali(track_length, average_speed):
    results = []

    for driver in driver_roster:
        base_lap_time = (track_length / average_speed) * 3600  

        morale_factor = driver["morale"] / 10.0  
        car_performance_factor = driver["car_performance"] / 10.0
        adjusted_lap_time = base_lap_time * (1 + (1 - morale_factor * car_performance_factor))

        lap_time = random.gauss(adjusted_lap_time, 1.0)  

        results.append({
            "driver_name": driver["name"],
            "lap_time": lap_time
        })

    results.sort(key=lambda x: x["lap_time"])

    print(f"Qualifying Session Results ({track_length} km track) ({selected_track['name']}):")
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
    plt.title(f'Qualifying Session Results ({track_length} km track) - Track: {selected_track["name"]}')

    for i, lap_time in enumerate(lap_times):
        plt.text(lap_time, i, f'{lap_time:.3f}', va='center', fontsize=10, color='black')

    plt.grid(axis='x', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('qualifying_results.png')

    return results  

qualifying_results = simulate_quali(track_length, average_speed)

def simulate_race(track_length, laps, selected_track):
    race_results = []
    driver_info = {driver["name"]: {"best_lap_time": float('inf'), "driver_of_the_day_count": 0, "laps_led": 0} for driver in driver_roster}
    starting_grid = sorted(qualifying_results, key=lambda x: x['lap_time'])

    driver_positions = {driver["name"]: [] for driver in driver_roster}

    for lap in range(1, laps + 1):
        lap_times = []

        for driver_result in starting_grid:
            driver_name = driver_result["driver_name"]
            base_lap_time = (track_length / average_speed) * 3600

            driver_attributes = next((d for d in driver_roster if d["name"] == driver_name), None)
            if driver_attributes:
                morale_factor = driver_attributes["morale"] / 10.0
                car_performance_factor = driver_attributes["car_performance"] / 10.0

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

race_laps = selected_track["laps"]
race_results = simulate_race(track_length, race_laps, selected_track)

race_data = {
    "track": selected_track["name"],
    "track_length": track_length,
    "average_speed": average_speed,
    "qualifying_results": qualifying_results,
    "race_results": race_results
}

data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
json_file_path = os.path.join(data_folder, 'race_results.json')
with open(json_file_path, 'w') as json_file:
    json.dump(race_data, json_file, indent=4)

print("Yarış sonuçları JSON dosyası 'data' klasörü içine kaydedildi:", json_file_path)


