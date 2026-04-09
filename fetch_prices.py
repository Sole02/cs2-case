import os
import json
import time
import urllib.request
import urllib.parse

API_KEY = os.environ.get('CSFLOAT_API_KEY', '')
CF_BASE = 'https://csfloat.com/api/v1'

# 가져올 아이템 목록 (market_hash_name, wear)
# wear가 None이면 마모도 없는 아이템 (케이스, 열쇠 등)
ITEMS = [
    # 케이스 / 열쇠
    ('Revolution Case', None),
    ('Recoil Case', None),
    ('Fracture Case', None),
    ('Dreams & Nightmares Case', None),
    ('CS2 Case Key', None),

    # 혁명 케이스 스킨
    ('AK-47 | Head Shot', 'Field-Tested'),
    ('M4A4 | Temukau', 'Field-Tested'),
    ('AWP | Duality', 'Field-Tested'),
    ('P2000 | Wicked Sick', 'Field-Tested'),
    ('UMP-45 | Wild Child', 'Field-Tested'),
    ('MAC-10 | Sakkaku', 'Field-Tested'),
    ('MP9 | Starship', 'Field-Tested'),
    ('SG 553 | Duality', 'Field-Tested'),
    ('Nova | Sobex', 'Field-Tested'),
    ('Five-SeveN | Scrawl', 'Field-Tested'),
    ('AK-47 | Leet Museo', 'Field-Tested'),
    ('MP5-SD | Liquidation', 'Field-Tested'),
    ('Glock-18 | Vogue', 'Field-Tested'),
    ('AUG | Impound', 'Field-Tested'),
    ('Desert Eagle | Blue Ply', 'Field-Tested'),
    ('FAMAS | Meow 36', 'Field-Tested'),
    ('M4A1-S | Emphorosaur-S', 'Field-Tested'),

    # 혁명 케이스 글러브
    ('★ Sport Gloves | Vice', 'Field-Tested'),
    ('★ Sport Gloves | Amphibious', 'Field-Tested'),
    ('★ Sport Gloves | Omega', 'Field-Tested'),
    ('★ Sport Gloves | Bronze Morph', 'Field-Tested'),
    ('★ Driver Gloves | King Snake', 'Field-Tested'),
    ('★ Driver Gloves | Imperial Plaid', 'Field-Tested'),
    ('★ Driver Gloves | Overtake', 'Field-Tested'),
    ('★ Driver Gloves | Racing Green', 'Field-Tested'),
    ('★ Specialist Gloves | Fade', 'Field-Tested'),
    ('★ Specialist Gloves | Crimson Web', 'Field-Tested'),
    ('★ Specialist Gloves | Mogul', 'Field-Tested'),
    ('★ Specialist Gloves | Buckshot', 'Field-Tested'),
    ('★ Hand Wraps | Cobalt Skulls', 'Field-Tested'),
    ('★ Hand Wraps | Overprint', 'Field-Tested'),
    ('★ Hand Wraps | Arboreal', 'Field-Tested'),
    ('★ Hand Wraps | Duct Tape', 'Field-Tested'),
    ('★ Moto Gloves | POW!', 'Field-Tested'),
    ('★ Moto Gloves | Polygon', 'Field-Tested'),
    ('★ Moto Gloves | Turtle', 'Field-Tested'),
    ('★ Moto Gloves | Transport', 'Field-Tested'),
    ('★ Hydra Gloves | Case Hardened', 'Field-Tested'),
    ('★ Hydra Gloves | Emerald', 'Field-Tested'),
    ('★ Hydra Gloves | Rattler', 'Field-Tested'),
    ('★ Hydra Gloves | Mangrove', 'Field-Tested'),

    # 리코일 케이스 스킨
    ('AK-47 | Vaq Cell', 'Field-Tested'),
    ('Glock-18 | Night', 'Field-Tested'),
    ('AWP | Chrome Cannon', 'Field-Tested'),
    ('M4A4 | Bllaster', 'Field-Tested'),
    ('USP-S | Jawbreaker', 'Field-Tested'),
    ('Desert Eagle | Blue Ply', 'Field-Tested'),
    ('MAC-10 | Aloha', 'Field-Tested'),
    ('Nova | Species', 'Field-Tested'),
    ('MP9 | Hydra', 'Field-Tested'),
    ('P250 | Vino Primo', 'Field-Tested'),
    ('M4A1-S | Purple DDPAT', 'Field-Tested'),
    ('Galil AR | Phoenix Blacklight', 'Field-Tested'),
    ('SG 553 | Lush Ruins', 'Field-Tested'),
    ('AUG | Fleet Flock', 'Field-Tested'),
    ('R8 Revolver | Crazy 8', 'Field-Tested'),
    ('PP-Bizon | Whisper', 'Field-Tested'),
    ('CZ75-Auto | Tacticat', 'Field-Tested'),

    # 리코일 나이프 (대표 스킨만)
    ('★ Stiletto Knife | Doppler', 'Factory New'),
    ('★ Stiletto Knife | Fade', 'Factory New'),
    ('★ Stiletto Knife | Case Hardened', 'Field-Tested'),
    ('★ Navaja Knife | Doppler', 'Factory New'),
    ('★ Navaja Knife | Fade', 'Factory New'),
    ('★ Navaja Knife | Case Hardened', 'Field-Tested'),
    ('★ Survival Knife | Doppler', 'Factory New'),
    ('★ Survival Knife | Case Hardened', 'Field-Tested'),
    ('★ Nomad Knife | Doppler', 'Factory New'),
    ('★ Nomad Knife | Case Hardened', 'Field-Tested'),
    ('★ Skeleton Knife | Doppler', 'Factory New'),
    ('★ Skeleton Knife | Case Hardened', 'Field-Tested'),
    ('★ Talon Knife | Doppler', 'Factory New'),
    ('★ Talon Knife | Case Hardened', 'Field-Tested'),

    # 프랙처 케이스 스킨
    ('AK-47 | Inheritance', 'Field-Tested'),
    ('M4A1-S | Night Lotus', 'Field-Tested'),
    ('Desert Eagle | Printstream', 'Field-Tested'),
    ('MP5-SD | Auto Loader', 'Field-Tested'),
    ('P250 | Shrouded', 'Field-Tested'),
    ('AWP | Atheris', 'Field-Tested'),
    ('SG 553 | Phantom', 'Field-Tested'),
    ('Glock-18 | Snack Attack', 'Field-Tested'),
    ('Five-SeveN | Angry Mob', 'Field-Tested'),
    ('AK-47 | Slate', 'Field-Tested'),
    ('PP-Bizon | Slash', 'Field-Tested'),
    ('R8 Revolver | Memento', 'Field-Tested'),
    ('Nova | Quick Sand', 'Field-Tested'),
    ('MAC-10 | Silver', 'Field-Tested'),
    ('P90 | Facility Negative', 'Field-Tested'),
    ('MP9 | Modest Threat', 'Field-Tested'),
    ('UMP-45 | Digi Camo', 'Field-Tested'),

    # 프랙처 나이프
    ('★ Paracord Knife | Doppler', 'Factory New'),
    ('★ Paracord Knife | Case Hardened', 'Field-Tested'),
    ('★ Classic Knife | Doppler', 'Factory New'),
    ('★ Classic Knife | Case Hardened', 'Field-Tested'),
    ('★ Falchion Knife | Doppler', 'Factory New'),
    ('★ Falchion Knife | Case Hardened', 'Field-Tested'),
    ('★ Bowie Knife | Doppler', 'Factory New'),
    ('★ Bowie Knife | Case Hardened', 'Field-Tested'),
    ('★ Gut Knife | Doppler', 'Factory New'),
    ('★ Gut Knife | Case Hardened', 'Field-Tested'),
    ('★ Flip Knife | Doppler', 'Factory New'),
    ('★ Flip Knife | Case Hardened', 'Field-Tested'),
    ('★ Shadow Daggers | Doppler', 'Factory New'),
    ('★ Shadow Daggers | Case Hardened', 'Field-Tested'),

    # 드림즈 케이스 스킨
    ('AK-47 | Circus Diabolique', 'Field-Tested'),
    ('M4A4 | Spider Lily', 'Field-Tested'),
    ('AWP | Chromatic Aberration', 'Field-Tested'),
    ('MP7 | Abyssal Apparition', 'Field-Tested'),
    ('Glock-18 | Visions', 'Field-Tested'),
    ("MP5-SD | Necro Jr.", 'Field-Tested'),
    ("Nova | Sobek's Bite", 'Field-Tested'),
    ('SG 553 | Kalavela', 'Field-Tested'),
    ("Five-SeveN | Fairy Tale", 'Field-Tested'),
    ('MAC-10 | Ensnared', 'Field-Tested'),
    ('P250 | Visions', 'Field-Tested'),
    ('Galil AR | Akoben', 'Field-Tested'),
    ('UMP-45 | Roadblock', 'Field-Tested'),
    ('FAMAS | Darkwater', 'Field-Tested'),
    ('XM1014 | Zombie Offensive', 'Field-Tested'),
    ('PP-Bizon | Space Cat', 'Field-Tested'),
    ('CZ75-Auto | Emerald Quartz', 'Field-Tested'),

    # 드림즈 나이프
    ('★ Shadow Daggers | Doppler', 'Factory New'),
    ('★ Shadow Daggers | Case Hardened', 'Field-Tested'),
    ('★ Navaja Knife | Doppler', 'Factory New'),
    ('★ Navaja Knife | Case Hardened', 'Field-Tested'),
    ('★ Survival Knife | Case Hardened', 'Field-Tested'),
    ('★ Bowie Knife | Case Hardened', 'Field-Tested'),
    ('★ Gut Knife | Case Hardened', 'Field-Tested'),
]

