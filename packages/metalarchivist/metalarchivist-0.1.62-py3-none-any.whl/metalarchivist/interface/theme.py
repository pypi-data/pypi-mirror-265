
import re

from enum import StrEnum, auto
from dataclasses import dataclass, field


class ThemePeriod(StrEnum):
    EARLY = auto()
    MID = auto()
    LATER = auto()
    ALL = auto()
    ERROR = auto()

    @classmethod
    def has_value(cls, value) -> bool:
        return value in cls._value2member_map_
    
    @classmethod
    def get(cls, value: str, default):
        try:
            return cls[value]
        except KeyError:
            return default



@dataclass
class ThemePhase:
    name: str
    period: ThemePeriod



class ThemeRules:

    junk = {r'\)[\/\b\w]': '), ',
            r'\(earlier\)': '(early)',
            r'\(early, later\)': '(early/later)',
            r'\(early\), \b': '(early); ',
            r'\(first album\),': '(early); ',
            r'\(later\), \b': '(later); ',
            r'\);$': ')',
            r'\(deb.\)': '',
            r'themes from ': '',
            r' themes': '',
            r'based on ': '',
            r' \(thematic\)': ''}

    substitutions = {r'\bw.a.r.\b': 'White Aryan Resistance'}


@dataclass
class Themes:
    full_theme: str
    clean_theme: str = field(init=False)
    phases: list[ThemePhase] = field(init=False)

    def __post_init__(self):
        clean_theme = self.full_theme
        for pattern, substitution in ThemeRules.junk.items():
            clean_theme = re.sub(pattern, substitution, clean_theme, flags=re.IGNORECASE)

        for pattern, substitution in ThemeRules.substitutions.items():
            clean_theme = re.sub(pattern, substitution, clean_theme, flags=re.IGNORECASE)
        
        self.clean_theme = clean_theme

        phases = clean_theme.split(';')
        phases = list(map(self._parse_phase, map(str.lstrip, phases)))
        
        phases = self._explode_phases_on_delimiter(phases, '/')
        phases = self._explode_phases_on_delimiter(phases, ',')

        self.phases = phases

    @staticmethod
    def _parse_phase(phase: str) -> ThemePhase:
        phase_match = re.compile(r'^(?P<name>.*?)(\((?P<period>[\w\/\, ]+)\))?$').match(phase)
        if phase_match is None:
            raise ValueError

        period_text = phase_match.group('period')
        if period_text is not None:
            period = ThemePeriod.get(period_text.upper(), ThemePeriod.ERROR)
        else:
            period = ThemePeriod.ALL

        phase_name = phase_match.group('name')

        return ThemePhase(phase_name, period)

    @staticmethod
    def _explode_phases_on_delimiter(phases: list[ThemePhase], delimiter: str) -> list[ThemePhase]:
        def explode(phase):
            return [ThemePhase(n.strip(), phase.period) for n in phase.name.split(delimiter)]
            
        return sum(list(map(explode, phases)), [])
    
    def to_dict(self) -> dict:
        phases = [dict(name=p.name.lower(), period=p.period.value) for p in self.phases]
        return dict(theme=self.clean_theme.lower(), theme_phases=phases)
