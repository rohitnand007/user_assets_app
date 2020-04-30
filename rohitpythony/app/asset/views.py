from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import asset

from forms import AssetForm
from .. import db
from ..models import Asset,Inventory,Location

# asset Views


@asset.route('/assets', methods=['GET', 'POST'])
@login_required
def list_assets():
    """
    List all departments
    """
    assets = current_user.assets #Asset.query.all()

    return render_template('assets/assets.html',
                           assets=assets, title="Assets")


@asset.route('/assets/add', methods=['GET', 'POST'])
@login_required
def add_asset():
    """
    Add a asset to the database
    """

    add_asset = True

    form = AssetForm()
    if form.validate_on_submit():
        asset = Asset(comments=form.comments.data,
            inventory_id=Inventory.query.first().id,
            location=Location.query.first().id,
            managed_by=current_user.id,
            assigned_to=current_user.id,
            certified_by=current_user.id,
             )
        try:
            # add asset to the database
            db.session.add(asset)
            db.session.commit()
            flash('You have successfully added a new Asset.')
        except:
            # in case asset name already exists
            flash('Error: Asset cannot be created.')

        # redirect to assets page
        return redirect(url_for('assets.list_assets'))

    # load department template
    return render_template('assets/asset.html', action="Add",
                           add_asset=add_asset, form=form,
                           title="Add Asset")


@asset.route('/assets/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_asset(id):
    """
    Edit an asset
    """

    add_asset = False

    asset = Asset.query.get_or_404(id)
    form = AssetForm(obj=asset)
    if form.validate_on_submit():
        asset.comments = form.comments.data
        db.session.commit()
        flash('You have successfully edited the asset.')

        # redirect to the departments page
        return redirect(url_for('assets.list_assets'))

    return render_template('assets/asset.html', action="Edit",
                           add_asset=add_asset, form=form,
                           asset=asset, title="Edit Asset")


@asset.route('/assets/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_asset(id):
    """
    Delete a department from the database
    """

    asset = Asset.query.get_or_404(id)
    db.session.delete(asset)
    db.session.commit()
    flash('You have successfully deleted the asset.')

    # redirect to the departments page
    return redirect(url_for('assets.list_assets'))

    return render_template(title="Delete Asset")
