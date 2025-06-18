import itertools
import random
import streamlit as st

def generar_rondas_para_todos_conocerse(n_mesas, m_por_mesa, max_rondas=None):
    total_personas = n_mesas * m_por_mesa
    personas = [f"P{i+1}" for i in range(total_personas)]
    todos_pares = set(itertools.combinations(personas, 2))
    pares_vistos = set()
    rondas = []
    max_intentos = 500
    coberturas = []

    while len(pares_vistos) < len(todos_pares):
        if max_rondas is not None and len(rondas) >= max_rondas:
            break

        mejor_ronda = None
        nuevos_pares_max = -1

        for _ in range(max_intentos):
            random.shuffle(personas)
            mesas = [personas[i:i + m_por_mesa] for i in range(0, total_personas, m_por_mesa)]

            pares_nuevos = set()
            for mesa in mesas:
                for p1, p2 in itertools.combinations(mesa, 2):
                    par = tuple(sorted((p1, p2)))
                    if par not in pares_vistos:
                        pares_nuevos.add(par)

            if len(pares_nuevos) > nuevos_pares_max:
                nuevos_pares_max = len(pares_nuevos)
                mejor_ronda = mesas

            if nuevos_pares_max == m_por_mesa * (m_por_mesa - 1) // 2 * n_mesas:
                break

        for mesa in mejor_ronda:
            for p1, p2 in itertools.combinations(mesa, 2):
                pares_vistos.add(tuple(sorted((p1, p2))))
        rondas.append(mejor_ronda)

        cobertura = len(pares_vistos) / len(todos_pares) * 100
        coberturas.append(cobertura)

    return rondas, coberturas

# Paleta de colores para personas (puedes agregar más si tienes más personas)
PERSON_COLORS = [
    "#0077b6", "#ef476f", "#ffd166", "#06d6a0", "#118ab2", "#8338ec", "#ffbe0b",
    "#ff006e", "#3a86ff", "#43aa8b", "#f3722c", "#90be6d", "#f94144", "#577590"
]

def mostrar_mesa(mesa):
    personas_ordenadas = sorted(mesa, key=lambda x: int(x[1:]))
    ancho = max(len(p) for p in personas_ordenadas)
    row = ""
    for idx, persona in enumerate(personas_ordenadas):
        color = PERSON_COLORS[idx % len(PERSON_COLORS)]
        persona_fmt = f"{persona:<{ancho}}"
        row += f'<span style="color:{color}; font-weight:bold;">| {persona_fmt} </span>'
    row += "|"
    return row

st.set_page_config(page_title="Generador de Rondas de Mesas", layout="wide")
st.title("🔄 Generador de Rondas de Mesas")

with st.sidebar:
    st.header("Parámetros")
    n_mesas = st.number_input("Número de mesas", min_value=1, max_value=100, value=5)
    m_por_mesa = st.number_input("Personas por mesa", min_value=2, max_value=100, value=7)
    max_rondas = st.number_input("Máximo de rondas (opcional)", min_value=0, value=0)
    if max_rondas == 0:
        max_rondas = None
    st.markdown("---")
    st.write("Hecho con ❤️ usando Streamlit")

if st.button("Generar rondas"):
    rondas, coberturas = generar_rondas_para_todos_conocerse(n_mesas, m_por_mesa, max_rondas)
    pares_vistos = set()
    total_pares_en_ronda = n_mesas * (m_por_mesa * (m_por_mesa - 1) // 2)

    for ronda_idx, (ronda, cobertura) in enumerate(zip(rondas, coberturas), 1):
        pares_repetidos = 0
        pares_ronda = set()
        for mesa in ronda:
            for p1, p2 in itertools.combinations(mesa, 2):
                par = tuple(sorted((p1, p2)))
                if par in pares_vistos:
                    pares_repetidos += 1
                pares_ronda.add(par)
        porcentaje_repetidos = (pares_repetidos / total_pares_en_ronda) * 100 if total_pares_en_ronda else 0

        if cobertura >= 99.9:
            color_cobertura = "#008000"
        elif cobertura >= 80:
            color_cobertura = "#e6b800"
        else:
            color_cobertura = "#d90429"

        st.markdown(
            f"<b>🌀 Ronda {ronda_idx} "
            f"(Cobertura: <span style='color:{color_cobertura}'>{cobertura:.2f}%</span>)"
            + (f" <span style='color:#b8860b'>[Repetidos: {porcentaje_repetidos:.2f}%]</span>" if cobertura >= 50 or porcentaje_repetidos > 0 else "")
            + ":</b>",
            unsafe_allow_html=True
        )
        for mesa_idx, mesa in enumerate(ronda, 1):
            mesa_label = f"Mesa {mesa_idx}:"
            st.markdown(
                f"<span style='color:#007f5c; font-weight:bold;'>{mesa_label.ljust(10)}</span> "
                + mostrar_mesa(mesa),
                unsafe_allow_html=True
            )
        st.markdown("---")
        pares_vistos.update(pares_ronda)

    if coberturas:
        st.success(f"Total de rondas: {len(rondas)} — Cobertura final: {coberturas[-1]:.2f}%")
    else:
        st.warning("No se generaron rondas.")
else:
    st.info("Configura los parámetros y pulsa 'Generar rondas'.")
