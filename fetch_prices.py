import os, json, time, urllib.request, urllib.parse, datetime

API_KEY    = os.environ.get('CSFLOAT_API_KEY', '')
CF_BASE    = 'https://csfloat.com/api/v1'
MAX_RETRY  = 5
RETRY_WAIT = 60
BASE_DELAY = 1.5

ALL_WEARS   = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
KNIFE_WEARS = ['Factory New', 'Minimal Wear', 'Field-Tested']  # 나이프/글러브 주요 외관

def w(name, knife=False):
    """일반 아이템 (name, wears) 반환"""
    return (name, KNIFE_WEARS if knife else ALL_WEARS)

def st(name, knife=False):
    """StatTrak 아이템 이름 생성 후 (name, wears) 반환
    나이프: ★ StatTrak™ Knife | Skin
    일반:   StatTrak™ Weapon | Skin
    """
    if knife:
        # "★ Paracord Knife | Doppler" → "★ StatTrak™ Paracord Knife | Doppler"
        st_name = name.replace('★ ', '★ StatTrak™ ')
    else:
        st_name = 'StatTrak™ ' + name
    return (st_name, KNIFE_WEARS if knife else ALL_WEARS)

ITEMS = [
    # ── 케이스 / 열쇠 (외관 없음, ST 없음) ─────────────────
    ('Revolution Case',           [None]),
    ('Recoil Case',               [None]),
    ('Fracture Case',             [None]),
    ('Dreams & Nightmares Case',  [None]),
    ('CS2 Case Key',              [None]),

    # ══════════════════════════════════════════
    # 혁명 케이스
    # ══════════════════════════════════════════
    w('AK-47 | Head Shot'),         st('AK-47 | Head Shot'),
    w('M4A4 | Temukau'),            st('M4A4 | Temukau'),
    w('AWP | Duality'),             st('AWP | Duality'),
    w('P2000 | Wicked Sick'),       st('P2000 | Wicked Sick'),
    w('UMP-45 | Wild Child'),       st('UMP-45 | Wild Child'),
    w('M4A1-S | Emphorosaur-S'),    st('M4A1-S | Emphorosaur-S'),
    w('Glock-18 | Umbral Rabbit'),  st('Glock-18 | Umbral Rabbit'),
    w('MAC-10 | Sakkaku'),          st('MAC-10 | Sakkaku'),
    w('R8 Revolver | Banana Cannon'),st('R8 Revolver | Banana Cannon'),
    w('P90 | Neoqueen'),            st('P90 | Neoqueen'),
    w('MAG-7 | Insomnia'),          st('MAG-7 | Insomnia'),
    w('MP9 | Featherweight'),       st('MP9 | Featherweight'),
    w('SCAR-20 | Fragments'),       st('SCAR-20 | Fragments'),
    w('Tec-9 | Rebel'),             st('Tec-9 | Rebel'),
    w('P250 | Re.built'),           st('P250 | Re.built'),
    w('MP5-SD | Liquidation'),      st('MP5-SD | Liquidation'),
    w('SG 553 | Cyberforce'),       st('SG 553 | Cyberforce'),
    # 글러브 (ST 없음)
    w('★ Sport Gloves | Vice',              knife=True),
    w('★ Sport Gloves | Amphibious',         knife=True),
    w('★ Sport Gloves | Omega',              knife=True),
    w('★ Sport Gloves | Bronze Morph',       knife=True),
    w('★ Driver Gloves | King Snake',        knife=True),
    w('★ Driver Gloves | Imperial Plaid',    knife=True),
    w('★ Driver Gloves | Overtake',          knife=True),
    w('★ Driver Gloves | Racing Green',      knife=True),
    w('★ Specialist Gloves | Fade',          knife=True),
    w('★ Specialist Gloves | Crimson Web',   knife=True),
    w('★ Specialist Gloves | Mogul',         knife=True),
    w('★ Specialist Gloves | Buckshot',      knife=True),
    w('★ Hand Wraps | Cobalt Skulls',        knife=True),
    w('★ Hand Wraps | Overprint',            knife=True),
    w('★ Hand Wraps | Arboreal',             knife=True),
    w('★ Hand Wraps | Duct Tape',            knife=True),
    w('★ Moto Gloves | POW!',                knife=True),
    w('★ Moto Gloves | Polygon',             knife=True),
    w('★ Moto Gloves | Turtle',              knife=True),
    w('★ Moto Gloves | Transport',           knife=True),
    w('★ Hydra Gloves | Case Hardened',      knife=True),
    w('★ Hydra Gloves | Emerald',            knife=True),
    w('★ Hydra Gloves | Rattler',            knife=True),
    w('★ Hydra Gloves | Mangrove',           knife=True),

    # ══════════════════════════════════════════
    # 리코일 케이스
    # ══════════════════════════════════════════
    w('USP-S | Printstream'),       st('USP-S | Printstream'),
    w('AWP | Chromatic Aberration'),st('AWP | Chromatic Aberration'),
    w('AK-47 | Ice Coaled'),        st('AK-47 | Ice Coaled'),
    w('P250 | Visions'),            st('P250 | Visions'),
    w('Sawed-Off | Kiss♥Love'),     st('Sawed-Off | Kiss♥Love'),
    w('SG 553 | Dragon Tech'),      st('SG 553 | Dragon Tech'),
    w('M249 | Downtown'),           st('M249 | Downtown'),
    w('Dual Berettas | Flora Carnivora'), st('Dual Berettas | Flora Carnivora'),
    w('R8 Revolver | Crazy 8'),     st('R8 Revolver | Crazy 8'),
    w('P90 | Vent Rush'),           st('P90 | Vent Rush'),
    w('M4A4 | Poly Mag'),           st('M4A4 | Poly Mag'),
    w('Galil AR | Destroyer'),      st('Galil AR | Destroyer'),
    w('Glock-18 | Winterized'),     st('Glock-18 | Winterized'),
    w('FAMAS | Meow 36'),           st('FAMAS | Meow 36'),
    w('UMP-45 | Roadblock'),        st('UMP-45 | Roadblock'),
    w('Negev | Drop Me'),           st('Negev | Drop Me'),
    w('MAC-10 | Monkeyflage'),      st('MAC-10 | Monkeyflage'),
    # 글러브 (ST 없음)
    w('★ Sport Gloves | Slingshot',          knife=True),
    w('★ Sport Gloves | Hedge Maze',         knife=True),
    w('★ Specialist Gloves | Marble Fade',   knife=True),
    w('★ Specialist Gloves | Lt. Commander', knife=True),
    w('★ Specialist Gloves | Crimson Kimono',knife=True),
    w('★ Specialist Gloves | Emerald Web',   knife=True),
    w('★ Specialist Gloves | Foundation',    knife=True),
    w('★ Specialist Gloves | Mogul',         knife=True),
    w('★ Driver Gloves | Queen Jaguar',      knife=True),
    w('★ Driver Gloves | Convoy',            knife=True),
    w('★ Hand Wraps | CAUTION!',             knife=True),
    w('★ Hand Wraps | Leather',              knife=True),
    w('★ Moto Gloves | Finish Line',         knife=True),
    w('★ Moto Gloves | Blood Pressure',      knife=True),
    w('★ Moto Gloves | 3rd Commando Company',knife=True),
    w('★ Hydra Gloves | Emerald',            knife=True),
    w('★ Hydra Gloves | Rattler',            knife=True),
    w('★ Hydra Gloves | Mangrove',           knife=True),
    w('★ Hydra Gloves | Case Hardened',      knife=True),
    w('★ Broken Fang Gloves | Jade',         knife=True),
    w('★ Broken Fang Gloves | Needle Point', knife=True),
    w('★ Broken Fang Gloves | Unhinged',     knife=True),
    w('★ Broken Fang Gloves | Yellow Jacket',knife=True),

    # ══════════════════════════════════════════
    # 프랙처 케이스
    # ══════════════════════════════════════════
    w('AK-47 | Legion of Anubis'),  st('AK-47 | Legion of Anubis'),
    w('Desert Eagle | Printstream'),st('Desert Eagle | Printstream'),
    w('M4A4 | Tooth Fairy'),        st('M4A4 | Tooth Fairy'),
    w('Glock-18 | Vogue'),          st('Glock-18 | Vogue'),
    w('MAC-10 | Allure'),           st('MAC-10 | Allure'),
    w('Five-SeveN | Angry Mob'),    st('Five-SeveN | Angry Mob'),
    w('MP9 | Hydra'),               st('MP9 | Hydra'),
    w("SG 553 | Ol' Rusty"),        st("SG 553 | Ol' Rusty"),
    w('AUG | Flame Jörmungandr'),   st('AUG | Flame Jörmungandr'),
    w('P250 | Contaminant'),        st('P250 | Contaminant'),
    w('CZ75-Auto | Distressed'),    st('CZ75-Auto | Distressed'),
    w('Nova | Windblown'),          st('Nova | Windblown'),
    w('Tec-9 | Bamboozle'),         st('Tec-9 | Bamboozle'),
    w('MP5-SD | Necro Jr.'),        st('MP5-SD | Necro Jr.'),
    w('UMP-45 | Momentum'),         st('UMP-45 | Momentum'),
    w('Dual Berettas | Melondrama'),st('Dual Berettas | Melondrama'),
    w('PP-Bizon | Space Cat'),      st('PP-Bizon | Space Cat'),
    # 나이프 (ST 있음)
    w('★ Paracord Knife | Doppler',       knife=True), st('★ Paracord Knife | Doppler',       knife=True),
    w('★ Paracord Knife | Fade',          knife=True), st('★ Paracord Knife | Fade',          knife=True),
    w('★ Paracord Knife | Marble Fade',   knife=True), st('★ Paracord Knife | Marble Fade',   knife=True),
    w('★ Paracord Knife | Tiger Tooth',   knife=True), st('★ Paracord Knife | Tiger Tooth',   knife=True),
    w('★ Paracord Knife | Case Hardened', knife=True), st('★ Paracord Knife | Case Hardened', knife=True),
    w('★ Survival Knife | Doppler',       knife=True), st('★ Survival Knife | Doppler',       knife=True),
    w('★ Survival Knife | Fade',          knife=True), st('★ Survival Knife | Fade',          knife=True),
    w('★ Survival Knife | Marble Fade',   knife=True), st('★ Survival Knife | Marble Fade',   knife=True),
    w('★ Survival Knife | Tiger Tooth',   knife=True), st('★ Survival Knife | Tiger Tooth',   knife=True),
    w('★ Survival Knife | Case Hardened', knife=True), st('★ Survival Knife | Case Hardened', knife=True),
    w('★ Nomad Knife | Doppler',          knife=True), st('★ Nomad Knife | Doppler',          knife=True),
    w('★ Nomad Knife | Fade',             knife=True), st('★ Nomad Knife | Fade',             knife=True),
    w('★ Nomad Knife | Marble Fade',      knife=True), st('★ Nomad Knife | Marble Fade',      knife=True),
    w('★ Nomad Knife | Case Hardened',    knife=True), st('★ Nomad Knife | Case Hardened',    knife=True),
    w('★ Skeleton Knife | Doppler',       knife=True), st('★ Skeleton Knife | Doppler',       knife=True),
    w('★ Skeleton Knife | Fade',          knife=True), st('★ Skeleton Knife | Fade',          knife=True),
    w('★ Skeleton Knife | Marble Fade',   knife=True), st('★ Skeleton Knife | Marble Fade',   knife=True),
    w('★ Skeleton Knife | Case Hardened', knife=True), st('★ Skeleton Knife | Case Hardened', knife=True),

    # ══════════════════════════════════════════
    # 드림즈 & 나이트메어 케이스
    # ══════════════════════════════════════════
    w('MP9 | Starlight Protector'),  st('MP9 | Starlight Protector'),
    w('AK-47 | Nightwish'),          st('AK-47 | Nightwish'),
    w('MP7 | Abyssal Apparition'),   st('MP7 | Abyssal Apparition'),
    w('Dual Berettas | Melondrama'), st('Dual Berettas | Melondrama'),
    w('FAMAS | Rapid Eye Movement'), st('FAMAS | Rapid Eye Movement'),
    w('Five-SeveN | Scrawl'),        st('Five-SeveN | Scrawl'),
    w('USP-S | Ticket to Hell'),     st('USP-S | Ticket to Hell'),
    w('Glock-18 | Night Terror'),    st('Glock-18 | Night Terror'),
    w('PP-Bizon | Space Cat'),       st('PP-Bizon | Space Cat'),
    w('M4A1-S | Night Lotus'),       st('M4A1-S | Night Lotus'),
    w('Nova | Night Spirit'),        st('Nova | Night Spirit'),
    w('MAC-10 | Ensnared'),          st('MAC-10 | Ensnared'),
    w('MP5-SD | Necro Jr.'),         st('MP5-SD | Necro Jr.'),
    w('XM1014 | Zombie Offensive'),  st('XM1014 | Zombie Offensive'),
    w('P250 | Visions'),             st('P250 | Visions'),
    w('Tec-9 | Decimator'),          st('Tec-9 | Decimator'),
    w('G3SG1 | Dream Glade'),        st('G3SG1 | Dream Glade'),
    # 나이프 (ST 있음)
    w('★ Falchion Knife | Doppler',       knife=True), st('★ Falchion Knife | Doppler',       knife=True),
    w('★ Falchion Knife | Gamma Doppler', knife=True), st('★ Falchion Knife | Gamma Doppler', knife=True),
    w('★ Falchion Knife | Fade',          knife=True), st('★ Falchion Knife | Fade',          knife=True),
    w('★ Falchion Knife | Marble Fade',   knife=True), st('★ Falchion Knife | Marble Fade',   knife=True),
    w('★ Falchion Knife | Tiger Tooth',   knife=True), st('★ Falchion Knife | Tiger Tooth',   knife=True),
    w('★ Falchion Knife | Case Hardened', knife=True), st('★ Falchion Knife | Case Hardened', knife=True),
    w('★ Bowie Knife | Doppler',          knife=True), st('★ Bowie Knife | Doppler',          knife=True),
    w('★ Bowie Knife | Gamma Doppler',    knife=True), st('★ Bowie Knife | Gamma Doppler',    knife=True),
    w('★ Bowie Knife | Fade',             knife=True), st('★ Bowie Knife | Fade',             knife=True),
    w('★ Bowie Knife | Marble Fade',      knife=True), st('★ Bowie Knife | Marble Fade',      knife=True),
    w('★ Bowie Knife | Tiger Tooth',      knife=True), st('★ Bowie Knife | Tiger Tooth',      knife=True),
    w('★ Bowie Knife | Case Hardened',    knife=True), st('★ Bowie Knife | Case Hardened',    knife=True),
]


