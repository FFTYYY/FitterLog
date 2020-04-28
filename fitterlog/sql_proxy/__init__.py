'''
数据库对象代理，提供方便的（更方便的）访问数据库对象的方式
包括自动查找、自动保存等功能
'''
from .experi import Experiment , ExperimentGroup , Project
from .variable import Variable , VariableTrack , SingleValue

from .experi import SQL_Experiment , SQL_ExperimentGroup , SQL_Project
from .variable import SQL_Variable , SQL_VariableTrack , SQL_SingleValue