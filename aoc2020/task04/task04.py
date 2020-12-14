import re
from typing import List


DEBUG = True


def log(msg: str) -> None:
    if DEBUG:
        print(msg)


class Field:

    def __init__(self, name: str, validation):
        self.name = name
        self.validation_fn = validation


class Fields:

    BIRTH_YEAR = Field(
        name="byr",
        validation=lambda val: Validator.validate_year(
            year=val,
            min_year=Validator.BIRTH_YEAR_MIN,
            max_year=Validator.BIRTH_YEAR_MAX
        )
    )
    ISSUE_YEAR = Field(
        name="iyr",
        validation=lambda val: Validator.validate_year(
            year=val,
            min_year=Validator.ISSUE_YEAR_MIN,
            max_year=Validator.ISSUE_YEAR_MAX
        )
    )
    EXPIRATION_YEAR = Field(
        name="eyr",
        validation=lambda val: Validator.validate_year(
            year=val,
            min_year=Validator.EXPIRATION_YEAR_MIN,
            max_year=Validator.EXPIRATION_YEAR_MAX
        )
    )
    HEIGHT = Field(
        name="hgt",
        validation=lambda val: Validator.validate_height(val)
    )
    HAIR_COLOR = Field(
        name="hcl",
        validation=lambda val: Validator.validate_hair_color(val)
    )
    EYE_COLOR = Field(
        name="ecl",
        validation=lambda val: Validator.validate_eye_color(val)
    )
    PASSPORT_ID = Field(
        name="pid",
        validation=lambda val: Validator.validate_id(val)
    )
    COUNTRY_ID = Field(
        name="cid",
        validation=lambda val: Validator.validate_id(val)
    )

    REQUIRED = [
        BIRTH_YEAR,
        ISSUE_YEAR,
        EXPIRATION_YEAR,
        HEIGHT,
        HAIR_COLOR,
        EYE_COLOR,
        PASSPORT_ID
    ]

    ALL = [
        BIRTH_YEAR,
        ISSUE_YEAR,
        EXPIRATION_YEAR,
        HEIGHT,
        HAIR_COLOR,
        EYE_COLOR,
        PASSPORT_ID,
        COUNTRY_ID
    ]

    ALL_NAMES = [f.name for f in ALL]


class PassportEntry:

    def __init__(self, fields=None):
        self.fields = fields if fields is not None else {}

    def has_all_required_fields(self) -> bool:
        missing = sum([
            (0 if field.name in self.fields.keys() else 1) for field in Fields.REQUIRED
        ])
        return missing == 0

    def is_valid(self) -> bool:
        if not self.has_all_required_fields():
            return False
        for required in Fields.REQUIRED:
            if not required.validation_fn(self.fields[required.name]):
                return False
        return True

    @staticmethod
    def parse(raw: str):
        entry_segments: List[str] = raw.split()
        fields = {}
        for entry_segment in entry_segments:
            field_segments = entry_segment.split(sep=":")
            if len(field_segments) == 2:
                field = field_segments[0].strip().lower()
                if field in Fields.ALL_NAMES:
                    fields[field] = field_segments[1].strip()
                else:
                    log("Unknown field name '%s'" % field)
            else:
                log("Invalid field entry '%s'" % entry_segment)
        return PassportEntry(fields) if len(fields) > 0 else None


class Validator:
    PATTERN_ID = re.compile("^\\d{9}$")
    PATTERN_HAIR_COLOR = re.compile("^#[0-9a-f]{6}$")
    PATTERN_HEIGHT = re.compile("^(\\d+)((cm)|(in))$")
    HEIGHT_CM_MIN = 150
    HEIGHT_CM_MAX = 193
    HEIGHT_IN_MIN = 59
    HEIGHT_IN_MAX = 76
    PATTERN_YEAR = re.compile("^\\d{4}$")
    BIRTH_YEAR_MIN = 1920
    BIRTH_YEAR_MAX = 2002
    ISSUE_YEAR_MIN = 2010
    ISSUE_YEAR_MAX = 2020
    EXPIRATION_YEAR_MIN = 2020
    EXPIRATION_YEAR_MAX = 2030
    EYE_COLORS = [
        "amb", "blu", "brn", "gry", "grn", "hzl", "oth"
    ]

    @staticmethod
    def validate_eye_color(eye_color: str) -> bool:
        return eye_color in Validator.EYE_COLORS

    @staticmethod
    def validate_hair_color(hair_color: str) -> bool:
        return Validator.validate_pattern(hair_color, Validator.PATTERN_HAIR_COLOR)

    @staticmethod
    def validate_year(year: str, min_year: int, max_year:int) -> bool:
        return (Validator.PATTERN_YEAR.match(year) is not None) and (min_year <= int(year) <= max_year)

    @staticmethod
    def validate_height(height: str) -> bool:
        m = Validator.PATTERN_HEIGHT.match(height)
        if m is None:
            return False
        value = int(m.group(1))
        unit = m.group(2)
        if unit == "cm":
            return Validator.HEIGHT_CM_MIN <= value <= Validator.HEIGHT_CM_MAX
        else:
            return Validator.HEIGHT_IN_MIN <= value <= Validator.HEIGHT_IN_MAX

    @staticmethod
    def validate_id(id_str: str) -> bool:
        return Validator.validate_pattern(id_str, Validator.PATTERN_ID)

    @staticmethod
    def validate_pattern(subject: str, pattern) -> bool:
        return pattern.match(subject) is not None


def load(input_path: str) -> List[PassportEntry]:
    ret_val: List[PassportEntry] = []
    buffer: str = ""
    with open(input_path, 'r') as input_file:
        for raw_line in input_file:
            line = raw_line.strip()
            if len(line) == 0:
                passport = PassportEntry.parse(buffer)
                if passport is not None:
                    ret_val.append(passport)
                buffer = ""
            else:
                buffer += " " + line
    passport = PassportEntry.parse(buffer)
    if passport is not None:
        ret_val.append(passport)
    return ret_val


def count_valid_entries(passports: List[PassportEntry]) -> int:
    return sum([
        (1 if passport.is_valid() else 0) for passport in passports
    ])


def count_entries_with_all_required_fields(passports: List[PassportEntry]) -> int:
    return sum([
        (1 if passport.has_all_required_fields() else 0) for passport in passports
    ])


def main() -> None:
    passports = load("./input.txt")
    valid_cnt = count_entries_with_all_required_fields(passports)
    print("Passports with all fields: %d out of %d" % (valid_cnt, len(passports)))

    valid_cnt = count_valid_entries(passports)
    print("Valid passports: %d out of %d" % (valid_cnt, len(passports)))


if __name__ == "__main__":
    main()
