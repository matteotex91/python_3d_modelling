import random
import cadquery as cq

# Parametri, in millimetri
N = 4  # celle per lato: griglia N × N × N
L = 10.0  # lato di ogni cella
diametro_sfera = 9
diametro_percorso = 7.5
diametro_stretto = 5.5
seme = 42  # cambia il labirinto; usa None per una scelta casuale

rng = random.Random(seme)
R = L * N

# Il blocco esterno è centrato nell'origine.
pezzo = cq.Workplane("XY").box(R, R, R)


def centro(i, j, k):
    """Centro della cella (i, j, k), con indici da 0 a N-1."""
    return (
        -R / 2 + (i + 0.5) * L,
        -R / 2 + (j + 0.5) * L,
        -R / 2 + (k + 0.5) * L,
    )


# Genera un labirinto 3D perfetto con una visita in profondità:
# ogni cella è raggiungibile e il percorso non contiene cicli.
celle = [(i, j, k) for i in range(N) for j in range(N) for k in range(N)]
rng.shuffle(celle)
iniziale = celle[0]

visitate = {iniziale}
percorso = set()
stack = [iniziale]

while stack:
    cella = stack[-1]
    i, j, k = cella

    vicine = [
        (i + 1, j, k),
        (i - 1, j, k),
        (i, j + 1, k),
        (i, j - 1, k),
        (i, j, k + 1),
        (i, j, k - 1),
    ]
    vicine = [
        v
        for v in vicine
        if all(0 <= coordinata < N for coordinata in v) and v not in visitate
    ]

    if not vicine:
        stack.pop()
        continue

    vicina = rng.choice(vicine)
    visitate.add(vicina)
    percorso.add(frozenset((cella, vicina)))
    stack.append(vicina)

# Scava una cavità sferica al centro di ogni cella.
r_sfera = diametro_sfera / 2
for cella in celle:
    sfera = cq.Solid.makeSphere(r_sfera, cq.Vector(*centro(*cella)))
    pezzo = pezzo.cut(sfera)

# Per ogni coppia adiacente, scava un cilindro tra i centri delle celle.
# Diametro 6 mm se l'arco appartiene al percorso, altrimenti 4 mm.
for i, j, k in celle:
    cella = (i, j, k)

    # Basta controllare le tre direzioni positive per evitare duplicati.
    for vicina in ((i + 1, j, k), (i, j + 1, k), (i, j, k + 1)):
        if not all(0 <= coordinata < N for coordinata in vicina):
            continue

        collegata = frozenset((cella, vicina)) in percorso
        diametro = diametro_percorso if collegata else diametro_stretto
        r_foro = diametro / 2

        p1 = cq.Vector(*centro(*cella))
        p2 = cq.Vector(*centro(*vicina))
        direzione = p2.sub(p1)
        lunghezza = direzione.Length

        cilindro = cq.Solid.makeCylinder(
            r_foro,
            lunghezza,
            p1,
            direzione.normalized(),
        )
        pezzo = pezzo.cut(cilindro)


# Apre dall'esterno le celle sul bordo, con fori ciechi fino alla cavità sferica.
# L'asse di ciascun foro punta dalla faccia esterna verso il centro della cella.
r_finestra = diametro_stretto / 2

for i, j, k in celle:
    x, y, z = centro(i, j, k)

    aperture = []

    if i == 0:
        aperture.append((cq.Vector(-R / 2, y, z), cq.Vector(1, 0, 0)))
    if i == N - 1:
        aperture.append((cq.Vector(R / 2, y, z), cq.Vector(-1, 0, 0)))

    if j == 0:
        aperture.append((cq.Vector(x, -R / 2, z), cq.Vector(0, 1, 0)))
    if j == N - 1:
        aperture.append((cq.Vector(x, R / 2, z), cq.Vector(0, -1, 0)))

    if k == 0:
        aperture.append((cq.Vector(x, y, -R / 2), cq.Vector(0, 0, 1)))
    if k == N - 1:
        aperture.append((cq.Vector(x, y, R / 2), cq.Vector(0, 0, -1)))

    for punto_iniziale, direzione in aperture:
        foro_cieco = cq.Solid.makeCylinder(
            r_finestra,
            L / 2 + 0.1,  # termina poco oltre il centro, dentro la cavità sferica
            punto_iniziale,
            direzione,
        )
        pezzo = pezzo.cut(foro_cieco)

# Esporta il solido risultante.
pezzo.export("labirinto_3d.step")
