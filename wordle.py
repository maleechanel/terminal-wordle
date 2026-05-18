#!/usr/bin/env python3
import json
import os
import random
import sys
from pathlib import Path

# ANSI color codes
GREEN  = "\033[42;30m"
YELLOW = "\033[43;30m"
GRAY   = "\033[100;37m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
CLEAR  = "\033[2J\033[H"

WORD_LIST = [
    "about","above","abuse","actor","acute","admit","adopt","adult","after","again",
    "agent","agree","ahead","alarm","album","alert","alien","align","alike","alive",
    "alley","allow","alone","along","aloud","alpha","alter","angel","anger","angle",
    "angry","anime","ankle","annex","apart","apple","apply","arena","argue","arise",
    "armor","aroma","arose","array","arrow","aside","asked","asset","atlas","attic",
    "audio","audit","avoid","awake","award","aware","awful","basic","basin","basis",
    "batch","beach","beard","beast","began","begin","being","below","bench","bible",
    "birth","black","blade","blame","bland","blank","blast","blaze","bleed","bless",
    "blind","block","blood","bloom","blown","board","bonus","booth","bound","boxer",
    "brain","brand","brave","bread","break","breed","brick","bride","brief","bring",
    "broad","broke","brook","brown","brush","buddy","build","built","bunch","burst",
    "buyer","cabin","cable","camel","canal","candy","carry","catch","cause","chain",
    "chair","chaos","chase","cheap","check","cheek","chess","chest","chief","child",
    "choir","chunk","civic","civil","claim","class","clean","clear","click","cliff",
    "climb","cling","clock","clone","close","cloud","coach","coast","cobra","comet",
    "comic","comma","coral","count","court","cover","craft","crane","crash","crazy",
    "cream","creek","crime","crisp","cross","crowd","crown","crush","curve","cycle",
    "daily","dance","datum","debut","decay","delay","delta","dense","depot","depth",
    "derby","devil","digit","dirty","disco","ditch","diver","dizzy","dodge","doing",
    "donor","doubt","dough","draft","drain","drama","drank","dread","dream","dress",
    "drink","drive","drone","drove","drown","drugs","drums","dryer","dunno","dwarf",
    "eagle","early","earth","eaten","eight","elite","email","empty","ended","enemy",
    "enjoy","enter","entry","equal","error","event","every","exact","exist","extra",
    "fable","faint","faith","false","fancy","fatal","fault","feast","fence","fever",
    "field","fifth","fifty","fight","final","first","fixed","flame","flash","fleet",
    "flesh","float","flood","floor","flour","fluid","flute","focus","force","forge",
    "forth","found","frame","frank","freed","fresh","front","frost","froze","fruit",
    "fully","funny","ghost","given","gland","glass","globe","gloom","glove","going",
    "grace","grade","grain","grand","grant","grasp","grass","grave","great","greed",
    "green","greet","grief","grill","grind","groan","groin","gross","group","grown",
    "guard","guide","guilt","gusto","happy","harsh","haven","heart","heavy","hence",
    "hinge","hiked","hippo","hoist","holly","homer","honey","honor","hotel","house",
    "human","humor","hurry","ideal","image","imply","inbox","index","indie","infer",
    "inner","input","issue","ivory","japan","jelly","jewel","joint","joker","joust",
    "judge","juice","juicy","jumbo","jumpy","keeps","knife","knock","known","label",
    "lance","laser","later","lemon","level","light","limit","liner","local","lodge",
    "logic","login","loose","lousy","lover","lower","lucky","lunar","lyric",
    "magic","major","maker","manor","maple","march","match","media","mercy","merge",
    "merit","metal","mirth","model","moose","moral","morph","motor","mount","mouse",
    "mouth","movie","mural","music","naive","naval","nerve","never","night","noble",
    "noise","north","noted","novel","nurse","nymph","occur","ocean","offer","often",
    "olive","onset","orbit","order","other","outer","owing","ozone","paint","panel",
    "panic","paper","party","pasta","patch","patio","pause","peace","pearl","pedal",
    "penny","perch","phase","phone","photo","piano","pixel","pizza","place","plain",
    "plane","plank","plant","plate","plaza","plead","pluck","plumb","plume","plunge",
    "point","polar","poppy","porch","posed","power","press","price","pride","prime",
    "print","prior","prize","probe","prone","proof","prose","proud","prove","proxy",
    "pulse","punch","pupil","purse","queen","query","quest","queue","quick","quiet",
    "quota","quote","radar","radio","raise","rally","range","rapid","ratio","reach",
    "ready","realm","rebel","recap","relax","reply","rider","ridge","rifle","right",
    "risky","rival","river","robot","rocky","roman","rouge","rough","round","route",
    "royal","ruler","rural","sadly","saint","salad","sauce","scale","scene","score",
    "scout","screw","seize","sense","serum","serve","seven","shade","shaft","shake",
    "shall","shame","shape","share","shark","sharp","sheep","sheer","shelf","shell",
    "shift","shine","shirt","shock","shoot","shore","short","shout","shove","shown",
    "sight","siege","sigma","silly","since","sixth","sixty","skill","skull","slave",
    "sleep","slice","slide","slime","sling","slope","smart","smile","smoke","snack",
    "snake","solar","solid","solve","sorry","south","space","spark","speak","spend",
    "spice","spike","spine","spite","split","spoke","sport","spout","spray","squad",
    "stack","stage","stain","stale","stall","stand","stare","stark","start","state",
    "stays","steam","steep","steer","stern","stick","stiff","still","stock","stone",
    "stood","store","story","stove","strap","straw","strip","study","stuff","style",
    "sugar","suite","super","surge","swamp","swear","sweat","sweep","sweet","swept",
    "swift","sword","sworn","syrup","table","talon","tango","tapir","taste","teach",
    "teeth","tempt","tense","tenth","terms","their","theme","there","these","thick",
    "thing","think","third","thorn","those","three","threw","throw","thumb","tiger",
    "tight","timer","tired","title","today","token","tooth","topic","torch","total",
    "touch","tough","towel","tower","toxic","track","trade","trail","train","trait",
    "tramp","trash","trawl","treat","trend","trial","tribe","trick","tried","troop",
    "trout","trove","truck","truly","trump","trunk","trust","truth","tummy","tuner",
    "tunic","tweak","twice","twist","ultra","unify","union","unity","until","upper",
    "upset","urban","usage","usual","utter","valid","value","valve","vapor","vault",
    "verse","video","vigor","viral","virus","visit","vista","vital","vivid","vocal",
    "voice","voter","wagon","waste","watch","water","weary","weave","weigh","weird",
    "whale","wheat","wheel","where","which","while","white","whole","whose","wider",
    "width","witch","woman","women","world","worry","worse","worst","worth","would",
    "wound","wrath","wrist","wrote","yacht","young","yours","youth","zebra","zonal",
]

