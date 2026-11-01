# Auto-generates mons.json and mons.js by scanning the mons/ directory
import os
import json
import re

TYPE_MAP = {
    '01': ('Normal', '01_Normal.png', '#aaaa99'),
    '02': ('Fire', '02_Fire.png', '#ff4422'),
    '03': ('Water', '03_Water.png', '#3399ff'),
    '04': ('Electric', '04_Electric.png', '#ffcc33'),
    '05': ('Grass', '05_Grass.png', '#77cc55'),
    '06': ('Ice', '06_Ice.png', '#66ccff'),
    '07': ('Fighting', '07_Fighting.png', '#c03028'),
    '08': ('Poison', '08_Poison.png', '#a040a0'),
    '09': ('Ground', '09_Ground.png', '#e0c068'),
    '10': ('Flying', '10_Flying.png', '#a890f0'),
    '11': ('Psychic', '11_Psychic.png', '#ff5599'),
    '12': ('Bug', '12_Bug.png', '#a8b820'),
    '13': ('Rock', '13_Rock.png', '#b8a038'),
    '14': ('Ghost', '14_Ghost.png', '#705898'),
    '15': ('Dragon', '15_Dragon.png', '#7038f8'),
    '16': ('Dark', '16_Dark.png', '#f4d35e'),
    '17': ('Steel', '17_Steel.png', '#b8b8d0'),
    '18': ('Fairy', '18_Fairy.png', '#ee99ee'),
}

def scan_mons():
    mons_data = []
    mons_dir = 'mons'
    if not os.path.exists(mons_dir):
        return mons_data

    for folder in sorted(os.listdir(mons_dir)):
        p = os.path.join(mons_dir, folder)
        if not os.path.isdir(p):
            continue

        m = re.match(r'^(\d{2})_(.*)$', folder)
        if m:
            prefix = m.group(1)
            raw_name = m.group(2).replace('_', ' ').title()
        else:
            prefix = folder[:2]
            raw_name = folder[2:].lstrip('_').replace('_', ' ').title()

        files = sorted(os.listdir(p))
        # Find sleep file (ends with _S.gif or _s.gif)
        sleep_files = [f for f in files if re.search(r'_[sS]\.gif$', f)]
        sleep_file = sleep_files[0] if sleep_files else None

        # Find numbered animation files (e.g. _1.gif, _2.gif)
        num_files = []
        for f in files:
            num_match = re.search(r'_(\d+)\.gif$', f, re.IGNORECASE)
            if num_match:
                num_files.append((int(num_match.group(1)), f))
        num_files.sort(key=lambda x: x[0])
        numbered_gifs = [f[1] for f in num_files]

        type_info = TYPE_MAP.get(prefix, ('Unknown', f'{prefix}.png', '#5cd65c'))

        mons_data.append({
            'id': prefix,
            'folder': folder,
            'name': raw_name,
            'type': type_info[0],
            'bgFile': type_info[1],
            'color': type_info[2],
            'sleepGif': sleep_file,
            'clickGifs': numbered_gifs
        })

    # 1. Write mons.json
    with open('mons.json', 'w', encoding='utf-8') as f:
        json.dump(mons_data, f, indent=2)

    # 2. Write mons.js (loads cleanly in browsers on file:/// without CORS issues)
    with open('mons.js', 'w', encoding='utf-8') as f:
        f.write('window.MON_CATALOG = ' + json.dumps(mons_data, indent=2) + ';\n')

    print(f'Successfully updated mons.json and mons.js with {len(mons_data)} mons!')
    return mons_data

if __name__ == '__main__':
    scan_mons()