def fetch_price(name, wear=None):
    """CSFloat API로 가격 조회. 반환값: 달러 센트"""
    query = name if wear is None else f'{name} ({wear})'
    encoded = urllib.parse.quote(query)
    url = f'{CF_BASE}/listings?market_hash_name={encoded}&limit=10&sort_by=lowest_price&category=0'
    req = urllib.request.Request(url, headers={'Authorization': API_KEY})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        if data.get('data'):
            listed = [l for l in data['data'] if l.get('type') == 'buy_now']
            src = listed if listed else data['data']
            ref = src[0].get('reference', {})
            price = ref.get('base_price') or src[0].get('price', 0)
            print(f'  ✓ {query}: ${price/100:.2f}')
            return price
    except Exception as e:
        print(f'  ✗ {query}: {e}')
    return 0

def main():
    prices = {}
    total = len(ITEMS)
    for i, (name, wear) in enumerate(ITEMS):
        key = f'{name}|{wear or ""}'
        print(f'[{i+1}/{total}] {key}')
        price = fetch_price(name, wear)
        prices[key] = price
        time.sleep(0.8)  # rate limit 대응

    with open('prices.json', 'w', encoding='utf-8') as f:
        json.dump({
            'updated_at': __import__('datetime').datetime.utcnow().isoformat() + 'Z',
            'prices': prices
        }, f, ensure_ascii=False, indent=2)
    print(f'\n완료! {len(prices)}개 아이템 가격 저장됨')

if __name__ == '__main__':
    main()
