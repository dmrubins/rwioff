var app = app || {};

app.offTogetherInputView = Backbone.View.extend({
	
  initialize : function(){
    this.listenTo(app.dispatcher, 'set:residents', this.render);
  },

  updateTags : function(){
  },

	render : function(){
    tags = app.residents.getNamesAndIds();
    this.$el.tokenInput(tags, {
        theme : 'facebook',
        hintText : 'Type in a resident\'s name'
    });

   /* this.$el.tokenInput('add', {'name' : 'Aabiog K', 'id' : '4479'});
    this.$el.tokenInput('add', {'name' : 'Ankit P', 'id' : '9005'});
    this.$el.tokenInput('add', {'name' : 'Travis ', 'id' : '8992'});
    this.$el.tokenInput('add', {'name' : 'Yuri Kim', 'id' : '3745'});*/

    //Add the button
    button = $('<button class="btn btn-lg btn-default">Search</button>');
    this.$el.after(button);
    el = this.$el;
    button.click(function(){
      app.dispatcher.trigger('intersect-residents-click', el.tokenInput('get') )
    })

	}


});

app.offTogetherListView = Backbone.View.extend({
  
  template : _.template($('#dateTemplate').html()),

  initialize : function(){
    this.listenTo(this.model, 'change:dates', this.render);
  },

  render : function(){
    this.$el.empty();
    dates = this.model.get('dates');
    for (var i = 0; i < dates.length; i++){
      t = this.template({date : $.datepicker.formatDate( "D, M d, yy", dates[i]) });
      this.$el.append($(t));
    }
  }


})