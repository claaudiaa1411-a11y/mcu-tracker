import gspread
from google.oauth2.service_account import Credentials
import streamlit as st

# Polączenie z API Google
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


@st.cache_resource
def get_google_sheet():
  creds_dict = st.secrets["gcp_service_account"]
  credentials = Credentials.from_service_account_info(
      creds_dict, scopes=SCOPE
  )
  client = gspread.authorize(credentials)
  return client.open("MCU Tracker Data").sheet1


sheet = get_google_sheet()


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


# Lista produkcji MCU
mcu_data = [
    {"title": "Iron Man (2008)", "type": "movie"},
    {"title": "The Avengers (2012)", "type": "movie"},
    {
        "title": "WandaVision (2021)",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 10)],
    },
    {
        "title": "Loki - Sezon 1 (2021)",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {"title": "Spider-Man: No Way Home (2021)", "type": "movie"},
    {"title": "Doctor Strange in the Multiverse of Madness (2022)", "type": "movie"},
    {
        "title": "Loki - Sezon 2 (2023)",
        "type": "series",
        "episodes": [f"Odcinek {i}" for i in range(1, 7)],
    },
    {"title": "Deadpool & Wolverine (2024)", "type": "movie"},
    {"title": "Fantastic Four: First Steps (2025)", "type": "movie"},
    {"title": "Avengers: Doomsday (2026)", "type": "movie"},
]

st.set_page_config(page_title="MCU Tracker", page_icon="🎬")
st.title("🎬 MCU Marathon Tracker — Road to Doomsday")

if "user_progress" not in st.session_state:
  st.session_state.user_progress = load_progress()

user_progress = st.session_state.user_progress

# Obliczanie postępu
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
    label="Twój postęp przed Avengers: Doomsday",
    value=f"{percentage:.1f}%",
    delta=f"{watched_items} / {total_items} obejrzanych elementów",
)
st.progress(percentage / 100)
st.divider()

# Lista interaktywna
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
