var app = app || {};

app.scheduleView = Backbone.View.extend({
	
	residentListTemplate : _.template( $('#residentListTemplate').html() ),

	render : function(){
		t = this.residentListTemplate( this.model.toJSON() )
		alert(t)
		this.$el.html( t );
		return this;
	}



})