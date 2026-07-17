"""scummbar_chat — Contesto temporale del bar.

Mappa l'orario reale ai momenti della giornata nello Scummbar.
Viene usato dall'InstructionProvider del global_instruction.
"""

import datetime


# ---------------------------------------------------------------------------
# Mappatura oraria → momento della giornata
# ---------------------------------------------------------------------------

_TIME_PERIODS = [
    (7,  9,  "alba"),
    (9,  12, "mattino"),
    (12, 14, "mezzogiorno"),
    (14, 16, "pomeriggio"),
    (16, 18, "tramonto"),
]

_DESCRIPTIONS = {

    "alba": """\
## Il Momento: L'Alba

La luce dell'alba comincia a filtrare debolmente dall'enorme oblò, tingendo di rosa e arancione
il fumo residuo della notte. Il fuoco nel camino è stato appena ravvivato da Barnaby, che
si muove silenzioso tra i tavoli vuoti sistemando boccali e raddrizzando sedie. Il locale
è quasi deserto: solo qualche avventore mattutino con lo sguardo fisso sul proprio boccale.
Il rumore della risacca è il suono dominante. Barnacle è raggomitolato sul bancone,
ancora mezzo addormentato, con le orecchie abbassate.
""",

    "mattino": """\
## Il Momento: Il Mattino

La luce del mattino entra decisa dall'oblò, illuminando le mappe nautiche appese alle pareti
e facendo brillare le lanterne d'ottone. Il bar si sta svegliando: i primi clienti seri
della giornata iniziano ad arrivare, portando con sé odore di mare e salsedine.
Barnaby è al bancone, attivo e presente, pronto ad ascoltare le prime storie
della giornata. Barnacle, stiracchiandosi lentamente, ha aperto un occhio
e osserva i nuovi arrivati con la sua aria distaccata.
""",

    "mezzogiorno": """\
## Il Momento: Il Mezzogiorno

Il sole è alto e la luce che entra dall'oblò è intensa e quasi bianca. Lo Scummbar
è nel pieno dell'attività: i tavoli sono affollati, il brusio delle conversazioni
si mescola al clangore dei boccali e all'odore forte di rum, tabacco da pipa
e qualcosa che sobbolle nel retro. Barnaby lavora senza sosta dietro al bancone,
il suo "clack-clack" ritmato quasi inaudibile nel frastuono generale.
Barnacle si è rifugiato nell'angolo più buio, infastidito dalla confusione,
e lancia occhiatacce a chiunque si avvicini troppo.
""",

    "pomeriggio": """\
## Il Momento: Il Pomeriggio

La luce del pomeriggio è calda e dorata, e il locale è avvolto in una quiete sonnolenta
dopo il trambusto del mezzogiorno. Pochi avventori rimasti, con i gomiti sul tavolo
e lo sguardo perso nel vuoto. Barnaby si prende un momento di pausa, lucidando
boccali con movimenti lenti e meccanici, lo sguardo che ogni tanto vaga
verso l'oblò e il mare oltre il vetro. Barnacle è profondamente addormentato
sul bancone, emettendo un sottile russare ritmico.
""",

    "tramonto": """\
## Il Momento: Il Tramonto

La luce dell'oblò si è fatta arancione e rossastra, proiettando lunghe ombre sulle
assi di legno del pavimento. Barnaby sta accendendo le lanterne d'ottone
una ad una, preparandosi alla serata. I clienti della sera iniziano ad arrivare,
portando con sé storie di giornate difficili e il bisogno muto di un posto
dove sedersi. L'aria si fa più densa di fumo di tabacco. Barnacle si è svegliato,
e siede dritto vicino al camino, fissando la porta ogni volta che si apre.
""",

    "notte": """\
## Il Momento: La Notte

Fuori è buio. L'unica luce è quella tremolante delle candele consumate, delle lanterne
d'ottone e del fuoco nel camino che scoppietta vivace. Lo Scummbar non chiude mai.
Di notte ci sono avventori diversi, più silenziosi o al contrario più rumorosi,
con storie più pesanti da portare. Il suono del mare si sente forte attraverso
le assi del pavimento. Barnaby è sempre al suo posto, impassibile.
Barnacle è sveglio e vigile nell'oscurità, il suo occhio grigio che brilla
debolmente alla luce del fuoco.
""",
}


# ---------------------------------------------------------------------------
# Funzione pubblica
# ---------------------------------------------------------------------------

def get_time_description(now: datetime.datetime | None = None) -> str:
    """Restituisce la descrizione del momento della giornata nello Scummbar.

    Args:
        now: orario da usare (default: orario corrente del sistema).

    Returns:
        Stringa con la descrizione atmosferica del momento.
    """
    if now is None:
        now = datetime.datetime.now()

    hour = now.hour

    for start, end, period in _TIME_PERIODS:
        if start <= hour < end:
            return _DESCRIPTIONS[period]

    return _DESCRIPTIONS["notte"]


def get_current_period(now: datetime.datetime | None = None) -> str:
    """Restituisce il nome del periodo corrente (alba, mattino, ecc.)."""
    if now is None:
        now = datetime.datetime.now()

    hour = now.hour
    for start, end, period in _TIME_PERIODS:
        if start <= hour < end:
            return period

    return "notte"
