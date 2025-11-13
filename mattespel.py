import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

# Konfigurera sidan
st.set_page_config(
    page_title="MatteSpel - Två Spelare", 
    page_icon="🎮",
    layout="centered"
)

# Initiera spelstatus
if 'spel' not in st.session_state:
    st.session_state.spel = {
        'spelare1': 0,
        'spelare2': 0, 
        'nuvarande': 1,
        'hemlig_k': random.randint(-3, 3),
        'hemlig_m': random.randint(-3, 3),
        'aktivt': True
    }

# Header
st.title("🎮 MatteSpel: Två Spelare")
st.markdown("---")

# Poängdisplay
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🔴 Spelare 1", st.session_state.spel['spelare1'])
with col2:
    st.metric("🟠 Spelare 2", st.session_state.spel['spelare2'])
with col3:
    st.metric("🎯 Tur", f"Spelare {st.session_state.spel['nuvarande']}")

st.markdown("---")

# Spelkontroller
col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Ny Graf", use_container_width=True):
        st.session_state.spel['hemlig_k'] = random.randint(-3, 3)
        st.session_state.spel['hemlig_m'] = random.randint(-3, 3)
        st.session_state.spel['aktivt'] = True
        st.rerun()
with col2:
    if st.button("🔄 Nollställ", use_container_width=True):
        st.session_state.spel['spelare1'] = 0
        st.session_state.spel['spelare2'] = 0  
        st.session_state.spel['nuvarande'] = 1
        st.session_state.spel['hemlig_k'] = random.randint(-3, 3)
        st.session_state.spel['hemlig_m'] = random.randint(-3, 3)
        st.rerun()

# Gissningssektion
st.subheader(f"📊 Spelare {st.session_state.spel['nuvarande']}s tur att gissa")

col1, col2 = st.columns(2)
with col1:
    k_giss = st.slider("Lutning k", -4, 4, 0, key="k_slider")
with col2:
    m_giss = st.slider("y-skärning m", -4, 4, 0, key="m_slider")

st.info(f"**Spelare {st.session_state.spel['nuvarande']} gissar:** y = {k_giss}x + {m_giss}")

# Rita graf
st.subheader("📈 Matcha grafen!")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.linspace(-8, 8, 100)

# Rita hemlig linje
y_hemlig = st.session_state.spel['hemlig_k'] * x + st.session_state.spel['hemlig_m']
ax.plot(x, y_hemlig, 'b-', linewidth=4, label='Grafen att matcha')

# Rita gissning  
y_giss = k_giss * x + m_giss
färg = 'red' if st.session_state.spel['nuvarande'] == 1 else 'orange'
ax.plot(x, y_giss, '--', color=färg, linewidth=3, 
        label=f'Spelare {st.session_state.spel["nuvarande"]}s gissning')

# Grafikinställningar
ax.axhline(y=0, color='black', linewidth=2)
ax.axvline(x=0, color='black', linewidth=2)
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_xlim(-8, 8)
ax.set_ylim(-8, 8)

st.pyplot(fig)

# Gissningsknapp
if st.button("✅ Gissa", type="primary", use_container_width=True):
    if k_giss == st.session_state.spel['hemlig_k'] and m_giss == st.session_state.spel['hemlig_m']:
        # Rätt svar!
        if st.session_state.spel['nuvarande'] == 1:
            st.session_state.spel['spelare1'] += 1
        else:
            st.session_state.spel['spelare2'] += 1
        
        st.success(f"🎉 Spelare {st.session_state.spel['nuvarande']} fick RÄTT! +1 poäng!")
        st.session_state.spel['aktivt'] = False
    else:
        # Fel svar - byt spelare
        st.error(f"❌ Fel! Tur för nästa spelare.")
        st.session_state.spel['nuvarande'] = 3 - st.session_state.spel['nuvarande']  # Byt mellan 1 och 2
    
    st.rerun()

# Vinstmeddelande
if st.session_state.spel['spelare1'] >= 5:
    st.balloons()
    st.success("🎊 🎊 SPELARE 1 VINNER! 🎊 🎊")
elif st.session_state.spel['spelare2'] >= 5:
    st.balloons()  
    st.success("🎊 🎊 SPELARE 2 VINNER! 🎊 🎊")

# Instruktioner
with st.expander("📖 Spelinstruktioner"):
    st.markdown("""
    **🎯 Så spelar ni:**
    
    1. **Spelare 1** börjar - använd glidarna för att gissa k och m
    2. Klicka **Gissa** för att kontrollera  
    3. **Rätt svar:** +1 poäng till aktuell spelare
    4. **Fel svar:** Tur för nästa spelare!
    5. Klicka **Ny Graf** för nästa omgång
    6. **Första till 5 poäng vinner!**
    
    **💡 Tips:**
    - **m** = var linjen skär y-axeln
    - **k** = hur brant linjen är
    - Samarbeta eller tävla mot varandra!
    """)

st.markdown("---")
st.caption("Skapad för matematiklärande • Dela denna länk med dina elever!")
