from enum import Enum


class TagMonthsDatas(Enum):
    Janeiro = '01'
    Fevereiro = '02'
    Março = '03'
    Abril = '04'
    Maio = '05'
    Junho = '06'
    Julho = '07'
    Agosto = '08'
    Setembro = '09'
    Outubro = '10'
    Novembro = '11'
    Dezembro = '12'


class ParseToTypes:

    def parseMonthToStr(self: str):

        match self:
            case 'Fevereiro':
                return [TagMonthsDatas[self].value, '29']

            case 'Abril' | 'Junho' | 'Setembro' | 'Novembro':
                return [TagMonthsDatas[self].value, '30']

            case _:
                return [TagMonthsDatas[self].value, '31']

    def parseMonthToDays(self: int):

        match self:
            case 2:
                return 29

            case 4 | 6 | 9 | 11:
                return 30

            case _:
                return 31