STREAK_FILE = Path(__file__).parent / ".streak.json"


def load_streak() -> dict:
    if STREAK_FILE.exists():
        return json.loads(STREAK_FILE.read_text())
    return {"wins": 0, "losses": 0, "streak": 0, "best": 0}


def save_streak(data: dict) -> None:
    STREAK_FILE.write_text(json.dumps(data))


def score_guess(guess: str, answer: str) -> list[str]:
    result = ["gray"] * 5
    answer_chars = list(answer)
    # First pass: greens
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            result[i] = "green"
            answer_chars[i] = None
    # Second pass: yellows
    for i, g in enumerate(guess):
        if result[i] == "green":
            continue
        if g in answer_chars:
            result[i] = "yellow"
            answer_chars[answer_chars.index(g)] = None
    return result


def render_tile(letter: str, color: str) -> str:
    mapping = {"green": GREEN, "yellow": YELLOW, "gray": GRAY}
    c = mapping.get(color, GRAY)
    return f"{c} {letter.upper()} {RESET}"


def render_board(guesses: list[tuple[str, list[str]]], max_guesses: int = 6) -> str:
    lines = []
    for guess, colors in guesses:
        lines.append(" ".join(render_tile(l, c) for l, c in zip(guess, colors)))
    for _ in range(max_guesses - len(guesses)):
        lines.append(" ".join(f"{GRAY}   {RESET}" for _ in range(5)))
    return "\n".join(lines)


def render_keyboard(used: dict[str, str]) -> str:
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    lines = []
    for row in rows:
        parts = []
        for ch in row:
            color = used.get(ch, "none")
            if color == "green":
                parts.append(f"{GREEN} {ch.upper()} {RESET}")
            elif color == "yellow":
                parts.append(f"{YELLOW} {ch.upper()} {RESET}")
            elif color == "gray":
                parts.append(f"{GRAY} {ch.upper()} {RESET}")
            else:
                parts.append(f" {ch.upper()} ")
        lines.append(" ".join(parts))
    return "\n".join(lines)


def draw(guesses, used, message="", streak_data=None):
    print(CLEAR, end="")
    print(f"{BOLD}  W O R D L E{RESET}  —  Guess the 5-letter word in 6 tries\n")
    print(render_board(guesses))
    print()
    print(render_keyboard(used))
    print()
    if streak_data:
        s = streak_data
        print(f"  Wins: {s['wins']}  Losses: {s['losses']}  "
              f"Streak: {s['streak']}  Best: {s['best']}")
    if message:
        print(f"\n  {message}")


def play():
    answer = random.choice(WORD_LIST)
    guesses: list[tuple[str, list[str]]] = []
    used: dict[str, str] = {}
    streak = load_streak()
    won = False

    COLOR_PRIORITY = {"green": 3, "yellow": 2, "gray": 1, "none": 0}

    draw(guesses, used, streak_data=streak)

    for attempt in range(1, 7):
        while True:
            try:
                raw = input(f"  Guess {attempt}/6: ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print(f"\n  The word was: {BOLD}{answer.upper()}{RESET}")
                sys.exit(0)

            if len(raw) != 5:
                draw(guesses, used, "Enter a 5-letter word.", streak)
                continue
            if not raw.isalpha():
                draw(guesses, used, "Letters only, please.", streak)
                continue
            break

        colors = score_guess(raw, answer)
        guesses.append((raw, colors))

        for letter, color in zip(raw, colors):
            if COLOR_PRIORITY[color] > COLOR_PRIORITY.get(letter, COLOR_PRIORITY["none"]):
                used[letter] = color

        if raw == answer:
            won = True
            streak["wins"] += 1
            streak["streak"] += 1
            streak["best"] = max(streak["best"], streak["streak"])
            save_streak(streak)
            draw(guesses, used, streak_data=streak)
            msgs = ["Genius!", "Magnificent!", "Impressive!", "Splendid!", "Great!", "Phew!"]
            print(f"\n  {BOLD}{msgs[attempt - 1]}{RESET}  Solved in {attempt}/6\n")
            break

        draw(guesses, used, streak_data=streak)

    if not won:
        streak["losses"] += 1
        streak["streak"] = 0
        save_streak(streak)
        draw(guesses, used, streak_data=streak)
        print(f"\n  Better luck next time! The word was: {BOLD}{answer.upper()}{RESET}\n")

    try:
        again = input("  Play again? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        again = "n"

    if again == "y":
        play()


if __name__ == "__main__":
    play()
