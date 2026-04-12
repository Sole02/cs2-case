import os, json, time, urllib.request, urllib.parse, datetime

API_KEY    = os.environ.get('CSFLOAT_API_KEY', '')
CF_BASE    = 'https://csfloat.com/api/v1'
MAX_RETRY  = 5
RETRY_WAIT = 60
BASE_DELAY = 1.5

ALL_WEARS   = ['Factory New', 'Minimal Wear', 'Field-Tested', 'Well-Worn', 'Battle-Scarred']
KNIFE_WEARS = ['Factory New', 'Minimal Wear', 'Field-Tested']  # 나이프/글러브 주요 외관

# ── 아이템 정의 ────────────────────────────────────────────
# (name, wears)  wears=None → ALL_WEARS, wears=KNIFE_WEARS → 나이프/글러브용
# ──────────────────────────────────────────────────────────
def w(name, knife=False):
    return (name, KNIFE_WEARS if knife else ALL_WEARS)

ITEMS = [
    # 케이스 / 열쇠 (외관 없음)
    ('Revolution Case',           [None]),
    ('Recoil Case',               [None]),
    ('Fracture Case',             [None]),
    ('Dreams & Nightmares Case',  [None]),
    ('CS2 Case Key',              [None]),

    # ── 혁명 케이스 ────────────────────────────
    w('AK-47 | Head Shot'),
    w('M4A4 | Temukau'),
    w('AWP | Duality'),
    w('P2000 | Wicked Sick'),
    w('UMP-45 | Wild Child'),
    w('M4A1-S | Emphorosaur-S'),
    w('Glock-18 | Umbral Rabbit'),
    w('MAC-10 | Sakkaku'),
    w('R8 Revolver | Banana Cannon'),
    w('P90 | Neoqueen'),
    w('MAG-7 | Insomnia'),
    w('MP9 | Featherweight'),
    w('SCAR-20 | Fragments'),
    w('Tec-9 | Rebel'),
    w('P250 | Re.built'),
    w('MP5-SD | Liquidation'),
    w('SG 553 | Cyberforce'),
    # 글러브 (혁명 = Clutch Gloves)
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

    # ── 리코일 케이스 ───────────────────────────
    w('USP-S | Printstream'),
    w('AWP | Chromatic Aberration'),
    w('AK-47 | Ice Coaled'),
    w('P250 | Visions'),
    w('Sawed-Off | Kiss♥Love'),
    w('SG 553 | Dragon Tech'),
    w('M249 | Downtown'),
    w('Dual Berettas | Flora Carnivora'),
    w('R8 Revolver | Crazy 8'),
    w('P90 | Vent Rush'),
    w('M4A4 | Poly Mag'),
    w('Galil AR | Destroyer'),
    w('Glock-18 | Winterized'),
    w('FAMAS | Meow 36'),
    w('UMP-45 | Roadblock'),
    w('Negev | Drop Me'),
    w('MAC-10 | Monkeyflage'),
    # 글러브 (리코일 = Broken Fang Gloves)
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

    # ── 프랙처 케이스 ───────────────────────────
    w('AK-47 | Legion of Anubis'),
    w('Desert Eagle | Printstream'),
    w('M4A4 | Tooth Fairy'),
    w('Glock-18 | Vogue'),
    w('MAC-10 | Allure'),
    w('Five-SeveN | Angry Mob'),
    w('MP9 | Hydra'),
    w("SG 553 | Ol' Rusty"),
    w('AUG | Flame Jörmungandr'),
    w('P250 | Contaminant'),
    w('CZ75-Auto | Distressed'),
    w('Nova | Windblown'),
    w('Tec-9 | Bamboozle'),
    w('MP5-SD | Necro Jr.'),
    w('UMP-45 | Momentum'),
    w('Dual Berettas | Melondrama'),
    w('PP-Bizon | Space Cat'),
    # 나이프 (프랙처 = Shattered Web Knives)
    w('★ Paracord Knife | Doppler',       knife=True),
    w('★ Paracord Knife | Fade',          knife=True),
    w('★ Paracord Knife | Marble Fade',   knife=True),
    w('★ Paracord Knife | Tiger Tooth',   knife=True),
    w('★ Paracord Knife | Case Hardened', knife=True),
    w('★ Survival Knife | Doppler',       knife=True),
    w('★ Survival Knife | Fade',          knife=True),
    w('★ Survival Knife | Marble Fade',   knife=True),
    w('★ Survival Knife | Tiger Tooth',   knife=True),
    w('★ Survival Knife | Case Hardened', knife=True),
    w('★ Nomad Knife | Doppler',          knife=True),
    w('★ Nomad Knife | Fade',             knife=True),
    w('★ Nomad Knife | Marble Fade',      knife=True),
    w('★ Nomad Knife | Case Hardened',    knife=True),
    w('★ Skeleton Knife | Doppler',       knife=True),
    w('★ Skeleton Knife | Fade',          knife=True),
    w('★ Skeleton Knife | Marble Fade',   knife=True),
    w('★ Skeleton Knife | Case Hardened', knife=True),

    # ── 드림즈 & 나이트메어 ──────────────────────
    w('MP9 | Starlight Protector'),
    w('AK-47 | Nightwish'),
    w('MP7 | Abyssal Apparition'),
    w('Dual Berettas | Melondrama'),
    w('FAMAS | Rapid Eye Movement'),
    w('Five-SeveN | Scrawl'),
    w('USP-S | Ticket to Hell'),
    w('Glock-18 | Night Terror'),
    w('PP-Bizon | Space Cat'),
    w('M4A1-S | Night Lotus'),
    w('Nova | Night Spirit'),
    w('MAC-10 | Ensnared'),
    w('MP5-SD | Necro Jr.'),
    w('XM1014 | Zombie Offensive'),
    w('P250 | Visions'),
    w('Tec-9 | Decimator'),
    w('G3SG1 | Dream Glade'),
    # 나이프 (드림즈 = Gamma Knives)
    w('★ Falchion Knife | Doppler',       knife=True),
    w('★ Falchion Knife | Gamma Doppler', knife=True),
    w('★ Falchion Knife | Fade',          knife=True),
    w('★ Falchion Knife | Marble Fade',   knife=True),
    w('★ Falchion Knife | Tiger Tooth',   knife=True),
    w('★ Falchion Knife | Case Hardened', knife=True),
    w('★ Bowie Knife | Doppler',          knife=True),
    w('★ Bowie Knife | Gamma Doppler',    knife=True),
    w('★ Bowie Knife | Fade',             knife=True),
    w('★ Bowie Knife | Marble Fade',      knife=True),
    w('★ Bowie Knife | Tiger Tooth',      knife=True),
    w('★ Bowie Knife | Case Hardened',    knife=True),
]


