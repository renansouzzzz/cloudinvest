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

class TagMonthsDays(Enum):
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

class ParseToTypes():
    
    def parseMonthToStr(month: str):
        
        match month:
            case 'Fevereiro':
                return [TagMonthsDatas[month].value, '29']
            
            case 'Abril' | 'Junho' | 'Setembro' | 'Novembro':
                return [TagMonthsDatas[month].value, '30']
            
            case _:
                return [TagMonthsDatas[month].value, '31']

    def parseMonthToDays(month: int):

        match month:
            case 2:
                return 29

            case 4 | 6 | 9 | 11:
                return 30

            case _:
                return 31
