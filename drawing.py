from trytond.model import ModelSQL, ModelView, fields

__all__ = ['Drawing', 'DrawingPosition']


class Drawing(ModelSQL, ModelView):
    'Production Drawing'
    __name__ = 'production.drawing'
    name = fields.Char('Name', required=True)
    active = fields.Boolean('Active')
    image = fields.Binary('Image')
    positions = fields.One2Many('production.drawing.position', 'drawing',
        'Positions')

    @staticmethod
    def default_active():
        return True


class DrawingPosition(ModelSQL, ModelView):
    'Production Drawing Position'
    __name__ = 'production.drawing.position'
    drawing = fields.Many2One('production.drawing', 'Drawing',
        required=True, ondelete='CASCADE')
    name = fields.Char('Name', required=True)
