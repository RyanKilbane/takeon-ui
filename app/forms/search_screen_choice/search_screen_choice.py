from flask import redirect, url_for, render_template, Blueprint, request

search_screen_choice_blueprint = Blueprint(name='search_selection',
                                           import_name=__name__)


@search_screen_choice_blueprint.route('/', methods=['GET', 'POST'])
def general_search_screen_selection():
    if request.method == "POST":
        print(request.form)
        criteria = ';'.join(i for i in request.form.keys())
        return redirect(url_for("contributor_search.general_search_screen", criteria=criteria))
    return render_template('./search_screen_choice/GeneralSearchScreenChoice.html')
