# ISEO Discord RPC

A lightweight local server that connects ISEO to Discord Rich Presence.

**For the best experience, tag your music files with [MusicBrainz Picard](https://picard.musicbrainz.org/) — this embeds the album ID (MBID) used for cover art lookup.**

---

## What it does

Runs a small Python server on your machine that listens for track updates from ISEO and displays them as Discord Rich Presence. It will display items such as song title, artist, album, progress bar, and cover art.

**Includes:**

- Listening to activity with song title, artist, and album
- Progress bar via Discord timestamps
- Album cover art via Cover Art Archive (falls back to ISEO logo)
- 5 second debounce to avoid spamming Discord on track skips

## Requirements

- Python 3
- Discord desktop app (must be running)
- ISEO with Discord RPC enabled in settings

---

## Setup

1. Clone the repo

```bash
   git clone https://github.com/ttakiwaki/iseo-discord-rpc
   cd iseo-discord-rpc
```

2. Install dependencies

```bash
   pip install -r requirements.txt
```

3. Create a `.env` file from the example

```bash
   cp .env.example .env
```

Fill in your Discord application's client ID. You can create one at [discord.com/developers](https://discord.com/developers/applications). If you wish to have a fallback album cover, you can use the iseo logo provided in the assets folder, and upload it to the 'Rich Presence Art Assets' section. Make sure the name of the asset matches with the name set in main.py (Line 68).

4. Run the server

```bash
   python main.py
```

5. Open ISEO, go to Settings, and enable **Discord Rich Presence**

---

## How it works

ISEO sends track data to the local server on every song change. The server debounces rapid skips, looks up cover art from [Cover Art Archive](https://coverartarchive.org) if the file has a MusicBrainz album ID embedded, then updates Discord via Rich Presence.

> ISEO (browser) → POST localhost:8000/update → Python → Discord

---

## Stack

Python, Flask, pypresence

---

## License

GPL v3 — free to use, modify, and distribute. Any derivative work must also be open source under the same license.

---

_A companion project to [ISEO](https://github.com/ttakiwaki/iseo-player)._
