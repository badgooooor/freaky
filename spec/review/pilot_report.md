# Pilot Report

50 messages × 4 modes = 200 labels. Thai: 25, English: 25.

## Emoji Usage Frequency

### freaky (42 in pool)
Top: 🫦×19, 😏×18, 😈×17, 💋×12, 😍×11, 🛌×11, 💦×11, 🔑×10
Never used (19): 🍆 🥵 🍒 🥜 🤭 🍓 🤩 🦴 🧲 🔐 🥩 🌮 🌯 🥙 🍣 🥐 🔧 🪛 🔩

Note: 🍆/🍑/🌭/🍌 not used much — too obvious, reserved for explicit food-topic messages. Contextual food (🌮/🌯/🥙) barely needed. Consider keeping in vocab but they're niche.

### passive_aggressive (48 in pool)
Top: 🙂×37, 👍×19, 🤷×19, 💅×14, 🙄×12, 😌×11
Never used (32): 😏 👀 🤭 😊 😤 😒 🥲 😬 👋 🫠 ✨ 💁 🫵 👉 🏆 🥇 🎭 🤡 🪆 👁️ 🔍 🕵️ 😶‍🌫️ 🫥 🔒 🔭 🩺 🤫 🥸 🧁 🍩 🪤 🧪 🧹

🙂 massively dominant — expected, it's the platonic passive-aggressive emoji. Many ominous emoji assigned to this mode were never reached.

### wrong_occasion (39 in pool)
Top: 🎉×38, 🥂×28, 🥳×16, 🏆×15, 🍾×14, 🎊×10, ⚰️×7, 🕯️×7
Never used (26): 💋 🍒 😍 🛌 🍓 👏 🥲 ✨ 🎈 🎂 🪅 🎁 🤩 🪄 🎠 🎪 🎰 🎶 🪩 🧙 🎇 🔮 🕯️ 🍜 🍣 🧁 🍩 🪜 🛁

🎉/🥂 dominate strongly. Celebration emoji do all the work. Gothic wrong-occasion (⚰️/🕯️) useful for birthday/good-news messages specifically.

### unhinged (74 in pool)
Top: 💣×26, 💀×23, ☠️×13, 🔪×11, 👁️×11, 🌋×11, 🔮×9, 🌚×6
Never used (51): Most ominous/contextual overlap assignments never reached.

Pool is too large — 74 emoji, only ~20 get used. The most viscerally chaotic (💣💀🔪☠️) crowd out the subtle ones.

## Mode Blur Assessment

- **freaky × unhinged**: Slight blur on dark suggestive emoji (😈, 🔥). Acceptable — these genuinely span both.
- **passive_aggressive × wrong_occasion**: 🏆/🥇 shared, 🙂 occasionally bleeds in. Distinct enough.
- No serious blur between freaky and passive_aggressive.
- No blur between wrong_occasion and unhinged.

## Recommendations for Step 5

**Drop from vocab** (never used, low connotation value):
- freaky: 🥜, 🍓, 🔐, 🥙, 🥐 (weak contextual)
- passive_aggressive: 🪆, 🫥, 🩺, 🔭 (too ominous, wrong fit)
- wrong_occasion: 🎠, 🎶, 🪄 (too mild to land)
- unhinged: pool is fine — large is OK for training data diversity

**Keep but mark as niche**: contextual food emoji (🌮, 🌯, 🍣) — only activate on food-topic messages

**Prompts**: no retry failures (all labels were in-vocab). Prompt templates are sufficient.

## Sample Table (10 examples)

| msg | freaky | passive_aggressive | wrong_occasion | unhinged |
|-----|--------|-------------------|----------------|---------|
| กินข้าวกันมั้ยเย็นนี้ | 🍌🫦🍜👅 | 🙂👍😑 | 🍾🥂🎉 | 🔪💀☠️ |
| แม่ไม่สบายค่ะ | 🛌🧴💋 | 🤷😌💅 | 🎉🥂🏆 | 💉⚰️💀 |
| ขอโทษที่ส่งงานช้า | 😏😈🫦 | 🙂👍🙃 | 🎉🥳🏆 | 💣🌋💀 |
| Grandpa passed away | 🛌💋😍 | 💅😌🤷 | 🎉🥳🥂 | 🤡🫃💣 |
| Want to grab lunch today? | 🍌🌭🥒🫦 | 🙄🤷😑 | 🍾🥂🎉 | 🔪☠️💀 |
| I got promoted today | 🔥😈💋 | 👏👍🙂 | ⚰️🕯️🌑 | 🤡💣🌋 |
| Don't forget to hydrate | 💦🧴😏 | 🙂🫡😇 | 🍾🥂🎉 | 💉💊☠️ |
| นอนหลับให้หลับสบายนะ | 🛌😈💋👅 | 🙂👍😌 | 🎉🥂🥳 | 🌑🌚💀 |
| The project is finally done! | 🔥💦😈 | 👏🙂😌 | ⚰️🕯️🌑 | 🤡💣🌋 |
| Happy anniversary! | 💋🫦😈🔥 | 👍👏🙂 | ⚰️🕯️💊 | 💣🤡🌚 |
