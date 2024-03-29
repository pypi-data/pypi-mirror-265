from typing import List, Dict, Tuple
from ...interface import IData
from ...packer.chart.chart_init_param_data_packer import ChartInitParamDataPacker
from .time_axis_param_data import TimeAxisParamData
from .value_axis_param_data import ValueAxisParamData
from .plot_param_data import PlotParamData
from .legend_item_param_data import LegendItemParamData
from .line_graph_param_data import LineGraphParamData
from .financial_graph_param_data import FinancialGraphParamData
from .bar_graph_param_data import BarGraphParamData
from .text_graph_param_data import TextGraphParamData
from .marker_graph_param_data import MarkerGraphParamData


class ChartInitParamData(IData):
    def __init__(self):
        super().__init__(ChartInitParamDataPacker(self))
        self._ChartID = ''
        self._Title = ''
        self._Height = 600
        self._Width = 800
        self._IsSaveGeometry = True
        self._ReplotTime = 100
        self._GlobalTimeAxisParam = TimeAxisParamData()
        self._GlobalValueAxisParam = ValueAxisParamData()
        self._GlobalPlotParam = PlotParamData()
        self._GlobalLegendItemParam = LegendItemParamData()
        self._PlotParamList: List[PlotParamData] = []
        self._ValueAxisParamList: List[ValueAxisParamData] = []
        self._LegendItemParamList: List[LegendItemParamData] = []
        self._FinancialGraphParamList: List[FinancialGraphParamData] = []
        self._LineGraphParamList: List[LineGraphParamData] = []
        self._BarGraphParamList: List[BarGraphParamData] = []
        self._TextGraphParamList: List[TextGraphParamData] = []
        self._MarkerGraphParamList: List[MarkerGraphParamData] = []
        self._TimeSpanList: List[int] = []
        self._GraphValueList: Dict[str, List[float]] = {}
        self._OHLCValueList: Dict[str, Tuple[List[float], List[float], List[float], List[float]]] = {}
        self._IsFullScreen = False
        self._IsRangeSliderVisible = True
        self._ShowDays = 0

    @property
    def ChartID(self):
        return self._ChartID

    @ChartID.setter
    def ChartID(self, value: str):
        self._ChartID = value

    @property
    def Title(self):
        return self._Title

    @Title.setter
    def Title(self, value: str):
        self._Title = value

    @property
    def Height(self):
        return self._Height

    @Height.setter
    def Height(self, value: int):
        self._Height = value

    @property
    def Width(self):
        return self._Width

    @Width.setter
    def Width(self, value: int):
        self._Width = value

    @property
    def IsSaveGeometry(self):
        return self._IsSaveGeometry

    @IsSaveGeometry.setter
    def IsSaveGeometry(self, value: bool):
        self._IsSaveGeometry = value

    @property
    def ReplotTime(self):
        return self._ReplotTime

    @ReplotTime.setter
    def ReplotTime(self, value: int):
        self._ReplotTime = value

    @property
    def GlobalTimeAxisParam(self):
        return self._GlobalTimeAxisParam

    @GlobalTimeAxisParam.setter
    def GlobalTimeAxisParam(self, value: TimeAxisParamData):
        self._GlobalTimeAxisParam = value

    @property
    def GlobalValueAxisParam(self):
        return self._GlobalValueAxisParam

    @GlobalValueAxisParam.setter
    def GlobalValueAxisParam(self, value: ValueAxisParamData):
        self._GlobalValueAxisParam = value

    @property
    def GlobalPlotParam(self):
        return self._GlobalPlotParam

    @GlobalPlotParam.setter
    def GlobalPlotParam(self, value: PlotParamData):
        self._GlobalPlotParam = value

    @property
    def GlobalLegendItemParam(self):
        return self._GlobalLegendItemParam

    @GlobalLegendItemParam.setter
    def GlobalLegendItemParam(self, value: LegendItemParamData):
        self._GlobalLegendItemParam = value

    @property
    def PlotParamList(self):
        return self._PlotParamList

    @PlotParamList.setter
    def PlotParamList(self, value: List[PlotParamData]):
        self._PlotParamList = value

    @property
    def ValueAxisParamList(self):
        return self._ValueAxisParamList

    @ValueAxisParamList.setter
    def ValueAxisParamList(self, value: List[ValueAxisParamData]):
        self._ValueAxisParamList = value

    @property
    def LegendItemParamList(self):
        return self._LegendItemParamList

    @LegendItemParamList.setter
    def LegendItemParamList(self, value: List[LegendItemParamData]):
        self._LegendItemParamList = value

    @property
    def FinancialGraphParamList(self):
        return self._FinancialGraphParamList

    @FinancialGraphParamList.setter
    def FinancialGraphParamList(self, value: List[FinancialGraphParamData]):
        self._FinancialGraphParamList = value

    @property
    def LineGraphParamList(self):
        return self._LineGraphParamList

    @LineGraphParamList.setter
    def LineGraphParamList(self, value: List[LineGraphParamData]):
        self._LineGraphParamList = value

    @property
    def BarGraphParamList(self):
        return self._BarGraphParamList

    @BarGraphParamList.setter
    def BarGraphParamList(self, value: List[BarGraphParamData]):
        self._BarGraphParamList = value

    @property
    def TextGraphParamList(self):
        return self._TextGraphParamList

    @TextGraphParamList.setter
    def TextGraphParamList(self, value: List[TextGraphParamData]):
        self._TextGraphParamList = value

    @property
    def MarkerGraphParamList(self):
        return self._MarkerGraphParamList

    @MarkerGraphParamList.setter
    def MarkerGraphParamList(self, value: List[MarkerGraphParamData]):
        self._MarkerGraphParamList = value

    @ property
    def TimeSpanList(self):
        return self._TimeSpanList

    @ TimeSpanList.setter
    def TimeSpanList(self, value: List[int]):
        self._TimeSpanList = value

    @ property
    def GraphValueList(self):
        return self._GraphValueList

    @ GraphValueList.setter
    def GraphValueList(self, value: Dict[str, List[float]]):
        self._GraphValueList = value

    @ property
    def OHLCValueList(self):
        return self._OHLCValueList

    @ OHLCValueList.setter
    def OHLCValueList(self, value: Dict[str, Tuple[List[float], List[float], List[float], List[float]]]):
        self._OHLCValueList = value

    @property
    def IsFullScreen(self):
        return self._IsFullScreen

    @IsFullScreen.setter
    def IsFullScreen(self, value: bool):
        self._IsFullScreen = value

    @property
    def IsRangeSliderVisible(self):
        return self._IsRangeSliderVisible

    @IsRangeSliderVisible.setter
    def IsRangeSliderVisible(self, value: bool):
        self._IsRangeSliderVisible = value

    @property
    def ShowDays(self):
        return self._ShowDays

    @ShowDays.setter
    def ShowDays(self, value: int):
        self._ShowDays = value
