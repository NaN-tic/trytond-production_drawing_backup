from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval, Bool
from trytond.pool import PoolMeta

__all__ = ['BOM', 'BOMDrawingLine']


class BOM:
    __name__ = 'production.bom'
    __metaclass__ = PoolMeta
    drawing = fields.Many2One('production.drawing', 'Drawing',
        ondelete='RESTRICT')
    drawing_lines = fields.One2Many('production.bom.drawing.line',
        'bom', 'Drawing Positions', states={
            'invisible': ~Bool(Eval('drawing')),
            })
    drawing_image = fields.Function(fields.Binary('Drawing Image'),
        'on_change_with_drawing_image')

    @fields.depends('drawing')
    def on_change_with_drawing_lines(self):
        if not self.drawing:
            to_remove = [x.id for x in self.drawing_lines]
            return {
                'remove': to_remove,
                }
        to_add = []
        for position in self.drawing.positions:
            to_add.append((-1, {
                    'position': position.id,
                    }))
        return {'add': to_add}

    @fields.depends('drawing')
    def on_change_with_drawing_image(self, name=None):
        return self.drawing.image if self.drawing else None


class BOMDrawingLine(ModelSQL, ModelView):
    'Production BOM Drawing Line'
    __name__ = 'production.bom.drawing.line'
    bom = fields.Many2One('production.bom', 'BOM', required=True,
        ondelete='CASCADE')
    position = fields.Many2One('production.drawing.position',
        'Drawing Position', required=True, ondelete='RESTRICT', domain=[
            ('drawing', '=', Eval('drawing', -1)),
            ], states={
            'readonly': True,
            }, depends=['drawing'])
    drawing = fields.Function(fields.Many2One('production.drawing', 'Drawing'),
        'get_drawing')
    product = fields.Many2One('product.product', 'Product',
        ondelete='RESTRICT')

    @classmethod
    def __setup__(cls):
        super(BOMDrawingLine, cls).__setup__()
        cls._sql_constraints += [
            ('check_bom_drawing_line_uniq', 'UNIQUE(bom, position)',
                'Drawing Position must be unique per BOM.'),
            ]

    def get_drawing(self, name):
        return self.bom.drawing.id if self.bom.drawing else None
