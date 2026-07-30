# 🎵 Music Mood Selector

Music Mood Selector is a Streamlit web app that creates a brand-new Spotify playlist filtered by mood. Give it a link to one of your existing playlists, pick a vibe — happy, sad, chill, or gym — and it will scan every track's [Last.fm](https://www.last.fm/) tags, pull out the songs that match, and build a new playlist on your Spotify account.

## How it works

1. You paste in a Spotify playlist URL or ID.
2. The app pulls every track from that playlist via the [Spotipy](https://spotipy.readthedocs.io/) library.
3. For each track, it queries the Last.fm API for the artist/track's top tags.
4. Tags are compared against a mood map (e.g. "chill" matches tags like `chill`, `mellow`, `relaxed`, `calm`, `ambient`, `lo-fi`).
5. Matching tracks are collected and used to create a new playlist on your Spotify account, named after the original playlist plus the chosen mood.

## Features

- Simple, pixel-themed Streamlit interface with a mood-reactive mascot image
- Four built-in moods: Happy, Sad, Chill, Gym
- Reset button to clear your mood selection
- Works with both local `.env` secrets and Streamlit Cloud's `st.secrets`

## Tech stack

- [Streamlit](https://streamlit.io/) – web UI
- [Spotipy](https://spotipy.readthedocs.io/) – Spotify Web API client
- [Last.fm API](https://www.last.fm/api) – track tag/mood data
- [python-dotenv](https://pypi.org/project/python-dotenv/) – local environment variable loading

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/music-mood-selector.git
cd music-mood-selector
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your API credentials

You'll need:

- **Spotify**: Create an app at the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) to get a `CLIENT_ID`, `CLIENT_SECRET`, and to set a `REDIRECT_URI`. You'll also need to generate a `REFRESH_TOKEN` with the appropriate `SCOPE` (e.g. `playlist-read-private playlist-modify-private playlist-modify-public`) using the OAuth flow.
- **Last.fm**: Register for a free API key at the [Last.fm API account page](https://www.last.fm/api/account/create) to get your `API_KEY`.

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
REDIRECT_URI=your_spotify_redirect_uri
SCOPE=playlist-read-private playlist-modify-private playlist-modify-public
REFRESH_TOKEN=your_spotify_refresh_token
API_KEY=your_lastfm_api_key
```

> If deploying to Streamlit Community Cloud, add the same keys to your app's `secrets.toml` instead — the app automatically checks `st.secrets` first and falls back to `.env`.

### 5. Run the app

```bash
streamlit run app.py
```

## Project structure

```
.
├── .devcontainer/        # Dev container configuration for consistent dev environments
├── .github/              # GitHub configuration (e.g. workflows/CI)
├── .streamlit/           # Streamlit configuration (e.g. theme, secrets.toml for deployment)
├── assets/               # Mood mascot images
├── tests/                # Test suite
├── app.py                # Streamlit UI and interaction logic
├── MusicMoodLogic.py     # Spotify/Last.fm integration and mood-matching logic
├── requirements.txt      # Python dependencies
├── .env                  # Local environment variables (not committed)
└── .gitignore            # Files/folders excluded from version control
```

## Notes & limitations

- Mood matching depends on Last.fm tag coverage, so lesser-known tracks/artists may not be tagged and won't match any mood.
- The app currently supports four fixed moods (`happy`, `sad`, `chill`, `gym`); add to `mood_map` in `MusicMoodLogic.py` to support more.
- Spotify's API requires a valid OAuth refresh token; tokens with expired or revoked scopes will cause playlist fetch/create requests to fail.

## License

This project is for personal/educational use. Add a license of your choice (e.g. MIT) if you plan to open-source it.
