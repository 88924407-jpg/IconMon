import random
import streamlit as st
import emoji

# Page Configuration
st.set_page_config(
    page_title="Ultimate Emoji Dex & Battle RPG",
    page_icon="📖",
    layout="wide"
)

# Custom CSS for Pokedex Tiling and Battle UI
st.markdown("""
    <style>
    .dex-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
        gap: 12px;
        margin-bottom: 20px;
    }
    .dex-card {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        cursor: pointer;
    }
    .dex-card-locked {
        background-color: #e9ecef;
        border: 2px dashed #ced4da;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        filter: blur(5px);
        opacity: 0.4;
        user-select: none;
    }
    .emoji-icon {
        font-size: 2.5rem;
        margin-bottom: 5px;
    }
    .badge-common { background-color: #adb5bd; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; }
    .badge-uncommon { background-color: #40c057; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; }
    .badge-rare { background-color: #228be6; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; }
    .badge-srare { background-color: #7950f2; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; }
    .badge-svrare { background-color: #f59f00; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75rem; }
    .battle-arena {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 16px;
        padding: 20px;
        border: 2px solid #dee2e6;
    }
    .evolution-chain-box {
        background-color: #ffffff;
        border: 1px solid #ced4da;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "collection" not in st.session_state:
    st.session_state.collection = []
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "evolution_stones" not in st.session_state:
    st.session_state.evolution_stones = {
        "🔥 Fire Stone": 2,
        "💧 Water Stone": 2,
        "⚡ Thunder Stone": 2,
        "🌿 Leaf Stone": 2,
        "🌙 Moon Stone": 2
    }
if "battle_state" not in st.session_state:
    st.session_state.battle_state = None
if "selected_dex_expansion" not in st.session_state:
    st.session_state.selected_dex_expansion = None

def add_xp(amount):
    st.session_state.xp += amount
    st.session_state.level = 1 + (st.session_state.xp // 100)

# Generate Dynamic Database with Strict Category Validation
@st.cache_resource
def load_full_emoji_dex():
    dex = {
        "Smileys & Emotion": [],
        "People & Body": [],
        "Animals & Nature": [],
        "Food & Drink": [],
        "Travel & Places": [],
        "Activities": [],
        "Objects": [],
        "Symbols": [],
        "Flags": []
    }
    
    cat_keys = list(dex.keys())
    
    for code, data in emoji.EMOJI_DATA.items():
        c_lower = code.lower()
        
        if any(k in c_lower for k in ["face", "smile", "laugh", "cry", "grin", "wink", "kiss", "heart", "emotion", "cat", "monkey", "devil", "angry", "sad", "fear", "ghost", "skull"]):
            category = "Smileys & Emotion"
        elif any(k in c_lower for k in ["man", "woman", "boy", "girl", "baby", "person", "people", "hand", "finger", "arm", "leg", "ear", "eye", "nose", "hair", "body", "bust", "family", "couple", "police", "guard", "construction", "prince", "princess"]):
            category = "People & Body"
        elif any(k in c_lower for k in ["dog", "cat", "mouse", "hamster", "rabbit", "fox", "bear", "panda", "koala", "tiger", "lion", "cow", "pig", "frog", "monkey", "bird", "chick", "penguin", "duck", "eagle", "owl", "bat", "wolf", "boar", "horse", "unicorn", "bee", "bug", "snail", "ant", "spider", "scorpion", "crab", "snake", "lizard", "turtle", "octopus", "fish", "whale", "dolphin", "seal", "bouquet", "flower", "rose", "hibiscus", "sunflower", "tulip", "seedling", "plant", "tree", "cactus", "rice", "herb", "shamrock", "clover", "leaf"]):
            category = "Animals & Nature"
        elif any(k in c_lower for k in ["fruit", "melon", "apple", "banana", "pineapple", "mango", "pear", "peach", "cherries", "strawberry", "blueberry", "kiwi", "tomato", "coconut", "avocado", "eggplant", "potato", "carrot", "corn", "pepper", "cucumber", "broccoli", "garlic", "onion", "mushroom", "bread", "croissant", "bagel", "pretzel", "pancake", "waffle", "cheese", "meat", "bacon", "burger", "fries", "pizza", "hot_dog", "sandwich", "taco", "burrito", "egg", "cooking", "salad", "popcorn", "rice", "curry", "sushi", "ice_cream", "cake", "cookie", "chocolate", "candy", "bottle", "milk", "coffee", "tea", "sake", "wine", "beer", "drink", "cup", "fork", "spoon", "knife"]):
            category = "Food & Drink"
        elif any(k in c_lower for k in ["globe", "map", "compass", "mountain", "volcano", "camping", "beach", "desert", "island", "city", "bridge", "train", "metro", "bus", "ambulance", "fire_engine", "police_car", "taxi", "car", "truck", "tractor", "bike", "scooter", "ship", "boat", "airplane", "rocket", "hotel", "house", "building", "office", "hospital", "bank", "school", "factory", "castle"]):
            category = "Travel & Places"
        elif any(k in c_lower for k in ["sport", "soccer", "basketball", "football", "baseball", "tennis", "volleyball", "rugby", "golf", "surfing", "swimming", "skate", "fishing", "trophy", "medal", "ticket", "game", "toy", "puzzle", "chess", "card", "art", "palette"]):
            category = "Activities"
        elif any(k in c_lower for k in ["computer", "laptop", "phone", "keyboard", "mouse", "camera", "tv", "radio", "clock", "watch", "lamp", "bulb", "book", "pencil", "pen", "paper", "folder", "lock", "key", "hammer", "wrench", "toolbox", "magnet", "bomb", "knife", "pill", "syringe", "soap", "sponge", "bed", "chair", "gift", "balloon"]):
            category = "Objects"
        elif any(k in c_lower for k in ["flag", "banner"]):
            category = "Flags"
        else:
            hash_val = sum(ord(char) for char in code)
            category = cat_keys[hash_val % len(cat_keys)]

        item_id = code.replace(":", "").replace("_", "-")
        dex[category].append({
            "id": item_id,
            "name": code.replace("_", " ").title(),
            "icon": code,
            "category": category
        })
    
    for cat in dex:
        dex[cat] = sorted(dex[cat], key=lambda x: x["name"])
        
    return dex

MASTER_EMOJI_DEX = load_full_emoji_dex()

STRICT_LOGICAL_EVOLUTION_FAMILIES = {
    "grinning_face": ["grinning_face_with_big_eyes", "grinning_squinting_face", "rofl"],
    "smiling_face_with_smiling_eyes": ["smiling_face_with_heart_eyes", "star_struck", "exploding_head"],
    "slightly_smiling_face": ["smiling_face", "grinning_face", "grinning_face_with_smiling_eyes"],
    "pensive_face": ["sad_but_relieved_face", "crying_face", "loudly_crying_face"],
    "pouting_face": ["angry_face", "face_with_symbols_on_mouth", "enraged_face"],
    "dog_face": ["poodle", "wolf", "fox"],
    "cat_face": ["grinning_cat", "cat_with_wry_smile", "black_cat"],
    "mouse_face": ["hamster", "rabbit_face", "chipmunk"],
    "seedling": ["herb", "potted_plant", "deciduous_tree"],
    "green_apple": ["red_apple", "pear", "tangerine"],
    "banana": ["pineapple", "mango", "melon"],
    "hamburger": ["pizza", "hot_dog", "burrito"],
    "hot_beverage": ["teacup_without_handle", "bubble_tea", "tumbler_glass"],
    "automobile": ["sports_car", "racing_car", "police_car"],
    "house": ["house_with_garden", "office_building", "castle"],
    "airplane": ["rocket", "helicopter", "flying_saucer"]
}

def get_logical_evolution(current_code, category):
    if current_code in STRICT_LOGICAL_EVOLUTION_FAMILIES:
        family_codes = STRICT_LOGICAL_EVOLUTION_FAMILIES[current_code]
        candidates = [c for c in family_codes if c != current_code and c in emoji.EMOJI_DATA]
        if candidates:
            chosen_code = random.choice(candidates)
            return chosen_code, chosen_code.replace("_", " ").title()
            
    pool = MASTER_EMOJI_DEX.get(category, [])
    candidates = [item for item in pool if item["icon"] != current_code]
    if not candidates:
        candidates = pool
    chosen = random.choice(candidates)
    return chosen["icon"], chosen["name"]

HABITAT_REQUIREMENTS = {
    "Smileys & Emotion": {"required_unique": 0, "required_level": 1},
    "Animals & Nature": {"required_unique": 2, "required_level": 3},
    "Food & Drink": {"required_unique": 4, "required_level": 5},
    "People & Body": {"required_unique": 6, "required_level": 7},
    "Activities": {"required_unique": 8, "required_level": 9},
    "Travel & Places": {"required_unique": 10, "required_level": 11},
    "Objects": {"required_unique": 12, "required_level": 12},
    "Symbols": {"required_unique": 14, "required_level": 14},
    "Flags": {"required_unique": 16, "required_level": 15}
}

# UI Header
st.title("📖 Ultimate Emoji Dex & Battle RPG")
st.write("Catch wild emojis, battle rival AI emojis, level up your team, and explore the complete Pokedex sorted by types and evolution lines!")

# Sidebar Navigation
st.sidebar.title("🎮 Dashboard")
st.sidebar.markdown(f"**Trainer Level:** {st.session_state.level} (XP: {st.session_state.xp})")
menu = st.sidebar.radio("Navigation", ["Explore & Catch", "⚔️ Battle Arena", "Active Inventory & Evolutions", "📚 Emoji Dex Tiled Grid", "🛠️ Admin Panel"])

def is_habitat_unlocked(habitat_name):
    reqs = HABITAT_REQUIREMENTS.get(habitat_name, {"required_unique": 0, "required_level": 1})
    unique_count = len({item["raw_icon"] for item in st.session_state.collection})
    return unique_count >= reqs["required_unique"] and st.session_state.level >= reqs["required_level"]

if menu == "Explore & Catch":
    st.subheader("🌲 Wild Ecosystem Habitats")
    st.write("Select an unlocked ecosystem environment to hunt for companions. Catching emojis grants XP based on their rarity tier!")

    habitat_options = []
    habitat_mapping = {}
    
    for hab in MASTER_EMOJI_DEX.keys():
        unlocked = is_habitat_unlocked(hab)
        req = HABITAT_REQUIREMENTS[hab]
        if unlocked:
            label = hab
        else:
            label = f"🔒 {hab} (Req: {req['required_unique']} Unique | Lvl {req['required_level']})"
        
        habitat_options.append(label)
        habitat_mapping[label] = hab

    selected_display = st.selectbox("Choose Habitat Ecosystem:", habitat_options)
    actual_habitat = habitat_mapping[selected_display]
    is_allowed = is_habitat_unlocked(actual_habitat)

    if is_allowed:
        if st.button("✨ Catch Wild Emoji", type="primary", use_container_width=True):
            available_pool = MASTER_EMOJI_DEX.get(actual_habitat, [])
            if available_pool:
                base_item = random.choice(available_pool).copy()
                rendered_icon = emoji.emojize(base_item["icon"])
                
                rarity_roll = random.randint(1, 100)
                if rarity_roll <= 20:
                    tier = "COMMON"
                    badge_class = "badge-common"
                    xp_gain = 15
                elif rarity_roll <= 40:
                    tier = "UNCOMMON"
                    badge_class = "badge-uncommon"
                    xp_gain = 35
                elif rarity_roll <= 60:
                    tier = "RARE"
                    badge_class = "badge-rare"
                    xp_gain = 70
                elif rarity_roll <= 80:
                    tier = "S-RARE"
                    badge_class = "badge-srare"
                    xp_gain = 120
                else:
                    tier = "SV-RARE"
                    badge_class = "badge-svrare"
                    xp_gain = 250

                caught_item = {
                    "instance_id": random.randint(10000, 99999),
                    "dex_id": base_item["id"],
                    "name": base_item["name"],
                    "raw_icon": base_item["icon"],
                    "icon": rendered_icon,
                    "stage": 1,
                    "level": random.randint(1, 21),
                    "hp": 100,
                    "max_hp": 100,
                    "tier": tier,
                    "badge_class": badge_class,
                    "category": actual_habitat
                }
                
                st.session_state.collection.append(caught_item)
                add_xp(xp_gain)
                
                st.balloons()
                st.success(f"Caught **{caught_item['name']}** ({caught_item['icon']})! Tier: **{tier}** (+{xp_gain} XP)")
                st.rerun()
            else:
                st.warning("No emojis found in this habitat yet.")
    else:
        st.warning("🔒 This habitat is locked! Catch more unique icons or level up your Trainer rank to unlock it.")

    st.divider()
    st.metric("Trainer Progression", f"Level {st.session_state.level}", delta=f"{st.session_state.xp} Total XP | {len({i['raw_icon'] for i in st.session_state.collection})} Unique Caught")

elif menu == "⚔️ Battle Arena":
    st.subheader("⚔️ Emoji Turn-Based Battle Arena")
    st.write("Send your caught companion into battle against a wild AI emoji opponent! Win battles to earn XP, level up, and win evolutionary stones.")

    if not st.session_state.collection:
        st.warning("You need at least one companion in your inventory to enter the battle arena! Visit **Explore & Catch** first.")
    else:
        fighter_options = {f"{item['icon']} {item['name']} (Lvl {item['level']})": item for item in st.session_state.collection}
        selected_fighter_label = st.selectbox("Choose Your Fighter:", list(fighter_options.keys()))
        my_fighter = fighter_options[selected_fighter_label]

        if st.session_state.battle_state is None:
            if st.button("🚀 Start New Battle Match", type="primary", use_container_width=True):
                all_cats = list(MASTER_EMOJI_DEX.keys())
                ai_cat = random.choice(all_cats)
                ai_pool = MASTER_EMOJI_DEX[ai_cat]
                ai_base = random.choice(ai_pool)
                
                st.session_state.battle_state = {
                    "my_fighter": my_fighter,
                    "my_hp": my_fighter["max_hp"],
                    "ai_name": ai_base["name"],
                    "ai_icon": emoji.emojize(ai_base["icon"]),
                    "ai_hp": 80 + (my_fighter["level"] * 3),
                    "ai_max_hp": 80 + (my_fighter["level"] * 3),
                    "log": f"Battle started between {my_fighter['icon']} {my_fighter['name']} and wild {emoji.emojize(ai_base['icon'])} {ai_base['name']}!"
                }
                st.rerun()

        if st.session_state.battle_state is not None:
            b = st.session_state.battle_state
            
            st.markdown('<div class="battle-arena">', unsafe_allow_html=True)
            col_p, col_vs, col_a = st.columns([2, 1, 2])
            
            with col_p:
                st.markdown(f"### {b['my_fighter']['icon']} {b['my_fighter']['name']}")
                st.write(f"Level: {b['my_fighter']['level']}")
                st.progress(max(0, min(100, int((b['my_hp'] / b['my_fighter']['max_hp']) * 100))))
                st.caption(f"HP: {b['my_hp']} / {b['my_fighter']['max_hp']}")
                
            with col_vs:
                st.markdown("<h2 style='text-align: center; padding-top: 15px;'>VS</h2>", unsafe_allow_html=True)
                
            with col_a:
                st.markdown(f"### {b['ai_icon']} {b['ai_name']}")
                st.write(f"AI Opponent")
                st.progress(max(0, min(100, int((b['ai_hp'] / b['ai_max_hp']) * 100))))
                st.caption(f"HP: {b['ai_hp']} / {b['ai_max_hp']}")
            
            st.markdown('</div>')
            st.info(b["log"])
            
            col_act1, col_act2, col_act3 = st.columns(3)
            with col_act1:
                if st.button("⚔️ Quick Attack", use_container_width=True):
                    dmg_to_ai = random.randint(15, 25) + (b['my_fighter']['level'] * 2)
                    b['ai_hp'] = max(0, b['ai_hp'] - dmg_to_ai)
                    log_text = f"You used Quick Attack for {dmg_to_ai} damage!"
                    
                    if b['ai_hp'] > 0:
                        dmg_to_me = random.randint(10, 20)
                        b['my_hp'] = max(0, b['my_hp'] - dmg_to_me)
                        log_text += f" Opponent counter-attacked for {dmg_to_me} damage!"
                    
                    b['log'] = log_text
                    
                    if b['ai_hp'] <= 0:
                        reward_xp = 50
                        add_xp(reward_xp)
                        b['my_fighter']['level'] += 1
                        stone_reward = random.choice(list(st.session_state.evolution_stones.keys()))
                        st.session_state.evolution_stones[stone_reward] += 1
                        st.success(f"🎉 Victory! You won the battle! (+{reward_xp} XP, Fighter Level Up, +1 {stone_reward})")
                        st.session_state.battle_state = None
                    st.rerun()
                    
            with col_act2:
                if st.button("💥 Heavy Smash", use_container_width=True):
                    if random.random() > 0.35:
                        dmg_to_ai = random.randint(30, 45) + (b['my_fighter']['level'] * 3)
                        b['ai_hp'] = max(0, b['ai_hp'] - dmg_to_ai)
                        b['log'] = f"Heavy Smash hit successfully for {dmg_to_ai} damage!"
                    else:
                        b['log'] = "Heavy Smash missed its target!"
                        
                    if b['ai_hp'] > 0:
                        dmg_to_me = random.randint(12, 22)
                        b['my_hp'] = max(0, b['my_hp'] - dmg_to_me)
                        b['log'] += f" Opponent struck back for {dmg_to_me} damage!"
                        
                    if b['ai_hp'] <= 0:
                        reward_xp = 50
                        add_xp(reward_xp)
                        b['my_fighter']['level'] += 1
                        stone_reward = random.choice(list(st.session_state.evolution_stones.keys()))
                        st.session_state.evolution_stones[stone_reward] += 1
                        st.success(f"🎉 Victory! You won the battle! (+{reward_xp} XP, Fighter Level Up, +1 {stone_reward})")
                        st.session_state.battle_state = None
                    st.rerun()

            with col_act3:
                if st.button("🏳️ Flee Battle", use_container_width=True):
                    st.session_state.battle_state = None
                    st.warning("You fled from the battle arena.")
                    st.rerun()

elif menu == "📚 Emoji Dex Tiled Grid":
    st.subheader("🗺️ Master Sorted Tiled Pokedex Grid")
    st.write("Browse all available companion entries. Unlocked icons will light up in color; uncaptured ones appear as locked mystery silhouettes.")

    col_search, col_jump, col_mode = st.columns([2, 1, 1])
    with col_search:
        search_query = st.text_input("🔍 Search Emoji Dex by Name:", "").strip().lower()
    with col_jump:
        category_list = list(MASTER_EMOJI_DEX.keys())
        jump_category = st.selectbox("📂 Skip to Category:", ["All Categories"] + category_list)
    with col_mode:
        compact_mode = st.toggle("Compact View (Click to Expand)", value=True)

    st.write("**🔤 Letter-by-Letter Index:**")
    alphabet = ["All"] + [chr(i) for i in range(ord('A'), ord('Z')+1)]
    
    if "selected_letter" not in st.session_state:
        st.session_state.selected_letter = "All"

    let_cols = st.columns(14)
    for idx, letter in enumerate(alphabet):
        with let_cols[idx % 14]:
            if st.button(letter, key=f"btn_let_{letter}", use_container_width=True):
                st.session_state.selected_letter = letter

    st.caption(f"Active Letter Filter: **{st.session_state.selected_letter}**")
    st.divider()

    # If an expansion card is selected, show its evolution chain popup info box
    if st.session_state.selected_dex_expansion:
        exp_item = st.session_state.selected_dex_expansion
        st.markdown(f"### 🧬 Evolution Line Inspection: {exp_item['name']}")
        
        # Build 3-stage chain for this specific item
        chain = [exp_item]
        curr_code = exp_item["icon"]
        for _ in range(2):
            nxt_code, nxt_name = get_logical_evolution(curr_code, exp_item["category"])
            if nxt_code and nxt_code != curr_code:
                chain.append({"icon": nxt_code, "name": nxt_name, "category": exp_item["category"]})
                curr_code = nxt_code
            else:
                break
        
        chain_box_html = '<div class="evolution-chain-box">'
        for idx, ch in enumerate(chain):
            ico = emoji.emojize(ch["icon"])
            chain_box_html += f'<span style="font-size: 1.8rem;">{ico}</span> <b>{ch["name"]}</b>'
            if idx < len(chain) - 1:
                chain_box_html += ' ➔ '
        chain_box_html += '</div>'
        st.markdown(chain_box_html, unsafe_allow_html=True)
        
        if st.button("❌ Close Inspection View"):
            st.session_state.selected_dex_expansion = None
            st.rerun()
        st.divider()

    unlocked_icons = {item["raw_icon"] for item in st.session_state.collection}
    categories_to_show = [jump_category] if jump_category != "All Categories" else category_list

    for category in categories_to_show:
        base_list = MASTER_EMOJI_DEX.get(category, [])
        if not base_list:
            continue
            
        filtered_list = []
        for item in base_list:
            name_lower = item["name"].lower()
            if search_query and search_query not in name_lower:
                continue
            if st.session_state.selected_letter != "All":
                if not name_lower.startswith(st.session_state.selected_letter.lower()):
                    continue
            filtered_list.append(item)

        if not filtered_list and (search_query or st.session_state.selected_letter != "All"):
            continue

        unlocked_status = is_habitat_unlocked(category)
        header_label = f"🏷️ {category}" if unlocked_status else f"🔒 {category} (Locked Habitat)"
        st.markdown(f"### {header_label}")
        
        items_to_render = filtered_list if (search_query or st.session_state.selected_letter != "All") else base_list
        
        if compact_mode:
            # Render as individual clickable buttons acting as grid cards
            cols = st.columns(8)
            for idx, base_item in enumerate(items_to_render):
                rendered_icon = emoji.emojize(base_item["icon"])
                is_unlocked = base_item["icon"] in unlocked_icons
                
                with cols[idx % 8]:
                    btn_label = f"{rendered_icon}\n{base_item['name']}" if is_unlocked else f"❓\n???"
                    if st.button(btn_label, key=f"dex_tile_{base_item['id']}", use_container_width=True):
                        st.session_state.selected_dex_expansion = base_item
                        st.rerun()
        else:
            grid_html = '<div class="dex-grid">'
            for base_item in items_to_render:
                rendered_icon = emoji.emojize(base_item["icon"])
                is_unlocked = base_item["icon"] in unlocked_icons
                
                if is_unlocked:
                    grid_html += f'<div class="dex-card"><div class="emoji-icon">{rendered_icon}</div><small><b>{base_item["name"]}</b></small></div>'
                else:
                    grid_html += f'<div class="dex-card-locked"><div class="emoji-icon">❓</div><small><b>???</b></small></div>'
            grid_html += '</div>'
            st.markdown(grid_html, unsafe_allow_html=True)

elif menu == "Active Inventory & Evolutions":
    st.subheader("🎒 Captured Inventory & Evolution Laboratory")
    st.write("Manage your companions, level them up through battles, evolve Stage 1/2 companions into logically related variants within the same category, or apply evolutionary stones!")

    st.markdown("### 💎 Evolutionary Stones Pouch")
    stone_cols = st.columns(5)
    stone_keys = list(st.session_state.evolution_stones.keys())
    for idx, stone in enumerate(stone_keys):
        with stone_cols[idx]:
            st.metric(stone, st.session_state.evolution_stones[stone])

    st.divider()

    if not st.session_state.collection:
        st.info("Your bag is empty! Go to **Explore & Catch** to find companions.")
    else:
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            filter_cat = st.selectbox("Filter Category:", ["All"] + list(MASTER_EMOJI_DEX.keys()))
        with f_col2:
            sort_opt = st.selectbox("Sort By:", ["Name", "Level"])

        items_to_show = st.session_state.collection
        if filter_cat != "All":
            items_to_show = [i for i in items_to_show if i["category"] == filter_cat]

        if sort_opt == "Name":
            items_to_show = sorted(items_to_show, key=lambda x: x["name"])
        else:
            items_to_show = sorted(items_to_show, key=lambda x: x["level"], reverse=True)

        st.write(f"Showing **{len(items_to_show)}** companions in your collection bag:")
        st.divider()

        for idx, item in enumerate(items_to_show):
            cols = st.columns([1, 3, 2, 2])
            with cols[0]:
                st.markdown(f"### {item['icon']}")
            with cols[1]:
                st.write(f"**{item['name']}** (Stage {item['stage']})")
                st.markdown(f'<span class="{item["badge_class"]}">{item["tier"]}</span> | Level: {item["level"]}', unsafe_allow_html=True)
            with cols[2]:
                st.caption(f"Category: {item['category']}")
            with cols[3]:
                can_level_evolve = (item["stage"] == 1 and item["level"] >= 22) or (item["stage"] == 2 and item["level"] >= 34)
                
                if item["stage"] < 3:
                    if st.button(f"🌀 Evolve Variant", key=f"evo_{item['instance_id']}", disabled=not can_level_evolve):
                        new_raw, new_name = get_logical_evolution(item["raw_icon"], item["category"])
                        item["stage"] += 1
                        item["raw_icon"] = new_raw
                        item["icon"] = emoji.emojize(new_raw)
                        item["name"] = new_name
                        st.balloons()
                        st.success(f"Evolved into related variant **{new_name}** ({item['icon']})!")
                        st.rerun()
                        
                    selected_stone = st.selectbox("Stone:", list(st.session_state.evolution_stones.keys()), key=f"stone_sel_{item['instance_id']}")
                    if st.button(f"✨ Stone Evolve", key=f"stone_btn_{item['instance_id']}"):
                        if st.session_state.evolution_stones[selected_stone] > 0:
                            st.session_state.evolution_stones[selected_stone] -= 1
                            new_raw, new_name = get_logical_evolution(item["raw_icon"], item["category"])
                            item["stage"] = min(3, item["stage"] + 1)
                            item["raw_icon"] = new_raw
                            item["icon"] = emoji.emojize(new_raw)
                            item["name"] = f"Aura {new_name}"
                            st.balloons()
                            st.success(f"Stone mutation successful! Mutated into **{item['name']}** ({item['icon']})!")
                            st.rerun()
                        else:
                            st.warning("Not enough stones of this type!")
                else:
                    st.caption("Max Evolution Stage Reached")
            st.divider()

        if st.button("🗑️ Clear Entire Inventory"):
            st.session_state.collection = []
            st.session_state.xp = 0
            st.session_state.level = 1
            st.rerun()

elif menu == "🛠️ Admin Panel":
    st.subheader("🛠️ Developer & Admin Control Panel")
    st.write("Customize your Trainer stats, inject any custom emoji companion directly into your inventory with custom levels, or unlock specific icons/habitats instantly!")

    tab1, tab2, tab3 = st.tabs(["🎁 Spawn Custom Icon", "🔓 Unlock Selected Icons", "⚡ Trainer & Bulk Options"])

    with tab1:
        st.markdown("### Spawn Custom Emoji Companion")
        admin_cat = st.selectbox("Select Category for Spawn:", list(MASTER_EMOJI_DEX.keys()))
        cat_items = MASTER_EMOJI_DEX[admin_cat]
        item_choices = {f"{emoji.emojize(i['icon'])} {i['name']}": i for i in cat_items}
        
        selected_spawn_label = st.selectbox("Choose Emoji:", list(item_choices.keys()))
        chosen_base = item_choices[selected_spawn_label]
        
        spawn_level = st.slider("Set Companion Level:", 1, 100, 25)
        spawn_tier = st.selectbox("Set Rarity Tier:", ["COMMON", "UNCOMMON", "RARE", "S-RARE", "SV-RARE"])
        
        badge_map = {
            "COMMON": "badge-common",
            "UNCOMMON": "badge-uncommon",
            "RARE": "badge-rare",
            "S-RARE": "badge-srare",
            "SV-RARE": "badge-svrare"
        }

        if st.button("📥 Add Companion to Inventory", type="primary"):
            spawned_item = {
                "instance_id": random.randint(10000, 99999),
                "dex_id": chosen_base["id"],
                "name": chosen_base["name"],
                "raw_icon": chosen_base["icon"],
                "icon": emoji.emojize(chosen_base["icon"]),
                "stage": 1,
                "level": spawn_level,
                "hp": 100 + (spawn_level * 5),
                "max_hp": 100 + (spawn_level * 5),
                "tier": spawn_tier,
                "badge_class": badge_map[spawn_tier],
                "category": admin_cat
            }
            st.session_state.collection.append(spawned_item)
            st.success(f"Successfully spawned **{spawned_item['name']}** ({spawned_item['icon']}) at Level {spawn_level}!")

    with tab2:
        st.markdown("### Unlock Specific Icons in Dex")
        unlock_cat = st.selectbox("Browse Category to Unlock:", list(MASTER_EMOJI_DEX.keys()), key="unlock_cat_sel")
        cat_dex_items = MASTER_EMOJI_DEX[unlock_cat]
        
        selected_to_unlock = st.multiselect("Select Emojis to Instant Unlock:", [f"{emoji.emojize(i['icon'])} {i['name']}" for i in cat_dex_items])
        
        if st.button("🔓 Unlock Selected Emojis"):
            unlocked_names = [s.split(" ")[1] for s in selected_to_unlock]
            for item in cat_dex_items:
                if item["name"] in unlocked_names:
                    already_exists = any(c["raw_icon"] == item["icon"] for c in st.session_state.collection)
                    if not already_exists:
                        forced_item = {
                            "instance_id": random.randint(10000, 99999),
                            "dex_id": item["id"],
                            "name": item["name"],
                            "raw_icon": item["icon"],
                            "icon": emoji.emojize(item["icon"]),
                            "stage": 1,
                            "level": 10,
                            "hp": 120,
                            "max_hp": 120,
                            "tier": "RARE",
                            "badge_class": "badge-rare",
                            "category": unlock_cat
                        }
                        st.session_state.collection.append(forced_item)
            st.success("Selected emojis have been unlocked and added to your collection bag!")

    with tab3:
        st.markdown("### Trainer & Bulk Management")
        new_trainer_level = st.slider("Override Trainer Level:", 1, 50, st.session_state.level)
        if st.button("Update Trainer Rank"):
            st.session_state.level = new_trainer_level
            st.success(f"Trainer level updated to Level {new_trainer_level}!")

        if st.button("🚀 UNLOCK ALL EMOJIS IN DEX", type="primary", use_container_width=True):
            current_raw_collected = {c["raw_icon"] for c in st.session_state.collection}
            for cat_name, cat_items in MASTER_EMOJI_DEX.items():
                for item in cat_items:
                    if item["icon"] not in current_raw_collected:
                        all_unlocked_item = {
                            "instance_id": random.randint(10000, 99999),
                            "dex_id": item["id"],
                            "name": item["name"],
                            "raw_icon": item["icon"],
                            "icon": emoji.emojize(item["icon"]),
                            "stage": 1,
                            "level": 15,
                            "hp": 150,
                            "max_hp": 150,
                            "tier": "S-RARE",
                            "badge_class": "badge-srare",
                            "category": cat_name
                        }
                        st.session_state.collection.append(all_unlocked_item)
            st.balloons()
            st.success("🎉 Master Dex Unlocked! All indexed emojis have been added to your collection bag!")

        if st.button("🎁 Add +5 Evolution Stones to Pouch"):
            for stone in st.session_state.evolution_stones:
                st.session_state.evolution_stones[stone] += 5
            st.success("Successfully added +5 of each evolution stone to your pouch!")