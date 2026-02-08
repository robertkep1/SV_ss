import streamlit as st
import numpy as np

st.header("Saint Venant uniform; z2 als onafhankelijke variable")

st.markdown(
    r"""
    Het script geeft nu als onafhankelijke variabele z2 uit. Gebaseerd is het op de steady state equation van de Saint Venant vergelijking of 1D Shallow water equation.
    
    $$\frac{d}{dx}\left(\frac{Q^2}{A}\right) + gA\frac{dh}{dx} = gA(S_0 - S_f)$$

    $$Q = \frac{1}{n} A R^{2/3} S_0^{1/2}$$

    Als variabelen hebben we:

    z2 (m) = hoogte van de eene kant van de channel, nu als afhankelijke variabele omdat je wilde weten hoe hoog zo'n aquaduct zou moeten zijn 
    
    b (m) = Breedte van de channel
    
    Q (m³) = Afvoer
    
    x1 (m) = Koordinat van het beginpunt
    
    x2 (m) = Koordinat van het eindpunt
    
    z1 (m) = Hoogte van heg beginpunt
    
    Waterdiepte h (m) = De water hoogte in je channel, tijdsonafhankelijk omdat we met een steady state solution werken. Zo hoog zou je muur in je aquaduct natuurlijk in ieder geval moeten zijn.
    
    Voor nu verondstellen we een rechthoekige channel met breedte b en hoogte h.

    Hieronder nog een paar typische n waardes voor de roughness term n. Waarschinlijk ergens rond de 0.02 voor jouw geval.
    """
)

st.markdown("""
| Surface / Channel Type | Typical Manning’s n |
|------------------------|---------------------|
| Smooth concrete | 0.012 – 0.015 |
| Finished concrete (slightly rough) | 0.015 – 0.017 |
| Rubble / brick masonry | 0.017 – 0.020 |
| Earth channel (straight & clean) | 0.020 – 0.030 |
| Earth channel (some weeds) | 0.030 – 0.035 |
| Earth channel (very weedy / irregular) | 0.035 – 0.050 |
| Rocky natural channel | 0.040 – 0.060 |
| Mountain streams (large rocks & debris) | 0.050 – 0.100 |
| Vegetated canals (heavy brush) | 0.080 – 0.150 |
""")

st.markdown("""
            ___________________________________________________________________________________
            Hieronder zie je de resultaten:

""")


# -----------------------
# Independent inputs
# -----------------------
st.sidebar.header("Onafhankelijke variabelen")
b = st.sidebar.slider("Breedte channel b (m)", 0.1, 5.0, 5.0, key="b")
n = st.sidebar.slider("Manning n", 0.00, 0.05, 0.01, key="n", step=0.0005)
st.sidebar.write("Manning n:", f"{n:.3f}")
st.sidebar.header("Afvoer")


Q_pd_str = st.sidebar.text_input("Afvoer Q (m³/d)", value="0.01", key="Q_text")

# ❗ Safe parsing
try:
    Q_pd = float(Q_pd_str)
except ValueError:
    st.sidebar.error("Q (e.g., 0.01)")
    st.stop()

Q = Q_pd / 86400

st.sidebar.header("Geometrie")
x1 = st.sidebar.number_input("x1 (m)", value=0.0, key="x1")
z1 = st.sidebar.number_input("z1 (m)", value=0.0, key="z1")
x2 = st.sidebar.number_input("x2 (m)", value=100.0, key="x2")

# -----------------------
# Depth
h = st.sidebar.slider("water dpiepte h (m)", 0.01, 3.0, 2.0, key="h")

A = b * h
R = A / (b + 2*h)

# -----------------------
# Solve for slope S0 using Manning
S0 = (Q * n / (A * R**(2/3)))**2

# -----------------------
# Compute dependent z2
if x2 == x1:
    st.error("x2 must be different from x1")
else:
    z2 = z1 + S0 * (x2 - x1)

    st.metric("Berekend z2 (m)", f"{z2:.5f}")
    st.write("Helling S0:", f"{S0:.7f}")

    st.write("### Samenvatting")
    st.write(f"Q = {Q:.6f} m³/s")
    st.write(f"Q = {Q_pd:.2f} m³/d")
    st.write(f"h = {h:.2f} m")
    st.write(f"b = {b:.2f} m")
    st.write(f"n = {n:.3f}")
