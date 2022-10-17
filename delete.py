from flask import render_template, request, url_for, redirect, flash flask import Flask


@app.route('/items/delete/<int:item_id>', methods=['POST'])
def delete(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete_one(item)
    db.session.commit()
    return redirect(url_for('index'))
    
    
