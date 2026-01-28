"""
SKY AS GROUND: 13-Sign Alignment Dashboard
Consciousness-as-Ground Expressing as Wholeperson, Planet, and Boundary: One Expression, Many Recognitions

Streamlit Interface for:
- The Aperture: Natal Chart Generation
- The Calibration: Birth Time Rectification
- The Current Frequency: Dasha Timeline Visualization

© 2026 Howard North | SkyAsGround.com
Licensed under Creative Commons BY-NC-ND 4.0: https://creativecommons.org
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from ground_engine import GroundEngine
from rectification import RectificationScanner
import json

# ==============================================================================
# PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="SkyAsGround | ZeroArbitrary™",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# DARK CELESTIAL THEME
# ==============================================================================

st.markdown("""
<style>
    /* Dark celestial background */
    .main {
        background: linear-gradient(180deg, #0a0e27 0%, #1a1a3e 100%);
        color: #e0e0e0;
    }
    
    /* Headers with cosmic glow */
    h1, h2, h3 {
        color: #a8c5e6;
        text-shadow: 0 0 10px rgba(168, 197, 230, 0.3);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: #1a1a3e;
        border-radius: 10px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #a8c5e6;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2d2d5f;
        color: #ffffff;
    }
    
    /* Data tables */
    .dataframe {
        background-color: #1a1a3e !important;
        color: #e0e0e0 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Input fields */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        background-color: #2d2d5f;
        color: #e0e0e0;
        border: 1px solid #4a4a7f;
        border-radius: 5px;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #2d2d5f;
        color: #a8c5e6;
        border-radius: 5px;
    }
    
    /* Success/Info boxes */
    .stAlert {
        background-color: #1a1a3e;
        border-left: 4px solid #667eea;
        color: #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# INITIALIZE ENGINE
# ==============================================================================

@st.cache_resource
def get_engine():
    """Initialize and cache the Ground Engine"""
    return GroundEngine()

@st.cache_resource
def get_scanner():
    """Initialize and cache the Rectification Scanner"""
    engine = get_engine()
    return RectificationScanner(engine)

engine = get_engine()
scanner = get_scanner()

# ==============================================================================
# MAIN INTERFACE HEADER
# ==============================================================================
st.title("SKY AS GROUND")
st.markdown("### Powered by the TrueNorthEngine | ZeroArbitrary™ Standard")
st.write("---")


# ==============================================================================
# VISUALIZATION FUNCTIONS
# ==============================================================================

def create_linear_horizon_chart(chart_data):
    """
    Create a linear 0-360° horizon map showing constellation boundaries
    and planetary positions with unequal constellation widths.
    """
    fig = go.Figure()
    
    # Get boundaries from engine
    boundaries = engine.boundaries
    
    # Create constellation segments
    colors = {
        'Aries': '#ff6b6b', 'Taurus': '#4ecdc4', 'Gemini': '#ffe66d',
        'Cancer': '#a8e6cf', 'Leo': '#ffd93d', 'Virgo': '#95e1d3',
        'Libra': '#f38181', 'Scorpius': '#aa4465', 'Ophiuchus': '#8b5a8e',
        'Sagittarius': '#6a0572', 'Capricornus': '#3d5a80', 
        'Aquarius': '#5e6472', 'Pisces': '#98c1d9'
    }
    
    # Draw constellation boundaries
    prev_boundary = 0.0
    for i, (sign, boundary) in enumerate(boundaries):
        # Handle wrap-around for Pisces
        if i == len(boundaries) - 1:
            end = 360.0
        else:
            end = boundary
        
        # Draw constellation segment
        fig.add_trace(go.Scatter(
            x=[prev_boundary, end, end, prev_boundary, prev_boundary],
            y=[0, 0, 1, 1, 0],
            fill='toself',
            fillcolor=colors.get(sign, '#666666'),
            opacity=0.3,
            line=dict(color=colors.get(sign, '#666666'), width=2),
            name=sign,
            hovertemplate=f"<b>{sign}</b><br>Arc: {end - prev_boundary:.1f}°<extra></extra>",
            showlegend=False
        ))
        
        # Add sign label
        mid_point = (prev_boundary + end) / 2
        fig.add_annotation(
            x=mid_point,
            y=0.5,
            text=sign,
            showarrow=False,
            font=dict(size=10, color='white'),
            bgcolor=colors.get(sign, '#666666'),
            opacity=0.7,
            borderpad=4
        )
        
        prev_boundary = end
    
    # Add planetary positions
    y_positions = {'Sun': 1.5, 'Moon': 1.4, 'Mercury': 1.3, 'Venus': 1.2, 
                   'Mars': 1.1, 'Jupiter': 1.0, 'Saturn': 0.9, 
                   'Uranus': 0.8, 'Neptune': 0.7, 'Pluto': 0.6,
                   'Rahu': 0.5, 'Ketu': 0.4}
    
    planet_colors = {
        'Sun': '#ffd700', 'Moon': '#c0c0c0', 'Mercury': '#87ceeb',
        'Venus': '#ff69b4', 'Mars': '#ff4500', 'Jupiter': '#daa520',
        'Saturn': '#4169e1', 'Uranus': '#40e0d0', 'Neptune': '#6495ed',
        'Pluto': '#8b4513', 'Rahu': '#8b008b', 'Ketu': '#8b008b'
    }
    
    for planet, data in chart_data['luminosities'].items():
        lon = data['longitude']
        y_pos = y_positions.get(planet, 0.5)
        
        # Planet marker
        fig.add_trace(go.Scatter(
            x=[lon],
            y=[y_pos],
            mode='markers+text',
            marker=dict(
                size=12,
                color=planet_colors.get(planet, '#ffffff'),
                line=dict(color='white', width=2)
            ),
            text=[planet[0]],  # First letter
            textposition='middle center',
            textfont=dict(size=8, color='black', family='Arial Black'),
            name=planet,
            hovertemplate=f"<b>{planet}</b><br>" +
                         f"{data['sign']} {data['position_dms']}<br>" +
                         f"{data['trigger_status']}<br>" +
                         f"Longitude: {lon:.2f}°<extra></extra>",
            showlegend=False
        ))
    
    # Add Ascendant
    if 'Ascendant' in chart_data['angles']:
        asc = chart_data['angles']['Ascendant']
        fig.add_trace(go.Scatter(
            x=[asc['longitude']],
            y=[1.6],
            mode='markers+text',
            marker=dict(size=15, color='#00ff00', symbol='triangle-up', 
                       line=dict(color='white', width=2)),
            text=['ASC'],
            textposition='top center',
            textfont=dict(size=10, color='white'),
            name='Ascendant',
            hovertemplate=f"<b>Ascendant</b><br>" +
                         f"{asc['sign']} {asc['position_dms']}<extra></extra>",
            showlegend=False
        ))
    
    # Layout
    fig.update_layout(
        title="Linear Horizon Map: Ground 13-Sign Ecliptic",
        xaxis=dict(
            title="Ecliptic Longitude (°)",
            range=[0, 360],
            dtick=30,
            gridcolor='rgba(255,255,255,0.1)',
            showgrid=True
        ),
        yaxis=dict(
            title="",
            range=[0, 1.8],
            showticklabels=False,
            showgrid=False
        ),
        height=400,
        plot_bgcolor='#0a0e27',
        paper_bgcolor='#0a0e27',
        font=dict(color='#e0e0e0'),
        hovermode='closest'
    )
    
    return fig


def create_dasha_timeline(dasha_info, current_date):
    """
    Create a visual timeline of the 120-year Dasha cycle
    """
    fig = go.Figure()
    
    # Colors for each sign (same as horizon chart)
    colors = {
        'Aries': '#ff6b6b', 'Taurus': '#4ecdc4', 'Gemini': '#ffe66d',
        'Cancer': '#a8e6cf', 'Leo': '#ffd93d', 'Virgo': '#95e1d3',
        'Libra': '#f38181', 'Scorpius': '#aa4465', 'Ophiuchus': '#8b5a8e',
        'Sagittarius': '#6a0572', 'Capricornus': '#3d5a80', 
        'Aquarius': '#5e6472', 'Pisces': '#98c1d9'
    }
    
    # Plot each Maha Dasha period
    for i, period in enumerate(dasha_info['sequence']):
        start = period['start']
        end = period['end']
        lord = period['lord']
        
        # Check if this is the current period
        is_current = start <= current_date < end
        
        fig.add_trace(go.Bar(
            x=[end - start],
            y=[0],
            base=start,
            orientation='h',
            marker=dict(
                color=colors.get(lord, '#666666'),
                line=dict(color='white' if is_current else colors.get(lord, '#666666'), 
                         width=3 if is_current else 1)
            ),
            name=lord,
            text=lord,
            textposition='inside',
            textfont=dict(size=12, color='white'),
            hovertemplate=f"<b>{lord} Maha Dasha</b><br>" +
                         f"Start: {start.strftime('%Y-%m-%d')}<br>" +
                         f"End: {end.strftime('%Y-%m-%d')}<br>" +
                         f"Duration: {period.get('total_years', period.get('remaining_at_birth', 0)):.1f} years<extra></extra>",
            showlegend=False
        ))
    
    # Add current date marker
    fig.add_vline(
        x=current_date,
        line_dash="dash",
        line_color="#00ff00",
        line_width=2,
        annotation_text=f"Today: {current_date.strftime('%Y-%m-%d')}",
        annotation_position="top"
    )
    
    # Layout
    fig.update_layout(
        title="120-Year Dasha Cycle: Temporal Frequencies",
        xaxis=dict(
            title="Timeline",
            gridcolor='rgba(255,255,255,0.1)',
            type='date'
        ),
        yaxis=dict(
            showticklabels=False,
            showgrid=False
        ),
        barmode='overlay',
        height=300,
        plot_bgcolor='#0a0e27',
        paper_bgcolor='#0a0e27',
        font=dict(color='#e0e0e0'),
        hovermode='x unified'
    )
    
    return fig

# ==============================================================================
# HEADER
# ==============================================================================

st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='font-size: 3em; margin-bottom: 0;'>⭐ NORTH STAR</h1>
    <p style='font-size: 1.2em; color: #a8c5e6; margin-top: 0;'>
        13-Sign Ground Astrology | Consciousness-as-Ground
    </p>
    <p style='font-size: 0.9em; color: #8891a5;'>
        The chart is the mirror, not the prediction. The wholeperson recognizes itself through astronomical precision.
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==============================================================================
# TABS
# ==============================================================================

tab1, tab2, tab3 = st.tabs([
    "🌅 THE APERTURE (Natal Chart)",
    "🔍 THE CALIBRATION (Rectification)",
    "⏳ THE CURRENT FREQUENCY (Dasha)"
])

# ==============================================================================
# TAB 1: THE APERTURE (Natal Chart)
# ==============================================================================

with tab1:
    st.markdown("### Generate Your Natal Chart")
    st.markdown("*The aperture through which consciousness-as-ground recognizes its localized blueprint.*")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Birth Data")
        
        # Quick load button for North calibration
        if st.button("⭐ Load North Calibration", help="Load the test case: Nov 30, 1970, 11:47 AM NZST"):
            st.session_state['birth_date'] = datetime(1970, 11, 30)
            st.session_state['birth_time'] = "23:47:23"
            st.session_state['latitude'] = -38.1368
            st.session_state['longitude'] = 176.2497
            st.session_state['location_name'] = "Rotorua, New Zealand"
        
        # Birth date
        birth_date = st.date_input(
            "Birth Date",
            value=st.session_state.get('birth_date', datetime(1990, 1, 1)),
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now(),
            key='birth_date_input'
        )
        
        # Birth time (UTC)
        birth_time_str = st.text_input(
            "Birth Time (UTC)",
            value=st.session_state.get('birth_time', "12:00:00"),
            help="Format: HH:MM:SS (24-hour format)",
            key='birth_time_input'
        )
        
        # Location
        st.markdown("**Birth Location**")
        location_name = st.text_input(
            "Location Name (optional)",
            value=st.session_state.get('location_name', ""),
            key='location_name_input'
        )
        
        col_lat, col_lon = st.columns(2)
        with col_lat:
            latitude = st.number_input(
                "Latitude",
                value=st.session_state.get('latitude', 0.0),
                format="%.4f",
                help="North positive, South negative",
                key='latitude_input'
            )
        with col_lon:
            longitude = st.number_input(
                "Longitude",
                value=st.session_state.get('longitude', 0.0),
                format="%.4f",
                help="East positive, West negative",
                key='longitude_input'
            )
        
        # Calculate button
        if st.button("🌟 Calculate Chart", type="primary", use_container_width=True):
            try:
                # Parse birth time
                time_parts = birth_time_str.split(':')
                hour = int(time_parts[0])
                minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                second = int(time_parts[2]) if len(time_parts) > 2 else 0
                hour_decimal = hour + (minute / 60.0) + (second / 3600.0)
                
                # Calculate chart
                chart = engine.calculate_chart(
                    year=birth_date.year,
                    month=birth_date.month,
                    day=birth_date.day,
                    hour_utc=hour_decimal,
                    latitude=latitude,
                    longitude=longitude
                )
                
                st.session_state['current_chart'] = chart
                st.success("✓ Chart calculated successfully!")
                
            except Exception as e:
                st.error(f"Error calculating chart: {e}")
    
    with col2:
        if 'current_chart' in st.session_state:
            chart = st.session_state['current_chart']
            
            st.markdown("#### Linear Horizon Map")
            fig = create_linear_horizon_chart(chart)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### Luminosities: Planetary Apertures")
            
            # Create planetary table
            planet_data = []
            for planet, data in chart['luminosities'].items():
                planet_data.append({
                    'Planet': planet,
                    'Sign': data['sign'],
                    'Position': data['position_dms'],
                    'Longitude': f"{data['longitude']:.2f}°",
                    'House': data.get('house', ''),
                    'Status': data['trigger_status'],
                    'Speed': f"{data['speed']:.4f}°/day"
                })
            
            df = pd.DataFrame(planet_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Angles
            st.markdown("#### Angles")
            col_asc, col_mc = st.columns(2)
            
            with col_asc:
                if 'Ascendant' in chart['angles']:
                    asc = chart['angles']['Ascendant']
                    st.info(f"**Ascendant:** {asc['sign']} {asc['position_dms']}")
            
            with col_mc:
                if 'MC' in chart['angles']:
                    mc = chart['angles']['MC']
                    st.info(f"**MC:** {mc['sign']} {mc['position_dms']}")
            
            # Consciousness-as-Ground Interpretation
            with st.expander("📖 Consciousness-as-Ground Interpretation", expanded=True):
                st.markdown("##### Sun Placement")
                if 'Sun' in chart['luminosities']:
                    sun = chart['luminosities']['Sun']
                    st.markdown(f"""
                    **The Sun in {sun['sign']}** ({sun['position_dms']})
                    
                    The wholeperson expresses the core solar frequency through the {sun['sign']} aperture.
                    
                    *Trigger Status: {sun['trigger_status']}*
                    """)
                    
                    # Add sign interpretation from SIGN_INTERPRETATIONS
                    # (You would load this from your document or database)
                
                st.markdown("---")
                
                st.markdown("##### Birth Dasha")
                if 'dasha' in chart:
                    dasha = chart['dasha']
                    st.markdown(f"""
                    **Birth Dasha Lord:** {dasha['birth_dasha_lord']}
                    
                    The wholeperson entered manifestation during the {dasha['birth_dasha_lord']} frequency,
                    with {dasha['remaining_years']:.1f} years remaining in this Maha Dasha at birth.
                    
                    This temporal signature colors the entire incarnation's unfoldment.
                    """)
        else:
            st.info("👈 Enter birth data and click 'Calculate Chart' to see results")

# ==============================================================================
# TAB 2: THE CALIBRATION (Rectification)
# ==============================================================================

with tab2:
    st.markdown("### Birth Time Rectification")
    st.markdown("*Calibrating the precise temporal aperture through event correlation.*")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Approximate Birth Data")
        
        rect_date = st.date_input(
            "Birth Date",
            value=datetime(1970, 11, 30),
            key='rect_date'
        )
        
        approx_time = st.text_input(
            "Approximate UTC Time",
            value="23:47:23",
            help="Your best estimate (HH:MM:SS)",
            key='rect_time'
        )
        
        window_hours = st.slider(
            "Scan Window (±hours)",
            min_value=0.5,
            max_value=4.0,
            value=2.0,
            step=0.5,
            key='window'
        )
        
        step_minutes = st.selectbox(
            "Time Step (minutes)",
            options=[1, 5, 10, 15],
            index=1,
            key='step'
        )
        
        col_lat2, col_lon2 = st.columns(2)
        with col_lat2:
            rect_lat = st.number_input(
                "Latitude",
                value=-38.1368,
                format="%.4f",
                key='rect_lat'
            )
        with col_lon2:
            rect_lon = st.number_input(
                "Longitude",
                value=176.2497,
                format="%.4f",
                key='rect_lon'
            )
        
        st.markdown("#### Life Events")
        st.markdown("*Add at least 3 significant events for accurate calibration.*")
        
        # Initialize events in session state
        if 'life_events' not in st.session_state:
            st.session_state['life_events'] = []
        
        # Event input form
        with st.form("add_event_form"):
            event_date = st.date_input("Event Date", key='event_date_form')
            
            event_type = st.selectbox(
                "Event Type",
                options=[
                    'career_launch', 'relationship_start', 'relationship_end',
                    'financial_gain', 'financial_reset', 'restriction',
                    'spiritual_awakening', 'identity_realization',
                    'healing_crisis', 'loss', 'expansion', 'disruption'
                ],
                key='event_type_form'
            )
            
            event_desc = st.text_input("Description", key='event_desc_form')
            
            event_intensity = st.slider(
                "Intensity (1-10)",
                min_value=1,
                max_value=10,
                value=5,
                key='event_intensity_form'
            )
            
            if st.form_submit_button("Add Event"):
                st.session_state['life_events'].append({
                    'date': event_date.strftime('%Y-%m-%d'),
                    'type': event_type,
                    'description': event_desc,
                    'intensity': event_intensity
                })
                st.success("Event added!")
        
        # Display current events
        if st.session_state['life_events']:
            st.markdown("**Current Events:**")
            for i, event in enumerate(st.session_state['life_events']):
                st.text(f"{i+1}. {event['date']}: {event['description']}")
            
            if st.button("Clear All Events"):
                st.session_state['life_events'] = []
                st.rerun()
        
        # Run rectification
        if st.button("🔍 Run Rectification Scan", type="primary", use_container_width=True):
            if len(st.session_state['life_events']) < 1:
                st.warning("Please add at least one life event for calibration.")
            else:
                try:
                    # Parse time
                    time_parts = approx_time.split(':')
                    hour = int(time_parts[0])
                    minute = int(time_parts[1]) if len(time_parts) > 1 else 0
                    second = int(time_parts[2]) if len(time_parts) > 2 else 0
                    hour_decimal = hour + (minute / 60.0) + (second / 3600.0)
                    
                    with st.spinner("Scanning temporal apertures..."):
                        candidates = scanner.scan_window(
                            birth_date=(rect_date.year, rect_date.month, rect_date.day),
                            approx_time_utc=hour_decimal,
                            latitude=rect_lat,
                            longitude=rect_lon,
                            life_events=st.session_state['life_events'],
                            window_hours=window_hours,
                            step_minutes=step_minutes
                        )
                        
                        st.session_state['rect_candidates'] = candidates
                        st.success(f"✓ Scan complete! Found {len(candidates)} candidates.")
                
                except Exception as e:
                    st.error(f"Error during rectification: {e}")
    
    with col2:
        if 'rect_candidates' in st.session_state:
            candidates = st.session_state['rect_candidates']
            
            st.markdown("#### Ranked Candidates")
            
            # Top 5 candidates
            for i, candidate in enumerate(candidates[:5], 1):
                time_utc = candidate['time_utc']
                date = candidate['date']
                score = candidate['score']
                
                with st.expander(f"#{i} - Score: {score:.1f} | Time: {int(time_utc):02d}:{int((time_utc % 1) * 60):02d} UTC", 
                               expanded=(i==1)):
                    
                    col_a, col_b = st.columns(2)
                    
                    with col_a:
                        st.markdown(f"""
                        **Date:** {date[0]}-{date[1]:02d}-{date[2]:02d}  
                        **Time:** {time_utc:.4f} ({int(time_utc):02d}:{int((time_utc % 1) * 60):02d}:{int(((time_utc % 1) * 60 % 1) * 60):02d} UTC)  
                        **Total Score:** {score:.1f}
                        """)
                    
                    with col_b:
                        breakdown = candidate['scoring_breakdown']
                        st.markdown(f"""
                        **Scoring Breakdown:**
                        - Dasha Correlation: +{breakdown['dasha_correlation']}
                        - Event Type Match: +{breakdown['event_type_match']}
                        - Natal Boundaries: +{breakdown['natal_boundaries']}
                        - Transit Boundaries: +{breakdown['transit_boundaries']}
                        - Special Patterns: +{breakdown['special_patterns']}
                        """)
                    
                    # Key placements
                    chart = candidate['chart']
                    st.markdown("**Key Placements:**")
                    
                    placement_text = ""
                    if 'Sun' in chart['luminosities']:
                        sun = chart['luminosities']['Sun']
                        placement_text += f"☉ Sun: {sun['sign']} {sun['position_dms']} ({sun['trigger_status']})\n\n"
                    
                    if 'Moon' in chart['luminosities']:
                        moon = chart['luminosities']['Moon']
                        placement_text += f"☽ Moon: {moon['sign']} {moon['position_dms']} ({moon['trigger_status']})\n\n"
                    
                    if 'Ascendant' in chart['angles']:
                        asc = chart['angles']['Ascendant']
                        placement_text += f"ASC: {asc['sign']} {asc['position_dms']} ({asc['trigger_status']})"
                    
                    st.text(placement_text)
                    
                    # Notable triggers
                    triggers = candidate['triggers']
                    if triggers['natal_hard']:
                        st.success(f"**HARD Triggers:** {', '.join(triggers['natal_hard'][:3])}")
                    if triggers['special']:
                        st.info(f"**Special:** {', '.join(triggers['special'][:2])}")
        else:
            st.info("👈 Configure parameters and click 'Run Rectification Scan' to see results")

# ==============================================================================
# TAB 3: THE CURRENT FREQUENCY (Dasha)
# ==============================================================================

with tab3:
    st.markdown("### Dasha Timeline Visualization")
    st.markdown("*The 120-year cycle of temporal frequencies.*")
    
    # Use chart from Tab 1 if available
    if 'current_chart' in st.session_state:
        chart = st.session_state['current_chart']
        
        if 'dasha' in chart:
            dasha_info = chart['dasha']
            
            # Current date
            current_date = datetime(2026, 1, 28)
            
            st.markdown(f"**Current Date:** {current_date.strftime('%Y-%m-%d')}")
            
            # Timeline visualization
            fig = create_dasha_timeline(dasha_info, current_date)
            st.plotly_chart(fig, use_container_width=True)
            
            # Current frequency details
            current_dasha = engine.get_current_dasha(dasha_info, current_date)
            
            if current_dasha['status'] == 'active':
                st.markdown("---")
                st.markdown("### Current Frequency Analysis")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    maha = current_dasha['maha_dasha']
                    st.markdown(f"""
                    #### Maha Dasha: {maha['lord']}
                    
                    **Period:** {maha['start'].strftime('%Y-%m-%d')} to {maha['end'].strftime('%Y-%m-%d')}  
                    **Duration:** {maha.get('total_years', maha.get('remaining_at_birth', 0)):.1f} years
                    
                    The wholeperson is currently moving through the **{maha['lord']} frequency** 
                    at the Maha Dasha level.
                    """)
                
                with col2:
                    bhukti = current_dasha['bhukti']
                    st.markdown(f"""
                    #### Bhukti (Sub-Period): {bhukti['lord']}
                    
                    **Period:** {bhukti['start'].strftime('%Y-%m-%d')} to {bhukti['end'].strftime('%Y-%m-%d')}  
                    **Duration:** {bhukti['duration_years']:.2f} years
                    
                    Within the {maha['lord']} Maha Dasha, consciousness expresses through 
                    the **{bhukti['lord']} sub-frequency**.
                    """)
                
                st.markdown("---")
                
                st.info(f"""
                ### The {maha['lord']}-{bhukti['lord']} Confluence
                
                The wholeperson is experiencing the intersection of two temporal apertures:
                the broader {maha['lord']} cycle and the specific {bhukti['lord']} sub-cycle.
                
                This is not prediction, but recognition of the current vibrational signature
                through which consciousness-as-ground is expressing itself.
                """)
            else:
                st.warning("Current date exceeds the 120-year Dasha cycle.")
        else:
            st.warning("No Dasha information available. Calculate a chart in Tab 1 first.")
    else:
        st.info("👈 Calculate a natal chart in **The Aperture** tab to view Dasha timeline")

# ==============================================================================
# FOOTER
# ==============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; padding: 20px; color: #8891a5;'>
    <p><strong>SkyAsGround</strong> | ZeroArbitrary™ 13-Sign System</p>
    <p style='font-size: 0.9em;'>Consciousness-as-Ground Framework</p>
    <p style='font-size: 0.8em;'>The wholeperson recognizes itself through the Mirror of Reality.</p>
    <p style='font-size: 0.8em;'>© 2026 Howard North | <a href='https://www.skyasground.com' style='color: #8891a5;'>skyasground.com</a></p>
</div>
""", unsafe_allow_html=True)

