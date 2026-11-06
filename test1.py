import cadquery as cq

# Dimensioni in millimetri
lato = 40
diametro_foro = 10

# Cubo centrato sull'origine
pezzo = cq.Workplane("XY").box(lato, lato, lato)

# Foro cilindrico passante lungo Z
foro = cq.Workplane("XY").cylinder(
    height=lato + 2,  # un po' più lungo del cubo
    radius=diametro_foro / 2,
)
pezzo = pezzo.cut(foro)

# Taglio diagonale: prisma con sezione parallelogramma nel piano XZ,
# estruso lungo Y per attraversare tutto il cubo.
taglio = (
    cq.Workplane("XZ")
    .polyline(
        [
            (-25, -20),
            (-17, -20),
            (25, 20),
            (17, 20),
        ]
    )
    .close()
    .extrude(lato + 2, both=True)
)

pezzo = pezzo.cut(taglio)

# Esporta il solido in STEP
pezzo.export("cubo_con_foro_e_taglio.step")
