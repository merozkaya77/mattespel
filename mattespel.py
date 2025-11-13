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
        'hemlig_k': random.randint(-10, 10),
        'hemlig_m': random.randint(-10, 10),
        'aktivt': True
    }

# Header
st.title("🎮 MatteSpel: Två Spelare")
st.markdown("---")

# Poängdisplay - Visa alltid aktuella poäng
st.subheader("🏆 Poängställning")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🔴 Spelare 1", st.session_state.spel['spelare1'])
with col2:
    st.metric("🟠 Spelare 2", st.session_state.spel['spelare2'])
with col3:
    st.metric("🎯 Tur", f"Spelare {st.session_state.spel['nuvarande']}")

# Vinstmeddelande - Visa tydligt när någon vinner
if st.session_state.spel['spelare1'] >= 10:
    st.balloons()
    st.success("🎊 🎊 SPELARE 1 VINNER SPELET! 🎊 🎊")
    st.session_state.spel['aktivt'] = False
elif st.session_state.spel['spelare2'] >= 10:
    st.balloons()  
    st.success("🎊 🎊 SPELARE 2 VINNER SPELET! 🎊 🎊")
    st.session_state.spel['aktivt'] = False

st.markdown("---")

# Nollställ knapp
if st.button("🔄 Nollställ Spelet", use_container_width=True):
    st.session_state.spel['spelare1'] = 0
    st.session_state.spel['spelare2'] = 0  
    st.session_state.spel['nuvarande'] = 1
    st.session_state.spel['hemlig_k'] = random.randint(-10, 10)
    st.session_state.spel['hemlig_m'] = random.randint(-10, 10)
    st.session_state.spel['aktivt'] = True
    st.rerun()

# HUVUDSPEL - Visa bara om spelet är aktivt
if st.session_state.spel['aktivt']:
    st.subheader(f"📊 Spelare {st.session_state.spel['nuvarande']}s tur att gissa")
    
    # Visa den aktuella grafen
    st.info(f"**Nuvarande graf för Spelare {st.session_state.spel['nuvarande']}**")

    # Rita graf FÖRE gissning
    fig, ax = plt.subplots(figsize=(10, 8))
    x = np.linspace(-10, 10, 100)

    # Rita hemlig linje
    y_hemlig = st.session_state.spel['hemlig_k'] * x + st.session_state.spel['hemlig_m']
    ax.plot(x, y_hemlig, 'b-', linewidth=4, label='Grafen att matcha')

    # Grafikinställningar - tydlig gradering
    ax.axhline(y=0, color='black', linewidth=2)
    ax.axvline(x=0, color='black', linewidth=2)
    ax.set_xticks(np.arange(-10, 11, 1))
    ax.set_yticks(np.arange(-10, 11, 1))
    ax.grid(True, alpha=0.4)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.legend()
    
    st.pyplot(fig)

    # Gissningssektion
    st.subheader("🎯 Din gissning")
    col1, col2 = st.columns(2)
    with col1:
        k_giss = st.slider("Lutning k", -10, 10, 0, key="k_slider")
    with col2:
        m_giss = st.slider("y-skärning m", -10, 10, 0, key="m_slider")

    st.info(f"**Du gissar:** y = {k_giss}x + {m_giss}")

    # Gissningsknapp
    if st.button("✅ Gissa", type="primary", use_container_width=True):
        if k_giss == st.session_state.spel['hemlig_k'] and m_giss == st.session_state.spel['hemlig_m']:
            # RÄTT SVAR - ge poäng
            if st.session_state.spel['nuvarande'] == 1:
                st.session_state.spel['spelare1'] += 1
                st.success(f"🎉 Spelare 1 gissade RÄTT och fick 1 poäng! Totala poäng: {st.session_state.spel['spelare1']}")
            else:
                st.session_state.spel['spelare2'] += 1
                st.success(f"🎉 Spelare 2 gissade RÄTT och fick 1 poäng! Totala poäng: {st.session_state.spel['spelare2']}")
            
            # ALLTID skapa NY LINJE efter gissning
            st.session_state.spel['hemlig_k'] = random.randint(-10, 10)
            st.session_state.spel['hemlig_m'] = random.randint(-10, 10)
            
        else:
            # FEL SVAR - ingen poäng
            st.error(f"❌ Spelare {st.session_state.spel['nuvarande']} gissade fel! Ingen poäng.")
        
        # ALLTID BYT SPELARE efter gissning (oavsett rätt/fel)
        st.session_state.spel['nuvarande'] = 3 - st.session_state.spel['nuvarande']
        st.info(f"🔄 Nu är det Spelare {st.session_state.spel['nuvarande']}s tur med en NY GRAF!")
        
        st.rerun()

else:
    # Visa när spelet inte är aktivt (efter vinst)
    st.info("🎯 Spelet är slut! Klicka på 'Nollställ Spelet' för att spela igen.")

# Instruktioner
with st.expander("📖 Spelinstruktioner"):
    st.markdown("""
    **🎯 Så spelar ni:**
    
    1. **Spelare 1** börjar med en graf
    2. **Gissa** k och m med glidarna  
    3. **Klicka Gissa** för att kontrollera
    4. **Rätt svar:** +1 poäng → NY GRAF → Byt spelare
    5. **Fel svar:** Ingen poäng → NY GRAF → Byt spelare
    6. **Alltid:** Ny graf efter varje gissning
    7. **Första till 10 poäng vinner!**
    
    **📊 Grafen:**
    - Varje ruta = 1 enhet
    - k: -10 till 10
    - m: -10 till 10
    
    **💡 Tips:**
    - **m** = var linjen skär y-axeln
    - **k** = lutning (positiv = uppåt, negativ = nedåt)
    """)

st.markdown("---")
st.caption("Skapad för matematiklärande • Räta linjens ekvation: y = kx + m")
