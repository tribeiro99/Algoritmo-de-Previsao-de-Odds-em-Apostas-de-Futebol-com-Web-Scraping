import requests
from bs4 import BeautifulSoup

def process_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        tables = soup.find_all('table', class_='stat-seqs stat-half-padding')

        home_table = tables[0]
        away_table = tables[1]

        home_team_title = home_table.find_previous('span', class_='stats-subtitle')
        away_team_title = away_table.find_previous('span', class_='stats-subtitle')

        if home_team_title and away_team_title:
            home_team_name = home_team_title.get_text(strip=True)
            away_team_name = away_team_title.get_text(strip=True)

            home_rows = home_table.find_all('tr')
            away_rows = away_table.find_all('tr')

            print(f"\nHome Team: {home_team_name}")
            print("Home Team Goals:")
            for row in home_rows:
                columns = row.find_all('td')
                if len(columns) == 4:
                    category = columns[0].get_text(strip=True)
                    home_team_goals = columns[1].get_text(strip=True)
                    away_team_goals = columns[2].get_text(strip=True)
                    global_goals = columns[3].get_text(strip=True)
                    print(f"{category}\t{home_team_goals}\t{away_team_goals}\t{global_goals}")

            print(f"\nAway Team: {away_team_name}")
            print("Away Team Goals:")
            for row in away_rows:
                columns = row.find_all('td')
                if len(columns) == 4:
                    category = columns[0].get_text(strip=True)
                    home_team_goals = columns[1].get_text(strip=True)
                    away_team_goals = columns[2].get_text(strip=True)
                    global_goals = columns[3].get_text(strip=True)
                    print(f"{category}\t{home_team_goals}\t{away_team_goals}\t{global_goals}")
        else:
            print("Failed to extract team information.")
    else:
        print(f'Failed to retrieve the page. Status code: {response.status_code}')



if __name__ == "__main__":
    url = input("Please enter the URL of the game: ")
    process_data(url)
