import os
import requests
from config import PERSPECTIVE_API_KEY, DEV_MODE

# Simple fallback keyword-based detector for dev
KEYWORDS = [
    # Basic insults
    "stupid", "idiot", "useless", "hate", "die", "fool", "dumb", "suck", "trash",
    "jerk", "loser", "pathetic", "worthless", "garbage", "scum", "moron",
    "clown", "pig", "donkey", "dog", "ugly", "liar", "fake", "cheater", "coward",

    # Commands / aggression
    "shut up", "get lost", "go away", "drop dead", "get out", "buzz off",
    "fuck off", "leave me alone", "nobody likes you", "no one likes you",

    # Threats / violence
    "kill", "kill yourself", "go kill yourself", "i will kill you", "stab you",
    "shoot you", "beat you", "hurt you", "destroy you", "smash you",
    "break your neck", "burn you", "bury you", "wipe you out", "ruin you",

    # Strong insults / profanity
    "fuck", "fucking", "shit", "asshole", "dick", "bitch", "slut", "whore",
    "piss off", "crap", "damn", "hell", "screw you", "son of a bitch",

    # Negativity / hate
    "i hate you", "you disgust me", "you make me sick", "worst", "gross",
    "dirty", "filthy", "hopeless", "lazy", "ignorant", "nasty",

    # Self-harm related
    "i want to die", "kill me", "end myself", "end my life", "suicide",
    "hang myself", "i hate my life", "life sucks", "cut myself",
    "i want to end it", "no reason to live"
    "stupid","idiot","useless","hate","die","fool","dumb","suck","trash",
    "jerk","loser","pathetic","worthless","garbage","scum","moron","clown","pig",
    "donkey","dog","ugly","liar","fake","cheater","coward","dumbass","stupid fool",
    "idiot face","retard","dumbhead","foolish","worthless human","pathetic loser",
    "trash human","scumbag","piece of crap","clown face","disgusting","filthy animal",
    "lowlife","rat","snake","parasite","creep","freak","ugly face","disgusting creature",
    "loser freak","psycho","weirdo","moronic","stupid idiot","hopeless fool","filthy pig",
    "dirtbag","trash bag","human garbage","clueless","stupid jerk","numbskull","airhead",
    
    "blockhead","nitwit","shut up","shut the hell up","shut your mouth","shut your face",
    "go away","get lost","disappear","buzz off","fuck off","piss off","screw off","leave me alone",
    "nobody likes you","no one cares","drop dead","get out of here","don't talk to me",
    "i don’t care about you","stay away","you’re nothing","don’t bother me","go die","get a life",
    "vanish","stop talking","get out","get out of my sight","you’re annoying","stop bothering me",
    "quit talking","mind your business","stay in your lane","kill","kill yourself","go kill yourself",
    "die now","i will kill you","i’ll hurt you","i’ll beat you up","i’ll destroy you","i’ll ruin you",
    "i’ll smash your face","i’ll burn you","i’ll break your bones","i’ll stab you","i’ll shoot you",
    "i’ll find you","i’ll bury you alive","i’ll choke you","i’ll hunt you down","i’ll make you pay",
    "i’ll make you suffer","i’ll destroy your life","fuck","fucking","fucker","shit","shitty","sh*t",
    "bullshit","asshole","a**hole","bastard","bitch","dumb bitch","stupid bitch","slut","whore","hoe",
    "dickhead","dick","prick","piss off","damn","hell","crap","son of a bitch","screw you","motherfucker",
    "motherf***er","jackass","cock","c*nt","jerkoff","wanker","twat","pisshead","bitchface","i hate you",
    "i despise you","you disgust me","you make me sick","i can’t stand you","worst person",
    "i regret knowing you","you’re awful","horrible","nasty","gross","dirty","filthy","smelly",
    "hopeless","lazy","ignorant","miserable","failure","disappointment","waste of space",
    "you ruin everything","i wish you’d disappear","i want to die","i want to kill myself",
    "i want to end it all","kill me now","i hate my life","i can’t go on","life sucks",
    "there’s no reason to live","i’m done","i want to end myself","i’m useless","i’m worthless",
    "nobody cares","i’m tired of living","everything hurts","i’m so alone","i don’t want to be here",
    "i wish i was dead","i feel empty","i can’t take it anymore","you’ll regret this","watch your back",
    "your time will come","karma will get you","you’ll pay for this","i hope you fail",
    "you don’t deserve anything","no one would miss you","you’re better off dead",
    "you’re nothing to me","everyone hates you","you ruin people’s lives","you’re such a mistake",
    "waste of oxygen","go cry","nobody cares about your feelings","worthless piece","failure at life",
    "pathetic excuse","utter trash","filth","garbage human","garbage person","zero","zip","garbo",
    "trashbag","ratbag","shithead","shithole","shitbag","sh!thead","fu*k","f**k","f***","f**ker",
    "fuk","fuker","fuking","fukk","fukoff","fkoff","sht","cr@p","crapola","darn","dang","bloody",
    "bugger","bollocks","arsehole","arse","a$$","piss off mate","eat shit","eat s**t","eat s***",
    "go to hell","go to h#ll","go to h*ll","drop dead already","u r useless","ur useless","u are useless",
    "ur trash","st00pid","1diot","l0ser","los3r","dumb0","dumb0ss","dumbasss","dumbsss","dooooomer","idi0t",
    "id10t","ret@rd","r3tard","r3t@rd","sh1t","sh1tty","f4ck","f4cker","m0therfucker",
    "m0therf***er","m0th3rf*cker","mother fcker","mother fkr","mthrf**ker","mthrfkr",
    "suck my dick","suck my d1ck","suck my d!ck","suck a dick","suck a d1ck",
    "suck a d!ck","blow me","blow u","blow you","kiss my ass","kiss my a**","kiss my @ss",
    "go f**k yourself","go f*ck yourself","go fk yourself","go fucc yourself","go fu*k yourself",
    "go to the deepest hell","i'll end you","im going to end you","im gonna end you","ur pathetic",
    "youre pathetic","youre garbage","u are garbage","you are garbage","you are trash","youre trash",
    "you make me vomit","you make me puke","vomit","puke","rot in hell","rot in h*ll",
    "die slow","die alone","die a lonely death","hope you choke","hope you choke on it",
    "hope you suffocate","hope you suffer","hope you rot","hope you burn","hope you drown",
    "may you die","may you rot","curse you","damn you","damn u","curse u","sickening","vile",
    "deplorable","despicable","detestable","repulsive","revolting","abomination","abominable",
    "trash-tier","trash tier","trash-tier human","trash-tier person","utter scum","utter filth",
    "utter trash","worthless scum","worthless trash","worthless filth","filthy scum",
    "pathetic scum","complete idiot","utter idiot","total idiot","total moron","utter moron",
    "absolute moron","absolute idiot","lying piece of trash","lying scumbag","lying bastard",
    "two-faced","backstabbing","fake friend","fake asshole","fake b*****d","fraud","con artist",
    "conman","cheating scum","cheating bastard","snake in the grass","rat bastard","rat-faced",
    "rotten","rotten human","rotten person","sicko","twisted","pervert","degenerate",
    "degenerate piece","perverted freak","gross freak","creepy creep","creepy bastard",
    "weird ass","weird a*s","weird a**","freak show","run of the mill trash","garbage-tier",
    "doomed","cursed","worthless dog","worthless pig","worthless human being","worthless person",
    "go jump off","go jump off a cliff","jump off","jump off a bridge","off yourself"
    "kill yourself now","youre finished","ur finished","youre done","ur done","end your life",
    "end it now","end yourself","off yourself now","u should die","you should die","hope you die",
    "hope you die soon","wish you dead","wish you were dead","wouldn't miss you","no one would miss you"
    "never mattered","not worth living","not worth existing","worthless cunt","filthy cunt","c*nt face",
    "beeped: f***","beeped: f**k","beeped: f*k","beeped: f***er","beeped: m********r","beeped: s***",
    "beeped: s**t","beeped: sh**","beeped: b****","beeped: b***h","beeped: c**t","beeped: a**hole",
    "beeped: a**h0le","beeped: mf***","beeped: mofo","beeped: m0th3rf*ck3r","beeped: f.u.c.k",
    "beeped: s.h.i.t","beeped: b.i.t.c.h","b!tch","b1tch","s1ut","slvt","slutty","slutt","wh0re",
    "wh0reface","whoreface","whor3","whorish","wh0rish","c0ck","d1ck","d!ck","d1ckhead","d!ckhead",
    "pr1ck","pr!ck","pr1ckhead","arsewipe","arsewipe","arseholeface","arseface","bellend","tosser",
    "munter","div","muppet","pillock","git","pratt","twonk","twit","berk","wazzock","plonker","numpty",
    "numptie","clot","nutter","spaz","spazzz","loserface","failboat","fail whale","failwail","failbag",
    "idiotbag","idiotbox","stup1d","stooopid","stuuupid","dumbfuck","dumbfuk","dumbfck","dumb f***",
    "effing idiot","effin idiot","effin moron","efing moron","effface","fkn idiot","fkn moron",
    "fkn loser","fkng idiot","fkng moron","fkng loser","fucccck","fuuuuuck","shiiiiit","shiiit",
    "shiiiiithead","sh1thead","cr@phead","crapface","crapolahead","crazyperson","batshit",
    "bat-shit-crazy","loony","loon","loony bin","loon bag","nutjob","nut job","psycho killer",
    "killer","stabber","gunman","gunslinger","gun nut","gun freak","violent nut","violent freak",
    "maniac","maniacal","dangerous","mutant","weirdo123","stupid123","idiot123","trash123","shit123",
    "f***123","fu*k123","s**t123","b***h123"

]
def _keyword_score(text: str) -> float:
    text = text.lower()
    hits = sum(text.count(k) for k in KEYWORDS)
    # normalize: 0..1
    return min(1.0, hits / 3.0)

def analyze_toxicity(text: str) -> float:
    """
    Returns toxicity score in [0,1].
    If PERSPECTIVE_API_KEY is configured and DEV_MODE is False, it calls Perspective API.
    Else returns a quick local heuristic score.
    """
    text = (text or "").strip()
    if not text:
        return 0.0

    if PERSPECTIVE_API_KEY and not DEV_MODE:
        url = "https://commentanalyzer.googleapis.com/v1/comments:analyze"
        data = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}}
        }
        try:
            r = requests.post(url, params={"key": PERSPECTIVE_API_KEY}, json=data, timeout=5)
            r.raise_for_status()
            resp = r.json()
            return float(resp["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
        except Exception:
            # fallback if API fails
            return _keyword_score(text)
    else:
        return _keyword_score(text)
