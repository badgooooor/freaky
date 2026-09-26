# freaky — Vocab Spec v1

## Overview

Emoji vocabulary for labeling messages with contextually cursed emoji across four distinct modes. Input: a text message. Output: an unordered set of 2–4 emoji per mode that make the message maximally cursed for that mode.

---

## Vocab

**Size**: 135 emoji  
**File**: `spec/vocab.v1.json` (frozen — do not modify)

### Annotation Schema

Each entry has 7 fields:

| field | type | description |
|-------|------|-------------|
| `emoji` | string | the emoji character |
| `name` | string | canonical English name |
| `literal` | string | what it literally depicts |
| `connotations` | string[] | cultural/contextual meanings that create cursedness |
| `cursed_when` | string | contexts where it lands wrong |
| `intensity` | 1–3 | 1 = subtle, 2 = medium, 3 = loud/explicit |
| `modes` | string[] | which modes this emoji belongs to |

---

## Modes

**File**: `spec/modes.v1.json` (frozen)

| mode | vibe | pool size |
|------|------|-----------|
| `freaky` | makes innocent messages sound suggestive | 42 |
| `passive_aggressive` | makes it passive aggressive | 48 |
| `wrong_occasion` | wrong emoji for the context | 39 |
| `unhinged` | chaos | 74 |

Modes are pre-fixed. No clustering was used — assignments were made by LLM in-context with manual review.

---

## Label Format

- **Per message**: 2–4 emoji per mode, unordered set
- **Input format**: `[mode] message`
- **Example input**: `[freaky] Want to grab lunch today?`
- **Example output**: `🍌🌭🥒🫦`

Same 50 messages were labeled across all 4 modes in pilot (200 total labels).

---

## Pilot Findings

**File**: `spec/review/pilot_report.md`

Key findings from 50 messages × 4 modes:

- `freaky`: 🫦/😏/😈 dominate. Explicit food (🍆🍌) rarely triggered — too obvious, reserved for food-topic messages. Contextual food (🌮🌯🥙) near-never needed.
- `passive_aggressive`: 🙂 massively dominant (×37/50). Pool of 48 is oversized — most ominous emoji assigned here were never reached.
- `wrong_occasion`: 🎉/🥂 do most of the work. Gothic wrong-occasion (⚰️🕯️) activates specifically for good-news/birthday messages.
- `unhinged`: Pool of 74 is large but acceptable for diversity. Top 8 (💣💀☠️🔪👁️🌋🔮🌚) crowd out subtler picks. No failures.

No serious mode blur. freaky×unhinged have mild overlap on dark suggestive emoji (😈🔥) — acceptable, they genuinely span both.

### Drop recommendations (never used, low value)

These remain in vocab.v1.json but are flagged as weak:

- freaky: 🥜 🍓 🔐 🥙 🥐
- passive_aggressive: 🪆 🫥 🩺 🔭
- wrong_occasion: 🎠 🎶 🪄
- unhinged: pool fine as-is

---

## Changelog

| version | change |
|---------|--------|
| v1 | Initial 135-emoji vocab, 4 modes, 200 pilot labels. No re-run — frozen with weak emoji noted above. |