def load_previous_prices():
    try:
        with open('prices.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('prices', {})
    except Exception:
        return {}


def fetch_price(name, wear):
    query   = name if wear is None else f'{name} ({wear})'
    encoded = urllib.parse.quote(query)
    url     = f'{CF_BASE}/listings?market_hash_name={encoded}&limit=10&sort_by=lowest_price&category=0'
    req     = urllib.request.Request(url, headers={'Authorization': API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())

        if not data.get('data'):
            return 0

        listed = [l for l in data['data'] if l.get('type') == 'buy_now']
        src    = listed if listed else data['data']
        ref    = src[0].get('reference', {})
        price  = ref.get('base_price') or src[0].get('price', 0)
        return price if price > 0 else 0

    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f'    → rate limit (429)')
            return None
        if e.code == 404:
            return 0
        print(f'    → HTTP {e.code}')
        return None
    except Exception as e:
        print(f'    → 오류: {e}')
        return None


def fetch_with_retry(name, wear):
    for attempt in range(1, MAX_RETRY + 1):
        result = fetch_price(name, wear)

        if result == 0:
            return 0
        if result is not None and result > 0:
            return result

        if attempt < MAX_RETRY:
            print(f'    → 재시도 ({attempt}/{MAX_RETRY}), {RETRY_WAIT}초 대기...')
            time.sleep(RETRY_WAIT)
        else:
            print(f'    → {MAX_RETRY}번 모두 실패')

    return None


def main():
    prev   = load_previous_prices()
    prices = {}
    failed = []

    requests = []
    for item in ITEMS:
        name, wears = item
        for wear in wears:
            requests.append((name, wear))

    total = len(requests)
    print(f'총 {total}개 요청 시작 (일반 + ST 포함)\n')

    for i, (name, wear) in enumerate(requests):
        key   = f'{name}|{wear or ""}'
        query = name if wear is None else f'{name} ({wear})'
        print(f'[{i+1}/{total}] {query}')

        result = fetch_with_retry(name, wear)

        if result is None:
            prev_val = prev.get(key)
            if prev_val:
                prices[key] = prev_val
                print(f'  ⚠ 이전 값 유지: ${prev_val/100:.2f}')
            else:
                prices[key] = 0
                failed.append(key)
                print(f'  ✗ 이전 값 없음 → 0')
        elif result == 0:
            prev_val = prev.get(key)
            prices[key] = prev_val if prev_val else 0
            print(f'  - 매물 없음' + (f' (이전 값 유지: ${prev_val/100:.2f})' if prev_val else ''))
        else:
            prices[key] = result
            krw = round(result / 100 * 1480)
            print(f'  ✓ ${result/100:.2f} → ₩{krw:,}')

        time.sleep(BASE_DELAY)

    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump({
            'updated_at': datetime.datetime.utcnow().isoformat() + 'Z',
            'prices': prices
        }, f, ensure_ascii=False, indent=2)

    print(f'\n완료! {len(prices)}개 처리')
    if failed:
        print(f'최종 실패 항목 ({len(failed)}개):')
        for k in failed:
            print(f'  - {k}')


if __name__ == '__main__':
    main()
