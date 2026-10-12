"""params.py - shared inputs of the Budlum Leaf audio team (hw/audio).

Every number carries its tag. Sources:
  FINAL/21 section 21.3.6 and 21.6, HARDWARE/13 parts 13, 14, 23, 24, 26, 30.
Units: mm, N, MPa, s, unless the name says otherwise.
"""

# ---------------------------------------------------------------- ring [DECISION]
RING_RO = 16.0          # outer radius, ring O32.0                 FINAL/21 21.3.1
RING_RI = 12.0          # window radius, O24.0                      FINAL/21 21.3.1
RING_T = 4.00           # module and ring thickness                 FINAL/21 21.3.1
WINDOW_T = 0.30         # sapphire window, each face                HARDWARE/13 #7, #8

# ---------------------------------------------------------------- jack bore [DECISION]
CHORD_D = 13.8          # bore axis distance from the ring centre   FINAL/21 21.3.6
BORE_D = 3.60           # bore diameter
WALL_T = 0.20           # LCP wall
CLOSED_L = 5.0          # closed blind end, stated
TROUGH_L = 9.0          # open trough, stated
BOSS_H = (0.5, 1.0)     # rim boss range that seats the plug collar

# ---------------------------------------------------------------- plug [HYPOTHESIS]
# IEC 60130-9 gives the 3.5 mm plug family. The CTIA / AHJ pin-out is the
# Android 3.5 mm headset spec. Zone limits below are a typical 14.0 mm
# 4-pole plug, measured from the tip end. They are [HYPOTHESIS] until the
# first build measures 20 commercial plugs (MON-22 step J1).
PLUG_D = 3.50           # shank diameter, nominal                   [GENERAL] IEC 60130-9
PLUG_D_TOL = (3.45, 3.55)
PLUG_L = 14.0           # tip end to the shoulder (reference plane)
PLUG_L_RANGE = (13.8, 15.0)   # spread of commercial plugs           [HYPOTHESIS]
NECK_D = 2.60           # tip neck (detent groove) diameter         [HYPOTHESIS]
PLUG_ZONES = [          # name, start, end (mm from the tip end), CTIA signal
    ("tip ball", 0.0, 2.0, "L"),
    ("tip neck", 2.0, 2.8, "L"),
    ("tip shank", 2.8, 3.6, "L"),
    ("insulator 1", 3.6, 4.4, "-"),
    ("ring 1", 4.4, 6.4, "R"),
    ("insulator 2", 6.4, 7.2, "-"),
    ("ring 2", 7.2, 9.2, "GND (CTIA)"),
    ("insulator 3", 9.2, 10.0, "-"),
    ("sleeve", 10.0, 14.0, "MIC (CTIA)"),
]

# ---------------------------------------------------------------- materials
# name: E (MPa), nu, nominal strength (MPa), design allowable (MPa), note
MATERIALS = {
    # LCP-GF40: nominal flexural strength is high, but a moulded tube has a
    # weld line and the hoop direction is transverse to flow.       [GENERAL]
    "LCP-GF40": dict(E=15000, nu=0.35, S_nom=230, S_allow=45,
                     note="weld line and transverse flow, about 20 % of nominal"),
    "PEEK": dict(E=3700, nu=0.40, S_nom=100, S_allow=60,
                 note="extruded tube, no weld line, tensile yield 100 MPa, 1e4-cycle fatigue"),
    "PEEK-GF30": dict(E=9700, nu=0.38, S_nom=155, S_allow=70,
                      note="moulded sleeve, weld line knock-down 0.45"),
    "Y-TZP": dict(E=205000, nu=0.31, S_nom=1000, S_allow=330,
                  note="3Y zirconia, CIM tube, Weibull design at one third of mean"),
    # metal liners: only for the captured trough, with RF-22 co-design
    "Ti-6Al-4V": dict(E=114000, nu=0.34, S_nom=880, S_allow=450,
                      note="PEO-coated for insulation, 1e4-cycle notched fatigue"),
    "17-4PH H900": dict(E=197000, nu=0.27, S_nom=1170, S_allow=600,
                        note="insulating DLC coat, 1e4-cycle notched fatigue"),
    "Zr-BMG": dict(E=96000, nu=0.36, S_nom=1800, S_allow=700,
                   note="Zr-based bulk metallic glass, moulded thin, fatigue limits it"),
}

# ---------------------------------------------------------------- side load [DECISION of this team]
# MON-22 names "a side load". This team sets the numbers.
SIDE_LOADS = {
    "service": dict(F=10.0, arm=15.0, note="10 N at 15 mm past the shoulder, 8 directions, no damage"),
    "abuse": dict(F=20.0, arm=15.0, note="20 N at 15 mm, no crack, plug can leave"),
}

# ---------------------------------------------------------------- audio parts
SPEAKER = dict(L=9.0, W=3.2, H=2.2)       # HARDWARE/13 #13          [DECISION]
MIC = dict(L=2.7, W=1.8, H=0.9, snr_db=68.0, aop_db=130.0)   # #14     [DECISION]
SPL_TARGET_DB = 78.0                      # MON-6, at 100 mm        FINAL/15
SPL_TARGET_R = 0.100                      # m
WATER_DEPTH_M = 1.5                       # MON-12 IP68, 30 min     FINAL/15

C_AIR = 343.0       # m/s  [GENERAL]
RHO_AIR = 1.204     # kg/m3 [GENERAL]
