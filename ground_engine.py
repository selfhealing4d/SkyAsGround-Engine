"""
SKY AS GROUND: 13-Sign True Sidereal Alignment Engine
GROUND Engine - Core Calculation System

ONTOLOGY: Consciousness-as-Ground
The chart is not prediction but recognition - the ground-of-being
observing its own localized blueprint through precise astronomical geometry.

ASTRONOMICAL STANDARDS:
- Ephemeris: Swiss Ephemeris (Fagan/Bradley Ayanamsha)
- Zodiac: 13-Sign IAU J2000 Ecliptic Boundaries
- House System: Whole-Sign (Constellation-as-House)
- Dasha: 120-Year Proportional Cycle (Actual Ecliptic Path)

© 2026 Howard North | SkyAsGround.com
Licensed under Creative Commons BY-NC-ND 4.0: https://creativecommons.org
 
"""

import swisseph as swe
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import math


class GroundEngine:
    """
    The Aperture Calculator: Precise IAU-boundary astronomical computation
    for consciousness recognizing itself through celestial geometry.
    """
    
    def __init__(self):
        """
        Initialize the engine with ZeroArbitrary™ IAU Gates.
        Calculated in Degrees and Minutes (DMS) for absolute precessional alignment.
        """
        
        # PHYSICAL GROUND: 13 IAU Ecliptic Gates (J2000)
        # We use decimal conversions of exact Degrees and Minutes.
        self.iau_gates = [
            ("Aries", 29 + 6/60),          # 29° 06'
            ("Taurus", 53 + 24/60),        # 53° 24'
            ("Gemini", 90 + 6/60),         # 90° 06'
            ("Cancer", 118 + 0/60),        # 118° 00'
            ("Leo", 138 + 6/60),          # 138° 06'
            ("Virgo", 173 + 54/60),        # 173° 54'
            ("Libra", 217 + 48/60),        # 217° 48'
            ("Scorpius", 241 + 6/60),      # 241° 06'
            ("Ophiuchus", 248 + 0/60),     # 248° 00' (The Sacred Gap / North Point)
            ("Sagittarius", 266 + 18/60),  # 266° 18'
            ("Capricornus", 299 + 42/60),  # 299° 42'
            ("Aquarius", 327 + 54/60),     # 327° 54'
            ("Pisces", 351 + 36/60)        # 351° 36'
        ]
        
        # PROPORTIONAL DASHA: 120-Year cycle locked to Physical Arc Length.
        # No symbolic rulers. The frequency follows the Ecliptic Sequence.
        self.dasha_info = {}
        for i in range(len(self.iau_gates)):
            name, start = self.iau_gates[i]
            _, end = self.iau_gates[(i + 1) % 13]
            arc = (end - start) % 360
            self.dasha_info[name] = round((arc / 360) * 120, 2)
        
        # Dual-Trigger Boundary Thresholds
        self.HARD_TRIGGER = 0.01   # ±36 arc-seconds
        self.SOFT_PROXIMITY = 0.5   # ±30 arc-minutes
        
        # Planet indices for Swiss Ephemeris
        self.planets = {
            'Sun': swe.SUN, 'Moon': swe.MOON, 'Mercury': swe.MERCURY,
            'Venus': swe.VENUS, 'Mars': swe.MARS, 'Jupiter': swe.JUPITER,
            'Saturn': swe.SATURN, 'Uranus': swe.URANUS, 'Neptune': swe.NEPTUNE,
            'Pluto': swe.PLUTO, 'Rahu': swe.MEAN_NODE,
        }
        
        # 13-HOUSE SYSTEM: Constellation-as-House
        self.house_archetypes = {
            1: "Aries: The Impulse of Emergence",
            2: "Taurus: The Density of Being",
            3: "Gemini: The Resonance of Connection",
            4: "Cancer: The Internal Sanctuary",
            5: "Leo: The Radiant Recognition",
            6: "Virgo: The Systemic Alignment",
            7: "Libra: The Harmonic Mirror",
            8: "Scorpius: The Narrow Gate",
            9: "Ophiuchus: The Sacred Bridge",
            10: "Sagittarius: The Directional Truth",
            11: "Capricornus: The Manifest Architecture",
            12: "Aquarius: The Collective Flow",
            13: "Pisces: The Boundless Return",
        }
    
    def normalize_longitude(self, lon: float) -> float:
        return lon % 360
    
    def get_constellation(self, lon: float) -> Tuple[str, str, float]:
        """
        Identifies the physical constellation and its trigger status.
        """
        lon = self.normalize_longitude(lon)
        
        # 1. Identify Status
        status = "STABLE"
        for _, start in self.iau_gates:
            diff = abs(lon - start)
            if diff < self.HARD_TRIGGER:
                status = "HARD_TRIGGER"
                break
            elif diff < self.SOFT_PROXIMITY:
                status = "SOFT_PROXIMITY"
                break
        
        # 2. Identify Constellation
        current_name = "Unknown"
        deg_into = 0.0
        
        for i in range(len(self.iau_gates)):
            name, start = self.iau_gates[i]
            _, end = self.iau_gates[(i + 1) % 13]
            
            if start < end:
                if start <= lon < end:
                    current_name = name
                    deg_into = lon - start
            else: # Pisces Wrap
                if lon >= start or lon < end:
                    current_name = name
                    deg_into = (lon - start) % 360
                    
        return current_name, status, deg_into
    
    
    def decimal_to_dms(self, decimal_degrees: float) -> Tuple[int, int, int]:
        """
        Convert decimal degrees to degrees, minutes, seconds.
        The ground-of-being expressing through numerical precision.
        """
        degrees = int(decimal_degrees)
        minutes_decimal = (decimal_degrees - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = int((minutes_decimal - minutes) * 60)
        return (degrees, minutes, seconds)
    
    
    def calculate_chart(self, 
                       year: int, 
                       month: int, 
                       day: int, 
                       hour_utc: float,
                       latitude: float,
                       longitude: float) -> Dict:
        """
        Calculate a complete natal chart with precise IAU boundaries.
        
        LUMINOSITIES OF THE GROUND: Each planetary position represents
        consciousness expressing through specific astronomical apertures.
        
        COORDINATE SYSTEM: Tropical J2000 ecliptic coordinates
        The IAU constellation boundaries are defined in J2000 ecliptic coordinates,
        which are tropical (fixed to J2000 vernal equinox). We use tropical
        planetary positions to match against these physical astronomical boundaries.
        
        Args:
            year, month, day: Birth date
            hour_utc: Birth time in UTC (decimal hours, e.g., 23.789 = 23:47:23)
            latitude: Birth latitude in decimal degrees (North positive, South negative)
            longitude: Birth longitude in decimal degrees (East positive, West negative)
        
        Returns:
            Dictionary containing:
                - planets: {planet_name: {lon, lat, speed, sign, status, house, ...}}
                - angles: Ascendant, MC with sign placements
                - houses: List of 12 house boundaries (whole-sign system)
                - dasha_sequence: Birth Dasha information
        """
        # Set topocentric coordinates for the birth location
        # This ensures planetary positions are calculated from the observer's exact position
        # Altitude default: 0 meters (sea level approximation)
        swe.set_topo(longitude, latitude, 0)
        
        # Calculate Julian Day for ephemeris lookup
        jd = swe.julday(year, month, day, hour_utc)
        
        chart = {
            'birth_data': {
                'year': year,
                'month': month,
                'day': day,
                'hour_utc': hour_utc,
                'latitude': latitude,
                'longitude': longitude,
                'julian_day': jd,
                'coordinate_system': 'Tropical J2000 Ecliptic (IAU)',
            },
            'luminosities': {},  # Planetary placements (luminosities of consciousness)
            'angles': {},
            'houses': [],
            'dasha': {},
        }
        
        # Calculate planetary luminosities (tropical J2000 ecliptic positions)
        # Using default flags (tropical) to match IAU constellation boundaries
        for planet_name, planet_id in self.planets.items():
            try:
                # Get tropical position (J2000 ecliptic coordinates)
                # No FLG_SIDEREAL - we use tropical to match IAU boundaries
                result = swe.calc_ut(jd, planet_id, swe.FLG_SPEED)
                lon = result[0][0]  # Tropical ecliptic longitude (J2000)
                lat = result[0][1]  # Celestial latitude
                speed = result[0][3]  # Daily motion in longitude
                
                # Determine constellation and trigger status
                sign, status, degrees_into = self.get_constellation(lon)
                
                # Convert to degrees/minutes/seconds for readability
                deg, min_val, sec = self.decimal_to_dms(degrees_into)
                
                chart['luminosities'][planet_name] = {
                    'longitude': lon,
                    'latitude': lat,
                    'speed': speed,
                    'sign': sign,
                    'trigger_status': status,
                    'degrees_into_sign': degrees_into,
                    'position_dms': f"{deg}°{min_val}'{sec}\"",
                    'retrograde': speed < 0,
                }
            except Exception as e:
                print(f"Error calculating {planet_name}: {e}")
        
        # Calculate Ketu (South Node) - opposite of Rahu
        if 'Rahu' in chart['luminosities']:
            rahu_lon = chart['luminosities']['Rahu']['longitude']
            ketu_lon = self.normalize_longitude(rahu_lon + 180.0)
            sign, status, degrees_into = self.get_constellation(ketu_lon)
            deg, min_val, sec = self.decimal_to_dms(degrees_into)
            
            chart['luminosities']['Ketu'] = {
                'longitude': ketu_lon,
                'latitude': 0.0,
                'speed': -chart['luminosities']['Rahu']['speed'],
                'sign': sign,
                'trigger_status': status,
                'degrees_into_sign': degrees_into,
                'position_dms': f"{deg}°{min_val}'{sec}\"",
                'retrograde': False,
            }
        
        # Calculate Ascendant and MC
        try:
            # Get house cusps using Placidus for accurate angles
            # Returns tropical J2000 ecliptic coordinates
            cusps, ascmc = swe.houses_ex(jd, latitude, longitude, b'P')
            
            # Ascendant (Eastern Horizon) - Index 0 in ascmc array
            # Already in tropical J2000 ecliptic coordinates - matches IAU boundaries
            asc_lon = ascmc[0]
            
            sign, status, degrees_into = self.get_constellation(asc_lon)
            deg, min_val, sec = self.decimal_to_dms(degrees_into)
            
            chart['angles']['Ascendant'] = {
                'longitude': asc_lon,
                'sign': sign,
                'trigger_status': status,
                'degrees_into_sign': degrees_into,
                'position_dms': f"{deg}°{min_val}'{sec}\"",
            }
            
            # MC (Midheaven) - Index 1 in ascmc array
            mc_lon = ascmc[1]
            
            sign, status, degrees_into = self.get_constellation(mc_lon)
            deg, min_val, sec = self.decimal_to_dms(degrees_into)
            
            chart['angles']['MC'] = {
                'longitude': mc_lon,
                'sign': sign,
                'trigger_status': status,
                'degrees_into_sign': degrees_into,
                'position_dms': f"{deg}°{min_val}'{sec}\"",
            }
            
        except Exception as e:
            print(f"Error calculating angles: {e}")
        
        # Calculate Houses (Whole-Sign from Ascendant)
        if 'Ascendant' in chart['angles']:
            chart['houses'] = self.calculate_houses(
                chart['angles']['Ascendant']['sign'],
                chart['angles']['Ascendant']['longitude']
            )
            
            # Assign house numbers to planets
            for planet_name, planet_data in chart['luminosities'].items():
                planet_data['house'] = self.get_house_number(
                    planet_data['longitude'],
                    chart['houses']
                )
        
        # Calculate Birth Dasha
        if 'Moon' in chart['luminosities']:
            chart['dasha'] = self.calculate_birth_dasha(
                chart['luminosities']['Moon']['longitude'],
                year, month, day, hour_utc
            )
        
        return chart
    
    
    def calculate_houses(self, asc_sign: str, asc_lon: float) -> List[Dict]:
        """
        Calculate Whole-Sign houses starting from Ascendant constellation.
        
        CONSCIOUSNESS-AS-GROUND: Each house is an aperture through which
        the ground-of-being expresses in different domains of experience.
        
        Args:
            asc_sign: The constellation containing the Ascendant
            asc_lon: Ascendant longitude (for reference)
        
        Returns:
            List of 12 houses with boundaries and ruling signs
        """
        # Find the index of the Ascendant sign
        sign_sequence = [sign for sign, _ in self.boundaries]
        
        try:
            asc_index = sign_sequence.index(asc_sign)
        except ValueError:
            asc_index = 0  # Default to Aries if error
        
        houses = []
        
        for house_num in range(1, 13):
            # Rotate through signs starting from Ascendant
            sign_index = (asc_index + house_num - 1) % 13
            sign_name = sign_sequence[sign_index]
            
            # Get constellation boundaries
            sign_end = self.boundaries[sign_index][1]
            if sign_index == 0:
                sign_start = 0.0
            else:
                sign_start = self.boundaries[sign_index - 1][1]
            
            houses.append({
                'house_number': house_num,
                'ruling_sign': sign_name,
                'start_longitude': sign_start,
                'end_longitude': sign_end,
                'archetype': self.house_archetypes.get(house_num, ""),
            })
        
        return houses
    
    
    def get_house_number(self, planet_lon: float, houses: List[Dict]) -> int:
        """
        Determine which house a planet occupies.
        The wholeperson's luminosity expressing through a specific domain.
        """
        planet_lon = self.normalize_longitude(planet_lon)
        
        for house in houses:
            start = house['start_longitude']
            end = house['end_longitude']
            
            # Handle wrap-around at Pisces/Aries boundary
            if start > end:  # Pisces wrapping to Aries
                if planet_lon >= start or planet_lon < end:
                    return house['house_number']
            else:
                if start <= planet_lon < end:
                    return house['house_number']
        
        return 1  # Default to 1st house if calculation error
    
    
    def calculate_birth_dasha(self, 
                             moon_lon: float,
                             year: int,
                             month: int,
                             day: int,
                             hour_utc: float) -> Dict:
        """
        Calculate the Birth Dasha (Maha Dasha at birth) and subsequent sequence.
        
        The Dasha system follows the actual ecliptic path:
        Aries → Taurus → ... → Scorpius → Ophiuchus → Sagittarius → ...
        
        Birth Dasha is determined by Moon's position, and the sequence
        continues from there for 120 years (full zodiac cycle).
        
        Args:
            moon_lon: Moon's sidereal longitude at birth
            year, month, day, hour_utc: Birth date/time
        
        Returns:
            Dictionary with birth Dasha lord, start date, and full sequence
        """
        # Determine Moon's constellation
        moon_sign, _, moon_degrees = self.get_constellation(moon_lon)
        
        # Calculate elapsed portion of Moon's Maha Dasha
        # Based on Moon's position within the constellation
        sign_sequence = [sign for sign, _ in self.boundaries]
        moon_index = sign_sequence.index(moon_sign)
        
        # Get constellation arc length
        if moon_index == 0:
            sign_start = 0.0
        else:
            sign_start = self.boundaries[moon_index - 1][1]
        sign_end = self.boundaries[moon_index][1]
        
        # Handle Pisces wrap-around
        if sign_start > sign_end:
            sign_arc = (360 - sign_start) + sign_end
            if moon_lon >= sign_start:
                elapsed_degrees = moon_lon - sign_start
            else:
                elapsed_degrees = (360 - sign_start) + moon_lon
        else:
            sign_arc = sign_end - sign_start
            elapsed_degrees = moon_lon - sign_start
        
        # Proportion of Maha Dasha elapsed
        elapsed_proportion = elapsed_degrees / sign_arc
        
        # Calculate remaining years in Moon's Maha Dasha
        total_years = self.dasha_years[moon_sign]
        elapsed_years = total_years * elapsed_proportion
        remaining_years = total_years - elapsed_years
        
        # Birth date as datetime
        birth_date = datetime(year, month, day) + timedelta(hours=hour_utc)
        
        # Dasha start date (when current Maha Dasha began)
        dasha_start = birth_date - timedelta(days=elapsed_years * 365.25)
        
        # Build complete Dasha sequence from birth
        dasha_sequence = self.build_dasha_sequence(
            moon_sign, 
            dasha_start,
            remaining_years,
            elapsed_years
        )
        
        return {
            'birth_dasha_lord': moon_sign,
            'maha_dasha_start': dasha_start,
            'elapsed_years': elapsed_years,
            'remaining_years': remaining_years,
            'sequence': dasha_sequence,
        }
    
    
    def build_dasha_sequence(self, 
                            start_sign: str,
                            start_date: datetime,
                            remaining_years: float,
                            elapsed_years: float) -> List[Dict]:
        """
        Build the complete 120-year Dasha sequence starting from birth Dasha.
        
        CONSCIOUSNESS-AS-GROUND: The Dasha sequence represents the unfolding
        of temporal frequencies through which the wholeperson experiences
        different qualities of the ground-of-being.
        
        Args:
            start_sign: Birth Dasha lord (Moon's constellation at birth)
            start_date: When current Maha Dasha began
            remaining_years: Years remaining in birth Dasha
            elapsed_years: Years already elapsed in birth Dasha
        
        Returns:
            List of Maha Dasha periods with start/end dates
        """
        sign_sequence = [sign for sign, _ in self.boundaries]
        start_index = sign_sequence.index(start_sign)
        
        dasha_periods = []
        current_date = start_date
        
        # Add the birth Dasha period (partial if already elapsed)
        birth_dasha = {
            'lord': start_sign,
            'start': current_date,
            'elapsed_at_birth': elapsed_years,
            'remaining_at_birth': remaining_years,
            'total_years': self.dasha_years[start_sign],
            'end': current_date + timedelta(days=self.dasha_years[start_sign] * 365.25),
        }
        dasha_periods.append(birth_dasha)
        
        # Continue through subsequent Dashas
        current_date = birth_dasha['end']
        
        for i in range(1, 13):  # 12 more periods after birth Dasha
            sign_index = (start_index + i) % 13
            sign = sign_sequence[sign_index]
            duration = self.dasha_years[sign]
            
            period = {
                'lord': sign,
                'start': current_date,
                'total_years': duration,
                'end': current_date + timedelta(days=duration * 365.25),
            }
            dasha_periods.append(period)
            current_date = period['end']
        
        return dasha_periods
    
    
    def calculate_proportional_bhuktis(self, 
                                      maha_lord: str,
                                      maha_start_date: datetime,
                                      maha_duration_years: float) -> List[Dict]:
        """
        Calculate sub-periods (Bhuktis/Antars) proportional to constellation arc-lengths.
        
        FRACTAL BHUKTI MATH: Each Maha Dasha subdivides into 13 Bhuktis,
        each proportional to its constellation's actual arc length.
        
        Formula: Bhukti duration = (Sign Arc / 360°) × Maha Duration
        
        Args:
            maha_lord: The ruling constellation of the Maha Dasha
            maha_start_date: datetime object for Maha Dasha start
            maha_duration_years: Total years for this Maha Dasha
        
        Returns:
            List of bhukti periods with start/end dates
        """
        # Sign sequence starting with Maha lord
        sign_sequence = [sign for sign, _ in self.boundaries]
        start_idx = sign_sequence.index(maha_lord)
        
        # Rotate sequence to start with Maha lord
        rotated_sequence = sign_sequence[start_idx:] + sign_sequence[:start_idx]
        
        bhuktis = []
        current_date = maha_start_date
        total_days = maha_duration_years * 365.25
        
        # Calculate total arc (should equal 360°)
        total_arc = sum(self.dasha_years.values())  # Sum of proportional years = 120
        
        for sign in rotated_sequence:
            # Calculate this bhukti's duration as proportion of total Maha Dasha
            # Proportion = (sign's years / total years) × Maha duration
            sign_proportion = self.dasha_years[sign] / 120.0
            bhukti_days = total_days * sign_proportion
            
            end_date = current_date + timedelta(days=bhukti_days)
            
            bhuktis.append({
                'lord': sign,
                'start': current_date,
                'end': end_date,
                'duration_days': bhukti_days,
                'duration_years': bhukti_days / 365.25,
            })
            
            current_date = end_date
        
        return bhuktis
    
    
    def get_current_dasha(self, 
                         birth_dasha_info: Dict,
                         current_date: datetime) -> Dict:
        """
        Determine the current Maha Dasha and Bhukti for a given date.
        
        The wholeperson's current frequency - which aperture of consciousness
        is most active in this temporal window.
        
        Args:
            birth_dasha_info: Output from calculate_birth_dasha()
            current_date: The date to check (typically today)
        
        Returns:
            Dictionary with current Maha Dasha and Bhukti information
        """
        # Find which Maha Dasha period contains current_date
        current_maha = None
        
        for period in birth_dasha_info['sequence']:
            if period['start'] <= current_date < period['end']:
                current_maha = period
                break
        
        if not current_maha:
            # Date is beyond 120-year cycle
            return {
                'status': 'beyond_cycle',
                'message': 'Date exceeds 120-year Dasha cycle'
            }
        
        # Calculate Bhuktis for this Maha Dasha
        bhuktis = self.calculate_proportional_bhuktis(
            current_maha['lord'],
            current_maha['start'],
            current_maha.get('total_years', current_maha.get('remaining_at_birth', 0))
        )
        
        # Find current Bhukti
        current_bhukti = None
        for bhukti in bhuktis:
            if bhukti['start'] <= current_date < bhukti['end']:
                current_bhukti = bhukti
                break
        
        return {
            'status': 'active',
            'maha_dasha': current_maha,
            'bhukti': current_bhukti,
            'current_date': current_date,
        }
    
    
    def format_chart_report(self, chart: Dict) -> str:
        """
        Generate a human-readable report of the natal chart.
        
        CONSCIOUSNESS-AS-GROUND LANGUAGE:
        - "The wholeperson expresses..."
        - Apertures, luminosities, frequencies
        - No "has", "will", "malefic", "benefic"
        """
        report = []
        report.append("=" * 70)
        report.append("SKY AS GROUND: 13-Sign True IAU Constellation Chart")
        report.append("Tropical J2000 Ecliptic Coordinates")
        report.append("Consciousness-as-Ground Recognition")
        report.append("=" * 70)
        report.append("")
        
        # Birth data
        bd = chart['birth_data']
        report.append(f"Birth Date: {bd['year']}-{bd['month']:02d}-{bd['day']:02d}")
        report.append(f"Birth Time (UTC): {bd['hour_utc']:.4f} ({bd['hour_utc']:.2f} hours)")
        report.append(f"Location: {bd['latitude']:.4f}°, {bd['longitude']:.4f}°")
        report.append(f"Julian Day: {bd['julian_day']:.6f}")
        report.append(f"Coordinate System: {bd['coordinate_system']}")
        report.append("")
        
        # Angles
        report.append("-" * 70)
        report.append("ANGLES: The Primary Apertures")
        report.append("-" * 70)
        
        if 'Ascendant' in chart['angles']:
            asc = chart['angles']['Ascendant']
            report.append(f"Ascendant: {asc['sign']} {asc['position_dms']}")
            report.append(f"           {asc['trigger_status']} - {asc['longitude']:.4f}°")
            report.append("")
        
        if 'MC' in chart['angles']:
            mc = chart['angles']['MC']
            report.append(f"MC:        {mc['sign']} {mc['position_dms']}")
            report.append(f"           {mc['trigger_status']} - {mc['longitude']:.4f}°")
            report.append("")
        
        # Luminosities (Planets)
        report.append("-" * 70)
        report.append("LUMINOSITIES: Planetary Apertures of Consciousness")
        report.append("-" * 70)
        report.append("")
        
        planet_order = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 
                       'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto',
                       'Rahu', 'Ketu']
        
        for planet in planet_order:
            if planet in chart['luminosities']:
                p = chart['luminosities'][planet]
                retro = " (R)" if p.get('retrograde', False) else ""
                house = f"House {p.get('house', '?')}"
                
                report.append(f"{planet:12s} {p['sign']:12s} {p['position_dms']:10s}{retro}")
                report.append(f"             {p['trigger_status']:15s} {house}")
                report.append(f"             Longitude: {p['longitude']:.4f}° | Speed: {p['speed']:.4f}°/day")
                
                if p['trigger_status'] != 'STABLE':
                    report.append(f"             ⚠ BOUNDARY ACTIVATION: Transmutative potential")
                
                report.append("")
        
        # Houses
        report.append("-" * 70)
        report.append("HOUSES: Whole-Sign System (Constellation-as-House)")
        report.append("-" * 70)
        report.append("")
        
        for house in chart['houses']:
            report.append(f"House {house['house_number']:2d}: {house['ruling_sign']:12s} - {house['archetype']}")
        
        report.append("")
        
        # Dasha
        if 'dasha' in chart and chart['dasha']:
            report.append("-" * 70)
            report.append("BIRTH DASHA: Temporal Frequency at Entry")
            report.append("-" * 70)
            report.append("")
            
            dasha = chart['dasha']
            report.append(f"Birth Dasha Lord: {dasha['birth_dasha_lord']}")
            report.append(f"Maha Dasha Start: {dasha['maha_dasha_start'].strftime('%Y-%m-%d')}")
            report.append(f"Elapsed at Birth: {dasha['elapsed_years']:.2f} years")
            report.append(f"Remaining Years:  {dasha['remaining_years']:.2f} years")
            report.append("")
        
        report.append("=" * 70)
        report.append("The chart is the mirror, not the prediction.")
        report.append("The wholeperson recognizes itself through astronomical precision.")
        report.append("=" * 70)
        
        return "\n".join(report)


