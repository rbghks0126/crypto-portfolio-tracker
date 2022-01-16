import app


def update_ghseets(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        #flask.Flask.make_response>`.
        `make_response <https://flask.palletsprojects.com/en/1.1.x/api/
    """
    request_json = request.get_json()
    if request.args and 'sheet' in request.args:
        sheet = request.args.get('sheet')
        if sheet == 'target_list':
            return app.update_target_list()
        elif sheet == 'farming':
            return app.update_farming()

    else:
        output1 = app.update_target_list()
        output2 = app.update_farming()
        return '200' if output1 == output2 else '400'
