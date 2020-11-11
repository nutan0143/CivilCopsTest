from rest_framework.renderers import JSONRenderer
from django.conf import settings

class APIJSONRenderer(JSONRenderer):
    """
    Custom render class to return uniq object for all API request
    all DRF API request will return object with this criteria
    {error: boolean, message: "error message", content: contentObject }
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        render_obj = {
            "error": False,
            "message": "",
            "content": {},
        }

        error = renderer_context.get('response').exception
        render_obj.update({
            'error': error
        })

        if error:
            render_obj.update({
                'message': data
                # 'message': data[next(iter(data))][0]
            })
        else:
            render_obj.update({
                'content': data
            })
        return super(APIJSONRenderer, self).render(render_obj, accepted_media_type, renderer_context)