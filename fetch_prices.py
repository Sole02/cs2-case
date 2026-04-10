import os, json, time, urllib.request, urllib.parse, datetime

API_KEY    = os.environ.get('CSFLOAT_API_KEY', '')
CF_BASE    = 'https://csfloat.com/api/v1'
MAX_RETRY  = 5
RETRY_WAIT = 60
BASE_DELAY = 1.5

# ─────────────────────────────────────────────
# 검색으로 확인된 정확한 아이템 이름 목록
# ─────────────────────────────────────────────
ITEMS = [
    # 케이스 / 열쇠
    ('Revolution Case',            None),
    ('Recoil Case',                None),
    ('Fracture Case',              None),
    ('Dreams & Nightmares Case',   None),
    ('CS2 Case Key',               None),

    # ── 혁명 케이스 (Revolution Case) ──────────
    # Covert
    ('AK-47 | Head Shot',          'Field-Tested'),
    ('M4A4 | Temukau',             'Field-Tested'),
    # Classified
    ('AWP | Duality',              'Field-Tested'),
    ('P2000 | Wicked Sick',        'Field-Tested'),
    ('UMP-45 | Wild Child',        'Field-Tested'),
    # Restricted
    ('M4A1-S | Emphorosaur-S',     'Field-Tested'),
    ('Glock-18 | Umbral Rabbit',   'Field-Tested'),
    ('MAC-10 | Sakkaku',           'Field-Tested'),
    ('R8 Revolver | Banana Cannon','Field-Tested'),
    ('P90 | Neoqueen',             'Field-Tested'),
    # Mil-Spec
    ('MAG-7 | Insomnia',           'Field-Tested'),
    ('MP9 | Featherweight',        'Field-Tested'),
    ('SCAR-20 | Fragments',        'Field-Tested'),
    ('Tec-9 | Rebel',              'Field-Tested'),
    ('P250 | Re.built',            'Field-Tested'),
    ('MP5-SD | Liquidation',       'Field-Tested'),
    ('SG 553 | Cyberforce',        'Field-Tested'),
    # Gloves (Revolution = Clutch Gloves)
    ('★ Sport Gloves | Vice',               'Field-Tested'),
    ('★ Sport Gloves | Amphibious',          'Field-Tested'),
    ('★ Sport Gloves | Omega',               'Field-Tested'),
    ('★ Sport Gloves | Bronze Morph',        'Field-Tested'),
    ('★ Driver Gloves | King Snake',         'Field-Tested'),
    ('★ Driver Gloves | Imperial Plaid',     'Field-Tested'),
    ('★ Driver Gloves | Overtake',           'Field-Tested'),
    ('★ Driver Gloves | Racing Green',       'Field-Tested'),
    ('★ Specialist Gloves | Fade',           'Field-Tested'),
    ('★ Specialist Gloves | Crimson Web',    'Field-Tested'),
    ('★ Specialist Gloves | Mogul',          'Field-Tested'),
    ('★ Specialist Gloves | Buckshot',       'Field-Tested'),
    ('★ Hand Wraps | Cobalt Skulls',         'Field-Tested'),
    ('★ Hand Wraps | Overprint',             'Field-Tested'),
    ('★ Hand Wraps | Arboreal',              'Field-Tested'),
    ('★ Hand Wraps | Duct Tape',             'Field-Tested'),
    ('★ Moto Gloves | POW!',                 'Field-Tested'),
    ('★ Moto Gloves | Polygon',              'Field-Tested'),
    ('★ Moto Gloves | Turtle',               'Field-Tested'),
    ('★ Moto Gloves | Transport',            'Field-Tested'),
    ('★ Hydra Gloves | Case Hardened',       'Field-Tested'),
    ('★ Hydra Gloves | Emerald',             'Field-Tested'),
    ('★ Hydra Gloves | Rattler',             'Field-Tested'),
    ('★ Hydra Gloves | Mangrove',            'Field-Tested'),

    # ── 리코일 케이스 (Recoil Case) ─────────────
    # Covert
    ('USP-S | Printstream',        'Field-Tested'),
    ('AWP | Chromatic Aberration', 'Field-Tested'),
    # Classified
    ('AK-47 | Ice Coaled',         'Field-Tested'),
    ('P250 | Visions',             'Field-Tested'),
    ('Sawed-Off | Kiss♥Love',      'Field-Tested'),
    # Restricted
    ('SG 553 | Dragon Tech',       'Field-Tested'),
    ('M249 | Downtown',            'Field-Tested'),
    ('Dual Berettas | Flora Carnivora', 'Field-Tested'),
    ('R8 Revolver | Crazy 8',      'Field-Tested'),
    ('P90 | Vent Rush',            'Field-Tested'),
    # Mil-Spec
    ('M4A4 | Poly Mag',            'Field-Tested'),
    ('Galil AR | Destroyer',       'Field-Tested'),
    ('Glock-18 | Winterized',      'Field-Tested'),
    ('FAMAS | Meow 36',            'Field-Tested'),
    ('UMP-45 | Roadblock',         'Field-Tested'),
    ('Negev | Drop Me',            'Field-Tested'),
    ('MAC-10 | Monkeyflage',       'Field-Tested'),
    # Gloves (Recoil = Broken Fang Gloves)
    ('★ Sport Gloves | Slingshot',           'Field-Tested'),
    ('★ Sport Gloves | Hedge Maze',          'Field-Tested'),
    ('★ Specialist Gloves | Marble Fade',    'Field-Tested'),
    ('★ Specialist Gloves | Lt. Commander',  'Field-Tested'),
    ('★ Driver Gloves | Queen Jaguar',       'Field-Tested'),
    ('★ Driver Gloves | Convoy',             'Field-Tested'),
    ('★ Hand Wraps | CAUTION!',              'Field-Tested'),
    ('★ Hand Wraps | Leather',               'Field-Tested'),
    ('★ Moto Gloves | Finish Line',          'Field-Tested'),
    ('★ Moto Gloves | Blood Pressure',       'Field-Tested'),
    ('★ Moto Gloves | 3rd Commando Company', 'Field-Tested'),
    ('★ Moto Gloves | POW!',                 'Field-Tested'),
    ('★ Hydra Gloves | Emerald',             'Field-Tested'),
    ('★ Hydra Gloves | Rattler',             'Field-Tested'),
    ('★ Hydra Gloves | Mangrove',            'Field-Tested'),
    ('★ Hydra Gloves | Case Hardened',       'Field-Tested'),
    ('★ Broken Fang Gloves | Jade',          'Field-Tested'),
    ('★ Broken Fang Gloves | Needle Point',  'Field-Tested'),
    ('★ Broken Fang Gloves | Unhinged',      'Field-Tested'),
    ('★ Broken Fang Gloves | Yellow Jacket', 'Field-Tested'),
    ('★ Specialist Gloves | Crimson Kimono', 'Field-Tested'),
    ('★ Specialist Gloves | Emerald Web',    'Field-Tested'),
    ('★ Specialist Gloves | Foundation',     'Field-Tested'),
    ('★ Specialist Gloves | Mogul',          'Field-Tested'),

    # ── 프랙처 케이스 (Fracture Case) ───────────
    # Covert
    ('AK-47 | Legion of Anubis',   'Field-Tested'),
    ('Desert Eagle | Printstream', 'Field-Tested'),
    # Classified
    ('M4A4 | Tooth Fairy',         'Field-Tested'),
    ('Glock-18 | Vogue',           'Field-Tested'),
    ('MAC-10 | Allure',            'Field-Tested'),
    # Restricted
    ('Five-SeveN | Angry Mob',     'Field-Tested'),
    ('MP9 | Hydra',                'Field-Tested'),
    ('SG 553 | Ol\' Rusty',        'Field-Tested'),
    ('AUG | Flame Jörmungandr',    'Field-Tested'),
    ('P250 | Contaminant',         'Field-Tested'),
    # Mil-Spec
    ('CZ75-Auto | Distressed',     'Field-Tested'),
    ('Nova | Windblown',           'Field-Tested'),
    ('Tec-9 | Bamboozle',          'Field-Tested'),
    ('MP5-SD | Necro Jr.',         'Field-Tested'),
    ('UMP-45 | Momentum',          'Field-Tested'),
    ('Dual Berettas | Melondrama', 'Field-Tested'),
    ('PP-Bizon | Space Cat',       'Field-Tested'),
    # Knives (Fracture = Shattered Web Knives)
    ('★ Paracord Knife | Doppler',      'Factory New'),
    ('★ Paracord Knife | Fade',         'Factory New'),
    ('★ Paracord Knife | Marble Fade',  'Factory New'),
    ('★ Paracord Knife | Tiger Tooth',  'Factory New'),
    ('★ Paracord Knife | Case Hardened','Field-Tested'),
    ('★ Survival Knife | Doppler',      'Factory New'),
    ('★ Survival Knife | Fade',         'Factory New'),
    ('★ Survival Knife | Marble Fade',  'Factory New'),
    ('★ Survival Knife | Tiger Tooth',  'Factory New'),
    ('★ Survival Knife | Case Hardened','Field-Tested'),
    ('★ Nomad Knife | Doppler',         'Factory New'),
    ('★ Nomad Knife | Fade',            'Factory New'),
    ('★ Nomad Knife | Marble Fade',     'Factory New'),
    ('★ Nomad Knife | Case Hardened',   'Field-Tested'),
    ('★ Skeleton Knife | Doppler',      'Factory New'),
    ('★ Skeleton Knife | Fade',         'Factory New'),
    ('★ Skeleton Knife | Marble Fade',  'Factory New'),
    ('★ Skeleton Knife | Case Hardened','Field-Tested'),

    # ── 드림즈 & 나이트메어 (Dreams & Nightmares) ─
    # Covert
    ('MP9 | Starlight Protector',  'Field-Tested'),
    ('AK-47 | Nightwish',          'Field-Tested'),
    # Classified
    ('MP7 | Abyssal Apparition',   'Field-Tested'),
    ('Dual Berettas | Melondrama', 'Field-Tested'),
    ('FAMAS | Rapid Eye Movement', 'Field-Tested'),
    # Restricted
    ('Five-SeveN | Scrawl',        'Field-Tested'),
    ('USP-S | Ticket to Hell',     'Field-Tested'),
    ('Glock-18 | Night Terror',    'Field-Tested'),
    ('PP-Bizon | Space Cat',       'Field-Tested'),
    ('M4A1-S | Night Lotus',       'Field-Tested'),
    # Mil-Spec
    ('Nova | Night Spirit',        'Field-Tested'),
    ('MAC-10 | Ensnared',          'Field-Tested'),
    ('MP5-SD | Necro Jr.',         'Field-Tested'),
    ('XM1014 | Zombie Offensive',  'Field-Tested'),
    ('P250 | Visions',             'Field-Tested'),
    ('Tec-9 | Decimator',          'Field-Tested'),
    ('G3SG1 | Dream Glade',        'Field-Tested'),
    # Knives (Dreams & Nightmares = Gamma Knives)
    ('★ Falchion Knife | Doppler',      'Factory New'),
    ('★ Falchion Knife | Gamma Doppler','Factory New'),
    ('★ Falchion Knife | Fade',         'Factory New'),
    ('★ Falchion Knife | Marble Fade',  'Factory New'),
    ('★ Falchion Knife | Tiger Tooth',  'Factory New'),
    ('★ Falchion Knife | Case Hardened','Field-Tested'),
    ('★ Bowie Knife | Doppler',         'Factory New'),
    ('★ Bowie Knife | Gamma Doppler',   'Factory New'),
    ('★ Bowie Knife | Fade',            'Factory New'),
    ('★ Bowie Knife | Marble Fade',     'Factory New'),
    ('★ Bowie Knife | Tiger Tooth',     'Factory New'),
    ('★ Bowie Knife | Case Hardened',   'Field-Tested'),
]


