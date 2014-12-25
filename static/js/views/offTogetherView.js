var app = app || {};

app.offTogetherView = Backbone.View.extend({
	
  residents : null,
  availableTags : null,


  initialize : function(){
  	this.availableTags = this.residents.getNamesAndIds(); 
  },


	render : function(){
    	this.$el.tokenInput(this.availableTags, {
    		theme : 'facebook',
    		hintText : 'Type in a resident\'s name'
    	});
	}


})