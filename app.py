import gspread
import streamlit as st

# 1. KONFIGURACJA POŁĄCZENIA Z GOOGLE SHEETS
@st.cache_resource
def get_google_sheet():
  # Streamlit odczytuje [gcp_service_account] z TOML jako zwykły słownik
  creds_dict = dict(st.secrets["gcp_service_account"])
  gc = gspread.service_account_from_dict(creds_dict)
  # Otwieranie po Twoim ID arkusza
  return gc.open_by_key("1q1g_51CjQQICHQ5kTOyIEVKelJudqSXSXxmwsbCd0fs").sheet1


sheet = get_google_sheet()


# 2. FUNKCJE DO ODCZYTU I ZAPISU W ARKUSZU GOOGLE
def load_progress():
  records = sheet.get_all_records()
  progress = {}
  for row in records:
    progress[row["item_key"]] = str(row["watched"]).upper() == "TRUE"
  return progress


def save_item_status(item_key, is_watched):
  cell = sheet.find(item_key, in_column=1)
  val = "TRUE" if is_watched else "FALSE"
  if cell:
    sheet.update_cell(cell.row, 2, val)
  else:
    sheet.append_row([item_key, val])


# 3. PEŁNA BAZA PRODUKCJI MCU (FAZY 1-6 CHRONOLOGICZNIE)
mcu_data = [
    # FAZA 1
    {"title": "Iron Man (2008)", "type": "movie"},
    {"title": "The Incredible Hulk (2008)", "type": "movie"},
    {"title": "Iron Man 2 (2010)", "type": "movie"},
    {"title": "Thor (2011)", "type": "movie"},
    {"title": "Captain America: The First Avenger (2011)", "type": "movie"},
    {"title": "The Avengers (2012)", "type": "movie"},
    # FAZA 2
    {"title": "Iron Man 3 (2013)", "type": "movie"},
    {"title": "Thor: The Dark World (2013)", "type": "movie"},
    {"title": "Captain America: The Winter Soldier (2014)", "type": "movie"},
    {"title": "Guardians of the Galaxy (2014)", "type": "movie"},
    {"title": "Avengers: Age of Ultron (2015)", "type": "movie"},
    {"title": "Ant-Man (2015)", "type": "movie"},
    # FAZA 3
    {"title": "Captain America: Civil War (2016)", "type": "movie"},
    {"title": "Doctor Strange (2016)", "type": "movie"},
    {"title": "Guardians of the Galaxy Vol. 2 (2017)", "type": "movie"},
    {"title": "Spider-Man: Homecoming (2017)", "type": "movie"},
    {"title": "Thor: Ragnarok (2017)", "type": "movie"},
    {"title": "Black Panther (2018)", "type": "movie"},
    {"title": "Avengers: Infinity War (2018)", "type": "movie"},
    {"title": "Ant-Man and the Wasp (2018)", "type": "movie"},
    {"title": "Captain Marvel (2019)", "type": "movie"},
    {"title": "Avengers: Endgame (2019)", "type": "movie"},
    {"title": "Spider-Man: Far From Home (2019)", "type": "movie"},
    # FAZA 4
    {
        "title": "WandaVision",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 10)],
    },
    {
        "title": "The Falcon and the Winter Soldier",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {
        "title": "Loki - Sezon 1",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {"title": "Black Widow (2021)", "type": "movie"},
    {
        "title": "What If...? - Sezon 1",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 10)],
    },
    {"title": "Shang-Chi and the Legend of the Ten Rings (2021)", "type": "movie"},
    {"title": "Eternals (2021)", "type": "movie"},
    {
        "title": "Hawkeye",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {"title": "Spider-Man: No Way Home (2021)", "type": "movie"},
    {
        "title": "Moon Knight",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {"title": "Doctor Strange in the Multiverse of Madness (2022)", "type": "movie"},
    {
        "title": "Ms. Marvel",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {"title": "Thor: Love and Thunder (2022)", "type": "movie"},
    {
        "title": "I Am Groot - Sezon 1",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 6)],
    },
    {
        "title": "She-Hulk: Attorney at Law",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 10)],
    },
    {"title": "Werewolf by Night (2022)", "type": "movie"},
    {"title": "Black Panther: Wakanda Forever (2022)", "type": "movie"},
    {"title": "The Guardians of the Galaxy Holiday Special (2022)", "type": "movie"},
    # FAZA 5
    {"title": "Ant-Man and the Wasp: Quantumania (2023)", "type": "movie"},
    {"title": "Guardians of the Galaxy Vol. 3 (2023)", "type": "movie"},
    {
        "title": "Secret Invasion",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {
        "title": "I Am Groot - Sezon 2",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 6)],
    },
    {
        "title": "Loki - Sezon 2",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {"title": "The Marvels (2023)", "type": "movie"},
    {
        "title": "What If...? - Sezon 2",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 10)],
    },
    {
        "title": "Echo",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 6)],
    },
    {
        "title": "X-Men '97 - Sezon 1",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 11)],
    },
    {"title": "Deadpool & Wolverine (2024)", "type": "movie"},
    {
        "title": "Agatha All Along",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 10)],
    },
    {
        "title": "What If...? - Sezon 3",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 9)],
    },
    {
        "title": "Your Friendly Neighborhood Spider-Man",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 11)],
    },
    {"title": "Captain America: Brave New World (2025)", "type": "movie"},
    {
        "title": "Daredevil: Born Again",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 10)],
    },
    {"title": "Thunderbolts* (2025)", "type": "movie"},
    {
        "title": "Ironheart",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {"title": "The Fantastic Four: First Steps (2025)", "type": "movie"},
    {
        "title": "Eyes of Wakanda",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 5)],
    },
    {
        "title": "Marvel Zombies",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 5)],
    },
    {
        "title": "Wonder Man",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 11)],
    },
    # FAZA 6
    {"title": "Avengers: Doomsday (2026)", "type": "movie"},
]

