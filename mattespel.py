import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="MatteSpel", layout="centered")

if 'spel' not in st.session_state:
    st.session_state.spel = {
        'spelare1': 0, 'spelare2': 0, 'nuvarande': 1,
        'k': random.randint(-3, 3), 'm': random.randint(-3, 3)
    }

st.title("🎮 MatteSpel: Två Spelare")

# Poäng
col1, col2, col3 = st.columns(3)
with col1: st.metric("🔴 Spelare 1", st.session_state.spel['spelare1'])
with col2: st.metric("🟠 Spelare 2", st.session_state.spel['spelare2'])
with col3: st.metric("🎯 Tur", f"Spelare {st.session_state.spel['nuvarande']}")

# Knappar
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Ny Graf"):
        st.session_state.spel['k'] = random.randint(-3, 3)
        st.session_state.spel['m'] = random.randint(-3, 3)
        st.rerun()
with col2:
    if st.button("🔄 Nollställ"):
        st.session_state.spel['spelare1'] = 0
        st.session_state.spel['spelare2'] = 0
        st.session_state.spel['nuvarande'] = 1
        st.rerun()

# Gissning
st.subheader(f"📊 Spelare {st.session_state.spel['nuvarande']}s tur")
k_giss = st.slider("Lutning k", -4, 4, 0)
m_giss = st.slider("y-skärning m", -4, 4, 0)
st.info(f"**Gissning:** y = {k_giss}x + {m_giss}")

# Graf
fig, ax = plt.subplots(figsize=(8, 5))
x = np.linspace(-8, 8, 100)
y_hemlig = st.session_state.spel['k'] * x + st.session_state.spel['m']
y_giss = k_giss * x + m_giss

ax.plot(x, y_hemlig, 'b-', linewidth=3, label='Grafen att matcha')
ax.plot(x, y_giss, 'r--', linewidth=2, label='Din gissning')
ax.axhline(y=0, color='black', linewidth=1)
ax.axvline(x=0, color='black', linewidth=1)
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Kontrollera
if st.button("✅ Gissa"):
    if k_giss == st.session_state.spel['k'] and m_giss == st.session_state.spel['m']:
        if st.session_state.spel['nuvarande'] == 1:
            st.session_state.spel['spelare1'] += 1
        else:
            st.session_state.spel['spelare2'] += 1
        st.success("🎉 Rätt! +1 poäng!")
    else:
        st.session_state.spel['nuvarande'] = 3 - st.session_state.spel['nuvarande']
        st.error("❌ Fel! Byt spelare")
    st.rerun()

# Vinnare
if st.session_state.spel['spelare1'] >= 3:
    st.balloons()
    st.success("🎊 SPELARE 1 VINNER!")
elif st.session_state.spel['spelare2'] >= 3:
    st.balloons()
    st.success("🎊 SPELARE 2 VINNER!")
