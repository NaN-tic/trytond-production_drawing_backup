from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Eval, Bool
from trytond.pool import PoolMeta

__all__ = ['Drawing', 'DrawingPosition', 'BOM', 'BOMDrawingPosition']


class Drawing(ModelSQL, ModelView):
    'Production Drawing'
    __name__ = 'production.drawing'
    name = fields.Char('Name', required=True)
    image = fields.Binary('Image')
    positions = fields.One2Many('production.drawing.position', 'drawing',
        'Positions')


class DrawingPosition(ModelSQL, ModelView):
    'Production Drawing Position'
    __name__ = 'production.drawing.position'
    drawing = fields.Many2One('production.drawing', 'Drawing',
        required=True, ondelete='CASCADE')
    name = fields.Char('Name', required=True)


class BOM:
    __name__ = 'production.bom'
    __metaclass__ = PoolMeta
    drawing = fields.Many2One('production.drawing', 'Drawing',
        ondelete='RESTRICT')
    drawing_positions = fields.One2Many('production.bom.drawing.position',
        'bom', 'Drawing Positions', states={
            'invisible': ~Bool(Eval('drawing')),
            })
    drawing_image = fields.Function(fields.Binary('Drawing Image'),
        'on_change_with_drawing_image')

    @fields.depends('drawing')
    def on_change_with_drawing_positions(self):
        if not self.drawing:
            to_remove = [x.id for x in self.drawing_positions]
            return {
                'remove': to_remove,
                }
        to_add = []
        for position in self.drawing.positions:
            to_add.append((-1, {
                    'position': position.id,
                    }))
        return {'add': to_add}

    def on_change_with_drawing_image(self, name):
        return self.drawing.image if self.drawing else None


class BOMDrawingPosition(ModelSQL, ModelView):
    'Production BOM Drawing Position'
    __name__ = 'production.bom.drawing.position'
    bom = fields.Many2One('production.bom', 'BOM', required=True,
        ondelete='CASCADE')
    position = fields.Many2One('production.drawing.position',
        'Drawing Position', required=True, ondelete='RESTRICT', states={
            'readonly': True,
            })
    product = fields.Many2One('product.product', 'Product', ondelete='RESTRICT')

    @classmethod
    def __setup__(cls):
        super(BOMDrawingPosition, cls).__setup__()
        cls._sql_constraints += [
            ('check_bom_drawing_position_uniq', 'UNIQUE(bom, position)',
                'Drawing Position must be unique per BOM.'),
            ]