# 4. INTERFEJS UŻYTKOWNIKA (STREAMLIT)
st.set_page_config(page_title="MCU Tracker", page_icon="🎬", layout="centered")
st.title("🎬 MCU Marathon Tracker — Road to Doomsday")

if "user_progress" not in st.session_state:
  st.session_state.user_progress = load_progress()

user_progress = st.session_state.user_progress

# Liczenie postępu
total_items = 0
watched_items = 0

for item in mcu_data:
  if item["type"] == "movie":
    total_items += 1
    if user_progress.get(item["title"], False):
      watched_items += 1
  elif item["type"] == "series":
    for ep in item["episodes"]:
      total_items += 1
      key = f"{item['title']} - {ep}"
      if user_progress.get(key, False):
        watched_items += 1

percentage = (watched_items / total_items * 100) if total_items > 0 else 0

st.metric(
    label="Twój postęp do Avengers: Doomsday",
    value=f"{percentage:.1f}%",
    delta=f"{watched_items} / {total_items} obejrzanych elementów",
)
st.progress(percentage / 100)
st.divider()

# Wyświetlanie listy z checkboxami
for item in mcu_data:
  if item["type"] == "movie":
    current_val = user_progress.get(item["title"], False)
    checked = st.checkbox(f"🎥 {item['title']}", value=current_val)
    if checked != current_val:
      user_progress[item["title"]] = checked
      save_item_status(item["title"], checked)
      st.rerun()

  elif item["type"] == "series":
    with st.expander(f"📺 {item['title']}"):
      for ep in item["episodes"]:
        key = f"{item['title']} - {ep}"
        current_val = user_progress.get(key, False)
        checked_ep = st.checkbox(ep, value=current_val, key=key)
        if checked_ep != current_val:
          user_progress[key] = checked_ep
          save_item_status(key, checked_ep)
          st.rerun()