def load_previous_prices():
    try:
        with open('prices.json', 'r', encoding='utf-8') as f:
            return json.load(f).get('prices', {})
    except Exception:
        return {}


def fetch_price(name, wear):
    """
    반환값:
      int  → 가격 (달러 센트)
      None → rate limit / 네트워크 오류 (재시도 필요)
      0    → 매물 없음 (재시도 불필요)
    """
    query   = name if wear is None else f'{name} ({wear})'
    encoded = urllib.parse.quote(query)
    url     = f'{CF_BASE}/listings?market_hash_name={encoded}&limit=10&sort_by=lowest_price&category=0'
    req     = urllib.request.Request(url, headers={'Authorization': API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            status = r.status
            data   = json.loads(r.read())

        # 매물 없음 → 즉시 0 반환 (재시도 X)
        if not data.get('data'):
            return 0

        listed = [l for l in data['data'] if l.get('type') == 'buy_now']
        src    = listed if listed else data['data']
        ref    = src[0].get('reference', {})
        price  = ref.get('base_price') or src[0].get('price', 0)
        return price if price > 0 else 0

    except urllib.error.HTTPError as e:
        # 429 rate limit → None (재시도)
        if e.code == 429:
            print(f'    → rate limit (429)')
            return None
        # 404 등 → 매물 없음으로 처리
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

        # 매물 없음 → 즉시 스킵
        if result == 0:
            return 0

        # 성공
        if result is not None and result > 0:
            return result

        # None = rate limit / 오류 → 재시도
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

    # 요청 목록 펼치기: (name, wear) 쌍으로 변환
    requests = []
    for item in ITEMS:
        name, wears = item
        for wear in wears:
            requests.append((name, wear))

    total = len(requests)
    print(f'총 {total}개 요청 시작\n')

    for i, (name, wear) in enumerate(requests):
        key   = f'{name}|{wear or ""}'
        query = name if wear is None else f'{name} ({wear})'
        print(f'[{i+1}/{total}] {query}')

        result = fetch_with_retry(name, wear)

        if result is None:
            # 최종 실패 → 이전 값 유지 or 0
            prev_val = prev.get(key)
            if prev_val:
                prices[key] = prev_val
                print(f'  ⚠ 이전 값 유지: ${prev_val/100:.2f}')
            else:
                prices[key] = 0
                failed.append(key)
                print(f'  ✗ 이전 값 없음 → 0')
        elif result == 0:
            # 매물 없음
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
