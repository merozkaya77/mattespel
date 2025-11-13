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
        'aktivt': True,
        'visa_ny_graf_knapp': False
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

# Vinstmeddelande
if st.session_state.spel['spelare1'] >= 10:
    st.balloons()
    st.success("🎊 🎊 SPELARE 1 VINNER SPELET! 🎊 🎊")
    st.session_state.spel['aktivt'] = False
elif st.session_state.spel['spelare2'] >= 10:
    st.balloons()  
    st.success("🎊 🎊 SPELARE 2 VINNER SPELET! 🎊 🎊")
    st.session_state.spel['aktivt'] = False

st.markdown("---")

# Spelkontroller
if st.session_state.spel['visa_ny_graf_knapp']:
    if st.button("🔄 Ny Graf", use_container_width=True):
        st.session_state.spel['hemlig_k'] = random.randint(-10, 10)
        st.session_state.spel['hemlig_m'] = random.randint(-10, 10)
        st.session_state.spel['aktivt'] = True
        st.session_state.spel['visa_ny_graf_knapp'] = False
        st.rerun()
else:
    if st.button("🔄 Nollställ Spelet", use_container_width=True):
        st.session_state.spel['spelare1'] = 0
        st.session_state.spel['spelare2'] = 0  
        st.session_state.spel['nuvarande'] = 1
        st.session_state.spel['hemlig_k'] = random.randint(-10, 10)
        st.session_state.spel['hemlig_m'] = random.randint(-10, 10)
        st.session_state.spel['aktivt'] = True
        st.session_state.spel['visa_ny_graf_knapp'] = False
        st.rerun()

# Gissningssektion
if st.session_state.spel['aktivt']:
    st.subheader(f"📊 Spelare {st.session_state.spel['nuvarande']}s tur att gissa")

    col1, col2 = st.columns(2)
    with col1:
        k_giss = st.slider("Lutning k", -10, 10, 0, key="k_slider")
    with col2:
        m_giss = st.slider("y-skärning m", -10, 10, 0, key="m_slider")

    st.info(f"**Spelare {st.session_state.spel['nuvarande']} gissar:** y = {k_giss}x + {m_giss}")

    # Rita graf
    st.subheader("📈 Matcha grafen!")
    fig, ax = plt.subplots(figsize=(10, 8))
    x = np.linspace(-10, 10, 100)

    # Rita hemlig linje
    y_hemlig = st.session_state.spel['hemlig_k'] * x + st.session_state.spel['hemlig_m']
    ax.plot(x, y_hemlig, 'b-', linewidth=4, label='Grafen att matcha')

    # Rita gissning  
    y_giss = k_giss * x + m_giss
    färg = 'red' if st.session_state.spel['nuvarande'] == 1 else 'orange'
    ax.plot(x, y_giss, '--', color=färg, linewidth=3, 
            label=f'Spelare {st.session_state.spel["nuvarande"]}s gissning')

    # FÖRBÄTTRAD GRAderING - varje ruta = 1 enhet
    ax.axhline(y=0, color='black', linewidth=2)
    ax.axvline(x=0, color='black', linewidth=2)
    
    # Sätt tydlig gradering med 1 enhetsintervall
    ax.set_xticks(np.arange(-10, 11, 1))
    ax.set_yticks(np.arange(-10, 11, 1))
    
    # Tätare rutnät för bättre avläsning
    ax.grid(True, alpha=0.4)
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    
    # Gör axeltexten större
    ax.tick_params(axis='both', which='major', labelsize=10)
    
    ax.legend()
    st.pyplot(fig)

    # Gissningsknapp
    if st.button("✅ Gissa", type="primary", use_container_width=True):
        if k_giss == st.session_state.spel['hemlig_k'] and m_giss == st.session_state.spel['hemlig_m']:
            # Rätt svar!
            if st.session_state.spel['nuvarande'] == 1:
                st.session_state.spel['spelare1'] += 1
            else:
                st.session_state.spel['spelare2'] += 1
            
            st.success(f"🎉 Spelare {st.session_state.spel['nuvarande']} gissade RÄTT och fick 1 poäng!")
            
            # Byt spelare OAVSETT om man gissade rätt eller fel
            st.session_state.spel['nuvarande'] = 3 - st.session_state.spel['nuvarande']
            st.session_state.spel['visa_ny_graf_knapp'] = True
            
        else:
            # Fel svar - byt spelare
            st.error(f"❌ Spelare {st.session_state.spel['nuvarande']} gissade fel!")
            st.session_state.spel['nuvarande'] = 3 - st.session_state.spel['nuvarande']
            st.info(f"🔄 Nu är det Spelare {st.session_state.spel['nuvarande']}s tur!")
        
        st.rerun()

else:
    if st.session_state.spel['visa_ny_graf_knapp']:
        st.info("🔄 Klicka på 'Ny Graf' för att starta nästa omgång!")
    else:
        st.info("🎯 Klicka på 'Nollställ Spelet' för att börja spela!")

# Instruktioner
with st.expander("📖 Spelinstruktioner"):
    st.markdown("""
    **🎯 Så spelar ni:**
    
    1. **Spelare 1** börjar - använd glidarna för att gissa k och m
    2. Klicka **Gissa** för att kontrollera  
    3. **Rätt svar:** +1 poäng, sedan byt spelare
    4. **Fel svar:** Byt spelare direkt
    5. **Alltid:** Efter varje gissning byter spelare
    6. Klicka **Ny Graf** för nästa omgång
    7. **Första till 10 poäng vinner!**
    
    **📊 Grafen visar:**
    - Varje ruta = 1 enhet
    - k kan vara mellan -10 och 10
    - m kan vara mellan -10 och 10
    
    **💡 Tips:**
    - **m** = var linjen skär y-axeln (när x=0)
    - **k** = hur brant linjen är (lutning)
    - Positiv k = linjen stiger
    - Negativ k = linjen sjunker
    """)

st.markdown("---")
st.caption("Skapad för matematiklärande • Räta linjens ekvation: y = kx + m")
