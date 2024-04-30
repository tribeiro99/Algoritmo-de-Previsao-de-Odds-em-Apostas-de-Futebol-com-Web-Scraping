import requests
from bs4 import BeautifulSoup

def process_data(url):

    response = requests.get(url)
    html_content = response.text

    if response.status_code == 200:
        soup = BeautifulSoup(html_content, 'html.parser')

        section_title = "Fora"

        section = soup.find('span', class_='stats-subtitle', string=section_title)
        if section:
            ranking_table = section.find_next('table', class_='results competition-rounds competition-half-padding')
            if ranking_table:
                rows = ranking_table.select('tbody > tr')

                for row in rows:
                    cols = row.find_all('td')
                    position = cols[0].get_text(strip=True)
                    team = cols[1].find('a').get_text(strip=True)
                    points = cols[2].get_text(strip=True)
                    matches_played = cols[3].get_text(strip=True)
                    wins = cols[4].get_text(strip=True)
                    draws = cols[5].get_text(strip=True)
                    losses = cols[6].get_text(strip=True)
                    goals = cols[7].get_text(strip=True)


                    print(f"Position: {position}, Team: {team}, Points: {points}, Matches Played: {matches_played}, Wins: {wins}, Draws: {draws}, Losses: {losses}, Goals: {goals}")

            else:
                print(f"{section_title} ranking table not found on the page.")
        else:
            print(f"{section_title} section subtitle not found on the page.")
    else:
        print("Failed to retrieve the web page.")

if __name__ == "__main__":
    url = input("Please enter the URL of the webpage: ")
    process_data(url)
