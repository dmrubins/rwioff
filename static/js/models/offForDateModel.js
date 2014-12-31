var app = app || {};

app.offForDateModel = Backbone.Model.extend({
	
	defaults: {
		schedule : Array(),
		residents : new app.residentsCollection(),
		pgy : "interns",
	}, 

	initialize : function(){
		this.listenTo(app.dispatcher, 'change:date', this.onDateChange);
	},

	onDateChange : function(){
		this.getResidentsOffForDate();
	}, 

	getResidentsOffForDate: function(){
		//console.log('get residents for date called');
		date = $.datepicker.formatDate( "yymmdd", app.date );

		var residents = new app.residentsCollection();
		var sm = this;

		$.ajax('/' + this.get('pgy') + '/off/' + date)
			.done(function(data){
				//console.log(data);
				data = $.parseJSON(data);
				names = data.names;
				blocks = data.blocks;
				for (var i = 0; i < names.length; i++){
					residents.add(new app.residentModel({'name': names[i], 'block': blocks[i]}) ) ;
				}
				sm.set('residents' , residents);
				//console.log(residents.size())
				residents.getEmails();
			})		
	}

})