# ==============================================================================
# TEST CASE VALIDATION
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("SKY AS GROUND - ENGINE CALIBRATION")
    print("=" * 70 + "\n")
    
    # Initialize engine
    engine = GroundEngine()
    
    # TEST CASE: North (Howard)
    # Born: November 30, 1970, 11:47 AM NZST
    # UTC Conversion: Nov 29, 1970, 23:47:23 UTC (11.47 hours before midnight)
    print("Test Subject: 'North'")
    print("Birth: November 30, 1970, 11:47 AM NZST")
    print("UTC:   November 29, 1970, 23:47:23 UTC")
    print()
    
    # Rotorua, New Zealand coordinates
    latitude = -38.1368  # South (negative)
    longitude = 176.2497  # East (positive)
    
    # Calculate chart
    hour_utc = 23 + (47/60) + (23/3600)  # 23.789722 hours
    chart = engine.calculate_chart(
        year=1970,
        month=11,
        day=29,
        hour_utc=hour_utc,
        latitude=latitude,
        longitude=longitude
    )
    
    # Display chart
    print(engine.format_chart_report(chart))
    
    # VALIDATION: Check Sun position against GROUND calibrated boundaries
    print("\n" + "=" * 70)
    print("VALIDATION CHECKS: GROUND Calibration")
    print("=" * 70)
    print()
    
    print(f"Coordinate System: Tropical J2000 Ecliptic (GROUND Calibrated)")
    print(f"Ophiuchus Entry: 247.1° tropical (native's zero-point)")
    print()
    
    if 'Sun' in chart['luminosities']:
        sun = chart['luminosities']['Sun']
        
        print(f"☉ SUN POSITION ANALYSIS:")
        print(f"  Ecliptic Longitude: {sun['longitude']:.6f}°")
        print(f"  Constellation: {sun['sign']}")
        print(f"  Position in Sign: {sun['position_dms']}")
        print(f"  Trigger Status: {sun['trigger_status']}")
        print()
        
        # Check against GROUND Scorpius/Ophiuchus boundary (247.1°)
        boundary_scorpius_ophiuchus = 247.1
        distance_from_boundary = sun['longitude'] - boundary_scorpius_ophiuchus
        
        print(f"  GROUND Scorpius/Ophiuchus Boundary: {boundary_scorpius_ophiuchus}°")
        print(f"  Distance from Boundary: {distance_from_boundary:+.6f}°")
        print()
        
        if distance_from_boundary >= 0:
            print(f"  Status: Sun in Ophiuchus ({distance_from_boundary:.4f}° past threshold)")
        else:
            print(f"  Status: Sun in Scorpius ({abs(distance_from_boundary):.4f}° before threshold)")
        print()
        
        print(f"  EXPECTED: Ophiuchus 0°-1° (247.1° - 248.1°)")
        print(f"  ACTUAL:   {sun['sign']} {sun['position_dms']} - {sun['trigger_status']}")
        print()
        
        # Check validation
        if sun['sign'] == 'Ophiuchus' and 0 <= distance_from_boundary <= 1.0:
            print("  ✓✓ VALIDATION PASSED: Sun at Ophiuchus threshold (native's zero-point)")
            if abs(distance_from_boundary - 0.255) <= 0.05:  # ~0°15'
                print("  ✓✓✓ PERFECT CALIBRATION: Sun at 0°15' Ophiuchus")
        elif sun['sign'] == 'Ophiuchus':
            print(f"  ✓ Sun in Ophiuchus (GROUND validated)")
        else:
            print(f"  ⚠ REVIEW: Sun at {sun['longitude']:.4f}° (expected ≥247.1°)")
            print(f"     The native IS the Ophiuchus aperture - boundary may need adjustment")
    
    print()
    
    # CURRENT DASHA CHECK: January 28, 2026
    print("=" * 70)
    print("CURRENT FREQUENCY CHECK: January 28, 2026")
    print("=" * 70)
    print()
    
    current_date = datetime(2026, 1, 28)
    current_dasha = engine.get_current_dasha(chart['dasha'], current_date)
    
    if current_dasha['status'] == 'active':
        maha = current_dasha['maha_dasha']
        bhukti = current_dasha['bhukti']
        
        print(f"Current Maha Dasha: {maha['lord']}")
        print(f"  Period: {maha['start'].strftime('%Y-%m-%d')} to {maha['end'].strftime('%Y-%m-%d')}")
        print(f"  Duration: {maha.get('total_years', maha.get('remaining_at_birth', 0)):.2f} years")
        print()
        
        print(f"Current Bhukti: {bhukti['lord']}")
        print(f"  Period: {bhukti['start'].strftime('%Y-%m-%d')} to {bhukti['end'].strftime('%Y-%m-%d')}")
        print(f"  Duration: {bhukti['duration_years']:.3f} years")
        print()
        
        print(f"The wholeperson is currently expressing through the")
        print(f"{maha['lord']}-{bhukti['lord']} frequency.")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70 + "\n")