def load_previous_prices():
    try:
        with open('prices.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('prices', {})
    except Exception:
        return {}


def fetch_price(name, wear=None):
    query   = name if wear is None else f'{name} ({wear})'
    encoded = urllib.parse.quote(query)
    url     = f'{CF_BASE}/listings?market_hash_name={encoded}&limit=10&sort_by=lowest_price&category=0'
    req     = urllib.request.Request(url, headers={'Authorization': API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        if data.get('data'):
            listed = [l for l in data['data'] if l.get('type') == 'buy_now']
            src    = listed if listed else data['data']
            ref    = src[0].get('reference', {})
            price  = ref.get('base_price') or src[0].get('price', 0)
            if price > 0:
                return price
    except Exception as e:
        print(f'    오류: {e}')
    return None


def fetch_with_retry(name, wear):
    for attempt in range(1, MAX_RETRY + 1):
        result = fetch_price(name, wear)
        if result:
            return result
        if attempt < MAX_RETRY:
            print(f'    → 실패 ({attempt}/{MAX_RETRY}), {RETRY_WAIT}초 후 재시도...')
            time.sleep(RETRY_WAIT)
        else:
            print(f'    → {MAX_RETRY}번 모두 실패')
    return None


def main():
    prev   = load_previous_prices()
    prices = {}
    failed = []
    total  = len(ITEMS)

    for i, (name, wear) in enumerate(ITEMS):
        key   = f'{name}|{wear or ""}'
        query = name if wear is None else f'{name} ({wear})'
        print(f'[{i+1}/{total}] {query}')

        result = fetch_with_retry(name, wear)

        if result:
            prices[key] = result
            krw = round(result / 100 * 1480)
            print(f'  ✓ ${result/100:.2f} → ₩{krw:,}')
        else:
            prev_val = prev.get(key)
            if prev_val:
                prices[key] = prev_val
                print(f'  ⚠ 이전 값 유지: ${prev_val/100:.2f}')
            else:
                prices[key] = 0
                failed.append(key)
                print(f'  ✗ 이전 값 없음 → 0')

        time.sleep(BASE_DELAY)

    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump({
            'updated_at': datetime.datetime.utcnow().isoformat() + 'Z',
            'prices': prices
        }, f, ensure_ascii=False, indent=2)

    print(f'\n완료! {len(prices)}개 처리')
    if failed:
        print(f'0으로 저장된 항목 ({len(failed)}개):')
        for k in failed:
            print(f'  - {k}')


if __name__ == '__main__':
    main()
