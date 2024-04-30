import requests
from bs4 import BeautifulSoup


def calculate_probability(goals_suffered, total_goals_suffered):
    if goals_suffered > 0 and total_goals_suffered > 0:
        return goals_suffered / total_goals_suffered
    else:
        return None


def process_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        away_team_tables = soup.find_all('table', class_='stat-goals')

        if len(away_team_tables) >= 2:
            away_team_table = away_team_tables[1]
            extract_and_print_away_team_goal_data(away_team_table)
        else:
            print("Away team data not found on the page.")

    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')


def extract_and_print_away_team_goal_data(away_team_table):
    rows = away_team_table.find('tbody').find_all('tr')

    print("\nAway Team Goals Suffered Data:")

    goals_suffered_in_periods = []

    for i in range(0, len(rows), 2):
        if i + 1 < len(rows):
            period = rows[i].find('td').get_text(strip=True)
            goals_suffered_element = rows[i + 1].find_all('td')

            if len(goals_suffered_element) >= 2:
                goals_suffered_str = goals_suffered_element[1].get_text(strip=True)

                if goals_suffered_str.isdigit():
                    goals_suffered = int(goals_suffered_str)
                    goals_suffered_in_periods.append(goals_suffered)
                    print(f"Period: {period}, Goals Suffered by Away Team: {goals_suffered}")
                else:
                    print(f"Period: {period}, Goals Suffered by Away Team: Data not available")
            else:
                print(f"Period: {period}, Goals Suffered by Away Team: Data not available")
        else:
            print("No data available for this period")


    total_goals_suffered = sum(goals_suffered_in_periods)
    for i in range(len(goals_suffered_in_periods)):
        period = rows[i * 2].find('td').get_text(strip=True)
        goals_suffered = goals_suffered_in_periods[i]

        probability = calculate_probability(goals_suffered, total_goals_suffered)
        odd = 1 / probability if probability is not None and 0 < probability < 1 else None

        print(f"Odd for Away Team to concede in {period}: {odd:.4f}" if odd is not None else "Unable to calculate odd.")


if __name__ == "__main__":
    url = input("Please enter the URL of the game: ")
    process_data(url)
