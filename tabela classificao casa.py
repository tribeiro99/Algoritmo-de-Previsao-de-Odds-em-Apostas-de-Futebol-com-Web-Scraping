import requests
from bs4 import BeautifulSoup

def process_data(url):
    response = requests.get(url)
    html_content = response.text
    if response.status_code == 200:
        soup = BeautifulSoup(html_content, 'html.parser')

        casa_section = soup.find('span', class_='stats-subtitle', string='Casa')

        if casa_section:
            table = casa_section.find_next('table', class_='results')

            if table:
                rows = table.find_all('tr')

                headers = [header.get_text(strip=True) for header in table.select('thead th')]
                print('\t'.join(headers))

                for row in rows:
                    cols = row.find_all('td')
                    if cols:
                        position = cols[0].get_text(strip=True)
                        team = cols[1].get_text(strip=True)
                        points = cols[2].get_text(strip=True)
                        matches_played = cols[3].get_text(strip=True)
                        wins = cols[4].get_text(strip=True)
                        draws = cols[5].get_text(strip=True)
                        losses = cols[6].get_text(strip=True)
                        goals = cols[7].get_text(strip=True)

                        print(
                            f"Position: {position}, Team: {team}, Points: {points}, Matches Played: {matches_played}, Wins: {wins}, Draws: {draws}, Losses: {losses}, Goals: {goals}")

            else:
                print("Sub-table not found in the 'Casa' section")
        else:
            print("Casa section not found")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

if __name__ == "__main__":
    url = input("Please enter the URL of the webpage: ")
    process_data(url)
