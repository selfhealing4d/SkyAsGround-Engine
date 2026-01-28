"""
NORTH STAR: Birth Time Rectification Scanner
The Calibration of Presence

ONTOLOGY: Consciousness-as-Ground
Rectification is not "finding the correct time" but recognizing which
temporal aperture allows life events to resonate with astronomical precision.

COORDINATE SYSTEM: Tropical J2000 Ecliptic (Ground Calibrated)
Uses the same Ground boundary calibration as ground_engine.py, where
Ophiuchus entry is set at 247.1° tropical (native's zero-point).

METHODOLOGY: Dual-Trigger Boundary Detection + Dasha Correlation
- HARD TRIGGER: ±0.01° (±36 arc-seconds)
- SOFT PROXIMITY: ±0.5° (±30 arc-minutes)
- Event-Dasha Correlation: Life events synchronized with Dasha transitions

Author: North Star Project
License: Consciousness-as-Ground Framework
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from ground_engine import GroundEngine
import swisseph as swe


class RectificationScanner:
    """
    The Calibration Tool: Scan birth time windows to find optimal alignment
    between life events and astronomical Dasha cycles.
    
    CONSCIOUSNESS-AS-GROUND: The rectification process reveals the precise
    temporal aperture through which the wholeperson entered manifestation.
    """
    
    def __init__(self, engine: Optional[GroundEngine] = None):
        """
        Initialize the scanner with a Ground Engine.
        
        Args:
            engine: GroundEngine instance (creates new one if None)
        """
        self.engine = engine if engine else GroundEngine()
        
        # Event type to Dasha lord mappings
        # Each event type resonates with specific planetary frequencies
        self.event_signatures = {
            # Mars/Aries frequencies: Action, conflict, initiation
            'career_launch': ['Aries', 'Leo', 'Sagittarius'],
            'conflict': ['Aries', 'Scorpius'],
            'surgery': ['Aries', 'Scorpius', 'Ophiuchus'],
            'competition': ['Aries', 'Leo'],
            
            # Venus frequencies: Relationship, beauty, resources
            'relationship_start': ['Taurus', 'Libra', 'Pisces'],
            'relationship_end': ['Libra', 'Scorpius', 'Aquarius'],
            'artistic_breakthrough': ['Taurus', 'Libra', 'Pisces'],
            'financial_gain': ['Taurus', 'Leo', 'Sagittarius'],
            
            # Saturn frequencies: Structure, restriction, responsibility
            'restriction': ['Capricornus', 'Aquarius', 'Virgo'],
            'responsibility': ['Capricornus', 'Virgo', 'Cancer'],
            'financial_reset': ['Capricornus', 'Scorpius', 'Aquarius'],
            'career_setback': ['Capricornus', 'Scorpius'],
            
            # Rahu/Ketu frequencies: Disruption, awakening, loss
            'disruption': ['Ophiuchus', 'Aquarius', 'Scorpius'],
            'spiritual_awakening': ['Ophiuchus', 'Pisces', 'Sagittarius'],
            'loss': ['Scorpius', 'Pisces', 'Cancer'],
            'radical_change': ['Ophiuchus', 'Aquarius', 'Aries'],
            
            # Mercury frequencies: Communication, learning, travel
            'education': ['Gemini', 'Virgo', 'Sagittarius'],
            'travel': ['Gemini', 'Sagittarius', 'Pisces'],
            'communication': ['Gemini', 'Libra', 'Aquarius'],
            'writing': ['Gemini', 'Virgo', 'Pisces'],
            
            # Jupiter frequencies: Expansion, philosophy, teaching
            'expansion': ['Sagittarius', 'Pisces', 'Leo'],
            'teaching': ['Sagittarius', 'Gemini', 'Virgo'],
            'philosophy': ['Sagittarius', 'Aquarius', 'Pisces'],
            'recognition': ['Leo', 'Sagittarius', 'Capricornus'],
            
            # Moon frequencies: Emotional, home, family
            'home_change': ['Cancer', 'Taurus', 'Capricornus'],
            'emotional_crisis': ['Cancer', 'Scorpius', 'Pisces'],
            'mother_event': ['Cancer', 'Virgo', 'Pisces'],
            'nurturing_role': ['Cancer', 'Virgo', 'Taurus'],
            
            # Ophiuchus frequencies: Healing, transmutation, identity
            'healing_crisis': ['Ophiuchus', 'Virgo', 'Scorpius'],
            'identity_realization': ['Ophiuchus', 'Leo', 'Aquarius'],
            'transmutation': ['Ophiuchus', 'Scorpius', 'Pisces'],
            'health_breakthrough': ['Ophiuchus', 'Virgo', 'Sagittarius'],
        }
        
        # Special trigger weights for identity-level events
        self.special_triggers = {
            'ophiuchus_mercury': 20,  # Mercury in Ophiuchus = Identity Realization
            'sun_boundary': 15,        # Sun at boundary = Core identity shift
            'moon_boundary': 12,       # Moon at boundary = Emotional transmutation
            'ascendant_hit': 18,       # Transit hits Ascendant = External manifestation
        }
    
    
    def scan_window(self,
                   birth_date: Tuple[int, int, int],
                   approx_time_utc: float,
                   latitude: float,
                   longitude: float,
                   life_events: List[Dict],
                   window_hours: float = 2.0,
                   step_minutes: int = 5) -> List[Dict]:
        """
        Scan a time window around approximate birth time to find optimal match.
        
        METHODOLOGY:
        1. Calculate charts for each time increment in window
        2. Score each chart based on:
           - Dasha-event correlations
           - Boundary triggers (natal + transits at event dates)
           - Special pattern recognition (e.g., Ophiuchus Mercury)
        3. Rank candidates by total score
        
        Args:
            birth_date: (year, month, day)
            approx_time_utc: Approximate UTC hour (decimal)
            latitude: Birth latitude (decimal degrees)
            longitude: Birth longitude (decimal degrees)
            life_events: List of event dictionaries with keys:
                - 'date': 'YYYY-MM-DD' or datetime object
                - 'type': Event type (see event_signatures)
                - 'description': Human description
                - 'intensity': 1-10 scale (optional)
            window_hours: ±hours to scan (default ±2)
            step_minutes: Time increment for scanning (default 5 min)
        
        Returns:
            List of candidate birth times ranked by score, each containing:
                - 'time_utc': Tested birth time
                - 'score': Total correlation score
                - 'chart': Full natal chart
                - 'event_matches': Details of event correlations
                - 'triggers': Boundary triggers found
        """
        print("\n" + "=" * 70)
        print("RECTIFICATION SCAN: The Calibration of Presence")
        print("=" * 70)
        print(f"Birth Date: {birth_date[0]}-{birth_date[1]:02d}-{birth_date[2]:02d}")
        print(f"Approximate UTC: {approx_time_utc:.2f} hours")
        print(f"Window: ±{window_hours} hours ({window_hours * 2} hour span)")
        print(f"Step: {step_minutes} minutes")
        print(f"Life Events: {len(life_events)}")
        print("=" * 70 + "\n")
        
        candidates = []
        
        # Calculate time range
        start_time = approx_time_utc - window_hours
        end_time = approx_time_utc + window_hours
        step_hours = step_minutes / 60.0
        
        # Scan through time window
        current_time = start_time
        scan_count = 0
        
        while current_time <= end_time:
            # Ensure time is within 0-24 hour range
            test_time = current_time % 24
            test_day = birth_date[2]
            test_month = birth_date[1]
            test_year = birth_date[0]
            
            # Adjust date if time wrapped around midnight
            if current_time < 0:
                # Time before midnight - use previous day
                test_date = datetime(test_year, test_month, test_day) - timedelta(days=1)
                test_day = test_date.day
                test_month = test_date.month
                test_year = test_date.year
                test_time = 24 + current_time
            elif current_time >= 24:
                # Time after midnight - use next day
                test_date = datetime(test_year, test_month, test_day) + timedelta(days=1)
                test_day = test_date.day
                test_month = test_date.month
                test_year = test_date.year
                test_time = current_time - 24
            
            # Calculate chart for this time
            try:
                chart = self.engine.calculate_chart(
                    year=test_year,
                    month=test_month,
                    day=test_day,
                    hour_utc=test_time,
                    latitude=latitude,
                    longitude=longitude
                )
                
                # Score this candidate
                score_result = self.score_candidate(
                    chart=chart,
                    life_events=life_events,
                    latitude=latitude,
                    longitude=longitude
                )
                
                candidates.append({
                    'time_utc': test_time,
                    'date': (test_year, test_month, test_day),
                    'score': score_result['total_score'],
                    'chart': chart,
                    'event_matches': score_result['event_matches'],
                    'triggers': score_result['triggers'],
                    'scoring_breakdown': score_result['breakdown'],
                })
                
                scan_count += 1
                
            except Exception as e:
                print(f"  Error at time {test_time:.4f}: {e}")
            
            current_time += step_hours
        
        # Sort by score (highest first)
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        print(f"\nScanned {scan_count} time points")
        print(f"Top candidate score: {candidates[0]['score'] if candidates else 0}")
        print()
        
        return candidates
    
    
    def score_candidate(self,
                       chart: Dict,
                       life_events: List[Dict],
                       latitude: float,
                       longitude: float) -> Dict:
        """
        Score a natal chart candidate based on event correlations and triggers.
        
        SCORING METHODOLOGY:
        
        PRIMARY SCORE: Dasha-Event Correlation
        - Event within ±30 days of Dasha transition: +10 points
        - Event type matches Dasha lord: +5 points
        - High intensity event (8-10): +3 bonus points
        
        SECONDARY SCORE: Boundary Hits
        - HARD_TRIGGER in natal chart: +8 points per trigger
        - SOFT_PROXIMITY in natal chart: +4 points per trigger
        - Transit HARD_TRIGGER at event date: +6 points
        - Transit SOFT_PROXIMITY at event: +3 points
        
        SPECIAL PATTERNS:
        - Ophiuchus Mercury trigger: +20 points (Identity Realization)
        - Sun at boundary: +15 points (Core identity shift)
        - Moon at boundary: +12 points (Emotional transmutation)
        - Transit hits Ascendant: +18 points
        
        Args:
            chart: Natal chart dictionary
            life_events: List of life event dictionaries
            latitude, longitude: Birth location
        
        Returns:
            Dictionary with total_score, event_matches, triggers, breakdown
        """
        total_score = 0
        event_matches = []
        triggers = {
            'natal_hard': [],
            'natal_soft': [],
            'transit_hard': [],
            'transit_soft': [],
            'special': [],
        }
        breakdown = {
            'dasha_correlation': 0,
            'event_type_match': 0,
            'natal_boundaries': 0,
            'transit_boundaries': 0,
            'special_patterns': 0,
        }
        
        # Check natal chart boundary triggers
        natal_hard_count = 0
        natal_soft_count = 0
        
        for planet, data in chart['luminosities'].items():
            if data['trigger_status'] == 'HARD_TRIGGER':
                natal_hard_count += 1
                triggers['natal_hard'].append(f"{planet} in {data['sign']}")
                total_score += 8
                breakdown['natal_boundaries'] += 8
                
            elif data['trigger_status'] == 'SOFT_PROXIMITY':
                natal_soft_count += 1
                triggers['natal_soft'].append(f"{planet} in {data['sign']}")
                total_score += 4
                breakdown['natal_boundaries'] += 4
        
        # Check for special natal patterns
        if 'Mercury' in chart['luminosities']:
            merc = chart['luminosities']['Mercury']
            if merc['sign'] == 'Ophiuchus':
                triggers['special'].append("Mercury in Ophiuchus (Identity Realization)")
                total_score += self.special_triggers['ophiuchus_mercury']
                breakdown['special_patterns'] += self.special_triggers['ophiuchus_mercury']
        
        if 'Sun' in chart['luminosities']:
            sun = chart['luminosities']['Sun']
            if sun['trigger_status'] in ['HARD_TRIGGER', 'SOFT_PROXIMITY']:
                triggers['special'].append(f"Sun boundary: {sun['sign']}")
                total_score += self.special_triggers['sun_boundary']
                breakdown['special_patterns'] += self.special_triggers['sun_boundary']
        
        if 'Moon' in chart['luminosities']:
            moon = chart['luminosities']['Moon']
            if moon['trigger_status'] in ['HARD_TRIGGER', 'SOFT_PROXIMITY']:
                triggers['special'].append(f"Moon boundary: {moon['sign']}")
                total_score += self.special_triggers['moon_boundary']
                breakdown['special_patterns'] += self.special_triggers['moon_boundary']
        
        # Score each life event
        for event in life_events:
            event_score = 0
            event_notes = []
            
            # Parse event date
            if isinstance(event['date'], str):
                event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            else:
                event_date = event['date']
            
            event_type = event.get('type', 'unknown')
            intensity = event.get('intensity', 5)
            
            # Get current Dasha at event date
            current_dasha = self.engine.get_current_dasha(
                chart['dasha'],
                event_date
            )
            
            if current_dasha['status'] == 'active':
                maha_lord = current_dasha['maha_dasha']['lord']
                bhukti_lord = current_dasha['bhukti']['lord']
                
                # Check if event date is near Dasha transition
                maha_start = current_dasha['maha_dasha']['start']
                bhukti_start = current_dasha['bhukti']['start']
                
                days_from_maha_start = abs((event_date - maha_start).days)
                days_from_bhukti_start = abs((event_date - bhukti_start).days)
                
                if days_from_maha_start <= 30:
                    event_score += 10
                    event_notes.append(f"±30 days from Maha Dasha transition ({maha_lord})")
                    breakdown['dasha_correlation'] += 10
                
                if days_from_bhukti_start <= 30:
                    event_score += 10
                    event_notes.append(f"±30 days from Bhukti transition ({maha_lord}-{bhukti_lord})")
                    breakdown['dasha_correlation'] += 10
                
                # Check event type signature match
                if event_type in self.event_signatures:
                    matching_signs = self.event_signatures[event_type]
                    if maha_lord in matching_signs:
                        event_score += 5
                        event_notes.append(f"Maha lord {maha_lord} matches event type")
                        breakdown['event_type_match'] += 5
                    if bhukti_lord in matching_signs:
                        event_score += 5
                        event_notes.append(f"Bhukti lord {bhukti_lord} matches event type")
                        breakdown['event_type_match'] += 5
                
                # Intensity bonus for strong events
                if intensity >= 8 and event_score > 0:
                    event_score += 3
                    event_notes.append(f"High intensity event (bonus)")
                    breakdown['dasha_correlation'] += 3
            
            # Check transits at event date
            transit_triggers = self.check_event_transits(
                event_date,
                chart,
                latitude,
                longitude
            )
            
            # Score transit triggers
            for trigger in transit_triggers['hard']:
                event_score += 6
                event_notes.append(f"Transit HARD: {trigger}")
                triggers['transit_hard'].append(f"{event_date.date()}: {trigger}")
                breakdown['transit_boundaries'] += 6
            
            for trigger in transit_triggers['soft']:
                event_score += 3
                event_notes.append(f"Transit SOFT: {trigger}")
                triggers['transit_soft'].append(f"{event_date.date()}: {trigger}")
                breakdown['transit_boundaries'] += 3
            
            # Special: Check for Ascendant hits
            if 'Ascendant' in chart['angles']:
                asc_lon = chart['angles']['Ascendant']['longitude']
                for trigger in transit_triggers['hard']:
                    if 'Ascendant' in trigger or abs(asc_lon - transit_triggers.get('longitude', 999)) < 1.0:
                        event_score += 18
                        event_notes.append("Transit conjunct Ascendant")
                        triggers['special'].append(f"{event_date.date()}: Ascendant hit")
                        breakdown['special_patterns'] += 18
                        break
            
            # Add to total
            total_score += event_score
            
            event_matches.append({
                'date': event_date,
                'type': event_type,
                'description': event.get('description', ''),
                'score': event_score,
                'notes': event_notes,
                'dasha': current_dasha if current_dasha['status'] == 'active' else None,
            })
        
        return {
            'total_score': total_score,
            'event_matches': event_matches,
            'triggers': triggers,
            'breakdown': breakdown,
        }
    
    
    def check_event_transits(self,
                            event_date: datetime,
                            natal_chart: Dict,
                            latitude: float,
                            longitude: float) -> Dict:
        """
        Check transits at event date for boundary triggers and natal conjunctions.
        
        COORDINATE SYSTEM: Tropical J2000 Ecliptic (Ground Calibrated)
        Uses tropical positions to match against Ground boundaries.
        
        SPECIAL FOCUS: Ophiuchus Mercury transits conjunct natal Moon
        
        Args:
            event_date: Date of the life event
            natal_chart: The candidate natal chart
            latitude, longitude: Birth location
        
        Returns:
            Dictionary with 'hard' and 'soft' trigger lists
        """
        triggers = {'hard': [], 'soft': [], 'conjunctions': []}
        
        # Calculate transit chart for event date (tropical coordinates)
        try:
            # Convert event_date to UTC time (use noon as default)
            jd = swe.julday(event_date.year, event_date.month, event_date.day, 12.0)
            
            # Get transit positions (tropical - no FLG_SIDEREAL)
            transit_positions = {}
            
            for planet_name, planet_id in self.engine.planets.items():
                result = swe.calc_ut(jd, planet_id, swe.FLG_SPEED)
                lon = result[0][0]  # Tropical longitude
                sign, status, degrees_into = self.engine.get_constellation(lon)
                
                transit_positions[planet_name] = {
                    'longitude': lon,
                    'sign': sign,
                    'status': status,
                }
                
                # Check for boundary triggers
                if status == 'HARD_TRIGGER':
                    triggers['hard'].append(f"{planet_name} at {sign} boundary")
                elif status == 'SOFT_PROXIMITY':
                    triggers['soft'].append(f"{planet_name} near {sign} boundary")
                
                # Check for conjunctions with natal planets
                for natal_planet, natal_data in natal_chart['luminosities'].items():
                    orb = abs(lon - natal_data['longitude'])
                    if orb > 180:
                        orb = 360 - orb
                    
                    if orb <= 2.0:  # 2° orb for conjunction
                        conj_str = f"Transit {planet_name} conjunct Natal {natal_planet}"
                        triggers['conjunctions'].append(conj_str)
                        
                        # SPECIAL: Ophiuchus Mercury conjunct Natal Moon
                        if (planet_name == 'Mercury' and 
                            sign == 'Ophiuchus' and 
                            natal_planet == 'Moon'):
                            triggers['hard'].append(
                                f"⚡ OPHIUCHUS MERCURY CONJUNCT NATAL MOON (Identity Realization)"
                            )
        
        except Exception as e:
            print(f"  Transit calculation error: {e}")
        
        return triggers
    
    
    def format_scan_report(self, candidates: List[Dict], top_n: int = 5) -> str:
        """
        Generate a human-readable report of the rectification scan results.
        
        CONSCIOUSNESS-AS-GROUND: The report reveals which temporal aperture
        creates maximum resonance between life events and cosmic geometry.
        
        Args:
            candidates: List of candidate results from scan_window()
            top_n: Number of top candidates to include in report
        
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 70)
        report.append("RECTIFICATION SCAN RESULTS")
        report.append("The Calibration of Presence")
        report.append("=" * 70)
        report.append("")
        
        if not candidates:
            report.append("No candidates found. Check scan parameters.")
            return "\n".join(report)
        
        # Summary statistics
        report.append(f"Total candidates scanned: {len(candidates)}")
        report.append(f"Score range: {candidates[-1]['score']:.1f} to {candidates[0]['score']:.1f}")
        report.append("")
        
        # Top candidates
        report.append("-" * 70)
        report.append(f"TOP {min(top_n, len(candidates))} CANDIDATES")
        report.append("-" * 70)
        report.append("")
        
        for i, candidate in enumerate(candidates[:top_n], 1):
            date = candidate['date']
            time_utc = candidate['time_utc']
            
            report.append(f"#{i} - SCORE: {candidate['score']:.1f}")
            report.append(f"    Date: {date[0]}-{date[1]:02d}-{date[2]:02d}")
            report.append(f"    Time (UTC): {time_utc:.4f} ({int(time_utc):02d}:{int((time_utc % 1) * 60):02d})")
            report.append("")
            
            # Scoring breakdown
            breakdown = candidate['scoring_breakdown']
            report.append("    Scoring Breakdown:")
            report.append(f"      Dasha Correlation:    +{breakdown['dasha_correlation']}")
            report.append(f"      Event Type Matches:   +{breakdown['event_type_match']}")
            report.append(f"      Natal Boundaries:     +{breakdown['natal_boundaries']}")
            report.append(f"      Transit Boundaries:   +{breakdown['transit_boundaries']}")
            report.append(f"      Special Patterns:     +{breakdown['special_patterns']}")
            report.append("")
            
            # Key placements
            chart = candidate['chart']
            if 'Sun' in chart['luminosities']:
                sun = chart['luminosities']['Sun']
                report.append(f"    Sun: {sun['sign']} {sun['position_dms']} - {sun['trigger_status']}")
            if 'Moon' in chart['luminosities']:
                moon = chart['luminosities']['Moon']
                report.append(f"    Moon: {moon['sign']} {moon['position_dms']} - {moon['trigger_status']}")
            if 'Ascendant' in chart['angles']:
                asc = chart['angles']['Ascendant']
                report.append(f"    Ascendant: {asc['sign']} {asc['position_dms']} - {asc['trigger_status']}")
            report.append("")
            
            # Notable triggers
            triggers = candidate['triggers']
            if triggers['natal_hard']:
                report.append(f"    Natal HARD Triggers: {', '.join(triggers['natal_hard'])}")
            if triggers['special']:
                report.append(f"    Special Patterns: {', '.join(triggers['special'][:3])}")
            
            report.append("")
            report.append("-" * 70)
            report.append("")
        
        report.append("=" * 70)
        report.append("The wholeperson recognizes the precise temporal aperture")
        report.append("through which consciousness entered this manifestation.")
        report.append("=" * 70)
        
        return "\n".join(report)


