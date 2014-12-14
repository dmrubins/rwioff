var app = app || {};

app.scheduleModel = Backbone.Model.extend({
	
	defaults: {
		schedule : Array(),
		residents : new app.residentsOffCollection(),
		currentDate : new Date()
	}, 

	initialize : function(){
		this.on('change:currentDate', this.getResidentsOffForDate);
	},

	setDate : function(date){
		this.set('currentDate', date);
	}, 

	getResidentsOffForDate: function(){
		//console.log('get residents for date called');
		date = $.datepicker.formatDate( "yymmdd", this.get('currentDate') );

		var residents = new app.residentsOffCollection();
		var sm = this;

		$.ajax('/residents/' + date)
			.done(function(data){
				//console.log(data);
				data = $.parseJSON(data);
				names = data.names;
				blocks = data.blocks;
				for (var i = 0; i < names.length; i++){
					residents.add(new app.residentOffForDayModel({'name': names[i], 'block': blocks[i]}) ) ;
				}
				sm.set('residents' , residents);
				console.log(residents.size())
			})

		
	}


})