# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .drawing import *
from .bom import *
from .production import *


def register():
    Pool.register(
        Drawing,
        DrawingPosition,
        BOM,
        BOMDrawingLine,
        Production,
        ProductionDrawingLine,
        module='production_drawing', type_='model')
