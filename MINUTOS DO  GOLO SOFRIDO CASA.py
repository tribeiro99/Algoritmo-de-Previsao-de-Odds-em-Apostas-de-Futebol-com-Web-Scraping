import requests
from bs4 import BeautifulSoup


def calculate_probability(goals_suffered, total_goals_suffered):
    if goals_suffered > 0 and total_goals_suffered > 0:
        return goals_suffered / total_goals_suffered
    else:
        return None


def calculate_odd(probability):
    return 1 / probability if probability is not None and 0 < probability < 1 else None


def process_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        home_goal_data = extract_home_goal_data(soup, "Home Team")

        print_goal_data(home_goal_data, "Home Team")

    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')


def extract_home_goal_data(soup, team_name):
    goal_data = []
    tables = soup.find_all('table', class_='stat-goals')
    home_team_table = tables[0]
    rows = home_team_table.find('tbody').find_all('tr')

    minute_ranges = ["0-15", "16-30", "31-45", "46-60", "61-75", "76-90"]
    goals_suffered_in_ranges = []

    for i in range(1, len(rows), 2):
        columns = rows[i].find_all('td')
        goals_suffered = columns[1].get_text(strip=True)

        # Skip invalid values
        if goals_suffered.isdigit():
            goal_data.append((goals_suffered, team_name))
            goals_suffered_in_ranges.append(int(goals_suffered))

    total_goals_suffered = sum(goals_suffered_in_ranges)
    for i in range(len(minute_ranges)):
        if i < len(goals_suffered_in_ranges):
            minute_range = minute_ranges[i]
            goals_suffered = goals_suffered_in_ranges[i]

            probability = calculate_probability(goals_suffered, total_goals_suffered)
            odd = calculate_odd(probability)

            print(f"Odd for {team_name} to concede in {minute_range}: {odd:.4f}" if odd is not None else "Unable to calculate odd.")

    return goal_data


def print_goal_data(goal_data, team_name):
    minute_ranges = ["0-15", "16-30", "31-45", "46-60", "61-75", "76-90"]
    print(f"\n{team_name} Goal Data:")
    for i in range(len(goal_data)):
        minute_range = minute_ranges[i]
        goals_suffered, team = goal_data[i]
        print(f"Minute Range {minute_range}: {team}\tGoals Suffered by {team_name}: {goals_suffered}")


if __name__ == "__main__":
    url = input("Please enter the URL of the game: ")
    process_data(url)
