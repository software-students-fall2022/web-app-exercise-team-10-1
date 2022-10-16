from flask import render_template, request, url_for, redirect, flash flask import Flask


@app.route('/movie/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))
    
    
