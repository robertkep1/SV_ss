import streamlit as st
import numpy as np
from scipy.optimize import fsolve

dependent = st.sidebar.selectbox(
    "Dependent variable",
    ["Depth h", "Discharge Q", "Slope S₀"]
)


b = st.sidebar.slider("Channel width b (m)", 1.0, 20.0, 5.0)
n = st.sidebar.slider("Manning n", 0.01, 0.05, 0.03)


Q  = st.slider("Discharge Q (m³/s)", 0.1, 200.0, 20.0)
S0 = st.slider("Slope S₀", 1e-4, 1e-2, 1e-3)

def residual_h(h):
    A = b * h
    R = A / (b + 2*h)
    Sf = (Q*n / (A * R**(2/3)))**2
    return S0 - Sf

h = fsolve(residual_h, x0=1.0)[0]

h  = st.slider("Depth h (m)", 0.1, 10.0, 2.0)
S0 = st.slider("Slope S₀", 1e-4, 1e-2, 1e-3)

A = b * h
R = A / (b + 2*h)
Q = (1/n) * A * R**(2/3) * S0**0.5


h = st.slider("Depth h (m)", 0.1, 10.0, 2.0)
Q = st.slider("Discharge Q (m³/s)", 0.1, 200.0, 20.0)

A = b * h
R = A / (b + 2*h)
S0 = (Q*n / (A * R**(2/3)))**2


st.subheader("Steady-state solution")

st.metric("Depth h (m)", f"{h:.3f}")
st.metric("Discharge Q (m³/s)", f"{Q:.3f}")
st.metric("Slope S₀", f"{S0:.5f}")