# ==============================================================================
# TEST CASE: EVENT VALIDATION
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("RECTIFICATION SCANNER - EVENT VALIDATION TEST")
    print("=" * 70 + "\n")
    
    # Initialize engine and scanner
    engine = GroundEngine()
    scanner = RectificationScanner(engine)
    
    # TEST EVENT: December 29, 2025, 8:11 PM NZDT
    # Expected: Transiting Mercury at ~14° Ophiuchus conjunct Natal Moon
    
    print("Test Event: December 29, 2025, 8:11 PM NZDT")
    print("Expected: Mercury ~14° Ophiuchus conjunct Natal Moon")
    print()
    
    # Convert NZDT to UTC
    # NZDT = UTC+13, so 8:11 PM NZDT = 7:11 AM UTC same day
    event_date_utc = datetime(2025, 12, 29, 7, 11)
    
    # Calculate transit chart for event
    jd = swe.julday(2025, 12, 29, 7.183333)  # 7:11 AM UTC
    
    print("Transit positions at event:")
    print("-" * 70)
    
    for planet_name, planet_id in engine.planets.items():
        try:
            result = swe.calc_ut(jd, planet_id, swe.FLG_SPEED)  # Tropical
            lon = result[0][0]
            sign, status, degrees_into = engine.get_constellation(lon)
            deg, min_val, sec = engine.decimal_to_dms(degrees_into)
            
            print(f"{planet_name:12s} {sign:12s} {deg:2d}°{min_val:02d}'{sec:02d}\" - {status}")
            
            if planet_name == 'Mercury':
                if sign == 'Ophiuchus' and 13 <= degrees_into <= 15:
                    print(f"  ✓✓ VALIDATION PASSED: Mercury at ~14° Ophiuchus")
                else:
                    print(f"  ⚠ CHECK: Mercury position differs from expected")
        
        except Exception as e:
            print(f"  Error: {e}")
    
    print()
    
    # Now test rectification with North's chart
    print("=" * 70)
    print("RECTIFICATION SCAN TEST")
    print("=" * 70)
    print()
    
    # Birth data (approximate)
    birth_date = (1970, 11, 30)
    approx_time_utc = 23.789  # Nov 29, 23:47:23 UTC
    latitude = -38.1368
    longitude = 176.2497
    
    # Life events for testing
    test_events = [
        {
            'date': '2025-12-29',
            'type': 'identity_realization',
            'description': 'Mercury conjunct Moon event',
            'intensity': 10,
        },
    ]
    
    # Scan a small window around the known time
    candidates = scanner.scan_window(
        birth_date=birth_date,
        approx_time_utc=approx_time_utc,
        latitude=latitude,
        longitude=longitude,
        life_events=test_events,
        window_hours=0.5,  # ±30 minutes for quick test
        step_minutes=10
    )
    
    # Display results
    print(scanner.format_scan_report(candidates, top_n=3))
    
    # Check if the correct time scores highest
    if candidates:
        top_candidate = candidates[0]
        if abs(top_candidate['time_utc'] - approx_time_utc) < 0.1:
            print("\n✓✓ VALIDATION PASSED: Correct birth time scored highest")
        else:
            print(f"\n⚠ Top candidate time: {top_candidate['time_utc']:.4f} vs expected {approx_time_utc:.4f}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70 + "\n")
